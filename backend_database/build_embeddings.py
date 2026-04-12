"""Build embeddings cache from the SQLite database."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend_database.embeddings import PostSearchEngine
from backend_database.init_db import DEFAULT_DB_PATH

if __name__ == "__main__":
    engine = PostSearchEngine(DEFAULT_DB_PATH)
    engine.build_index(force=True)
    print("✅ Embeddings cache built successfully.")