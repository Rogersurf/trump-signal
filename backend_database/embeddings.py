"""Semantic search using precomputed Trump post embeddings."""
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

CACHE_PATH = "backend_database/trump_embeddings.pkl"  # ← same name
MODEL_NAME = "all-MiniLM-L6-v2"

class PostSearchEngine:
    def __init__(self):
        with open(CACHE_PATH, "rb") as f:
            data = pickle.load(f)
        self.posts = data["posts"]
        self.embeddings = data["embeddings"]
        self.model = SentenceTransformer(MODEL_NAME)

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.model.encode([query])[0]
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
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

def get_search_engine():
    global _engine
    if _engine is None:
        _engine = PostSearchEngine()
    return _engine