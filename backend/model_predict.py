"""
backend/model_predict.py
========================
Trump Truth Social -> Next-Day Market Impact Predictor (Inference).
Depends on model artifacts saved by model_training.py.

Usage:
    python -m backend.model_predict
    from backend.model_predict import predict_latest, predict_for_date
"""

import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from backend.model_training import (
    MODEL_DIR,
    CAT_COLS,
    GDELT_COLS,
    aggregate_daily,
    load_posts,
)

warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────
# 1.  CORE INFERENCE
#     Input  : raw post DataFrame (same schema as load_posts())
#     Output : daily-level DataFrame with next-day impact probability
# ─────────────────────────────────────────────
def predict_from_posts(posts: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate posts to daily level and predict next-day market impact.

    Args:
        posts : raw post DataFrame with same schema as load_posts()

    Returns:
        daily DataFrame with columns:
            date, post_count, next_day_impact_proba, high_impact_pred
        sorted by date descending
    """
    if not (MODEL_DIR / "xgb_model.pkl").exists():
        raise FileNotFoundError(
            f"Model artifacts not found at: {MODEL_DIR}\n"
            "Please run backend.model_training first."
        )

    clf    = joblib.load(MODEL_DIR / "xgb_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    with open(MODEL_DIR / "feature_cols.json") as f:
        feature_cols = json.load(f)

    print(f"      Model loaded  |  Expected features: {len(feature_cols)}")

    # Aggregate posts to daily level using the same logic as training
    cat_cols_infer   = [c for c in posts.columns if c in CAT_COLS]
    gdelt_cols_infer = [c for c in posts.columns if c in GDELT_COLS]
    daily, _ = aggregate_daily(posts.copy(), cat_cols_infer, gdelt_cols_infer,predict_mode=True)

    # Align feature columns (fill missing with 0)
    for c in feature_cols:
        if c not in daily.columns:
            daily[c] = 0.0

    X    = daily[feature_cols].fillna(0).astype(float).values
    X_sc = scaler.transform(X)

    daily["next_day_impact_proba"] = clf.predict_proba(X_sc)[:, 1]
    daily["high_impact_pred"]      = (daily["next_day_impact_proba"] >= 0.5).astype(int)

    high_risk = daily["high_impact_pred"].sum()
    print(f"      Predicted {len(daily):,} days  |  "
          f"High-risk days (>=0.5): {high_risk:,}  |  "
          f"Max proba: {daily['next_day_impact_proba'].max():.3f}")

    keep = ["date", "post_count", "next_day_ret", "high_impact",
            "next_day_impact_proba", "high_impact_pred"]
    keep = [c for c in keep if c in daily.columns]

    return daily[keep].sort_values("date", ascending=False).reset_index(drop=True)


# ─────────────────────────────────────────────
# 2.  PREDICT LATEST N DAYS
#     Convenient wrapper for scheduled jobs / API calls
# ─────────────────────────────────────────────
def predict_latest(days: int = 7) -> pd.DataFrame:
    """
    Load the most recent posts and predict next-day impact for each day.

    Args:
        days : how many recent calendar days to include (default 7)

    Returns:
        daily prediction DataFrame sorted by date descending

    Example:
        from backend.model_predict import predict_latest
        result = predict_latest(days=7)
    """
    raw, _, _ = load_posts()

    cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=days)
    recent = raw[raw["datetime"] >= cutoff].copy()

    if recent.empty:
        print(f"      No posts found in the last {days} days. Using latest 30 days.")
        cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=30)
        recent = raw[raw["datetime"] >= cutoff].copy()

    if recent.empty:
        raise ValueError("No posts available for prediction.")

    print(f"      Input: {len(recent):,} posts  "
          f"({recent['datetime'].min().date()} -> {recent['datetime'].max().date()})")

    result = predict_from_posts(recent)
    _print_prediction_table(result)
    return result


# ─────────────────────────────────────────────
# 3.  PREDICT FOR A SPECIFIC DATE
#     Given a date, predict what next-day impact will be
#     based on that day's posts.
# ─────────────────────────────────────────────
def predict_for_date(target_date: str) -> pd.DataFrame:
    """
    Predict next-day market impact based on posts from a specific date.

    Args:
        target_date : date string in 'YYYY-MM-DD' format

    Returns:
        single-row daily prediction DataFrame

    Example:
        from backend.model_predict import predict_for_date
        result = predict_for_date("2025-03-15")
    """
    raw, _, _ = load_posts()

    target = pd.Timestamp(target_date).normalize()
    day_posts = raw[raw["date"].dt.normalize() == target].copy()

    if day_posts.empty:
        raise ValueError(f"No posts found for date: {target_date}")

    print(f"      Input: {len(day_posts):,} posts on {target_date}")

    result = predict_from_posts(day_posts)
    _print_prediction_table(result)
    return result


# ─────────────────────────────────────────────
# 4.  PRINT HELPER
# ─────────────────────────────────────────────
def _print_prediction_table(result: pd.DataFrame) -> None:
    print(f"\n      {'date':<12} {'posts':>6}  {'proba':>6}  {'pred':>5}  {'actual':>6}")
    print(f"      {'-'*12} {'-'*6}  {'-'*6}  {'-'*5}  {'-'*6}")
    for _, row in result.head(10).iterrows():
        date   = str(row["date"])[:10]
        posts  = int(row["post_count"]) if "post_count" in row else "-"
        proba  = f"{row['next_day_impact_proba']:.3f}"
        pred   = "HIGH" if row["high_impact_pred"] else "low"
        actual = str(int(row["high_impact"])) if "high_impact" in row and pd.notna(row["high_impact"]) else "?"
        print(f"      {date:<12} {posts:>6}  {proba:>6}  {pred:>5}  {actual:>6}")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("PREDICT TEST -- latest 7 days")
    print("=" * 55)
    result = predict_latest(days=7)
    print(result)