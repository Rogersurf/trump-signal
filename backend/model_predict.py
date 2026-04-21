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
# CORE
# ─────────────────────────────────────────────
def predict_from_posts(posts: pd.DataFrame) -> pd.DataFrame:

    if not (MODEL_DIR / "xgb_model.pkl").exists():
        raise FileNotFoundError(
            f"Model artifacts not found at: {MODEL_DIR}\n"
            "Please run backend.model_training first."
        )

    clf    = joblib.load(MODEL_DIR / "xgb_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    with open(MODEL_DIR / "feature_cols.json") as f:
        feature_cols = json.load(f)

    print(f"Model loaded | features: {len(feature_cols)}")
    print(f"RAW POSTS: {len(posts)}")

    cat_cols_infer   = [c for c in posts.columns if c in CAT_COLS]
    gdelt_cols_infer = [c for c in posts.columns if c in GDELT_COLS]

    daily, _ = aggregate_daily(posts.copy(), cat_cols_infer, gdelt_cols_infer)

    print(f"DAILY ROWS: {len(daily)}")

    if daily is None or daily.empty:
        return pd.DataFrame(columns=[
            "date",
            "post_count",
            "next_day_impact_proba",
            "high_impact_pred"
        ])

    for c in feature_cols:
        if c not in daily.columns:
            daily[c] = 0.0

    X_df = daily[feature_cols].fillna(0).astype(float)

    if X_df.shape[0] == 0:
        return pd.DataFrame(columns=[
            "date",
            "post_count",
            "next_day_impact_proba",
            "high_impact_pred"
        ])

    X = X_df.values
    X_sc = scaler.transform(X)

    daily["next_day_impact_proba"] = clf.predict_proba(X_sc)[:, 1]
    daily["high_impact_pred"]      = (daily["next_day_impact_proba"] >= 0.5).astype(int)

    keep = [
        "date",
        "post_count",
        "next_day_ret",
        "high_impact",
        "next_day_impact_proba",
        "high_impact_pred"
    ]
    keep = [c for c in keep if c in daily.columns]

    return (
        daily[keep]
        .sort_values("date", ascending=False)
        .reset_index(drop=True)
    )


# ─────────────────────────────────────────────
# LATEST
# ─────────────────────────────────────────────
def predict_latest(days: int = 7) -> pd.DataFrame:
    raw, _, _ = load_posts()

    cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=days)
    recent = raw[raw["datetime"] >= cutoff].copy()

    if recent.empty:
        cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=30)
        recent = raw[raw["datetime"] >= cutoff].copy()

    if recent.empty:
        raise ValueError("No posts available")

    print(f"Input: {len(recent)} posts")

    return predict_from_posts(recent)


# ─────────────────────────────────────────────
# DATE
# ─────────────────────────────────────────────
def predict_for_date(target_date: str) -> pd.DataFrame:
    raw, _, _ = load_posts()

    target = pd.Timestamp(target_date).normalize()
    day_posts = raw[raw["date"].dt.normalize() == target].copy()

    if day_posts.empty:
        raise ValueError(f"No posts for {target_date}")

    print(f"Input: {len(day_posts)} posts on {target_date}")

    return predict_from_posts(day_posts)