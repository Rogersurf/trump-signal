"""Unit tests for /qa endpoint with semantic search."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to Python path so we can import app.api.main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.api.main import app

client = TestClient(app)


class TestQAEndpoint:
    @patch("app.api.main.get_search_engine")
    def test_qa_returns_semantic_results(self, mock_get_engine):
        """Should return query and results with scores."""
        mock_engine = MagicMock()
        mock_engine.search.return_value = [
            {"post": {"post_id": "1", "date": "2024-01-01", "text": "Test"}, "score": 85.5}
        ]
        mock_get_engine.return_value = mock_engine

        response = client.get("/qa?query=China&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "China"
        assert len(data["results"]) == 1
        assert "score" in data["results"][0]

    @patch("app.api.main.get_search_engine")
    def test_qa_handles_engine_exception(self, mock_get_engine):
        """Should return error message when search engine fails."""
        mock_get_engine.side_effect = Exception("Cache file missing")

        response = client.get("/qa?query=test")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data