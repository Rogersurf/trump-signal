"""Build the ChromaDB vector index from the Trump posts SQLite database."""
import os
import sys

# Add the parent directory to Python path so we can import from backend_database
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_database.embeddings import PostSearchEngine
from backend_database.init_db import DEFAULT_DB_PATH


def build_index(db_path: str = None, force: bool = False):
    """
    Build the ChromaDB vector index.

    Args:
        db_path: Path to the SQLite database. If None, uses the default path.
        force: If True, rebuild the index even if it already exists.
    """
    if db_path is None:
        db_path = DEFAULT_DB_PATH

    print(f"Using database at: {db_path}")
    engine = PostSearchEngine(db_path)
    engine.build_index(force=force)
    print("✅ ChromaDB index build process completed.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build ChromaDB vector index for Trump posts.")
    parser.add_argument("--db-path", help="Path to the SQLite database file.")
    parser.add_argument("--force", action="store_true", help="Force rebuild of the index.")
    args = parser.parse_args()
    build_index(args.db_path, args.force)