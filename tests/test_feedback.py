"""Unit tests for feedback endpoint."""
import pytest
from fastapi.testclient import TestClient
from app.api.main import app
import sqlite3
import os

client = TestClient(app)
TEST_DB = "data/test_feedback.db"


@pytest.fixture
def clean_db():
    """Remove test database before and after test."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_feedback_endpoint_accepts_valid_data(clean_db):
    """Should store feedback and return 200."""
    response = client.post("/feedback", json={
        "query": "What is AI?",
        "response": "Artificial Intelligence",
        "rating": 5,
        "comment": "Great answer"
    })
    assert response.status_code == 200
    assert response.json() == {"status": "feedback recorded"}


def test_feedback_endpoint_creates_table():
    """Should create feedback table in database."""
    response = client.post("/feedback", json={
        "query": "Test",
        "response": "Test response",
        "rating": 3,
        "comment": ""
    })
    assert response.status_code == 200
    
    # Verify table exists
    conn = sqlite3.connect("data/trump_pulse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
    assert cursor.fetchone() is not None
    conn.close()


def test_feedback_endpoint_handles_missing_fields():
    """Should return 422 for invalid payload."""
    response = client.post("/feedback", json={
        "query": "Test"
        # missing required fields
    })
    assert response.status_code == 422