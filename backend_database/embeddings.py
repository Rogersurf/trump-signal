"""Semantic search using ChromaDB vector store."""
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import pandas as pd
import sqlite3

MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_PATH = os.environ.get("CHROMA_DB_PATH", "./chroma_db")
COLLECTION_NAME = "trump_posts"

class PostSearchEngine:
    def __init__(self, db_path: str):
        self.model = SentenceTransformer(MODEL_NAME)
        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH,
            settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True,
            is_persistent=True          # <-- adição chave
    )
)
        self.collection = self._get_or_create_collection()
        self.db_path = db_path

    def _get_or_create_collection(self):
        try:
            return self.client.get_collection(COLLECTION_NAME)
        except:
            return self.client.create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )

    def build_index(self, force: bool = False):
        """Build initial index from SQLite database if collection is empty."""
        if self.collection.count() > 0 and not force:
            print(f"Collection already contains {self.collection.count()} documents. Skipping build.")
            return

        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql("SELECT post_id, date, text FROM truth_social WHERE text IS NOT NULL", conn)
        conn.close()

        ids = df["post_id"].astype(str).tolist()
        texts = df["text"].tolist()
        metadatas = [{"date": d} for d in df["date"].tolist()]

        print(f"Generating embeddings for {len(texts)} posts...")
        embeddings = self.model.encode(texts, show_progress_bar=True).tolist()

        # ChromaDB has a max batch size; add in chunks of 5000
        batch_size = 5000
        for i in range(0, len(ids), batch_size):
            end = i + batch_size
            print(f"Adding batch {i//batch_size + 1} ({i} to {end-1})...")
            self.collection.add(
                ids=ids[i:end],
                embeddings=embeddings[i:end],
                documents=texts[i:end],
                metadatas=metadatas[i:end]
            )
        print(f"Index built with {self.collection.count()} documents.")

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        posts = []
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i]
            # Cosine distance to similarity percentage (0-100)
            score = max(0, (2 - distance) / 2 * 100)
            posts.append({
                "post": {
                    "post_id": results['ids'][0][i],
                    "date": results['metadatas'][0][i]['date'],
                    "text": results['documents'][0][i]
                },
                "score": round(score, 1)
            })
        return posts

_engine = None

def get_search_engine(db_path: str = None):
    global _engine
    if _engine is None:
        if db_path is None:
            db_path = os.environ.get("TRUMPPULSE_DATA_DIR", ".") + "/trump_data.db"
        _engine = PostSearchEngine(db_path)
    return _engine