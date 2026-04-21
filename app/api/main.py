from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

from app.services.model_service import run_prediction

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "db_exists": os.path.exists(DB_PATH),
        "engine_ready": _index_ready,
        "engine_building": _index_building,
        "engine_loaded": _engine is not None
    }


<<<<<<< HEAD
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
        df = pd.read_sql(
            "SELECT DISTINCT date FROM daily_features ORDER BY date",
            conn
        )
        conn.close()

        return df["date"].tolist()

    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------------------------------------
# GDELT
# ------------------------------------------------------------------------------
@app.get("/gdelt/range")
def gdelt_range(start: str, end: str):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DB_PATH)
        df = client.get_gdelt_trend(start, end)

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


@app.get("/gdelt/summary")
def gdelt_summary(start: str, end: str):
    return gdelt_range(start, end)


@app.get("/gdelt")
def gdelt():
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DB_PATH)

        end = datetime.now()
        start = end - pd.Timedelta(days=30)

        df = client.get_gdelt_trend(
            start.strftime("%Y-%m-%d"),
            end.strftime("%Y-%m-%d")
        )

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


@app.get("/gdelt/timeseries")
def gdelt_timeseries(weeks: int = 8):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DB_PATH)

        end = datetime.now()
        start = end - pd.Timedelta(weeks=weeks)

        df = client.get_gdelt_trend(
            start.strftime("%Y-%m-%d"),
            end.strftime("%Y-%m-%d")
        )

        if df.empty:
            return []

        df["week"] = pd.to_datetime(df["date"]).dt.to_period("W").astype(str)

        agg = df.groupby("week").agg({
            "gdelt_avg_tone": "mean",
            "gdelt_verbal_conflict": "mean"
        }).reset_index()

        return agg.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------------------------------------
# POSTS
# ------------------------------------------------------------------------------
@app.get("/posts")
def get_posts(start_date: str = None, end_date: str = None):
    try:
        from backend_database.data_api import TrumpDataClient

        print(f"[POSTS] start={start_date} end={end_date}")

        if start_date is None and end_date is None:
            return {"error": "Date range required"}

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

from backend.model_predict import predict_for_date
from backend_database.data_api import TrumpDataClient

import traceback

@app.get("/model/predict/date/{date}")
def predict_date(date: str):
    try:
        return predict_for_date(date)
    except Exception as e:
        print("🔥 PREDICT ERROR:", str(e))
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/categories")
def categories(period: str = "month", date_from: str = None, date_to: str = None):
    try:
        client = TrumpDataClient(DB_PATH)
        df = client.get_full_data(date_from=date_from, date_to=date_to)

        if df is None or df.empty:
            return []

        if "category" not in df.columns:
            return []

        result = df["category"].value_counts().reset_index()
        result.columns = ["category", "count"]

        return result.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

@app.get("/stocks")
def stocks(index: str = "sp500", days: int = 30):
    try:
        import numpy as np
        import pandas as pd
        from datetime import datetime

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
=======
@app.get("/predict")
def predict():
    return run_prediction()
>>>>>>> backup/stable-working
