"""Integration tests for daily_update using a real subset of the production database."""
import os
import sys
import tempfile
import sqlite3
import shutil
import pytest
from unittest.mock import patch
import pandas as pd
from datasets import Dataset

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_database.init_db import DEFAULT_DB_PATH as REAL_DB_PATH


@pytest.fixture(scope="function")
def isolated_env():
    """Create a temporary copy of the real database with a subset of posts and isolated ChromaDB."""
    if not os.path.exists(REAL_DB_PATH):
        pytest.skip(f"Real database not found at {REAL_DB_PATH}")

    tmpdir = tempfile.mkdtemp()
    db_copy = os.path.join(tmpdir, "trump_data.db")

    # Copy real database and keep only 10 posts
    shutil.copy2(REAL_DB_PATH, db_copy)
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

    # Reload embeddings module to pick up new ChromaDB path
    import backend_database.embeddings
    import importlib
    importlib.reload(backend_database.embeddings)

    yield db_copy, tmpdir

    shutil.rmtree(tmpdir, ignore_errors=True)
    if old_chroma:
        os.environ["CHROMA_DB_PATH"] = old_chroma
    else:
        del os.environ["CHROMA_DB_PATH"]
    importlib.reload(backend_database.embeddings)


@patch("backend_database.daily_update.load_dataset")
def test_sync_task_updates_database_and_chromadb(mock_load_dataset, isolated_env):
    """sync_task should replace the database and rebuild ChromaDB with new data."""
    temp_db_path, temp_dir = isolated_env

    # Get actual columns from the subset
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(truth_social)")
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()

    # Create two new posts with the same schema
    new_rows = []
    for col in columns:
        if col == "post_id":
            new_rows.append(["new_id_1", "new_id_2"])
        elif col == "date":
            new_rows.append(["2025-01-01 12:00:00", "2025-01-02 13:00:00"])
        elif col == "text":
            new_rows.append(["New post about economy.", "Another new post about trade."])
        else:
            new_rows.append([None, None])

    new_data = pd.DataFrame(dict(zip(columns, new_rows)))
    mock_load_dataset.return_value = {"train": Dataset.from_pandas(new_data)}

    # Patch the database path used by sync_task
    with patch("backend_database.daily_update.DEFAULT_DB_PATH", temp_db_path):
        # Also ensure TRUMPPULSE_DATA_DIR is set to temp_dir so init_db defaults work
        with patch.dict(os.environ, {"TRUMPPULSE_DATA_DIR": temp_dir}):
            from backend_database.daily_update import sync_task
            sync_task()

    # Verify SQLite now contains exactly the 2 new posts
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM truth_social")
    assert cursor.fetchone()[0] == 2
    cursor.execute("SELECT text FROM truth_social")
    texts = [row[0] for row in cursor.fetchall()]
    assert "New post about economy." in texts
    conn.close()

    # Verify ChromaDB was rebuilt with 2 documents
    from backend_database.embeddings import PostSearchEngine
    engine = PostSearchEngine(temp_db_path)
    assert engine.collection.count() == 2