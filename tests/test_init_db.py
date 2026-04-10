"""Unit tests for backend_database/init_db.py using real temporary database."""
import os
import sqlite3
import tempfile
import pandas as pd
import pytest
from unittest.mock import patch
from datasets import Dataset

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend_database.init_db import initialize, HF_REPO


# Real sample data (minimal, representative)
REAL_SAMPLE_DATA = {
    "date": ["2024-01-01 10:00:00", "2024-01-02 11:00:00"],
    "text": ["Sample post one.", "Sample post two."],
    # Add other columns that the dataset actually has (if any)
}


class TestInitialize:
    @patch("backend_database.init_db.load_dataset")
    def test_initialize_creates_database_and_table(self, mock_load_dataset, tmp_path):
        """Initialize should create a SQLite database with the truth_social table."""
        db_path = str(tmp_path / "trump_data.db")

        # Create a real Hugging Face Dataset object from the sample data
        real_dataset = Dataset.from_pandas(pd.DataFrame(REAL_SAMPLE_DATA))
        mock_load_dataset.return_value = {"train": real_dataset}

        initialize(db_path)

        # Verify database file exists
        assert os.path.exists(db_path)

        # Verify table exists and contains rows
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='truth_social'")
        assert cursor.fetchone() is not None
        cursor.execute("SELECT COUNT(*) FROM truth_social")
        assert cursor.fetchone()[0] == 2
        conn.close()

    @patch("backend_database.init_db.load_dataset")
    def test_initialize_skips_if_db_exists(self, mock_load_dataset, tmp_path):
        """Initialize should skip if the database file already exists."""
        db_path = str(tmp_path / "trump_data.db")
        # Create an empty file to simulate existing database
        with open(db_path, "w") as f:
            f.write("")

        initialize(db_path)

        # load_dataset should not be called
        mock_load_dataset.assert_not_called()