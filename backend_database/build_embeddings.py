"""Build and cache sentence embeddings for all Trump posts."""
import sqlite3
import pickle
import os
from sentence_transformers import SentenceTransformer

DB_PATH = "backend_database/trump_data.db"
CACHE_PATH = "backend_database/trump_embeddings.pkl"  # ← changed name
MODEL_NAME = "all-MiniLM-L6-v2"

def build_embeddings():
    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Fetching posts from database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT post_id, date, text FROM truth_social WHERE text IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()

    posts = [{"post_id": r[0], "date": r[1], "text": r[2]} for r in rows]
    texts = [p["text"] for p in posts]

    print(f"Encoding {len(texts)} posts...")
    embeddings = model.encode(texts, show_progress_bar=True)

    print(f"Saving cache to {CACHE_PATH}...")
    with open(CACHE_PATH, "wb") as f:
        pickle.dump({"posts": posts, "embeddings": embeddings}, f)

    print("✅ Embeddings built successfully.")

if __name__ == "__main__":
    build_embeddings()