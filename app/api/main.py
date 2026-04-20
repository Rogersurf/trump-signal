"""FastAPI application for TrumpPulse (FULL version, production-ready)."""

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
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ------------------------------------------------------------------------------
# SINGLE SOURCE OF TRUTH FOR DB
# ------------------------------------------------------------------------------
from backend_database.data_api import DB_PATH

print(f"[CONFIG] Using database at: {DB_PATH}")

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from backend_database.embeddings import get_search_engine
from app.api.soy_trump_rhetoric import router as rhetoric_router
from app.api import monitoring

# ------------------------------------------------------------------------------
# App
# ------------------------------------------------------------------------------
app = FastAPI()

app.include_router(rhetoric_router)
app.include_router(monitoring.router)

# ------------------------------------------------------------------------------
# Background Engine
# ------------------------------------------------------------------------------
_engine = None
_index_ready = False
_index_building = False


def _initialize_engine():
    global _engine, _index_ready, _index_building

    _index_building = True

    try:
        time.sleep(2)
        print(f"[STARTUP] Loading search engine from {DB_PATH}")

        _engine = get_search_engine(DB_PATH)

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
# HEALTH
# ------------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ------------------------------------------------------------------------------
# QA
# ------------------------------------------------------------------------------
@app.get("/qa")
def qa(query: str, limit: int = 5):
    engine = get_engine()

    if engine is None:
        return {"error": "Search engine initializing"}

    try:
        results = engine.search(query, top_k=limit)

        conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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
# POSTS / STOCKS / ETC
# ------------------------------------------------------------------------------
@app.get("/posts")
def get_posts(start_date: str = None, end_date: str = None):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DB_PATH)
        df = client.get_full_data(date_from=start_date, date_to=end_date)

        if df.empty:
            return []

        df = df.replace({np.nan: None})
        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


@app.get("/stocks")
def get_stocks(index: str = "sp500", days: int = 30):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DB_PATH)
        df = client.get_stock_series(index, days)

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


@app.get("/categories")
def get_categories(date_from: str = None, date_to: str = None):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DB_PATH)
        df = client.get_category_distribution(date_from, date_to)

        if isinstance(df, pd.Series):
            df = pd.DataFrame({"category": df.index, "count": df.values})

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


@app.get("/categories/impact")
def get_category_impact(start: str, end: str):
    try:
        from backend_database.data_api import TrumpDataClient

        client = TrumpDataClient(DB_PATH)
        df = client.get_category_market_impact(start, end)

        if df.empty:
            return []

        return df[["category", "sp500_5min_pct"]].rename(
            columns={"sp500_5min_pct": "avg_impact"}
        ).to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------------------------------------
# MODEL
# ------------------------------------------------------------------------------
@app.get("/model/predict/date/{date}")
def model_predict_date(date: str):
    try:
        from backend.model_predict import predict_for_date
        return predict_for_date(date)
    except Exception as e:
        return {"error": str(e), "date": date}


# ------------------------------------------------------------------------------
# DEBUG
# ------------------------------------------------------------------------------
@app.get("/debug")
def debug():
    engine = get_engine()

    return {
        "engine_ready": engine is not None,
        "posts_loaded": len(engine.posts) if engine else 0,
        "db_exists": os.path.exists(DB_PATH),
    }


# ------------------------------------------------------------------------------
# ROOT
# ------------------------------------------------------------------------------
@app.get("/")
def root():
    return {"status": "running"}


# ------------------------------------------------------------------------------
# ROUTES DEBUG
# ------------------------------------------------------------------------------
print("\n===== REGISTERED ROUTES =====")
for route in app.routes:
    print(f"  {route.path} -> {route.methods}")
print("==============================\n")