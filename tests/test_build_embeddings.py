"""Unit tests for backend_database/build_embeddings.py"""
import os
import pickle
import pytest
from unittest.mock import patch, MagicMock
import sys

sys.path.insert(0, "backend_database")
import build_embeddings


class TestBuildEmbeddings:
    @patch("build_embeddings.SentenceTransformer")
    @patch("build_embeddings.sqlite3.connect")
    @patch("build_embeddings.pickle.dump")
    @patch("build_embeddings.open")
    def test_build_embeddings_creates_cache(
        self, mock_open, mock_pickle_dump, mock_connect, mock_model_class
    ):
        """Should fetch posts, encode them, and save to pickle file."""
        # Mock database rows: (post_id, date, text)
        mock_rows = [
            ("123", "2024-01-01", "Great post"),
            ("456", "2024-01-02", "Another post"),
        ]
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_rows
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock SentenceTransformer
        mock_model = MagicMock()
        mock_model.encode.return_value = [[0.1, 0.2], [0.3, 0.4]]
        mock_model_class.return_value = mock_model

        # Run build
        build_embeddings.build_embeddings()

        # Verify database query
        mock_cursor.execute.assert_called_once_with(
            "SELECT post_id, date, text FROM truth_social WHERE text IS NOT NULL"
        )

        # Verify encoding
        mock_model.encode.assert_called_once()

        # Verify pickle dump was called with expected data
        args, kwargs = mock_pickle_dump.call_args
        saved_data = args[0]
        assert "posts" in saved_data
        assert "embeddings" in saved_data
        assert len(saved_data["posts"]) == 2
        assert saved_data["embeddings"] == [[0.1, 0.2], [0.3, 0.4]]