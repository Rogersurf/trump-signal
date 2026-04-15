"""
data/api_client.py
==================
Pure HTTP client for the TrumpPulse FastAPI backend.
All data is fetched via API calls — no direct database access.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from frontend.config import API_URL

# -----------------------------------------------------------------------------
# Health Check (Real HTTP)
# -----------------------------------------------------------------------------
def is_api_alive() -> bool:
    """Perform a real HTTP health check against the running API with retries."""
    import time
    max_retries = 20
    for _ in range(max_retries):
        try:
            r = requests.get(f"{API_URL}/", timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(3)
    return False


# -----------------------------------------------------------------------------
# Posts (Daily Feed)
# -----------------------------------------------------------------------------
def get_posts(start_date=None, end_date=None) -> pd.DataFrame:
    """Fetch posts from the API. Returns empty DataFrame on failure."""
    params = {}
    if start_date:
        params["start_date"] = str(start_date)
    if end_date:
        params["end_date"] = str(end_date)
    try:
        r = requests.get(f"{API_URL}/posts", params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data:
                df = pd.DataFrame(data)
                if "datetime" in df.columns:
                    df["datetime"] = pd.to_datetime(df["datetime"])
                if "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"])
                return df
    except Exception as e:
        print(f"[api_client] get_posts error: {e}")
    return pd.DataFrame()


def get_sentiments() -> pd.DataFrame:
    """Alias for get_posts."""
    return get_posts()


# -----------------------------------------------------------------------------
# Category Summary
# -----------------------------------------------------------------------------
def get_category_summary(period: str = "month", date_from: str = None, date_to: str = None) -> pd.DataFrame:
    """Fetch category distribution from the API."""
    params = {"period": period}
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    try:
        r = requests.get(f"{API_URL}/categories", params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data:
                return pd.DataFrame(data)
    except Exception as e:
        print(f"[api_client] get_category_summary error: {e}")
    return pd.DataFrame(columns=["category", "count"])


# -----------------------------------------------------------------------------
# Stock Series
# -----------------------------------------------------------------------------
def get_stock_series(index: str = "sp500", days: int = 30) -> pd.DataFrame:
    """Fetch stock series from the API."""
    try:
        r = requests.get(f"{API_URL}/stocks", params={"index": index, "days": days}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data:
                return pd.DataFrame(data)
    except Exception as e:
        print(f"[api_client] get_stock_series error: {e}")
    return pd.DataFrame(columns=["date", "price", "has_big_post", "pct_change"])


# -----------------------------------------------------------------------------
# GDELT
# -----------------------------------------------------------------------------
def get_gdelt_summary() -> dict:
    """Fetch GDELT summary from the API."""
    try:
        r = requests.get(f"{API_URL}/gdelt", timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"[api_client] get_gdelt_summary error: {e}")
    return {}


def get_gdelt_timeseries(weeks: int = 8) -> pd.DataFrame:
    """Fetch GDELT timeseries from the API."""
    try:
        r = requests.get(f"{API_URL}/gdelt/timeseries", params={"weeks": weeks}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data:
                return pd.DataFrame(data)
    except Exception as e:
        print(f"[api_client] get_gdelt_timeseries error: {e}")
    return pd.DataFrame(columns=["week", "avg_tone", "verbal_conflict"])


# -----------------------------------------------------------------------------
# Q&A (Semantic Search)
# -----------------------------------------------------------------------------
def ask_question(query: str, top_k: int = 4) -> list:
    """Call the semantic search API endpoint."""
    try:
        r = requests.get(f"{API_URL}/qa", params={"query": query, "limit": top_k}, timeout=15)
        if r.status_code == 200:
            data = r.json()
            # Handle both response formats
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "results" in data:
                return data["results"]
    except Exception as e:
        print(f"[api_client] ask_question error: {e}")
    return []


# -----------------------------------------------------------------------------
# Pipeline Status (Developer Dashboard)
# -----------------------------------------------------------------------------
def get_pipeline_status() -> dict:
    """Fetch pipeline status from the API."""
    try:
        r = requests.get(f"{API_URL}/pipeline/status", timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"[api_client] get_pipeline_status error: {e}")
    return {"status": "error", "errors": ["API unreachable"]}


def get_artifact_log() -> pd.DataFrame:
    """Fetch artifact log from the API."""
    try:
        r = requests.get(f"{API_URL}/pipeline/logs", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data:
                return pd.DataFrame(data)
    except Exception as e:
        print(f"[api_client] get_artifact_log error: {e}")
    return pd.DataFrame()