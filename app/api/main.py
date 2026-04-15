"""FastAPI application for TrumpPulse."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import math
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timezone
import sys
import os
import threading
import time
import pandas as pd
import numpy as np

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend_database.embeddings import get_search_engine
from backend_database.init_db import DEFAULT_DB_PATH

# ------------------------------------------------------------------------------
# Create FastAPI app FIRST (so Uvicorn can start immediately)
# ------------------------------------------------------------------------------
app = FastAPI()

# Add monitoring router
from app.api import monitoring
app.include_router(monitoring.router)

# ------------------------------------------------------------------------------
# Background index initialization (does NOT block startup)
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
            print("[STARTUP] Embeddings cache missing. Building index (this may take a few minutes)...")
            _engine.build_index(force=True)
        print(f"[STARTUP] Engine ready with {len(_engine.posts)} posts.")
        _index_ready = True
    except Exception as e:
        print(f"[STARTUP] ERROR initializing search engine: {e}")
        _index_ready = False
    finally:
        _index_building = False

threading.Thread(target=_initialize_engine, daemon=True).start()

def get_engine():
    global _engine, _index_ready, _index_building
    if _index_building or not _index_ready:
        return None
    return _engine

# ------------------------------------------------------------------------------
# Health Endpoint
# ------------------------------------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}

# ------------------------------------------------------------------------------
# Q&A Endpoint (Semantic Search)
# ------------------------------------------------------------------------------
@app.get("/qa")
def qa(query: str, limit: int = 5):
    engine = get_engine()
    if engine is None:
        return {"error": "Search engine is still initializing. Please try again in a minute."}
    try:
        results = engine.search(query, top_k=limit)
        return {"query": query, "results": results}
    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# Feedback Endpoint
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
        (datetime.now(timezone.utc).isoformat(), feedback.query, feedback.response, feedback.rating, feedback.comment)
    )
    conn.commit()
    conn.close()
    return {"status": "feedback recorded"}

# ------------------------------------------------------------------------------
# Market Impact & Data Endpoints (for frontend pages)
# ------------------------------------------------------------------------------
@app.get("/stocks")
def get_stocks(index: str = "sp500", days: int = 30):
    """Return stock series data for the given index."""
    try:
        from backend_database.data_api import TrumpDataClient
        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_stock_series(index, days)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

@app.get("/categories/impact")
def get_category_impact(start: str, end: str):
    """Return average market impact by category for a date range."""
    try:
        from backend_database.data_api import TrumpDataClient
        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_category_market_impact(start=start, end=end)
        if not df.empty:
            return df[["category", "sp500_5min_pct"]].rename(
                columns={"sp500_5min_pct": "avg_impact"}
            ).to_dict(orient="records")
        return []
    except Exception as e:
        return {"error": str(e)}

@app.get("/data/available_dates")
def get_available_dates():
    """Return the min and max dates available in the dataset."""
    try:
        import sqlite3
        conn = sqlite3.connect(DEFAULT_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(date), MAX(date) FROM truth_social")
        min_date, max_date = cursor.fetchone()
        conn.close()
        return {"min_date": min_date, "max_date": max_date}
    except Exception as e:
        return {"error": str(e)}

@app.get("/posts")
def get_posts(start_date: str = None, end_date: str = None):
    """Return posts for a given date range, formatted for frontend."""
    try:
        from backend_database.data_api import TrumpDataClient
        from datetime import datetime

        # Helper to convert various date inputs to YYYY-MM-DD
        def _parse_date(date_str: str) -> str | None:
            if not date_str:
                return None
            # Try common formats
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y%m%d"):
                try:
                    return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue
            # If all fail, return original (might already be correct)
            return date_str

        start = _parse_date(start_date)
        end = _parse_date(end_date)

        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_full_data(date_from=start, date_to=end)
        if df.empty:
            return []
        
        # Ensure datetime column exists and is string for JSON
        if 'date' in df.columns:
            df['datetime'] = pd.to_datetime(df['date'], errors='coerce')
            df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            df['datetime'] = None
        
        # Rename columns to match frontend expectations
        df = df.rename(columns={
            "replies_count":    "replies",
            "reblogs_count":    "reblogs",
            "favourites_count": "favourites",
        })
        
        # Add missing columns with defaults if not present
        if "sentiment" not in df.columns:
            df["sentiment"] = "NEUTRAL"
        if "sentiment_score" not in df.columns:
            df["sentiment_score"] = 0.5
        if "dominant_category" not in df.columns:
            df["dominant_category"] = "Other"
        if "has_media" not in df.columns:
            df["has_media"] = False
        if "is_president" not in df.columns:
            df["is_president"] = True
        if "post_type" not in df.columns:
            df["post_type"] = "original"
        
        import json, math
        records = df.to_dict(orient="records")
        clean = [{k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in r.items()} for r in records]
        return clean
    except Exception as e:
        return {"error": str(e)}

@app.get("/categories")
def get_categories(period: str = "month", date_from: str = None, date_to: str = None):
    """Return category distribution."""
    try:
        from backend_database.data_api import TrumpDataClient
        client = TrumpDataClient(DEFAULT_DB_PATH)
        # Use get_category_distribution
        result = client.get_category_distribution(date_from=date_from, date_to=date_to)
        if isinstance(result, pd.Series):
            df = pd.DataFrame({"category": result.index, "count": result.values})
        else:
            df = result
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

@app.get("/pipeline/status")
def pipeline_status():
    """Return pipeline status for dev dashboard."""
    try:
        from backend_database.data_api import TrumpDataClient
        client = TrumpDataClient(DEFAULT_DB_PATH)
        kpis = client.get_kpis()
        return {
            "last_ingest": "daily @ 00:00 UTC (APScheduler)",
            "last_preprocess": "on ingest",
            "last_sentiment_run": "pre-labeled in dataset",
            "last_embedding_build": "on ingest",
            "last_gdelt_update": "weekly",
            "total_posts": int(kpis.get("total_posts", 0)),
            "posts_today": int(kpis.get("posts_today", 0)),
            "pct_market_hours": round(float(kpis.get("pct_market_hours", 0)), 1),
            "model_name": "cardiffnlp/twitter-roberta-base-sentiment",
            "embedding_model": "all-MiniLM-L6-v2",
            "dataset_version": "chrissoria/trump-truth-social @ main",
            "artifact_path": "backend_database/trump_data.db",
            "status": "healthy",
            "errors": [],
        }
    except Exception as e:
        return {"status": "error", "errors": [str(e)]}

# ------------------------------------------------------------------------------
# GDELT Endpoints (for geopolitical page)
# ------------------------------------------------------------------------------
@app.get("/gdelt/range")
def get_gdelt_range(start: str, end: str):
    """Return GDELT trend data for a date range."""
    try:
        from backend_database.data_api import TrumpDataClient
        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_gdelt_trend(start=start, end=end)
        if df.empty:
            return []
        df["day"] = pd.to_datetime(df["day"]).dt.strftime("%Y-%m-%d")
        # Replace NaN with None (JSON compliant)
        df = df.replace({np.nan: None})
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

@app.get("/gdelt/summary")
def get_gdelt_summary(start: str, end: str):
    """Return GDELT summary metrics for a date range."""
    try:
        from backend_database.data_api import TrumpDataClient
        client = TrumpDataClient(DEFAULT_DB_PATH)
        df = client.get_gdelt_trend(start=start, end=end)
        if df.empty:
            return {}
        # Build summary
        summary = {
            "week_of": pd.to_datetime(df["day"]).max().strftime("%d %b %Y"),
            "military_events": int(df["gdelt_military"].fillna(0).sum()),
            "verbal_conflict": int(df["gdelt_verbal_conflict"].fillna(0).sum()),
            "verbal_cooperation": int(df["gdelt_verbal_cooperation"].fillna(0).sum()),
            "material_conflict": int(df["gdelt_material_conflict"].fillna(0).sum()),
            "diplomatic": 0,
            "goldstein_avg": round(float(df["gdelt_goldstein_avg"].fillna(0).mean()), 2),
            "avg_tone": round(float(df["gdelt_avg_tone"].fillna(0).mean()), 2),
            "total_events": int(df["gdelt_total_events"].fillna(0).sum()),
            "interpretation": (
                "Global tension elevated — verbal conflict high."
                if df["gdelt_avg_tone"].mean() < -2 else
                "Moderate tension detected." if df["gdelt_avg_tone"].mean() < -1 else
                "Global tone relatively neutral."
            ),
        }
        return summary
    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# Debug Endpoints (optional, keep for monitoring)
# ------------------------------------------------------------------------------
@app.get("/debug/config")
def debug_config():
    return {
        "API_URL": os.environ.get("API_URL", "not set"),
        "TRUMPPULSE_DATA_DIR": os.environ.get("TRUMPPULSE_DATA_DIR", "not set"),
        "CHROMA_DB_PATH": os.environ.get("CHROMA_DB_PATH", "not set"),
    }

@app.get("/debug/status")
def debug_status():
    engine = get_engine()
    if engine is None:
        return {"error": "Search engine not yet initialized"}
    return {
        "db_path": engine.db_path,
        "db_exists": os.path.exists(engine.db_path),
        "posts_loaded": len(engine.posts) if engine.posts else 0,
    }

@app.get("/debug/paths")
def debug_paths():
    return {
        "TRUMPPULSE_DATA_DIR": os.environ.get("TRUMPPULSE_DATA_DIR", "not set"),
        "DEFAULT_DB_PATH": DEFAULT_DB_PATH,
        "db_exists": os.path.exists(DEFAULT_DB_PATH),
    }

@app.get("/debug/index")
def debug_index():
    engine = get_engine()
    if engine is None:
        return {"error": "Search engine not yet initialized"}
    return {
        "collection_count": len(engine.posts) if engine.posts else 0,
        "db_path": engine.db_path,
    }