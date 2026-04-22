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

    # 🔥 USE CONTEXT WINDOW (30 DAYS BACK)
    window_start = target - pd.Timedelta(days=30)

    day_posts = raw[
        (raw["date"].dt.normalize() >= window_start) &
        (raw["date"].dt.normalize() <= target)
    ].copy()

    if day_posts.empty:
        raise ValueError(f"No posts for {target_date}")

    print(f"Input: {len(day_posts)} posts on {target_date}")

    return predict_from_posts(day_posts)

def aggregate_daily(df: pd.DataFrame, cat_cols: list, gdelt_cols: list):
    """
    Robust daily aggregation that NEVER collapses to empty due to:
    - rolling windows
    - missing values
    - sparse days

    Returns:
        daily DataFrame + feature_cols
    """

    print(f"STEP 0 - INPUT ROWS: {len(df)}")

    if df is None or df.empty:
        print("🔥 EMPTY INPUT DF")
        return pd.DataFrame(), []

    # ─────────────────────────────
    # BASIC CLEAN
    # ─────────────────────────────
    df = df.copy()

    # guarantee datetime
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime"])

    if df.empty:
        print("🔥 ALL DATETIME INVALID")
        return pd.DataFrame(), []

    df["date"] = df["datetime"].dt.normalize()

    print(f"STEP 1 - AFTER DATETIME CLEAN: {len(df)}")

    # ─────────────────────────────
    # OPTIONAL FILTER (SAFE)
    # ─────────────────────────────
    if "during_market_hours" in df.columns:
        before = len(df)
        df = df[df["during_market_hours"].fillna(1) == 1]
        print(f"STEP 2 - MARKET FILTER: {before} → {len(df)}")

    if df.empty:
        print("🔥 ALL DATA REMOVED BY FILTER")
        return pd.DataFrame(), []

    # ─────────────────────────────
    # GROUP BY DAY
    # ─────────────────────────────
    agg_dict = {}

    # post count
    agg_dict["post_id"] = "count"

    # categories
    for c in cat_cols:
        if c in df.columns:
            agg_dict[c] = "sum"

    # gdelt
    for c in gdelt_cols:
        if c in df.columns:
            agg_dict[c] = "mean"

    daily = df.groupby("date").agg(agg_dict).reset_index()

    daily = daily.rename(columns={"post_id": "post_count"})

    print(f"STEP 3 - AFTER GROUPBY: {len(daily)}")

    if daily.empty:
        print("🔥 GROUPBY RETURNED EMPTY")
        return pd.DataFrame(), []

    # ─────────────────────────────
    # SAFE FEATURE ENGINEERING
    # ─────────────────────────────

    # Normalize categories (per post)
    for c in cat_cols:
        if c in daily.columns:
            daily[c] = daily[c] / daily["post_count"].replace(0, 1)

    # ─────────────────────────────
    # ROLLING FEATURES (SAFE)
    # ─────────────────────────────
    rolling_cols = []

    for col in daily.columns:
        if col in ["date"]:
            continue

        # 3-day rolling
        r3 = f"{col}_r3"
        daily[r3] = daily[col].rolling(3, min_periods=1).mean()
        rolling_cols.append(r3)

        # 7-day rolling
        r7 = f"{col}_r7"
        daily[r7] = daily[col].rolling(7, min_periods=1).mean()
        rolling_cols.append(r7)

    print(f"STEP 4 - AFTER ROLLING: {len(daily)}")

    # ─────────────────────────────
    # TARGET (SAFE)
    # ─────────────────────────────
    if "sp500_close" in df.columns:
        price = df.groupby("date")["sp500_close"].mean().reset_index()
        daily = daily.merge(price, on="date", how="left")

        daily["next_day_ret"] = daily["sp500_close"].pct_change().shift(-1)
        daily["high_impact"] = (daily["next_day_ret"].abs() > 0.01).astype(int)

    # ─────────────────────────────
    # FINAL CLEAN (DO NOT DROP ALL)
    # ─────────────────────────────
    daily = daily.sort_values("date")

    # ⚠️ CRITICAL FIX: DO NOT DROP ROWS
    daily = daily.fillna(0)

    print(f"STEP 5 - FINAL ROWS: {len(daily)}")

    # ─────────────────────────────
    # FEATURE LIST
    # ─────────────────────────────
    feature_cols = [
        c for c in daily.columns
        if c not in ["date", "next_day_ret", "high_impact"]
    ]

    return daily, feature_cols