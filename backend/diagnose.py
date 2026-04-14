"""
backend/diagnose.py
===================
Diagnose whether the model is genuinely learning or just
memorising the label distribution (majority-class baseline).

Run:
    python -m backend.diagnose
"""

import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    roc_auc_score,
)

from backend.model_training import (
    MODEL_DIR,
    CAT_COLS,
    GDELT_COLS,
    aggregate_daily,
    load_posts,
)

warnings.filterwarnings("ignore")

SEP = "=" * 60


# ─────────────────────────────────────────────
# 1.  RAW LABEL DISTRIBUTION
# ─────────────────────────────────────────────
def check_label_distribution(daily: pd.DataFrame) -> None:
    print(f"\n{SEP}")
    print("1. LABEL DISTRIBUTION")
    print(SEP)

    total     = len(daily)
    n_high    = int(daily["high_impact"].sum())
    n_low     = total - n_high
    pct_high  = n_high / total * 100

    print(f"   Total days      : {total:,}")
    print(f"   high_impact = 1 : {n_high:,}  ({pct_high:.1f}%)")
    print(f"   high_impact = 0 : {n_low:,}  ({100 - pct_high:.1f}%)")
    print(f"   Naive baseline AUC (always predict majority): 0.500")
    print(f"   Naive accuracy (always predict 0)           : {n_low/total*100:.1f}%")

    print(f"\n   next_day_ret stats:")
    print(daily["next_day_ret"].describe().to_string())


# ─────────────────────────────────────────────
# 2.  PREDICTION DISTRIBUTION
#     Are all probabilities clustered around the same value?
# ─────────────────────────────────────────────
def check_prediction_distribution(daily: pd.DataFrame, proba: np.ndarray) -> None:
    print(f"\n{SEP}")
    print("2. PREDICTION DISTRIBUTION")
    print(SEP)

    s = pd.Series(proba)
    print(f"   min    : {s.min():.4f}")
    print(f"   max    : {s.max():.4f}")
    print(f"   mean   : {s.mean():.4f}")
    print(f"   median : {s.median():.4f}")
    print(f"   std    : {s.std():.4f}")

    # bucket counts
    buckets = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.01]
    print("\n   Probability bucket distribution:")
    print(f"   {'bucket':<15} {'count':>6}  {'%':>6}")
    print(f"   {'-'*15} {'-'*6}  {'-'*6}")
    for lo, hi in zip(buckets[:-1], buckets[1:]):
        n   = ((s >= lo) & (s < hi)).sum()
        pct = n / len(s) * 100
        bar = "#" * int(pct / 2)
        print(f"   [{lo:.1f} – {hi:.1f})      {n:>6}  {pct:>5.1f}%  {bar}")

    std_warning = s.std() < 0.05
    print(f"\n   std < 0.05 (degenerate / collapsed output): "
          f"{'YES -- WARNING' if std_warning else 'NO -- OK'}")


# ─────────────────────────────────────────────
# 3.  CONFUSION MATRIX AT THRESHOLD 0.5
# ─────────────────────────────────────────────
def check_confusion_matrix(y_true: np.ndarray, proba: np.ndarray) -> None:
    print(f"\n{SEP}")
    print("3. CONFUSION MATRIX  (threshold = 0.50)")
    print(SEP)

    y_pred = (proba >= 0.5).astype(int)
    cm     = confusion_matrix(y_true, y_pred)

    tn, fp, fn, tp = cm.ravel()
    total          = len(y_true)
    accuracy       = (tp + tn) / total
    precision      = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall         = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1             = (2 * precision * recall / (precision + recall)
                      if (precision + recall) > 0 else 0)

    print(f"   {'':20}  Pred=0   Pred=1")
    print(f"   {'Actual=0 (low)':20}  {tn:>6}   {fp:>6}")
    print(f"   {'Actual=1 (high)':20}  {fn:>6}   {tp:>6}")
    print(f"\n   Accuracy  : {accuracy:.3f}")
    print(f"   Precision : {precision:.3f}  (of predicted HIGH, how many were right)")
    print(f"   Recall    : {recall:.3f}  (of actual HIGH, how many did we catch)")
    print(f"   F1        : {f1:.3f}")

    # red flag: model predicts everything as one class
    if tp == 0:
        print("\n   WARNING: model never predicts HIGH -- collapsed to majority class")
    elif tn == 0:
        print("\n   WARNING: model always predicts HIGH -- collapsed output")
    else:
        print("\n   OK: model predicts both classes")


# ─────────────────────────────────────────────
# 4.  COMPARE MODEL AUC VS NAIVE BASELINES
# ─────────────────────────────────────────────
def check_vs_baselines(y_true: np.ndarray, proba: np.ndarray) -> None:
    print(f"\n{SEP}")
    print("4. MODEL vs BASELINES")
    print(SEP)

    model_auc    = roc_auc_score(y_true, proba)
    model_ap     = average_precision_score(y_true, proba)
    random_auc   = 0.500
    majority_ap  = y_true.mean()          # AP of always-predict-positive

    # shuffle baseline (destroy any signal, keep distribution)
    rng           = np.random.default_rng(42)
    shuffled      = rng.permutation(proba)
    shuffled_auc  = roc_auc_score(y_true, shuffled)
    shuffled_ap   = average_precision_score(y_true, shuffled)

    print(f"   {'Model AUC':<30} : {model_auc:.4f}")
    print(f"   {'Random baseline AUC':<30} : {random_auc:.4f}")
    print(f"   {'Shuffled proba AUC':<30} : {shuffled_auc:.4f}  (expected ~0.50)")
    print(f"")
    print(f"   {'Model AP':<30} : {model_ap:.4f}")
    print(f"   {'Majority-class AP baseline':<30} : {majority_ap:.4f}  (label rate)")
    print(f"   {'Shuffled proba AP':<30} : {shuffled_ap:.4f}  (expected ~{majority_ap:.4f})")

    lift = model_ap / majority_ap if majority_ap > 0 else float("inf")
    print(f"\n   AP lift over baseline : {lift:.2f}x")

    if model_auc <= shuffled_auc + 0.02:
        print("\n   VERDICT: model AUC is NOT better than shuffled -- likely no signal")
    elif model_auc < 0.55:
        print("\n   VERDICT: model barely better than random -- weak signal")
    elif model_auc < 0.65:
        print("\n   VERDICT: modest signal detected")
    else:
        print("\n   VERDICT: meaningful signal -- model is learning something real")


# ─────────────────────────────────────────────
# 5.  CALIBRATION CHECK
#     Are high-proba days actually more often high-impact?
# ─────────────────────────────────────────────
def check_calibration(y_true: np.ndarray, proba: np.ndarray) -> None:
    print(f"\n{SEP}")
    print("5. CALIBRATION CHECK")
    print("   (are high-probability predictions actually correct more often?)")
    print(SEP)

    df = pd.DataFrame({"y": y_true, "p": proba})
    df["bucket"] = pd.cut(df["p"], bins=5)

    cal = (
        df.groupby("bucket", observed=True)
          .agg(count=("y", "count"), actual_rate=("y", "mean"))
          .reset_index()
    )

    print(f"   {'proba bucket':<22} {'count':>6}  {'actual high_impact rate':>24}")
    print(f"   {'-'*22} {'-'*6}  {'-'*24}")
    for _, row in cal.iterrows():
        bar  = "#" * int(row["actual_rate"] * 20)
        print(f"   {str(row['bucket']):<22} {int(row['count']):>6}  "
              f"{row['actual_rate']:>8.3f}  {bar}")

    # check if rate is monotonically increasing with proba bucket
    rates = cal["actual_rate"].tolist()
    is_monotone = all(rates[i] <= rates[i+1] + 0.05 for i in range(len(rates)-1))
    print(f"\n   Monotone calibration (higher proba -> higher actual rate): "
          f"{'YES -- OK' if is_monotone else 'NO -- WARNING'}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def run_diagnosis() -> None:
    print(f"\n{SEP}")
    print("TRUMP-SIGNAL MODEL DIAGNOSIS")
    print(SEP)

    # Load data
    posts, cat_cols, gdelt_cols = load_posts()
    daily, feature_cols = aggregate_daily(posts, cat_cols, gdelt_cols)
    daily = daily[daily["high_impact"].notna()].copy()

    # Load model
    clf    = joblib.load(MODEL_DIR / "xgb_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    with open(MODEL_DIR / "feature_cols.json") as f:
        saved_features = json.load(f)

    for c in saved_features:
        if c not in daily.columns:
            daily[c] = 0.0

    X     = daily[saved_features].fillna(0).astype(float).values
    X_sc  = scaler.transform(X)
    proba = clf.predict_proba(X_sc)[:, 1]
    y     = daily["high_impact"].astype(int).values

    # Split into test portion only (last 20%) for honest evaluation
    split_idx  = int(len(daily) * 0.80)
    y_test     = y[split_idx:]
    proba_test = proba[split_idx:]

    print(f"\n   Evaluating on TEST SET only (last 20%): {len(y_test):,} days")

    # Run all checks
    check_label_distribution(daily)
    check_prediction_distribution(daily, proba_test)
    check_confusion_matrix(y_test, proba_test)
    check_vs_baselines(y_test, proba_test)
    check_calibration(y_test, proba_test)

    print(f"\n{SEP}")
    print("DIAGNOSIS COMPLETE")
    print(SEP)


if __name__ == "__main__":
    run_diagnosis()