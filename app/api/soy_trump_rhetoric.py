from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
import io
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fastapi import APIRouter
from backend_database.data_api import TrumpDataClient
from backend.model_predict import predict_from_posts, predict_latest, predict_for_date
from backend.model_training import load_posts, MODEL_DIR

router = APIRouter(
    prefix="/rhetoric",    # path prefix all
    tags=["Rhetoric"]      # categorize endpoints in docs
)

db_client = TrumpDataClient("trump_data.db")


# ─────────────────────────────────────────────
# EXISTING ENDPOINTS
# ─────────────────────────────────────────────

@router.get("/")
def read_root():
    return {
        "status": "Online",
        "engine": "SQLite Local Storage",
        "message": "API is running using the Local Data API."
    }


@router.get("/stats")
def get_top_correlations():
    top_corrs = db_client.get_top_rhetoric_correlations(limit=5)
    return {"top_impact_pairs": top_corrs.to_dict()}


@router.get("/chart/pie")
def get_pie_chart():
    df = db_client.get_full_data()
    r_cols = [c for c in df.columns if c.startswith("cat_")]
    rhetoric_sums = df[r_cols].mean().sort_values(ascending=False)

    plt.figure(figsize=(8, 8))
    plt.pie(
        rhetoric_sums,
        labels=[c.replace("cat_", "").replace("_", " ").title() for c in rhetoric_sums.index],
        autopct="%1.1f%%",
        colors=sns.color_palette("rocket"),
    )
    plt.title("Trump Rhetoric Composition")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.get("/data/daily")
def get_daily_json():
    df_daily = db_client.get_daily_metrics()
    df_daily["day"] = df_daily["day"].dt.strftime("%Y-%m-%d")
    return df_daily.to_dict(orient="records")


@router.get("/data/latest")
def get_recent_posts(n: int = 5):
    posts = db_client.get_latest_posts(limit=n)
    return posts.to_dict(orient="records")


# ─────────────────────────────────────────────
# MODEL ENDPOINTS
# ─────────────────────────────────────────────

@router.get("/model/info")
def get_model_info():
    """
    Return saved model metrics and best threshold.
    """
    metrics_path = MODEL_DIR / "metrics.json"
    if not metrics_path.exists():
        raise HTTPException(status_code=404, detail="Model not trained yet. Run model_training first.")

    with open(metrics_path) as f:
        metrics = json.load(f)

    return {
        "status": "loaded",
        "test_auc":        round(metrics.get("roc_auc", 0), 4),
        "cv_auc_mean":     round(metrics.get("cv_auc_mean", 0), 4),
        "cv_auc_std":      round(metrics.get("cv_auc_std", 0), 4),
        "avg_precision":   round(metrics.get("avg_precision", 0), 4),
        "best_threshold":  round(metrics.get("best_threshold", 0.5), 4),
        "f1":              round(metrics.get("f1_t", 0), 4),
        "precision":       round(metrics.get("precision_t", 0), 4),
        "recall":          round(metrics.get("recall_t", 0), 4),
        "n_total_days":    metrics.get("n_total"),
        "n_high_impact":   metrics.get("n_high"),
        "test_period":     f"{metrics.get('test_start')} -> {metrics.get('test_end')}",
    }


@router.get("/model/predict/latest")
def predict_latest_endpoint(
    days: int = Query(default=7, ge=1, le=365, description="Number of recent calendar days to predict")
):
    """
    Predict next-day market impact probability for each of the last N days.

    Returns one row per day, sorted by date descending.
    """
    try:
        result = predict_latest(days=days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return _df_to_json(result)


@router.get("/model/predict/date/{target_date}")
def predict_date_endpoint(target_date: str):
    """
    Predict next-day market impact based on all posts from a specific date.

    Path param: target_date in YYYY-MM-DD format (e.g. /model/predict/date/2025-03-15)
    """
    try:
        result = predict_for_date(target_date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return _df_to_json(result)


@router.get("/model/predict/range")
def predict_range_endpoint(
    start: str = Query(..., description="Start date YYYY-MM-DD"),
    end:   str = Query(..., description="End date YYYY-MM-DD"),
):
    """
    Predict next-day market impact for every day in a date range.

    Example: /model/predict/range?start=2025-01-01&end=2025-03-31
    """
    try:
        raw, _, _ = load_posts()
        mask   = (raw["date"].dt.normalize() >= pd.Timestamp(start)) & \
                 (raw["date"].dt.normalize() <= pd.Timestamp(end))
        subset = raw[mask].copy()

        if subset.empty:
            raise HTTPException(status_code=404, detail=f"No posts found between {start} and {end}")

        result = predict_from_posts(subset)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return _df_to_json(result)


@router.get("/model/predict/today")
def predict_today_endpoint():
    """
    Predict next-day market impact based on today's posts so far.
    Returns the probability that TOMORROW will be a high-impact day.
    """
    try:
        today = pd.Timestamp.now(tz="UTC").date().isoformat()
        result = predict_for_date(today)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return _df_to_json(result)


@router.get("/model/predict/chart")
def predict_chart_endpoint(
    days: int = Query(default=30, ge=7, le=365, description="Number of recent days to chart")
):
    """
    Return a line chart of next-day impact probability over recent days.
    """
    try:
        result = predict_latest(days=days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    result = result.sort_values("date")

    fig, ax1 = plt.subplots(figsize=(14, 5))

    # Probability line
    ax1.plot(result["date"], result["next_day_impact_proba"],
             color="#e63946", linewidth=1.8, label="Next-Day Impact Proba")
    ax1.axhline(y=result["next_day_impact_proba"].mean(),
                color="#e63946", linestyle="--", alpha=0.4, linewidth=1)

    # Load best threshold from metrics
    metrics_path = MODEL_DIR / "metrics.json"
    if metrics_path.exists():
        with open(metrics_path) as f:
            saved = json.load(f)
        thresh = saved.get("best_threshold", 0.5)
    else:
        thresh = 0.5

    ax1.axhline(y=thresh, color="orange", linestyle=":", linewidth=1.5,
                label=f"Threshold ({thresh:.3f})")
    ax1.set_ylabel("Next-Day Impact Probability", color="#e63946")
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis="y", labelcolor="#e63946")

    # Actual high_impact markers
    if "high_impact" in result.columns:
        hi = result[result["high_impact"] == 1]
        ax1.scatter(hi["date"], hi["next_day_impact_proba"],
                    color="black", s=25, zorder=5, label="Actual High-Impact Day")

    # Post count bars on secondary axis
    if "post_count" in result.columns:
        ax2 = ax1.twinx()
        ax2.bar(result["date"], result["post_count"],
                alpha=0.15, color="#457b9d", label="Post Count")
        ax2.set_ylabel("Post Count", color="#457b9d")
        ax2.tick_params(axis="y", labelcolor="#457b9d")

    ax1.set_xlabel("Date")
    ax1.set_title(f"Next-Day Market Impact Probability (last {days} days)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc="upper left", fontsize=8)

    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=120)
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────
def _df_to_json(df: pd.DataFrame) -> list:
    """Convert DataFrame to JSON-safe list of dicts."""
    df = df.copy()
    for col in df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]):
        df[col] = df[col].astype(str)
    if "date" in df.columns:
        df["date"] = df["date"].astype(str)
    return df.where(pd.notnull(df), None).to_dict(orient="records")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn
