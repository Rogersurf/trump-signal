"""
backend/model_training.py
=========================
Trump Truth Social -> Next-Day Market Impact Predictor.

Core logic:
    - Aggregate ALL posts from a given day into daily-level features
    - Label = next trading day's market return (shift -1 on daily index)
    - One row per day, not per post -> no leakage, realistic prediction
    - Threshold: 75th percentile (25% high-impact days, less sparse)
    - Best classification threshold found via F1 on training set

Usage:
    python -m backend.model_training
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

from backend_database.init_db import DB_PATH

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
TABLE_NAME      = "truth_social"
PRIMARY_TICKER  = "sp500"
MODEL_DIR       = Path(__file__).parent / "model_artifacts"
IMPACT_QUANTILE = 0.75          # top 25% absolute return = high-impact

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
    df["date"]     = pd.to_datetime(df["date"],     errors="coerce").dt.normalize()

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
# 2.  BUILD POST-LEVEL TEXT FEATURES
# ──────────��──────────────────────────────────
def build_post_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["text_len"]              = df["content"].str.len().fillna(0)
    df["caps_count"]            = df["content"].str.findall(r"[A-Z]").apply(len)
    df["caps_ratio"]            = df["caps_count"] / (df["text_len"] + 1)
    df["exclaim"]               = df["content"].str.count("!")
    df["question"]              = df["content"].str.count(r"\?")
    df["has_url"]               = df["content"].str.contains(r"https?://", regex=True).astype(int)
    df["word_count"]            = df["content"].str.split().apply(len)
    df["has_media_int"]         = df["has_media"].astype(int)         if "has_media"         in df.columns else 0
    df["is_president_int"]      = df["is_president"].astype(int)      if "is_president"      in df.columns else 0
    df["is_pres_elect_int"]     = df["is_president_elect"].astype(int) if "is_president_elect" in df.columns else 0
    df["during_market_hours_int"] = df["during_market_hours"].astype(int)
    return df


# ─────────────────────────────────────────────
# 3.  AGGREGATE TO DAILY LEVEL
# ─────────────────────────────────────────────
def aggregate_daily(
    df: pd.DataFrame,
    cat_cols: list,
    gdelt_cols: list,
) -> tuple[pd.DataFrame, list]:

    df = df.sort_values("datetime").reset_index(drop=True)
    df = build_post_features(df)

    existing_cat   = [c for c in cat_cols   if c in df.columns]
    existing_gdelt = [c for c in gdelt_cols if c in df.columns]

    # Post-level text / behaviour aggregations
    text_agg = {
        "post_count":          ("text_len",                "count"),
        "text_len_mean":       ("text_len",                "mean"),
        "text_len_max":        ("text_len",                "max"),
        "caps_ratio_mean":     ("caps_ratio",              "mean"),
        "caps_count_sum":      ("caps_count",              "sum"),
        "exclaim_sum":         ("exclaim",                 "sum"),
        "exclaim_mean":        ("exclaim",                 "mean"),
        "question_sum":        ("question",                "sum"),
        "has_url_sum":         ("has_url",                 "sum"),
        "word_count_mean":     ("word_count",              "mean"),
        "word_count_max":      ("word_count",              "max"),
        "has_media_sum":       ("has_media_int",           "sum"),
        "market_hours_posts":  ("during_market_hours_int", "sum"),
        "is_president_any":    ("is_president_int",        "max"),
        "is_pres_elect_any":   ("is_pres_elect_int",       "max"),
    }

    # cat_* aggregations
    cat_agg = {}
    for c in existing_cat:
        s = c.replace("cat_", "")
        cat_agg[f"{s}_sum"]  = (c, "sum")
        cat_agg[f"{s}_mean"] = (c, "mean")

    # GDELT aggregations
    gdelt_agg = {f"{c}_mean": (c, "mean") for c in existing_gdelt}

    # Market price: last value of the day (for label computation only)
    price_agg = {}
    for t in TICKERS:
        for suf in ["_open", "_close"]:
            col = f"{t}{suf}"
            if col in df.columns:
                price_agg[f"{col}_daily"] = (col, "last")

    all_agg = {**text_agg, **cat_agg, **gdelt_agg, **price_agg}

    daily = (
        df.groupby("date")
          .agg(**all_agg)
          .reset_index()
          .sort_values("date")
          .reset_index(drop=True)
    )

    # Compute next-day return label (shift -1 on daily index)
    p_close = f"{PRIMARY_TICKER}_close_daily"
    p_open  = f"{PRIMARY_TICKER}_open_daily"

    if p_close in daily.columns:
        daily["next_day_ret"] = (
            daily[p_close].shift(-1) - daily[p_close]
        ) / daily[p_close]
    elif p_open in daily.columns:
        daily["next_day_ret"] = (
            daily[p_open].shift(-1) - daily[p_open]
        ) / daily[p_open]
    else:
        daily["next_day_ret"] = np.nan

    # Drop raw price cols — leakage if used as features
    daily = daily.drop(columns=list(price_agg.keys()), errors="ignore")

    # Drop last row (no next-day label)
    daily = daily[daily["next_day_ret"].notna()].copy()

    # High-impact label: top 25% absolute return (75th percentile)
    thresh = daily["next_day_ret"].abs().quantile(IMPACT_QUANTILE)
    daily["high_impact"] = (daily["next_day_ret"].abs() >= thresh).astype(int)

    n_high = daily["high_impact"].sum()
    print(f"      Daily rows      : {len(daily):,}")
    print(f"      High-impact days: {n_high:,}  ({n_high/len(daily)*100:.1f}%)")
    print(f"      Threshold ({IMPACT_QUANTILE*100:.0f}th pct): {thresh * 100:.3f}%")

    # Rolling cat_* context (shift 1 to avoid same-day leakage)
    cat_sum_cols  = [f"{c.replace('cat_', '')}_sum"  for c in existing_cat]
    cat_mean_cols = [f"{c.replace('cat_', '')}_mean" for c in existing_cat]
    all_cat_daily = [c for c in cat_sum_cols + cat_mean_cols if c in daily.columns]

    rolling_cols = []
    for c in all_cat_daily:
        for w in CAT_WINDOWS:
            rolled           = daily[c].shift(1).rolling(window=w, min_periods=1)
            roll_mean        = f"roll{w}_{c}_mean"
            roll_std         = f"roll{w}_{c}_std"
            daily[roll_mean] = rolled.mean()
            daily[roll_std]  = rolled.std().fillna(0)
            rolling_cols    += [roll_mean, roll_std]

    # Day-of-week encoding
    daily["dow"]     = daily["date"].dt.dayofweek
    daily["dow_sin"] = np.sin(2 * np.pi * daily["dow"] / 7)
    daily["dow_cos"] = np.cos(2 * np.pi * daily["dow"] / 7)

    # Final feature list
    text_feat_cols  = list(text_agg.keys())
    gdelt_feat_cols = list(gdelt_agg.keys())

    feature_cols = (
        text_feat_cols
        + all_cat_daily
        + rolling_cols
        + gdelt_feat_cols
        + ["dow_sin", "dow_cos"]
    )
    feature_cols = [c for c in feature_cols if c in daily.columns]

    print(f"      Features        : {len(feature_cols)} total  "
          f"({len(text_feat_cols)} text  |  "
          f"{len(all_cat_daily)} cat_daily  |  "
          f"{len(rolling_cols)} rolling  |  "
          f"{len(gdelt_feat_cols)} gdelt)")

    return daily, feature_cols


# ─────────────────────────────────────────────
# 4.  FIND BEST CLASSIFICATION THRESHOLD
#     Maximise F1 on training set predictions.
# ─────────────────────────────────────────────
def find_best_threshold(y_train: np.ndarray, proba_train: np.ndarray) -> float:
    prec, rec, thresholds = precision_recall_curve(y_train, proba_train)
    f1     = 2 * prec * rec / (prec + rec + 1e-9)
    best_i = f1.argmax()
    best_t = float(thresholds[best_i]) if best_i < len(thresholds) else 0.5
    print(f"      Best threshold (max F1 on train): {best_t:.4f}  "
          f"| F1={f1[best_i]:.3f}  "
          f"P={prec[best_i]:.3f}  R={rec[best_i]:.3f}")
    return best_t


# ─────────────────────────────────────────────
# 5.  TRAIN XGBOOST
# ─────────────────────────────────────────────
def train_model(daily: pd.DataFrame, feature_cols: list):
    data = daily[daily["high_impact"].notna()].copy()
    for c in feature_cols:
        if c not in data.columns:
            data[c] = 0.0

    X = data[feature_cols].fillna(0).astype(float).values
    y = data["high_impact"].astype(int).values

    split_idx       = int(len(data) * 0.80)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    test_start = data["date"].iloc[split_idx]
    test_end   = data["date"].iloc[-1]
    print(f"      Train: {len(X_train):,} days  |  "
          f"Test: {len(X_test):,} days  |  "
          f"Test period: {test_start.date()} -> {test_end.date()}")

    scaler     = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    scale_pos  = max(1, int((y_train == 0).sum() / max(y_train.sum(), 1)))
    xgb_params = dict(
        n_estimators=400, max_depth=4, learning_rate=0.04,
        subsample=0.8, colsample_bytree=0.8,
        scale_pos_weight=scale_pos,
        eval_metric="logloss", random_state=42, n_jobs=-1,
    )

    # Round 1: full feature set, find top-50
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

    top_n     = min(50, len(feature_cols))
    top50     = importance_full.head(top_n)["feature"].tolist()
    top50_idx = [feature_cols.index(f) for f in top50]

    X_train_50 = X_train_sc[:, top50_idx]
    X_test_50  = X_test_sc[:,  top50_idx]

    # Round 2: retrain on top-50
    clf50       = XGBClassifier(**xgb_params)
    cv_scores50 = cross_val_score(clf50, X_train_50, y_train,
                                  cv=TimeSeriesSplit(n_splits=5), scoring="roc_auc")
    clf50.fit(X_train_50, y_train)

    # Dedicated scaler for top-50
    scaler50 = StandardScaler()
    scaler50.fit(X_train[:, top50_idx])

    proba_train = clf50.predict_proba(X_train_50)[:, 1]
    proba_test  = clf50.predict_proba(X_test_50)[:,  1]

    # Find best threshold via F1 on training set
    best_thresh = find_best_threshold(y_train, proba_train)

    roc_train = roc_auc_score(y_train, proba_train)
    roc_test  = roc_auc_score(y_test,  proba_test)
    ap_test   = average_precision_score(y_test, proba_test)
    gap       = roc_train - roc_test

    # Evaluate at best threshold
    y_pred_test = (proba_test >= best_thresh).astype(int)
    tp = int(((y_pred_test == 1) & (y_test == 1)).sum())
    fp = int(((y_pred_test == 1) & (y_test == 0)).sum())
    fn = int(((y_pred_test == 0) & (y_test == 1)).sum())
    prec_t = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec_t  = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_t   = 2 * prec_t * rec_t / (prec_t + rec_t + 1e-9)

    print(f"      [Top-{top_n}] Train AUC : {roc_train:.3f}  |  "
          f"Test AUC: {roc_test:.3f}  |  "
          f"Gap: {gap:.3f}  "
          f"({'overfit WARNING' if gap > 0.05 else 'OK'})")
    print(f"      [Top-{top_n}] CV AUC    : {cv_scores50.mean():.3f} "
          f"+/- {cv_scores50.std():.3f}  |  "
          f"per-fold: {[f'{s:.3f}' for s in cv_scores50]}")
    print(f"      [Threshold={best_thresh:.3f}] "
          f"P={prec_t:.3f}  R={rec_t:.3f}  F1={f1_t:.3f}  "
          f"TP={tp}  FP={fp}  FN={fn}")

    fpr,  tpr,  _ = roc_curve(y_test,  proba_test)
    prec, rec,  _ = precision_recall_curve(y_test, proba_test)

    importance = pd.DataFrame({
        "feature":    top50,
        "importance": clf50.feature_importances_,
    }).sort_values("importance", ascending=False)
    print(importance.to_string(index=False))

    data = data.copy()
    data["impact_proba"] = np.concatenate([proba_train, proba_test])

    metrics = dict(
        roc_auc        = roc_test,
        roc_auc_train  = roc_train,
        avg_precision  = ap_test,
        cv_auc_mean    = cv_scores50.mean(),
        cv_auc_std     = cv_scores50.std(),
        best_threshold = best_thresh,
        precision_t    = prec_t,
        recall_t       = rec_t,
        f1_t           = f1_t,
        n_total        = len(data),
        n_high         = int(y.sum()),
        n_train        = len(X_train),
        n_test         = len(X_test),
        test_start     = str(test_start.date()),
        test_end       = str(test_end.date()),
        fpr=fpr, tpr=tpr, prec=prec, rec=rec,
    )
    return clf50, scaler50, data[["date", "impact_proba"]], importance, metrics


# ─────────────────────────────────────────────
# 6.  SAVE MODEL
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
    print(f"      Model saved -> {MODEL_DIR}")
    print(f"      Best threshold saved: {metrics['best_threshold']:.4f}")


# ─────────────────────────────────────────────
# 7.  PIPELINE
# ─────────────────────────────────────────────
def run_pipeline():
    print("[1/3] Loading posts ...")
    posts, cat_cols, gdelt_cols = load_posts()

    print("[2/3] Aggregating to daily level & computing next-day labels ...")
    daily, feature_cols = aggregate_daily(posts, cat_cols, gdelt_cols)

    print("[3/3] Training XGBoost ...")
    clf, scaler, proba_df, importance, metrics = train_model(daily, feature_cols)

    save_model(clf, scaler, importance["feature"].tolist(), metrics)

    daily = daily.merge(proba_df, on="date", how="left")

    print(f"\nPipeline done  |  "
          f"Test AUC: {metrics['roc_auc']:.3f}  |  "
          f"CV AUC: {metrics['cv_auc_mean']:.3f} +/- {metrics['cv_auc_std']:.3f}  |  "
          f"Best threshold: {metrics['best_threshold']:.3f}  |  "
          f"F1: {metrics['f1_t']:.3f}  |  "
          f"High-impact days: {metrics['n_high']:,} / {metrics['n_total']:,}")

    return daily, importance, metrics, cat_cols, gdelt_cols


# ─────────────────────────────────────────────
if __name__ == "__main__":
    run_pipeline()