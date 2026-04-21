from fastapi import FastAPI
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import traceback
import os

from backend_database.data_api import TrumpDataClient
from backend.model_predict import predict_for_date
from backend.model_training import load_posts

app = FastAPI()

DB_PATH = os.environ.get("DB_PATH", "/data/trump_pulse/trump_data.db")

# ------------------------------------------------------------------------------
# HEALTH
# ------------------------------------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "db_exists": os.path.exists(DB_PATH)
    }

# ------------------------------------------------------------------------------
# MAX DATE
# ------------------------------------------------------------------------------
@app.get("/data/max_date")
def max_date():
    try:
        conn = sqlite3.connect(DB_PATH)
        date = conn.execute("SELECT MAX(date) FROM truth_social").fetchone()[0]
        conn.close()

        if date is None:
            return {"max_date": datetime.today().strftime("%Y-%m-%d")}

        return {"max_date": date}

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# AVAILABLE DATES
# ------------------------------------------------------------------------------
@app.get("/data/available_dates")
def available_dates():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT DISTINCT date FROM truth_social ORDER BY date", conn)
        conn.close()

        return df["date"].tolist()

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# POSTS
# ------------------------------------------------------------------------------
@app.get("/posts")
def get_posts(start_date: str = None, end_date: str = None):
    try:
        client = TrumpDataClient(DB_PATH)

        df = client.get_full_data(
            date_from=start_date,
            date_to=end_date
        )

        if df is None or df.empty:
            return []

        df = df.replace({np.nan: None})
        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# CATEGORIES (FIXED)
# ------------------------------------------------------------------------------
@app.get("/categories")
def categories(date_from: str = None, date_to: str = None):
    try:
        client = TrumpDataClient(DB_PATH)
        df = client.get_full_data(date_from=date_from, date_to=date_to)

        if df is None or df.empty:
            return []

        cat_cols = [c for c in df.columns if c.startswith("cat_")]

        if not cat_cols:
            return []

        # Derive category
        df["category"] = df[cat_cols].idxmax(axis=1)
        df["category"] = df["category"].str.replace("cat_", "")

        result = df["category"].value_counts().reset_index()
        result.columns = ["category", "count"]

        return result.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# CATEGORY IMPACT (NEW)
# ------------------------------------------------------------------------------
@app.get("/categories/impact")
def get_category_impact(start: str, end: str):
    import pandas as pd

    df, cat_cols, _ = load_posts()

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    df = df[(df["date"] >= start) & (df["date"] <= end)].copy()

    if df.empty:
        return []

    # 🔥 CREATE IMPACT (YOU LOST THIS)
    if "sp500_close" in df.columns and "sp500_open" in df.columns:
        df["impact"] = (df["sp500_close"] - df["sp500_open"]).fillna(0)
    else:
        return []

    results = []

    for cat in cat_cols:
        if cat not in df.columns:
            continue

        subset = df[df[cat] > 0.5]

        if subset.empty:
            continue

        avg_impact = subset["impact"].mean()

        results.append({
            "category": cat.replace("cat_", ""),
            "avg_impact": float(avg_impact)
        })

    return results

# ------------------------------------------------------------------------------
# GDELT (FIXED)
# ------------------------------------------------------------------------------
@app.get("/gdelt/range")
def gdelt_range(start: str, end: str):
    try:
        client = TrumpDataClient(DB_PATH)
        df = client.get_gdelt_trend(start, end)

        if df is None or df.empty:
            return []

        import numpy as np

        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.replace({np.nan: None})

        return df.to_dict(orient="records")

    except Exception as e:
        print("ERROR:", e)  # 👈 IMPORTANTE
        return {"error": str(e)}

@app.get("/gdelt/summary")
def gdelt_summary(start: str, end: str):
    return gdelt_range(start, end)

@app.get("/gdelt/timeseries")
def gdelt_timeseries(weeks: int = 8):
    try:
        client = TrumpDataClient(DB_PATH)

        end = datetime.now()
        start = end - pd.Timedelta(weeks=weeks)

        df = client.get_gdelt_trend(
            start.strftime("%Y-%m-%d"),
            end.strftime("%Y-%m-%d")
        )

        if df is None or df.empty:
            return []

        df = df.fillna(0)

        df["week"] = pd.to_datetime(df["date"]).dt.to_period("W").astype(str)

        agg = df.groupby("week").agg({
            "gdelt_avg_tone": "mean",
            "gdelt_verbal_conflict": "mean"
        }).reset_index()

        return agg.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# MODEL
# ------------------------------------------------------------------------------
@app.get("/model/predict/date/{date}")
def predict_date(date: str):
    try:
        return predict_for_date(date)
    except Exception as e:
        print("🔥 PREDICT ERROR:", str(e))
        traceback.print_exc()
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# QA (SAFE FALLBACK)
# ------------------------------------------------------------------------------
@app.get("/qa")
def qa(q: str):
    return {
        "answer": "Q&A engine not ready yet",
        "matches": []
    }

# ------------------------------------------------------------------------------
# STOCKS (MOCK SAFE)
# ------------------------------------------------------------------------------
@app.get("/stocks")
def stocks(index: str = "sp500", days: int = 30):
    try:
        dates = pd.date_range(end=datetime.today(), periods=days)

        df = pd.DataFrame({
            "date": dates.astype(str),
            "price": np.random.rand(days) * 100,
            "has_big_post": np.random.choice([True, False], days),
            "pct_change": np.random.randn(days)
        })

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}