import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd   # ← THIS MUST BE HERE

from backend.model_training import (
    MODEL_DIR,
    CAT_COLS,
    GDELT_COLS,
    aggregate_daily,
    load_posts,
)
def predict_from_posts(posts: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate posts to daily level and predict next-day market impact.
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
    print(f"      STEP 1 - RAW POSTS: {len(posts)}")

    # ─────────────────────────────
    # AGGREGATION
    # ─────────────────────────────
    cat_cols_infer   = [c for c in posts.columns if c in CAT_COLS]
    gdelt_cols_infer = [c for c in posts.columns if c in GDELT_COLS]

    daily, _ = aggregate_daily(posts.copy(), cat_cols_infer, gdelt_cols_infer)

    print(f"      STEP 2 - DAILY ROWS AFTER AGG: {len(daily)}")

    if daily is None or daily.empty:
        print("🔥 WARNING: aggregate_daily returned EMPTY dataframe")

        return pd.DataFrame([{
            "date": None,
            "post_count": 0,
            "next_day_impact_proba": 0.0,
            "high_impact_pred": 0,
            "error": "No data after aggregation"
        }])

    # ─────────────────────────────
    # FEATURE ALIGNMENT
    # ─────────────────────────────
    for c in feature_cols:
        if c not in daily.columns:
            daily[c] = 0.0

    # Ensure correct column order
    X_df = daily[feature_cols].copy()

    print(f"      STEP 3 - FEATURE DF SHAPE: {X_df.shape}")

    X_df = X_df.fillna(0).astype(float)

    if X_df.shape[0] == 0:
        print("🔥 WARNING: Feature matrix is empty")

        return pd.DataFrame([{
            "date": None,
            "post_count": 0,
            "next_day_impact_proba": 0.0,
            "high_impact_pred": 0,
            "error": "Empty feature matrix"
        }])

    # ─────────────────────────────
    # SCALING + PREDICTION
    # ─────────────────────────────
    X = X_df.values
    X_sc = scaler.transform(X)

    daily["next_day_impact_proba"] = clf.predict_proba(X_sc)[:, 1]
    daily["high_impact_pred"]      = (daily["next_day_impact_proba"] >= 0.5).astype(int)

    high_risk = daily["high_impact_pred"].sum()

    print(f"      STEP 4 - FINAL ROWS: {len(daily)}")
    print(f"      High-risk days: {high_risk}")
    print(f"      Max proba: {daily['next_day_impact_proba'].max():.3f}")

    # ─────────────────────────────
    # OUTPUT
    # ─────────────────────────────
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