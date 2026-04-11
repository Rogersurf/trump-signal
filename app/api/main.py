"""FastAPI application for TrumpPulse."""
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timezone
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend_database.embeddings import get_search_engine
from backend_database.init_db import DEFAULT_DB_PATH

# Ensure ChromaDB index is populated on startup
print(f"[STARTUP] Using database: {DEFAULT_DB_PATH}")
engine = get_search_engine(DEFAULT_DB_PATH)
count = engine.collection.count()
print(f"[STARTUP] ChromaDB collection count: {count}")
if count == 0:
    print("[STARTUP] Collection is empty. Building index from database...")
    engine.build_index(force=True)
    print(f"[STARTUP] Index built. New count: {engine.collection.count()}")

app = FastAPI()

# Add monitoring router
from app.api import monitoring
app.include_router(monitoring.router)

# ---------- Health Endpoint ----------
@app.get("/")
def health():
    return {"status": "running", "database": DEFAULT_DB_PATH}


# ---------- Q&A Endpoint (Semantic Search) ----------
@app.get("/qa")
def qa(query: str, limit: int = 5):
    """Semantic search over Trump posts with similarity scores."""
    try:
        results = engine.search(query, top_k=limit)
        return {"query": query, "results": results}
    except Exception as e:
        return {"error": str(e)}


# ---------- Feedback Endpoint ----------
class FeedbackRequest(BaseModel):
    query: str
    response: str
    rating: int
    comment: str = ""


@app.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    """Store user feedback for LLM evaluation."""
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


# ---------- Debug Endpoints ----------
@app.get("/debug/config")
def debug_config():
    return {
        "API_URL": os.environ.get("API_URL", "not set"),
        "TRUMPPULSE_DATA_DIR": os.environ.get("TRUMPPULSE_DATA_DIR", "not set"),
        "CHROMA_DB_PATH": os.environ.get("CHROMA_DB_PATH", "not set"),
    }


@app.get("/debug/status")
def debug_status():
    from backend_database.embeddings import CHROMA_PATH
    return {
        "db_path": engine.db_path,
        "db_exists": os.path.exists(engine.db_path),
        "chroma_path": CHROMA_PATH,
        "chroma_count": engine.collection.count(),
    }