from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timezone

from data.sample import get_sample_data
from app.services.sentiment_service import analyze_dataset
from app.models.qa import simple_qa

app = FastAPI()

# Add monitoring router AFTER app is created
from app.api import monitoring
app.include_router(monitoring.router)

# Load sample data at startup
texts = get_sample_data()
sentiments = analyze_dataset(texts)

# Database path
DB_PATH = "data/trump_pulse.db"

# ---------- Existing Endpoints ----------
@app.get("/")
def health():
    return {"status": "running"}

@app.get("/sentiments")
def get_sentiments():
    return sentiments

@app.get("/qa")
def qa(query: str):
    return simple_qa(query, texts)

# ---------- New Feedback Endpoint ----------
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