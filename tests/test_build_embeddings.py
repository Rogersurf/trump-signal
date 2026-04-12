"""Integration tests for build_embeddings using a real subset of the production database."""
import os
import sys
import tempfile
import sqlite3
import shutil
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_database.build_embeddings import build_index
from backend_database.init_db import DEFAULT_DB_PATH


@pytest.fixture(scope="function")
def real_subset_env():
    """Create a temporary database with a subset of real posts and isolated ChromaDB."""
    if not os.path.exists(DEFAULT_DB_PATH):
        pytest.skip(f"Real database not found at {DEFAULT_DB_PATH}")

    tmpdir = tempfile.mkdtemp()
    db_copy = os.path.join(tmpdir, "trump_data.db")

    # Copy the real database to temporary location
    shutil.copy2(DEFAULT_DB_PATH, db_copy)

    # Reduce the table to a small subset for fast testing
    conn = sqlite3.connect(db_copy)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE truth_social_subset AS
        SELECT * FROM truth_social WHERE text IS NOT NULL LIMIT 10
    """)
    cursor.execute("DROP TABLE truth_social")
    cursor.execute("ALTER TABLE truth_social_subset RENAME TO truth_social")
    conn.commit()
    conn.close()

    # Isolate ChromaDB path
    old_chroma = os.environ.get("CHROMA_DB_PATH")
    chroma_path = os.path.join(tmpdir, "chroma_db")
    os.environ["CHROMA_DB_PATH"] = chroma_path

    # Reload embeddings module to pick up new environment
    import backend_database.embeddings
    import importlib
    importlib.reload(backend_database.embeddings)

    yield db_copy

    shutil.rmtree(tmpdir, ignore_errors=True)
    if old_chroma:
        os.environ["CHROMA_DB_PATH"] = old_chroma
    else:
        del os.environ["CHROMA_DB_PATH"]
    importlib.reload(backend_database.embeddings)


def test_build_index_creates_chromadb_collection(real_subset_env):
    """build_index should create a ChromaDB collection with the correct number of documents."""
    build_index(db_path=real_subset_env, force=True)

    from backend_database.embeddings import PostSearchEngine
    engine = PostSearchEngine(real_subset_env)

    # Verify we have exactly the subset size (10 posts)
    assert engine.collection.count() == 10


def test_build_index_skips_if_collection_exists(real_subset_env):
    """build_index should skip if the collection already has documents (unless forced)."""
    # First build
    build_index(db_path=real_subset_env, force=True)

    # Second build without force should not modify the collection
    build_index(db_path=real_subset_env, force=False)

    from backend_database.embeddings import PostSearchEngine
    engine = PostSearchEngine(real_subset_env)
    assert engine.collection.count() == 10