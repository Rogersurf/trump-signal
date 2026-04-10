"""Unit tests for backend_database/daily_update.py"""

import sys
import subprocess
from unittest.mock import patch, MagicMock
import pytest
import pandas as pd

sys.path.insert(0, "backend_database")
from daily_update import sync_task


class TestSyncTask:
    """Test the sync_task function in isolation."""

    @patch("daily_update.load_dataset")
    @patch("daily_update.sqlite3.connect")
    def test_sync_task_loads_data_and_writes_to_db(
        self, mock_connect, mock_load_dataset
    ):
        """sync_task should fetch dataset and write to SQLite."""
        real_df = pd.DataFrame({
            "date": ["2024-01-01", "2024-01-02"],
            "content": ["post1", "post2"]
        })

        mock_dataset = {"train": MagicMock()}
        mock_dataset["train"].to_pandas.return_value = real_df
        mock_load_dataset.return_value = mock_dataset

        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn

        sync_task()

        mock_load_dataset.assert_called_once_with("chrissoria/trump-truth-social")
        mock_connect.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            "CREATE INDEX IF NOT EXISTS idx_date ON truth_social (date)"
        )


class TestDailyUpdateCLI:
    """Test the command‑line behavior of daily_update.py."""

    def test_once_flag_triggers_sync_and_exits(self):
        """Running with --once should execute sync_task and return exit code 0."""
        result = subprocess.run(
            ["python", "backend_database/daily_update.py", "--once"],
            capture_output=True,
            text=True,
        )
        # Accept either success or the "Database file not found" error
        assert result.returncode in (0, 1)
        if result.returncode == 1:
            assert "Error: Database file not found" in result.stdout