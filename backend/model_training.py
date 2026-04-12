"""
backend/model_training.py
=========================
Trump Truth Social → Market Impact 模型训练模块。

用法：
    python -m backend.model_training          # 直接运行训练并保存模型
    from backend.model_training import run_pipeline
"""

import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from backend_database.data_api import DB_PATH

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
TABLE_NAME     = "truth_social"
PRIMARY_TICKER = "sp500"
MODEL_DIR      = Path(__file__).parent / "model_artifacts"

TICKERS = [
    "sp500", "dia", "qqq", "djt", "lmt", "war", "xli", "xlv",
    "xph", "cnrg", "gld", "uso", "fxi", "eww", "vgk", "ibit", "tlt", "uup",
]

TICKER_NAMES = {
    "sp500": "S&P 500",     "dia":  "Dow Jones",    "qqq":  "Nasdaq-100",
    "djt":  "Trump Media",  "lmt":  "Lockheed",     "war":  "Military ETF",
    "xli":  "Industrials",  "xlv":  "Healthcare",   "xph":  "Pharma",
    "cnrg": "Clean Energy", "gld":  "Gold",          "uso":  "Oil",
    "fxi":  "China ETF",    "eww":  "Mexico ETF",   "vgk":  "Europe ETF",
    "ibit": "Bitcoin ETF",  "tlt":  "Bonds",         "uup":  "USD Index",
}

CAT_COLS = [
    "cat_attacking_individual", "cat_attacking_opposition",
    "cat_threatening_intl",     "cat_enacting_aggressive",
    "cat_enacting_nonaggressive","cat_deescalating",
    "cat_praising_endorsing",   "cat_self_promotion", "cat_other",
]

GDELT_COLS = [
    "gdelt_military", "gdelt_sanctions", "gdelt_threat", "gdelt_protest",
    "gdelt_force_posture", "gdelt_diplomatic", "gdelt_material_conflict",
    "gdelt_verbal_conflict", "gdelt_material_cooperation",
    "gdelt_verbal_cooperation", "gdelt_goldstein_avg", "gdelt_avg_tone",
    "gdelt_total_events",
]

CAT_WINDOWS  = [5, 10, 20]
LEAKAGE_COLS = {
    "favourites_count", "replies_count", "reblogs_count",
    "likes", "reposts", "replies", "views",
}


# ─────────────────────────────────────────────
# 1.  LOAD DATA
# ─────────────────────────────────────────────
def load_posts() -> tuple[pd.DataFrame, list, list]:
    import sqlite3

    print(f"[DB] Using DB_PATH: {DB_PATH}")
    conn     = sqlite3.connect(DB_PATH)
    cur      = conn.execute(f"PRAGMA table_info({TABLE_NAME})")
    all_cols = [r[1] for r in cur.fetchall()]

    ticker_suffixes = [
        "_open", "_close", "_1hr_before", "_5min_before",
        "_at_post", "_5min_after", "_1hr_after",
    ]
    ticker_cols = [
        c for c in all_cols
        if any(c == f"{t}{s}" for t in TICKERS for s in ticker_suffixes)
    ]
    cat_cols   = [c for c in all_cols if c in CAT_COLS]
    gdelt_cols = [c for c in all_cols if c in GDELT_COLS]

    base_cols = [
        "datetime", "date", "time", "time_eastern", "day_of_week",
        "text", "url", "post_id",
        "is_president", "is_president_elect",
        "during_market_hours", "market_period",
        "has_media", "sp500_resolution",
    ]
    base_cols   = [c for c in base_cols if c in all_cols]
    select_cols = base_cols + ticker_cols + cat_cols + gdelt_cols

    df = pd.read_sql(f"SELECT {', '.join(select_cols)} FROM {TABLE_NAME}", conn)
    conn.close()

    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
    df["date"]     = pd.to_datetime(df["date"],     errors="coerce")

    for bc in ["during_market_hours", "is_president", "is_president_elect", "has_media"]:
        if bc in df.columns:
            df[bc] = df[bc].astype(float).fillna(0) == 1.0

    skip     = {"sp500_resolution"} | LEAKAGE_COLS
    num_cols = [c for c in ticker_cols + cat_cols + gdelt_cols if c not in skip]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df["content"] = df["text"].fillna("").astype(str)
    df = df.dropna(subset=["datetime"]).reset_index(drop=True)

    print(f"      {len(df):,} posts  |  "
          f"{len(ticker_cols)} ticker cols  |  "
          f"{len(cat_cols)} cat cols  |  "
          f"{len(gdelt_cols)} gdelt cols")

    return df, cat_cols, gdelt_cols


# ─────────────────────────────────────────────
# 2.  COMPUTE RETURNS & LABELS
# ─────────────────────────────────────────────
def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    for t in TICKERS:
        if f"{t}_open" in df.columns and f"{t}_close" in df.columns:
            df[f"{t}_daily_ret"] = (
                (df[f"{t}_close"] - df[f"{t}_open"]) / df[f"{t}_open"]
            )
        if f"{t}_5min_before" in df.columns and f"{t}_5min_after" in df.columns:
            df[f"{t}_immediate_ret"] = (
                (df[f"{t}_5min_after"] - df[f"{t}_5min_before"])
                / df[f"{t}_5min_before"]
            )
        if f"{t}_at_post" in df.columns and f"{t}_1hr_after" in df.columns:
            df[f"{t}_sustained_ret"] = (
                (df[f"{t}_1hr_after"] - df[f"{t}_at_post"])
                / df[f"{t}_at_post"]
            )

    t         = PRIMARY_TICKER
    imm_col   = f"{t}_immediate_ret"
    daily_col = f"{t}_daily_ret"

    is_during = (
        df["during_market_hours"] & df[imm_col].notna()
        if imm_col in df.columns
        else pd.Series(False, index=df.index)
    )

    if imm_col in df.columns and daily_col in df.columns:
        df["primary_ret"] = np.where(is_during, df[imm_col], df[daily_col])
    elif daily_col in df.columns:
        df["primary_ret"] = df[daily_col]
    else:
        df["primary_ret"] = np.nan

    # 只保留开市时间 + 2025 年之后
    df = df[df["during_market_hours"]].copy()
    df = df[df["date"] >= "2025-01-01"].copy()

    dynamic_thresh = df["primary_ret"].dropna().abs().quantile(0.85)
    print(f"      Threshold (85th pct): {dynamic_thresh * 100:.3f}%")

    df["high_impact"] = np.where(
        df["primary_ret"].isna(),
        np.nan,
        (df["primary_ret"].abs() >= dynamic_thresh).astype(float),
    )

    print(f"      during_market_hours=True : {df['during_market_hours'].sum():,}")
    print(f"      Using immediate_ret      : {is_during.sum():,} posts")
    print(f"      Using daily_ret          : {(~is_during).sum():,} posts")
    print(f"      High-impact              : "
          f"{int(df['high_impact'].fillna(0).sum()):,} "
          f"/ {df['primary_ret'].notna().sum():,}")

    return df


# ─────────────────────────────────────────────
# 3.  FEATURE ENGINEERING
# ─────────────────────────────────────────────
def engineer_features(df: pd.DataFrame,
                       cat_cols: list,
                       gdelt_cols: list) -> tuple[pd.DataFrame, list]:
    df = df.sort_values("datetime").reset_index(drop=True)

    # 文本结构
    df["text_len"]       = df["content"].str.len().fillna(0)
    df["caps_ratio"]     = df["content"].str.findall(r"[A-Z]").apply(len) / (df["text_len"] + 1)
    df["caps_count"]     = df["content"].str.findall(r"[A-Z]").apply(len)
    df["exclaim"]        = df["content"].str.count("!")
    df["question"]       = df["content"].str.count(r"\?")
    df["has_url"]        = df["content"].str.contains(r"https?://", regex=True).astype(int)
    df["word_count"]     = df["content"].str.split().apply(len)
    df["has_media_flag"] = df["has_media"].astype(int) if "has_media" in df.columns else 0

    # 시간
    df["hour"]     = df["datetime"].dt.hour
    df["dow"]      = df["datetime"].dt.dayofweek
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    df["dow_sin"]  = np.sin(2 * np.pi * df["dow"]  / 7)
    df["dow_cos"]  = np.cos(2 * np.pi * df["dow"]  / 7)

    # 上下文 flag
    df["is_market_hours"]    = df["during_market_hours"].astype(int)
    df["is_president_flag"]  = df["is_president"].astype(int)    if "is_president"       in df.columns else 0
    df["is_pres_elect_flag"] = df["is_president_elect"].astype(int) if "is_president_elect" in df.columns else 0
    mp_dummies = pd.get_dummies(df["market_period"].fillna("unknown"), prefix="mp").astype(int)
    df = pd.concat([df, mp_dummies], axis=1)

    # cat_* 当前帖子
    existing_cat = [c for c in cat_cols if c in df.columns]

    # Rolling cat_* 上下文（shift(1) 无泄露）
    rolling_feat_cols = []
    for c in existing_cat:
        sname = c.replace("cat_", "")
        for w in CAT_WINDOWS:
            rolled = df[c].shift(1).rolling(window=w, min_periods=1)
            mean_col  = f"roll{w}_{sname}_mean"
            std_col   = f"roll{w}_{sname}_std"
            ratio_col = f"roll{w}_{sname}_ratio"
            df[mean_col]  = rolled.mean()
            df[std_col]   = rolled.std().fillna(0)
            df[ratio_col] = df[c] / (df[mean_col] + 1e-6)
            rolling_feat_cols += [mean_col, std_col, ratio_col]

    # 每天累计 cat_*（当天之前的帖子，无泄露）
    df["_date_only"] = df["datetime"].dt.date
    daily_cat_cols   = []
    for c in existing_cat:
        sname    = c.replace("cat_", "")
        dcol     = f"daily_{sname}_sum"
        df[dcol] = df.groupby("_date_only")[c].transform(
            lambda x: x.shift(1).cumsum().fillna(0)
        )
        daily_cat_cols.append(dcol)
    df = df.drop(columns=["_date_only"])

    # GDELT
    existing_gdelt = [c for c in gdelt_cols if c in df.columns]

    feature_cols = (
        ["text_len", "caps_ratio", "caps_count", "exclaim", "question",
         "has_url", "word_count", "has_media_flag"]
        + ["hour_sin", "hour_cos", "dow_sin", "dow_cos"]
        + ["is_market_hours", "is_president_flag", "is_pres_elect_flag"]
        + list(mp_dummies.columns)
        + existing_cat
        + rolling_feat_cols
        + daily_cat_cols
        + existing_gdelt
    )

    print(f"      Features: {len(feature_cols)} total  "
          f"({len(existing_cat)} cat_*  |  "
          f"{len(rolling_feat_cols)} rolling  |  "
          f"{len(daily_cat_cols)} daily_cat  |  "
          f"{len(existing_gdelt)} gdelt)")

    return df, feature_cols


# ─────────────────────────────────────────────
# 4.  TRAIN XGBOOST
# ──────────���──────────────────────────────────
def train_model(df: pd.DataFrame, feature_cols: list):
    labelled = df[df["high_impact"].notna()].copy()
    for c in feature_cols:
        if c not in labelled.columns:
            labelled[c] = 0.0

    X = labelled[feature_cols].fillna(0).astype(float).values
    y = labelled["high_impact"].astype(int).values

    split_idx       = int(len(labelled) * 0.80)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    test_start = labelled["datetime"].iloc[split_idx].date()
    test_end   = labelled["datetime"].iloc[-1].date()
    print(f"      Train: {len(X_train):,}  |  "
          f"Test (holdout): {len(X_test):,}  |  "
          f"Test period: {test_start} → {test_end}")

    scaler     = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    scale_pos = max(1, int((y_train == 0).sum() / max(y_train.sum(), 1)))
    xgb_params = dict(
        n_estimators=400, max_depth=4, learning_rate=0.04,
        subsample=0.8, colsample_bytree=0.8,
        scale_pos_weight=scale_pos,
        eval_metric="logloss", random_state=42, n_jobs=-1,
    )

    # 第一轮：全特征，找 top-50
    clf_full = XGBClassifier(**xgb_params)
    tscv     = TimeSeriesSplit(n_splits=5)
    cross_val_score(clf_full, X_train_sc, y_train, cv=tscv, scoring="roc_auc")
    clf_full.fit(X_train_sc, y_train)

    importance_full = pd.DataFrame({
        "feature":    feature_cols,
        "importance": clf_full.feature_importances_,
    }).sort_values("importance", ascending=False)

    print("      [Full model top-10]")
    print(importance_full.head(10).to_string(index=False))

    top50     = importance_full.head(50)["feature"].tolist()
    top50_idx = [feature_cols.index(f) for f in top50]

    X_train_50 = X_train_sc[:, top50_idx]
    X_test_50  = X_test_sc[:,  top50_idx]

    # 第二轮：top-50 重新训练
    clf50       = XGBClassifier(**xgb_params)
    cv_scores50 = cross_val_score(clf50, X_train_50, y_train,
                                  cv=TimeSeriesSplit(n_splits=5), scoring="roc_auc")
    clf50.fit(X_train_50, y_train)

    # top-50 专用 scaler（供 predict 使用）
    scaler50 = StandardScaler()
    scaler50.fit(X_train[:, top50_idx])

    proba_train = clf50.predict_proba(X_train_50)[:, 1]
    proba_test  = clf50.predict_proba(X_test_50)[:,  1]

    roc_train = roc_auc_score(y_train, proba_train)
    roc_test  = roc_auc_score(y_test,  proba_test)
    ap_test   = average_precision_score(y_test, proba_test)
    gap       = roc_train - roc_test

    print(f"      [Top-50] Train AUC: {roc_train:.3f}  |  "
          f"Test AUC: {roc_test:.3f}  |  "
          f"Gap: {gap:.3f}  "
          f"({'⚠️  overfit' if gap > 0.05 else '✅ OK'})")
    print(f"      [Top-50] CV AUC: {cv_scores50.mean():.3f} "
          f"± {cv_scores50.std():.3f}  |  "
          f"per-fold: {[f'{s:.3f}' for s in cv_scores50]}")

    fpr,  tpr,  _ = roc_curve(y_test,  proba_test)
    prec, rec,  _ = precision_recall_curve(y_test, proba_test)

    importance = pd.DataFrame({
        "feature":    top50,
        "importance": clf50.feature_importances_,
    }).sort_values("importance", ascending=False)
    print(importance.to_string(index=False))

    labelled = labelled.copy()
    labelled["impact_proba"] = np.concatenate([proba_train, proba_test])

    metrics = dict(
        roc_auc       = roc_test,
        roc_auc_train = roc_train,
        avg_precision = ap_test,
        cv_auc_mean   = cv_scores50.mean(),
        cv_auc_std    = cv_scores50.std(),
        n_total       = len(labelled),
        n_high        = int(y.sum()),
        n_train       = len(X_train),
        n_test        = len(X_test),
        test_start    = str(test_start),
        test_end      = str(test_end),
        fpr=fpr, tpr=tpr, prec=prec, rec=rec,
    )
    return clf50, scaler50, labelled[["datetime", "impact_proba"]], importance, metrics


# ─────────────────────────────────────────────
# 5.  SAVE MODEL
# ─────────────────────────────────────────────
def save_model(clf, scaler, feature_cols: list, metrics: dict):
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf,    MODEL_DIR / "xgb_model.pkl")
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
    with open(MODEL_DIR / "feature_cols.json", "w") as f:
        json.dump(feature_cols, f, indent=2)
    save_metrics = {k: v for k, v in metrics.items()
                    if k not in ("fpr", "tpr", "prec", "rec")}
    with open(MODEL_DIR / "metrics.json", "w") as f:
        json.dump(save_metrics, f, indent=2)
    print(f"      💾 Model saved → {MODEL_DIR}")


# ─────────────────────────────────────────────
# 6.  PIPELINE
# ─────────────────────────────────────────────
def run_pipeline():
    print("[1/4] Loading posts …")
    posts, cat_cols, gdelt_cols = load_posts()

    print("[2/4] Computing returns & impact labels …")
    posts = compute_returns(posts)

    print("[3/4] Engineering features …")
    posts, feature_cols = engineer_features(posts, cat_cols, gdelt_cols)

    print("[4/4] Training XGBoost …")
    clf, scaler, proba_df, importance, metrics = train_model(posts, feature_cols)

    save_model(clf, scaler, importance["feature"].tolist(), metrics)

    posts = posts.merge(proba_df, on="datetime", how="left")

    print(f"\n✅  Pipeline done  |  "
          f"Test ROC-AUC: {metrics['roc_auc']:.3f}  |  "
          f"CV AUC: {metrics['cv_auc_mean']:.3f} ± {metrics['cv_auc_std']:.3f}  |  "
          f"High-impact: {metrics['n_high']:,} / {metrics['n_total']:,}")

    return posts, importance, metrics, cat_cols, gdelt_cols


# ─────────────────────────────────────────────
if __name__ == "__main__":
    run_pipeline()