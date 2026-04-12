"""FastAPI application for TrumpPulse."""
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timezone
import sys
import os
import threading
import time

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
        # Wait a moment to ensure the filesystem is fully ready (helpful in HF Spaces)
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

# ------------------------------------------------------------------------------
# Helper to get engine (waits until ready)
# ------------------------------------------------------------------------------
def get_engine():
    global _engine, _index_ready, _index_building
    # If still building, return None; caller should handle gracefully
    if _index_building or not _index_ready:
        return None
    return _engine

# ------------------------------------------------------------------------------
# Health Endpoint (always responds immediately)
# ------------------------------------------------------------------------------
@app.get("/")
def health():
    return {"status": "running", "database": DEFAULT_DB_PATH}

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
# Feedback Endpoint (unchanged)
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