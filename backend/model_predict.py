"""
backend/model_predict.py
========================
Trump Truth Social → Market Impact 预测模块。
依赖 model_training.py 训练并保存的模型文件。

用法：
    python -m backend.model_predict           # 预测最新 7 天数据
    from backend.model_predict import predict_latest, predict_new_posts
"""

import json
import warnings
from pathlib import Path

import joblib
import pandas as pd

from backend.model_training import (
    MODEL_DIR,
    CAT_COLS,
    GDELT_COLS,
    engineer_features,
    load_posts,
)

warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────
# 1.  PREDICT NEW POSTS (核心方法，供外部调用)
# ─────────────────────────────────────────────
def predict_new_posts(new_posts: pd.DataFrame) -> pd.DataFrame:
    """
    把新帖子喂进已保存的模型，返回带 impact_proba 的 DataFrame。

    参数：
        new_posts : load_posts() 返回的原始 DataFrame，或列结构相同的 DataFrame

    返回：
        result : 原始列 + impact_proba，按概率降序排列

    外部调用：
        from backend.model_predict import predict_new_posts
        from backend.model_training import load_posts
        posts, cat_cols, gdelt_cols = load_posts()
        result = predict_new_posts(posts.tail(100))
    """
    if not (MODEL_DIR / "xgb_model.pkl").exists():
        raise FileNotFoundError(
            f"模型文件不存在: {MODEL_DIR}\n请先运行 backend.model_training 完成训练。"
        )

    clf    = joblib.load(MODEL_DIR / "xgb_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    with open(MODEL_DIR / "feature_cols.json") as f:
        feature_cols = json.load(f)

    print(f"      📦 Model loaded  |  Expected features: {len(feature_cols)}")

    # 特征工程（和训练时完全一致）
    cat_cols_infer   = [c for c in new_posts.columns if c in CAT_COLS]
    gdelt_cols_infer = [c for c in new_posts.columns if c in GDELT_COLS]
    df, _ = engineer_features(new_posts.copy(), cat_cols_infer, gdelt_cols_infer)

    # 对齐特征列（缺失列补 0）
    for c in feature_cols:
        if c not in df.columns:
            df[c] = 0.0

    X    = df[feature_cols].fillna(0).astype(float).values
    X_sc = scaler.transform(X)

    df["impact_proba"] = clf.predict_proba(X_sc)[:, 1]

    high_risk = (df["impact_proba"] >= 0.6).sum()
    print(f"      🔍 Predicted {len(df):,} posts  |  "
          f"High-risk (≥0.6): {high_risk:,}  |  "
          f"Max proba: {df['impact_proba'].max():.3f}")

    keep = ["datetime", "content", "market_period", "during_market_hours", "impact_proba"]
    keep = [c for c in keep if c in df.columns]

    return df[keep].sort_values("impact_proba", ascending=False).reset_index(drop=True)


# ─────────────────────────────────────────────
# 2.  PREDICT LATEST (便捷方法，供外部/定时任务调用)
# ─────────────────────────────────────────────
def predict_latest(days: int = 7, fallback_n: int = 50) -> pd.DataFrame:
    """
    加载最新数据并预测，无需重新训练。

    参数：
        days       : 取最近多少天的帖子，默认 7 天
        fallback_n : 最近 days 天无数据时，改取最新 N 条，默认 50

    外部调用：
        from backend.model_predict import predict_latest
        result = predict_latest(days=3)
    """
    raw, _, _ = load_posts()

    cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=days)
    recent = raw[raw["datetime"] >= cutoff].copy()

    if recent.empty:
        print(f"      ⚠️  最近 {days} 天无数据，改用最新 {fallback_n} 条")
        recent = raw.sort_values("datetime").tail(fallback_n).copy()

    print(f"      Input: {len(recent):,} posts  "
          f"({recent['datetime'].min().date()} → {recent['datetime'].max().date()})")

    result = predict_new_posts(recent)

    # 打印 top-10 预览
    print(f"\n      {'datetime':<22} {'proba':>6}  {'market_period':<18}  content")
    print(f"      {'-'*22} {'-'*6}  {'-'*18}  {'-'*50}")
    for _, row in result.head(10).iterrows():
        dt      = str(row["datetime"])[:19]
        proba   = f"{row['impact_proba']:.3f}"
        period  = str(row.get("market_period", ""))[:18]
        content = str(row.get("content", ""))[:60].replace("\n", " ")
        print(f"      {dt:<22} {proba:>6}  {period:<18}  {content}")

    return result


# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("🧪  PREDICT TEST — latest 7 days")
    print("=" * 55)
    print(predict_latest(days=7))