from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timezone
import sys
import os
from backend_database.embeddings import get_search_engine

# Add project root to path to import from backend_database
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend_database.data_api import TrumpDataClient

app = FastAPI()

# Add monitoring router AFTER app is created
from app.api import monitoring
app.include_router(monitoring.router)

# Initialize data client with the real database path
DB_PATH = "backend_database/trump_data.db"  # Created by init_db.py in project root
client = TrumpDataClient(db_path=DB_PATH)

# ---------- Health Endpoint ----------
@app.get("/")
def health():
    return {"status": "running"}

# ---------- Sentiments Endpoint (Real Data) ----------
@app.get("/sentiments")
def get_sentiments(limit: int = 50):
    """Return recent posts with engagement metrics."""
    try:
        df = client.get_top_posts(limit=limit)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# ---------- QA Endpoint (Real Data, Simple Keyword Search) ----------
@app.get("/qa")
def qa(query: str, limit: int = 5):
    """Semantic search over Trump posts with similarity scores."""
    try:
        engine = get_search_engine()
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
        (datetime.now(timezone.utc).isoformat(), feedback.query, feedback.response, feedback.rating, feedback.comment)
    )
    conn.commit()
    conn.close()
    return {"status": "feedback recorded"}