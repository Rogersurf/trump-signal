"""Unit tests for TrumpDataClient logic (mocked database)."""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

# Adjust import path based on where the client file lives
import sys
sys.path.insert(0, "backend_database")
from data_client import TrumpDataClient  # assumes file is named data_client.py


@pytest.fixture
def client():
    return TrumpDataClient(db_path=":memory:")


class TestTrumpDataClient:
    """Test client methods with mocked SQLite and pandas."""

    @patch("data_client.pd.read_sql")
    @patch("data_client.sqlite3.connect")
    def test_get_kpis_constructs_query(self, mock_connect, mock_read_sql, client):
        """get_kpis should include date filters in the WHERE clause."""
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_read_sql.return_value = pd.DataFrame([{"total_posts": 10}])

        client.get_kpis(date_from="2024-01-01", date_to="2024-01-31")

        sql = mock_read_sql.call_args[0][0]
        assert "date >= '2024-01-01'" in sql
        assert "date <= '2024-01-31'" in sql

    @patch("data_client.pd.read_sql")
    @patch("data_client.sqlite3.connect")
    def test_get_daily_metrics_returns_dataframe(self, mock_connect, mock_read_sql, client):
        """get_daily_metrics should return a DataFrame with expected columns."""
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        expected = pd.DataFrame({"day": ["2024-01-01"], "posts": [5]})
        mock_read_sql.return_value = expected

        result = client.get_daily_metrics()
        assert "day" in result.columns

    @patch("data_client.pd.read_sql")
    @patch("data_client.sqlite3.connect")
    def test_get_top_posts_orders_by_specified_metric(self, mock_connect, mock_read_sql, client):
        """get_top_posts should ORDER BY the given metric and LIMIT."""
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_read_sql.return_value = pd.DataFrame()

        client.get_top_posts(metric="reblogs_count", limit=7)

        sql = mock_read_sql.call_args[0][0]
        assert "ORDER BY reblogs_count DESC" in sql
        assert "LIMIT 7" in sql

    @patch("data_client.pd.read_sql")
    @patch("data_client.sqlite3.connect")
    def test_get_category_ratio_raises_on_empty(self, mock_connect, mock_read_sql, client):
        """get_category_ratio should raise ValueError when no rows returned."""
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_read_sql.return_value = pd.DataFrame()  # empty

        with pytest.raises(ValueError, match="No data found"):
            client.get_category_ratio()

    @patch("data_client.pd.read_sql")
    @patch("data_client.sqlite3.connect")
    def test_get_market_impact_calculates_percentages(self, mock_connect, mock_read_sql, client):
        """get_market_impact should compute 5min/1hr percentage changes."""
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        test_df = pd.DataFrame([{
            "post_id": 1,
            "date": "2024-01-01 10:00:00",
            "text_snippet": "test",
            "sp500_at_post": 100.0,
            "sp500_5min_after": 101.0,
            "sp500_1hr_after": 102.0,
            "qqq_at_post": 200.0,
            "qqq_5min_after": 198.0,
            "qqq_1hr_after": 202.0,
            "dia_at_post": 300.0,
            "dia_5min_after": 300.0,
            "dia_1hr_after": 303.0,
        }])
        mock_read_sql.return_value = test_df

        result = client.get_market_impact(start="2024-01-01", end="2024-01-02")

        assert result.iloc[0]["sp500_5min_pct"] == 1.0
        assert result.iloc[0]["sp500_1hr_pct"] == 2.0

    @patch("data_client.pd.read_sql")
    @patch("data_client.sqlite3.connect")
    def test_get_gdelt_correlation_returns_two_dataframes(self, mock_connect, mock_read_sql, client):
        """get_gdelt_correlation should return (corr_df, pval_df)."""
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        # Provide minimal data that won't crash correlation calculation
        data = {
            "cat_self_promotion": [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            "gdelt_avg_tone": [0.1, -0.2, 0.3, 0.0, -0.1, 0.2, -0.3, 0.1, 0.0, 0.2],
        }
        # Fill other required columns with zeros
        for col in [
            "cat_attacking_individual", "cat_attacking_opposition", "cat_threatening_intl",
            "cat_enacting_aggressive", "cat_enacting_nonaggressive", "cat_deescalating",
            "cat_praising_endorsing", "cat_other",
            "gdelt_total_events", "gdelt_goldstein_avg", "gdelt_military", "gdelt_sanctions",
            "gdelt_threat", "gdelt_protest", "gdelt_verbal_conflict", "gdelt_material_conflict",
            "gdelt_verbal_cooperation", "gdelt_material_cooperation"
        ]:
            data[col] = [0] * 10
        mock_read_sql.return_value = pd.DataFrame(data)

        corr, pval = client.get_gdelt_correlation(start="2024-01-01", end="2024-01-31")

        assert corr.shape == pval.shape
        assert "Avg Tone" in corr.index