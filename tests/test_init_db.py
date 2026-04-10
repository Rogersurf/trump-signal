"""Unit tests for backend_database/init_db.py"""
import os
import sys
import sqlite3
from unittest.mock import patch, MagicMock
import pytest
import pandas as pd

# Add backend_database to path
sys.path.insert(0, "backend_database")
import init_db


class TestInitialize:
    """Test the initialize() function from init_db.py"""

    @patch("init_db.load_dataset")
    @patch("init_db.os.path.exists")
    def test_initialize_skips_if_db_exists(self, mock_exists, mock_load_dataset):
        """Should print warning and return if database file already exists."""
        mock_exists.return_value = True

        with patch("builtins.print") as mock_print:
            init_db.initialize()

        mock_load_dataset.assert_not_called()
        mock_print.assert_any_call(f"警告: {init_db.DB_PATH} 已存在。若需重新初始化，请手动删除该文件。")

    @patch("init_db.sqlite3.connect")
    @patch("init_db.load_dataset")
    @patch("init_db.os.path.exists")
    def test_initialize_creates_db_and_table_when_missing(
        self, mock_exists, mock_load_dataset, mock_connect
    ):
        """Should download data and create truth_social table with index."""
        mock_exists.return_value = False

        # Mock dataset from Hugging Face
        mock_df = pd.DataFrame({
            "date": ["2024-01-01 10:00:00", "2024-01-02 11:00:00"],
            "content": ["Post 1", "Post 2"],
            "other_col": [1, 2]
        })
        mock_dataset = {"train": MagicMock()}
        mock_dataset["train"].to_pandas.return_value = mock_df
        mock_load_dataset.return_value = mock_dataset

        # Mock SQLite connection
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn

        with patch("builtins.print") as mock_print:
            init_db.initialize()

        # Verify dataset loaded
        mock_load_dataset.assert_called_once_with(init_db.HF_REPO)

        # Verify to_sql called with correct parameters
        # The DataFrame's to_sql is called on the mock_df, which is a real DataFrame
        # We can't easily assert on that, but we can check the connection execute call for index
        mock_conn.execute.assert_called_once_with(
            "CREATE INDEX idx_date ON truth_social (date)"
        )

        # Check success message printed
        mock_print.assert_any_call("--- 初始化成功！---")

    @patch("init_db.load_dataset")
    @patch("init_db.os.path.exists")
    def test_initialize_handles_dataset_load_failure(self, mock_exists, mock_load_dataset):
        """Should propagate exception if dataset download fails."""
        mock_exists.return_value = False
        mock_load_dataset.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Network error"):
            init_db.initialize()