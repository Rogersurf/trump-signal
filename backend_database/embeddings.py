"""
Semantic search using precomputed embeddings stored in a pickle file.

Design goals:
- NEVER rebuild embeddings automatically
- ALWAYS try local cache first
- FALLBACK to Hugging Face dataset if cache missing
- LOAD model lazily (only when needed)
"""

import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# =========================
# CONFIG
# =========================
MODEL_NAME = "all-MiniLM-L6-v2"
CACHE_FILENAME = "trump_embeddings.pkl"

# Use HF persistent storage if available
_data_dir = os.environ.get(
    "TRUMPPULSE_DATA_DIR",
    os.path.dirname(os.path.abspath(__file__))
)

CACHE_PATH = os.path.join(_data_dir, CACHE_FILENAME)


# =========================
# ENGINE
# =========================
class PostSearchEngine:
    def __init__(self, db_path: str = None):
        """
        Initialize engine WITHOUT loading model immediately.
        """
        self.model = None  # Lazy load
        self.db_path = db_path
        self.posts = []
        self.embeddings = None

        self._load_cache()

    # -------------------------
    # Lazy model loading
    # -------------------------
    def _get_model(self):
        if self.model is None:
            print("[Embeddings] Loading SentenceTransformer model...")
            self.model = SentenceTransformer(MODEL_NAME)
        return self.model

    # -------------------------
    # Load cache
    # -------------------------
    def _load_cache(self):
        """
        Load embeddings from:
        1. Local cache
        2. Hugging Face dataset (fallback)
        """

        # ---- LOCAL CACHE ----
        if os.path.exists(CACHE_PATH):
            try:
                with open(CACHE_PATH, "rb") as f:
                    data = pickle.load(f)

                self.posts = data.get("posts", [])
                self.embeddings = data.get("embeddings", None)

                print(f"[Embeddings] Loaded {len(self.posts)} posts from LOCAL cache.")
                return

            except Exception as e:
                print(f"[Embeddings] Failed loading local cache: {e}")

        # ---- HF DOWNLOAD ----
        try:
            from huggingface_hub import hf_hub_download

            print("[Embeddings] Local cache not found. Downloading from HF...")

            downloaded_path = hf_hub_download(
                repo_id="Rogersurf/trump-pulse-embeddings",
                filename="trump_embeddings.pkl",
                repo_type="dataset"
            )

            # Save to expected path
            os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)

            with open(downloaded_path, "rb") as src, open(CACHE_PATH, "wb") as dst:
                dst.write(src.read())

            with open(CACHE_PATH, "rb") as f:
                data = pickle.load(f)

            self.posts = data.get("posts", [])
            self.embeddings = data.get("embeddings", None)

            print(f"[Embeddings] Loaded {len(self.posts)} posts from HF dataset.")

        except Exception as e:
            print(f"[Embeddings] ERROR: Could not load embeddings: {e}")
            self.posts = []
            self.embeddings = None

    # -------------------------
    # Build index (MANUAL ONLY)
    # -------------------------
    def build_index(self, force: bool = False):

        if not force:
            print("[Embeddings] build_index skipped (force=False).")
            return

        print("[Embeddings] Building embeddings index...")

        import sqlite3
        import pandas as pd

        if not self.db_path:
            raise ValueError("Database path required to build index.")

        conn = sqlite3.connect(self.db_path)

        df = pd.read_sql(
            "SELECT * FROM truth_social WHERE text IS NOT NULL",
            conn
        )

        conn.close()

        self.posts = df.to_dict(orient="records")
        texts = df["text"].fillna("").tolist()

        print(f"[Embeddings] Generating embeddings for {len(texts)} posts...")

        model = self._get_model()
        self.embeddings = model.encode(texts, show_progress_bar=True)

        import os
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)

        with open(CACHE_PATH, "wb") as f:
            pickle.dump({
                "posts": self.posts,
                "embeddings": self.embeddings
            }, f)

        print(f"[Embeddings] Cache saved to {CACHE_PATH}")

    # -------------------------
    # Search
    # -------------------------
    def search(self, query: str, top_k: int = 5):
        """
        Perform semantic search over posts.
        """

        if self.embeddings is None or len(self.posts) == 0:
            print("[Embeddings] No embeddings available.")
            return []

        model = self._get_model()
        query_emb = model.encode([query])[0]

        similarities = np.dot(self.embeddings, query_emb) / (
            np.linalg.norm(self.embeddings, axis=1) *
            np.linalg.norm(query_emb)
        )

        scores = (similarities + 1) / 2 * 100

        top_indices = np.argsort(similarities)[-top_k:][::-1]

        return [
            {
                "post": self.posts[i],
                "score": round(float(scores[i]), 1)
            }
            for i in top_indices
        ]


# =========================
# GLOBAL ENGINE (singleton)
# =========================
_engine = None


def get_search_engine(db_path: str = None):
    """
    Singleton access to search engine.

    Ensures:
    - only one model instance
    - no repeated loading
    """
    global _engine

    if _engine is None:
        if db_path is None:
            from backend_database.init_db import DEFAULT_DB_PATH
            db_path = DEFAULT_DB_PATH

        _engine = PostSearchEngine(db_path)

    return _engine