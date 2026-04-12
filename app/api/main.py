"""FastAPI application for TrumpPulse."""
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timezone
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend_database.embeddings import get_search_engine
from backend_database.init_db import DEFAULT_DB_PATH

# Initialize search engine (loads embeddings from pickle cache)
print(f"[STARTUP] Loading search engine from {DEFAULT_DB_PATH}")
engine = get_search_engine(DEFAULT_DB_PATH)
if engine.embeddings is None:
    print("[STARTUP] Embeddings cache missing. Building index (this will take a few minutes)...")
    engine.build_index(force=True)
print(f"[STARTUP] Engine ready with {len(engine.posts)} posts.")

app = FastAPI()

from app.api import monitoring
app.include_router(monitoring.router)

@app.get("/")
def health():
    return {"status": "running", "database": DEFAULT_DB_PATH}

@app.get("/qa")
def qa(query: str, limit: int = 5):
    try:
        results = engine.search(query, top_k=limit)
        return {"query": query, "results": results}
    except Exception as e:
        return {"error": str(e)}

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