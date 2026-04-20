"""FastAPI application for TrumpPulse (FULL version, production-ready)."""

# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import sqlite3
from datetime import datetime, timezone
import threading
import time
import os
import sys

import pandas as pd
import numpy as np

# ------------------------------------------------------------------------------
# Fix Python path (Docker / HF Spaces)
# ------------------------------------------------------------------------------
sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

# ------------------------------------------------------------------------------
# SINGLE SOURCE OF TRUTH FOR DB
# ------------------------------------------------------------------------------
from backend_database.data_api import DB_PATH
print(f"[CONFIG] Using database at: {DB_PATH}")

# ------------------------------------------------------------------------------
# Imports internos
# ------------------------------------------------------------------------------
from backend_database.embeddings import get_search_engine
from app.api.soy_trump_rhetoric import router as rhetoric_router
from app.api import monitoring

# ------------------------------------------------------------------------------
# APP
# ------------------------------------------------------------------------------
app = FastAPI()

app.include_router(rhetoric_router)
app.include_router(monitoring.router)

# ------------------------------------------------------------------------------
# ENGINE STATE (EXPLÍCITO)
# ------------------------------------------------------------------------------
_engine = None
_index_ready = False
_index_building = False
_engine_started = False

# ------------------------------------------------------------------------------
# ENGINE INITIALIZATION (VERBOSE)
# ------------------------------------------------------------------------------
def _initialize_engine():
    global _engine, _index_ready, _index_building

    retries = 5
    delay = 3

    print("[STARTUP] Engine initialization started")

    for attempt in range(retries):

        print(f"[STARTUP] Attempt {attempt + 1}/{retries}")

        _index_building = True
        _index_ready = False

        try:
            print(f"[STARTUP] Loading engine from DB: {DB_PATH}")

            engine = get_search_engine(DB_PATH)

            # ---------------- VALIDATION ----------------
            if engine is None:
                raise Exception("Engine is None")

            if not hasattr(engine, "embeddings"):
                raise Exception("Missing embeddings")

            if engine.embeddings is None:
                raise Exception("Embeddings not loaded")

            if not hasattr(engine, "posts"):
                raise Exception("Missing posts")

            if len(engine.posts) == 0:
                raise Exception("No posts loaded")

            # ---------------- SUCCESS ----------------
            _engine = engine
            _index_ready = True
            _index_building = False

            print(f"[STARTUP] SUCCESS: {len(engine.posts)} posts loaded")

            return

        except Exception as e:
            print(f"[STARTUP] ERROR: {e}")

            _index_ready = False
            _index_building = True

            if attempt < retries - 1:
                print(f"[STARTUP] Retrying in {delay}s...")
                time.sleep(delay)

    print("[STARTUP] FAILED after retries")

    _engine = None
    _index_ready = False
    _index_building = False


def get_engine():
    if _index_building:
        print("[ENGINE] Requested while building")
        return None

    if not _index_ready:
        print("[ENGINE] Requested but not ready")
        return None

    if _engine is None:
        print("[ENGINE] Unexpected None")
        return None

    return _engine


# ------------------------------------------------------------------------------
# STARTUP THREAD CONTROL
# ------------------------------------------------------------------------------
@app.on_event("startup")
def startup_event():
    global _engine_started

    if _engine_started:
        print("[STARTUP] Engine already started")
        return

    print("[STARTUP] Starting engine thread")

    _engine_started = True

    thread = threading.Thread(
        target=_initialize_engine,
        daemon=True
    )
    thread.start()


# ------------------------------------------------------------------------------
# HEALTH
# ------------------------------------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "db_exists": os.path.exists(DB_PATH),
        "engine_ready": _index_ready,
        "engine_building": _index_building,
        "engine_loaded": _engine is not None
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