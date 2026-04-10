"""Unit tests for backend_database/embeddings.py"""
import pickle
import numpy as np
import pytest
from unittest.mock import patch, MagicMock
import sys

sys.path.insert(0, "backend_database")
from embeddings import PostSearchEngine, get_search_engine


class TestPostSearchEngine:
    @patch("embeddings.pickle.load")
    @patch("embeddings.open")
    @patch("embeddings.SentenceTransformer")
    def test_search_returns_scored_results(
        self, mock_model_class, mock_open, mock_pickle_load
    ):
        """Should return top_k posts with similarity scores."""
        # Mock cached data
        mock_posts = [
            {"post_id": "1", "date": "2024-01-01", "text": "Hello world"},
            {"post_id": "2", "date": "2024-01-02", "text": "Trump economy"},
        ]
        mock_embeddings = np.array([[0.5, 0.5], [0.2, 0.8]])
        mock_pickle_load.return_value = {"posts": mock_posts, "embeddings": mock_embeddings}

        # Mock model encode for query
        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([[0.4, 0.6]])  # query embedding
        mock_model_class.return_value = mock_model

        engine = PostSearchEngine()
        results = engine.search("economy", top_k=2)

        assert len(results) == 2
        assert "post" in results[0]
        assert "score" in results[0]
        assert isinstance(results[0]["score"], float)

    def test_get_search_engine_returns_singleton(self):
        """get_search_engine should return the same instance."""
        with patch("embeddings.PostSearchEngine") as mock_engine_class:
            mock_engine_class.return_value = MagicMock()
            engine1 = get_search_engine()
            engine2 = get_search_engine()
            assert engine1 is engine2
            mock_engine_class.assert_called_once()