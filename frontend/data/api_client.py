"""
data/api_client.py
==================
Centralized API client for TrumpPulse.
NO MOCK FALLBACKS — failures return empty data or raise exceptions.
"""

import requests
import pandas as pd
import sys
import time
from datetime import datetime, timedelta
from frontend.config import API_URL


# -----------------------------------------------------------------------------
# Connection with retry
# -----------------------------------------------------------------------------
def is_api_alive(max_retries: int = 10, delay: float = 3.0) -> bool:
    """Check if API is running, with retries."""
    for _ in range(max_retries):
        try:
            r = requests.get(f"{API_URL}/", timeout=2)
            if r.status_code == 200 and r.json().get("status") == "running":
                return True
        except Exception:
            pass
        time.sleep(delay)
    return False


# -----------------------------------------------------------------------------
# Posts (real only)
# -----------------------------------------------------------------------------
def get_posts(start_date=None, end_date=None) -> pd.DataFrame:
    """Fetch posts from the real API. Returns empty DataFrame on failure."""
    params = {}
    if start_date:
        params["start_date"] = str(start_date)
    if end_date:
        params["end_date"] = str(end_date)

    try:
        r = requests.get(f"{API_URL}/posts", params=params, timeout=10)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if "datetime" in df.columns:
                df["datetime"] = pd.to_datetime(df["datetime"])
            return df
    except Exception as e:
        print(f"[API CLIENT] get_posts error: {e}", file=sys.stderr)

    return pd.DataFrame()


# -----------------------------------------------------------------------------
# Sentiments (real only)
# -----------------------------------------------------------------------------
def get_sentiments() -> pd.DataFrame:
    try:
        r = requests.get(f"{API_URL}/sentiments", timeout=10)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except Exception as e:
        print(f"[API CLIENT] get_sentiments error: {e}", file=sys.stderr)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# Category Summary (real only)
# -----------------------------------------------------------------------------
def get_category_summary(period: str = "month") -> pd.DataFrame:
    try:
        r = requests.get(f"{API_URL}/categories", params={"period": period}, timeout=10)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except Exception as e:
        print(f"[API CLIENT] get_category_summary error: {e}", file=sys.stderr)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# Stock Series (real only)
# -----------------------------------------------------------------------------
def get_stock_series(index: str = "sp500", days: int = 30) -> pd.DataFrame:
    try:
        r = requests.get(f"{API_URL}/stocks", params={"index": index, "days": days}, timeout=10)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except Exception as e:
        print(f"[API CLIENT] get_stock_series error: {e}", file=sys.stderr)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# GDELT (real only)
# -----------------------------------------------------------------------------
def get_gdelt_summary() -> dict:
    try:
        r = requests.get(f"{API_URL}/gdelt", timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"[API CLIENT] get_gdelt_summary error: {e}", file=sys.stderr)
    return {}


def get_gdelt_timeseries(weeks: int = 8) -> pd.DataFrame:
    try:
        r = requests.get(f"{API_URL}/gdelt/timeseries", params={"weeks": weeks}, timeout=10)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except Exception as e:
        print(f"[API CLIENT] get_gdelt_timeseries error: {e}", file=sys.stderr)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# Q&A – Semantic Search (real only, with retry on empty because of index build)
# -----------------------------------------------------------------------------
def ask_question(query: str, top_k: int = 4) -> list:
    """
    Call the real semantic search API. Returns list of {post: {...}, score: float}.
    If the engine is still initializing, retry a few times.
    """
    url = f"{API_URL}/qa"
    params = {"query": query, "limit": top_k}
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            r = requests.get(url, params=params, timeout=15)
            if r.status_code == 200:
                data = r.json()
                results = data.get("results", [])
                # If we got results, return them
                if results:
                    return results
                # Otherwise, maybe the engine is still building – wait and retry
                if "error" in data and "initializing" in data["error"].lower():
                    print(f"[QA CLIENT] Engine initializing, retry {attempt+1}/{max_attempts}", file=sys.stderr)
                    time.sleep(5)
                    continue
                # Empty results but no initializing message – just return empty
                return []
            else:
                print(f"[QA CLIENT] Non-200 status: {r.status_code}", file=sys.stderr)
        except Exception as e:
            print(f"[QA CLIENT] Exception (attempt {attempt+1}): {e}", file=sys.stderr)
            time.sleep(3)

    # Exhausted retries
    print("[QA CLIENT] Giving up after retries.", file=sys.stderr)
    return []


# -----------------------------------------------------------------------------
# Pipeline Status (real only)
# -----------------------------------------------------------------------------
def get_pipeline_status() -> dict:
    try:
        r = requests.get(f"{API_URL}/pipeline/status", timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"[API CLIENT] get_pipeline_status error: {e}", file=sys.stderr)
    return {}


def get_artifact_log() -> pd.DataFrame:
    try:
        r = requests.get(f"{API_URL}/pipeline/logs", timeout=5)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except Exception as e:
        print(f"[API CLIENT] get_artifact_log error: {e}", file=sys.stderr)
    return pd.DataFrame()