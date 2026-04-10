"""Integration tests for embeddings using the real database and ChromaDB."""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_database.embeddings import PostSearchEngine
from backend_database.init_db import DEFAULT_DB_PATH


@pytest.fixture(scope="module")
def real_engine():
    """Load the real search engine. Skip if database does not exist."""
    if not os.path.exists(DEFAULT_DB_PATH):
        pytest.skip(f"Real database not found at {DEFAULT_DB_PATH}")
    engine = PostSearchEngine(DEFAULT_DB_PATH)
    # Ensure index is built (it should already exist, but just in case)
    if engine.collection.count() == 0:
        engine.build_index()
    return engine


def test_engine_loads_real_data(real_engine):
    """Engine should successfully load the real ChromaDB collection."""
    count = real_engine.collection.count()
    assert count > 30000, f"Expected over 30000 posts, got {count}"


def test_search_returns_real_posts(real_engine):
    """Search with a known keyword should return relevant real posts."""
    results = real_engine.search("China", top_k=3)
    assert len(results) == 3
    for r in results:
        assert "post" in r
        assert "score" in r
        assert r["score"] >= 0


def test_search_score_is_reasonable(real_engine):
    """Scores for highly relevant queries should be high."""
    results = real_engine.search("China", top_k=1)
    assert results[0]["score"] > 50, f"Expected high relevance for 'China', got {results[0]['score']}"


def test_search_handles_empty_query(real_engine):
    """Empty query should return results (or handle gracefully)."""
    results = real_engine.search("", top_k=2)
    assert isinstance(results, list)
    if results:
        assert "score" in results[0]