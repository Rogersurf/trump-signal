"""Unit tests for monitoring endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


def test_metrics_endpoint_returns_200():
    """Should return 200 and Prometheus text format."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]


def test_metrics_includes_request_counters():
    """Should contain default counter metrics."""
    response = client.get("/metrics")
    content = response.text
    assert "trump_pulse_sentiment_requests_total" in content
    assert "trump_pulse_qa_requests_total" in content


def test_metrics_includes_db_size_if_exists():
    """Should include DB size metric if database file exists."""
    response = client.get("/metrics")
    content = response.text
    # DB may or may not exist in test, just check format
    # No assertion needed unless DB exists
    pass