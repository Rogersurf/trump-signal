"""Semantic search using precomputed embeddings stored in a pickle file."""
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
CACHE_FILENAME = "trump_embeddings.pkl"

_data_dir = os.environ.get("TRUMPPULSE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
CACHE_PATH = os.path.join(_data_dir, CACHE_FILENAME)


class PostSearchEngine:
    def __init__(self, db_path: str = None):
        self.model = SentenceTransformer(MODEL_NAME)
        self.db_path = db_path
        self.posts = []
        self.embeddings = None
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(CACHE_PATH):
            with open(CACHE_PATH, "rb") as f:
                data = pickle.load(f)
                self.posts = data.get("posts", [])
                self.embeddings = data.get("embeddings", None)
            print(f"[Embeddings] Loaded {len(self.posts)} posts from cache.")
        else:
            print("[Embeddings] No cache found. Run build_embeddings.py to generate it.")
            self.posts = []
            self.embeddings = None

    def build_index(self, force: bool = False):
        import sqlite3
        import pandas as pd

        if not force and os.path.exists(CACHE_PATH):
            self._load_cache()
            return

        if not self.db_path:
            raise ValueError("Database path required to build index.")

        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql("SELECT post_id, date, text FROM truth_social WHERE text IS NOT NULL", conn)
        conn.close()

        self.posts = [{"post_id": row.post_id, "date": row.date, "text": row.text} for row in df.itertuples()]
        texts = [p["text"] for p in self.posts]

        print(f"[Embeddings] Generating embeddings for {len(texts)} posts...")
        self.embeddings = self.model.encode(texts, show_progress_bar=True)

        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, "wb") as f:
            pickle.dump({"posts": self.posts, "embeddings": self.embeddings}, f)
        print(f"[Embeddings] Cache saved to {CACHE_PATH}")

    def search(self, query: str, top_k: int = 5):
        if self.embeddings is None or len(self.posts) == 0:
            return []
        query_emb = self.model.encode([query])[0]
        similarities = np.dot(self.embeddings, query_emb) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_emb)
        )
        scores = (similarities + 1) / 2 * 100
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = []
        for idx in top_indices:
            results.append({
                "post": self.posts[idx],
                "score": round(float(scores[idx]), 1)
            })
        return results


_engine = None

def get_search_engine(db_path: str = None):
    global _engine
    if _engine is None:
        if db_path is None:
            from backend_database.init_db import DEFAULT_DB_PATH
            db_path = DEFAULT_DB_PATH
        _engine = PostSearchEngine(db_path)
    return _engine