"""Unit tests for backend_database/data_api.py (TrumpDataClient) with real data."""
import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend_database.data_api import TrumpDataClient
from backend_database.init_db import DEFAULT_DB_PATH


@pytest.fixture(scope="module")
def client():
    """Create a TrumpDataClient connected to the real database."""
    if not os.path.exists(DEFAULT_DB_PATH):
        pytest.skip(f"Real database not found at {DEFAULT_DB_PATH}")
    return TrumpDataClient(db_path=DEFAULT_DB_PATH)


class TestTrumpDataClient:
    """Test client methods with the real database."""

    def test_get_kpis_returns_data(self, client):
        """get_kpis should return a Series with expected metrics."""
        kpis = client.get_kpis()
        assert kpis["total_posts"] > 0
        assert "avg_replies" in kpis

    def test_get_daily_metrics_returns_dataframe(self, client):
        """get_daily_metrics should return a DataFrame with posts per day."""
        df = client.get_daily_metrics()
        assert not df.empty
        assert "day" in df.columns
        assert "posts" in df.columns

    def test_get_top_posts_returns_correct_limit(self, client):
        """get_top_posts should return exactly the requested number of posts."""
        limit = 5
        df = client.get_top_posts(limit=limit)
        assert len(df) == limit
        assert "text" in df.columns or "snippet" in df.columns