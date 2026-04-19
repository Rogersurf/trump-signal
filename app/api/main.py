"""FastAPI application for TrumpPulse (FULL version, production-ready)."""

from fastapi import FastAPI, HTTPException, APIRouter
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
# Fix database path for Hugging Face
# ------------------------------------------------------------------------------
import os
from backend_database.init_db import DEFAULT_DB_PATH as ORIGINAL_DB_PATH

# Override with HF data directory if it exists
HF_DATA_DIR = os.environ.get("TRUMPPULSE_DATA_DIR")
if HF_DATA_DIR:
    DEFAULT_DB_PATH = os.path.join(HF_DATA_DIR, "trump_data.db")
else:
    DEFAULT_DB_PATH = ORIGINAL_DB_PATH

print(f"[CONFIG] Using database at: {DEFAULT_DB_PATH}")

# ------------------------------------------------------------------------------
# Fix Python path (Docker / HF Spaces)
# ------------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from backend_database.embeddings import get_search_engine
from backend_database.init_db import DEFAULT_DB_PATH
from app.api.soy_trump_rhetoric import router as rhetoric_router
from app.api import monitoring

# ------------------------------------------------------------------------------
# App
# ------------------------------------------------------------------------------
app = FastAPI()

# External routers (inclui PRIMEIRO pra evitar conflitos)
app.include_router(rhetoric_router)
app.include_router(monitoring.router)

# ------------------------------------------------------------------------------
# Background Engine (NO rebuild allowed)
# ------------------------------------------------------------------------------
_engine = None
_index_ready = False
_index_building = False


def _initialize_engine():
    global _engine, _index_ready, _index_building

    _index_building = True

    try:
        time.sleep(2)
        print(f"[STARTUP] Loading search engine from {DEFAULT_DB_PATH}")

        _engine = get_search_engine(DEFAULT_DB_PATH)

        if _engine.embeddings is None:
            print("[STARTUP] WARNING: embeddings NOT loaded")
        else:
            print(f"[STARTUP] Engine ready with {len(_engine.posts)} posts")

        _index_ready = True

    except Exception as e:
        print(f"[STARTUP] ERROR: {e}")
        _index_ready = False

    finally:
        _index_building = False


threading.Thread(target=_initialize_engine, daemon=True).start()


def get_engine():
    if _index_building or not _index_ready:
        return None
    return _engine


# ------------------------------------------------------------------------------
# HEALTH (só uma, no app direto)
# ------------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ------------------------------------------------------------------------------
# QA (Semantic Search)
# ------------------------------------------------------------------------------
@app.get("/qa")
def qa(query: str, limit: int = 5):
    engine = get_engine()

    if engine is None:
        return {"error": "Search engine initializing"}

    try:
        results = engine.search(query, top_k=limit)

        conn = sqlite3.connect(DEFAULT_DB_PATH)
        enriched = []

        for r in results:
            post_id = r["post"].get("post_id", "")

            try:
                row = pd.read_sql(
                    """
                    SELECT url,
                           sp500_5min_before, sp500_5min_after,
                           qqq_5min_before, qqq_5min_after,
                           djt_5min_before, djt_5min_after,
                           during_market_hours
                    FROM truth_social
                    WHERE post_id = ?
                    LIMIT 1
                    """,
                    conn,
                    params=[str(post_id)],
                )

                if not row.empty:
                    extra = row.iloc[0].where(pd.notnull(row.iloc[0]), None).to_dict()
                    r["post"].update(extra)

            except:
                pass

            enriched.append(r)

        conn.close()

        return {"query": query, "results": enriched}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------------------------
# FEEDBACK
# ------------------------------------------------------------------------------
class FeedbackRequest(BaseModel):
    query: str
    response: str
    rating: int
    comment: str = ""


@app.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    conn = sqlite3.connect(DEFAULT_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            query TEXT,
            response TEXT,
            rating INTEGER,
            comment TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO feedback (timestamp, query, response, rating, comment) VALUES (?, ?, ?, ?, ?)",
        (
            datetime.now(timezone.utc).isoformat(),
            feedback.query,
            feedback.response,
            feedback.rating,
            feedback.comment,
        ),
    )

    conn.commit()
    conn.close()

    return {"status": "feedback recorded"}


# ------------------------------------------------------------------------------
# POSTS
# ------------------------------------------------------------------------------
@app.get("/posts")
def get_posts(start_date: str = None, end_date: str = None):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_full_data(date_from=start_date, date_to=end_date)

        if df.empty:
            return []

        df = df.replace({np.nan: None})

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------------------------------------
# STOCKS
# ------------------------------------------------------------------------------
@app.get("/stocks")
def get_stocks(index: str = "sp500", days: int = 30):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_stock_series(index, days)

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------------------------------------
# CATEGORIES
# ------------------------------------------------------------------------------
@app.get("/categories")
def get_categories(date_from: str = None, date_to: str = None):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_category_distribution(date_from, date_to)

        if isinstance(df, pd.Series):
            df = pd.DataFrame({"category": df.index, "count": df.values})

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------------------------------------
# CATEGORY IMPACT
# ------------------------------------------------------------------------------
@app.get("/categories/impact")
def get_category_impact(start: str, end: str):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_category_market_impact(start, end)

        if df.empty:
            return []

        return df[["category", "sp500_5min_pct"]].rename(
            columns={"sp500_5min_pct": "avg_impact"}
        ).to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------------------------------------
# GDELT
# ------------------------------------------------------------------------------
@app.get("/gdelt/range")
def gdelt_range(start: str, end: str):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_gdelt_trend(start, end)

        df = df.replace({np.nan: None})
        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


@app.get("/gdelt/summary")
def gdelt_summary(start: str, end: str):
    """Alias for gdelt_range - frontend expects this."""
    return gdelt_range(start, end)


# ------------------------------------------------------------------------------
# DATA / AVAILABLE DATES
# ------------------------------------------------------------------------------
@app.get("/data/available_dates")
def available_dates():
    try:
        conn = sqlite3.connect(DEFAULT_DB_PATH)
        df = pd.read_sql("SELECT DISTINCT date FROM daily_features ORDER BY date", conn)
        conn.close()
        return df["date"].tolist()
    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------------------------------------
# MODEL PREDICT
# ------------------------------------------------------------------------------
@app.get("/model/predict/date/{date}")
def model_predict_date(date: str):
    try:
        from backend.model_predict import predict_for_date
        
        result = predict_for_date(date, DEFAULT_DB_PATH)
        return result
    except Exception as e:
        return {"error": str(e), "date": date}


# ------------------------------------------------------------------------------
# PIPELINE STATUS
# ------------------------------------------------------------------------------
@app.get("/pipeline/status")
def pipeline_status():
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DEFAULT_DB_PATH)
        kpis = client.get_kpis()

        return {
            "total_posts": int(kpis.get("total_posts", 0)),
            "posts_today": int(kpis.get("posts_today", 0)),
            "status": "healthy",
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# ------------------------------------------------------------------------------
# DEBUG
# ------------------------------------------------------------------------------
@app.get("/debug")
def debug():
    engine = get_engine()

    return {
        "engine_ready": engine is not None,
        "posts_loaded": len(engine.posts) if engine else 0,
        "db_exists": os.path.exists(DEFAULT_DB_PATH),
    }


# ------------------------------------------------------------------------------
# ROOT
# ------------------------------------------------------------------------------
@app.get("/")
def root():
    return {"status": "running"}


# ------------------------------------------------------------------------------
# DEBUG: Print all registered routes
# ------------------------------------------------------------------------------
print("\n===== REGISTERED ROUTES =====")
for route in app.routes:
    print(f"  {route.path} -> {route.methods}")
print("==============================\n")