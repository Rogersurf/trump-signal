"""
data/api_client.py
==================
จุดเดียวที่ติดต่อกับ API ทั้งหมด
ถ้า API ยังไม่พร้อม จะ fallback เป็น mock data อัตโนมัติ
REPLACE: แต่ละฟังก์ชันมี comment บอกว่าต้องเปลี่ยนอะไร
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from frontend.config import API_URL
import random

random.seed(42)
np.random.seed(42)

# ─────────────────────────────────────────────────────────────────────────────
# CONNECTION
# ─────────────────────────────────────────────────────────────────────────────

def is_api_alive() -> bool:
    try:
        r = requests.get(f"{API_URL}/", timeout=2)
        return r.json().get("status") == "running"
    except:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# POSTS
# ─────────────────────────────────────────────────────────────────────────────

def get_posts(start_date=None, end_date=None) -> pd.DataFrame:
    """
    REPLACE: GET {API_URL}/posts?start_date=...&end_date=...
    ต้องการ columns: date, time, datetime, text, sentiment, sentiment_score,
    dominant_category, engagement_score, replies, reblogs, favourites,
    has_media, is_president, sp500_5min_before, sp500_5min_after,
    market_impact_pct, post_type
    """
    try:
        params = {}
        if start_date: params["start_date"] = str(start_date)
        if end_date:   params["end_date"]   = str(end_date)
        r = requests.get(f"{API_URL}/posts", params=params, timeout=5)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            df["datetime"] = pd.to_datetime(df["datetime"])
            return df
    except:
        pass
    return _mock_posts(start_date, end_date)


def _mock_posts(start_date=None, end_date=None) -> pd.DataFrame:
    posts = [
        {
            "post_id": "p001", "date": "2026-04-06", "time": "11:08",
            "datetime": datetime(2026, 4, 6, 11, 8),
            "text": "Great going Freedom Caucus. Proud of you!!! President DJT",
            "sentiment": "POSITIVE", "sentiment_score": 0.94,
            "dominant_category": "Self-promotion",
            "engagement_score": 22825, "replies": 1574, "reblogs": 4835, "favourites": 16414,
            "has_media": True, "is_president": True,
            "sp500_5min_before": 6581.56, "sp500_5min_after": 6590.99,
            "market_impact_pct": 0.14, "post_type": "original",
        },
        {
            "post_id": "p002", "date": "2026-04-05", "time": "12:03",
            "datetime": datetime(2026, 4, 5, 12, 3),
            "text": "Open the Fuckin' Strait, you crazy bastards, or you'll be living in Hell - JUST WATCH! Praise be to Allah. President DONALD J. TRUMP",
            "sentiment": "NEGATIVE", "sentiment_score": 0.97,
            "dominant_category": "Threatening intl.",
            "engagement_score": 125335, "replies": 22306, "reblogs": 19346, "favourites": 83683,
            "has_media": False, "is_president": True,
            "sp500_5min_before": 6581.56, "sp500_5min_after": 6562.50,
            "market_impact_pct": -0.29, "post_type": "original",
        },
        {
            "post_id": "p003", "date": "2026-04-05", "time": "11:52",
            "datetime": datetime(2026, 4, 5, 11, 52),
            "text": "We have rescued the seriously wounded F-15 Crew Member from deep inside the mountains of Iran. He is a highly respected Colonel.",
            "sentiment": "POSITIVE", "sentiment_score": 0.88,
            "dominant_category": "Self-promotion",
            "engagement_score": 73034, "replies": 3789, "reblogs": 11936, "favourites": 57309,
            "has_media": False, "is_president": True,
            "sp500_5min_before": 6578.00, "sp500_5min_after": 6591.00,
            "market_impact_pct": 0.20, "post_type": "original",
        },
        {
            "post_id": "p004", "date": "2026-04-04", "time": "13:32",
            "datetime": datetime(2026, 4, 4, 13, 32),
            "text": "Not only were the jobs numbers GREAT yesterday, 178,000 new jobs, but the TRADE DEFICIT was down 55%, the biggest drop in history. THANK YOU MR. TARIFF! MAGA!!!",
            "sentiment": "POSITIVE", "sentiment_score": 0.91,
            "dominant_category": "Enacting non-agg.",
            "engagement_score": 60557, "replies": 3150, "reblogs": 9820, "favourites": 47587,
            "has_media": False, "is_president": True,
            "sp500_5min_before": 6560.00, "sp500_5min_after": 6572.00,
            "market_impact_pct": 0.18, "post_type": "original",
        },
        {
            "post_id": "p005", "date": "2026-04-04", "time": "14:05",
            "datetime": datetime(2026, 4, 4, 14, 5),
            "text": "Remember when I gave Iran ten days to MAKE A DEAL or OPEN UP THE HORMUZ STRAIT. Time is running out - 48 hours before all Hell will reign down on them.",
            "sentiment": "NEGATIVE", "sentiment_score": 0.93,
            "dominant_category": "Threatening intl.",
            "engagement_score": 65339, "replies": 6841, "reblogs": 10745, "favourites": 47753,
            "has_media": False, "is_president": True,
            "sp500_5min_before": 6572.00, "sp500_5min_after": 6553.00,
            "market_impact_pct": -0.29, "post_type": "original",
        },
        {
            "post_id": "p006", "date": "2026-04-04", "time": "19:00",
            "datetime": datetime(2026, 4, 4, 19, 0),
            "text": "\"If you import The Third World, you become The Third World!\" — AND THAT'S NOT GOING TO HAPPEN TO THE USA AS LONG AS I AM PRESIDENT.",
            "sentiment": "NEGATIVE", "sentiment_score": 0.82,
            "dominant_category": "Attacking opposition",
            "engagement_score": 58844, "replies": 3775, "reblogs": 10382, "favourites": 44687,
            "has_media": False, "is_president": True,
            "sp500_5min_before": 6553.00, "sp500_5min_after": 6548.00,
            "market_impact_pct": -0.08, "post_type": "original",
        },
        {
            "post_id": "p007", "date": "2026-04-03", "time": "09:15",
            "datetime": datetime(2026, 4, 3, 9, 15),
            "text": "The Economy is doing GREAT. Best numbers in years. Stock Market is up, jobs are up, inflation is down. FAKE NEWS won't report it!",
            "sentiment": "POSITIVE", "sentiment_score": 0.87,
            "dominant_category": "Enacting non-agg.",
            "engagement_score": 45200, "replies": 2900, "reblogs": 8100, "favourites": 34200,
            "has_media": False, "is_president": True,
            "sp500_5min_before": 6540.00, "sp500_5min_after": 6551.00,
            "market_impact_pct": 0.17, "post_type": "original",
        },
        {
            "post_id": "p008", "date": "2026-04-03", "time": "14:30",
            "datetime": datetime(2026, 4, 3, 14, 30),
            "text": "Crooked Joe Biden has done more damage to America than any President in history. Radical Left DISASTER!",
            "sentiment": "NEGATIVE", "sentiment_score": 0.96,
            "dominant_category": "Attacking opposition",
            "engagement_score": 52000, "replies": 4200, "reblogs": 9800, "favourites": 38000,
            "has_media": False, "is_president": True,
            "sp500_5min_before": 6551.00, "sp500_5min_after": 6546.00,
            "market_impact_pct": -0.08, "post_type": "original",
        },
    ]
    df = pd.DataFrame(posts)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"]     = pd.to_datetime(df["date"])
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    return df.sort_values("datetime", ascending=False).reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# SENTIMENTS  (endpoint /sentiments มีอยู่แล้ว)
# ─────────────────────────────────────────────────────────────────────────────

def get_sentiments() -> pd.DataFrame:
    """
    REPLACE: GET {API_URL}/sentiments — endpoint มีอยู่แล้ว
    """
    try:
        r = requests.get(f"{API_URL}/sentiments", timeout=5)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except:
        pass
    return get_posts()[["post_id", "text", "sentiment", "sentiment_score", "dominant_category"]]


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

def get_category_summary(period: str = "month") -> pd.DataFrame:
    """
    REPLACE: คำนวณจาก get_posts() groupby dominant_category
    หรือเพิ่ม endpoint GET {API_URL}/categories?period=month
    """
    data = {
        "week":  {"Threatening intl.": 12, "Self-promotion": 18,
                  "Attacking opposition": 9, "Enacting non-agg.": 11,
                  "Praising/endorsing": 6, "De-escalating": 3, "Other": 4},
        "month": {"Threatening intl.": 38, "Self-promotion": 72,
                  "Attacking opposition": 44, "Enacting non-agg.": 35,
                  "Praising/endorsing": 21, "De-escalating": 8, "Other": 14},
        "year":  {"Threatening intl.": 180, "Self-promotion": 340,
                  "Attacking opposition": 210, "Enacting non-agg.": 170,
                  "Praising/endorsing": 95, "De-escalating": 40, "Other": 65},
    }
    d = data.get(period, data["month"])
    return pd.DataFrame({"category": list(d.keys()), "count": list(d.values())})


# ─────────────────────────────────────────────────────────────────────────────
# STOCK SERIES
# ─────────────────────────────────────────────────────────────────────────────

def get_stock_series(index: str = "sp500", days: int = 30) -> pd.DataFrame:
    """
    REPLACE: query columns {index}_open, {index}_close etc. from dataset
    grouped by date — endpoint GET {API_URL}/stocks?index=sp500&days=30
    """
    try:
        r = requests.get(f"{API_URL}/stocks",
                         params={"index": index, "days": days}, timeout=5)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except:
        pass
    return _mock_stock(index, days)


def _mock_stock(index: str, days: int) -> pd.DataFrame:
    base = {"sp500": 6500.0, "djt": 8.80, "qqq": 570.0, "gld": 425.0, "tlt": 86.0}
    price = base.get(index, 6500.0)
    dates, prices = [], [price]
    for i in range(days - 1, -1, -1):
        dates.append((datetime(2026, 4, 6) - timedelta(days=i)).strftime("%Y-%m-%d"))
    for _ in range(days - 1):
        prices.append(round(prices[-1] * (1 + np.random.normal(0, 0.008)), 2))
    if index == "sp500":
        prices[-3], prices[-2], prices[-1] = 6560.00, 6581.56, 6582.69
    high_impact = {"2026-04-05", "2026-04-04"}
    df = pd.DataFrame({
        "date": dates, "price": prices,
        "has_big_post": [d in high_impact for d in dates],
    })
    df["pct_change"] = df["price"].pct_change().fillna(0).round(4)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# GDELT
# ─────────────────────────────────────────────────────────────────────────────

def get_gdelt_summary() -> dict:
    """
    REPLACE: GET {API_URL}/gdelt — updates weekly, cache this
    """
    try:
        r = requests.get(f"{API_URL}/gdelt", timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {
        "week_of": "Apr 1–6, 2026",
        "military_events": 2326, "verbal_conflict": 7642,
        "verbal_cooperation": 1710, "material_conflict": 1625,
        "diplomatic": 0, "goldstein_avg": 0.11,
        "avg_tone": -2.28, "total_events": 13303,
        "interpretation": (
            "Global tension was elevated this week. Verbal conflict was high "
            "relative to cooperation — world was already tense when Trump posted "
            "his Iran threats. Posts likely amplified rather than created tension."
        ),
    }


def get_gdelt_timeseries(weeks: int = 8) -> pd.DataFrame:
    """
    REPLACE: aggregate gdelt_* columns by week from dataset
    """
    try:
        r = requests.get(f"{API_URL}/gdelt/timeseries",
                         params={"weeks": weeks}, timeout=5)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except:
        pass
    dates = [datetime(2026, 4, 6) - timedelta(weeks=i) for i in range(weeks - 1, -1, -1)]
    return pd.DataFrame({
        "week": [d.strftime("%b %d") for d in dates],
        "avg_tone":       [-1.2, -1.8, -2.1, -0.9, -1.5, -2.8, -2.1, -2.28][:weeks],
        "verbal_conflict": [5200, 6100, 7200, 4800, 6500, 8900, 7100, 7642][:weeks],
    })


# ─────────────────────────────────────────────────────────────────────────────
# Q&A  (endpoint /qa มีอยู่แล้ว)
# ─────────────────────────────────────────────────────────────────────────────

def ask_question(query: str, top_k: int = 4) -> list:
    """
    Get semantically similar posts from the real backend.
    Returns list of {post: {...}, score: float}
    """
    try:
        r = requests.get(
            f"{API_URL}/qa",
            params={"query": query, "limit": top_k},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            if "results" in data:
                return data["results"]
        # If we get here, something went wrong
        print(f"QA API error: {r.status_code}")
        return []
    except Exception as e:
        print(f"QA API connection failed: {e}")
        return []


def _mock_search(query: str, top_k: int) -> list:
    posts = _mock_posts().to_dict("records")
    keywords = query.lower().split()
    scored = []
    for p in posts:
        score = sum(1 for kw in keywords if kw in p["text"].lower())
        scored.append((score + random.uniform(0, 0.3), p))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {"post": p, "score": round(min(s / max(len(keywords), 1), 1.0), 2)}
        for s, p in scored[:top_k]
    ]


# ─────────────────────────────────────────────────────────────────────────────
# DEVELOPER — PIPELINE STATUS
# ─────────────────────────────────────────────────────────────────────────────

def get_pipeline_status() -> dict:
    """
    REPLACE: GET {API_URL}/pipeline/status
    หรืออ่านจาก artifacts/runs/ directory โดยตรง
    """
    try:
        r = requests.get(f"{API_URL}/pipeline/status", timeout=3)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {
        "last_ingest":          "2026-04-06 08:00 UTC",
        "last_preprocess":      "2026-04-06 08:05 UTC",
        "last_sentiment_run":   "2026-04-06 08:07 UTC",
        "last_embedding_build": "2026-04-06 08:10 UTC",
        "last_gdelt_update":    "2026-04-01 00:00 UTC",
        "total_posts":          32418,
        "posts_today":          14,
        "rows_dropped_today":   2,
        "model_name":           "cardiffnlp/twitter-roberta-base-sentiment",
        "embedding_model":      "all-MiniLM-L6-v2",
        "dataset_version":      "chrissoria/trump-truth-social @ main",
        "artifact_path":        "artifacts/processed/processed_20260406.parquet",
        "status":               "healthy",
        "errors":               [],
    }


def get_artifact_log() -> pd.DataFrame:
    """
    REPLACE: GET {API_URL}/pipeline/logs
    หรืออ่านจาก artifacts/runs/*.json
    """
    try:
        r = requests.get(f"{API_URL}/pipeline/logs", timeout=3)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except:
        pass
    return pd.DataFrame([
        {"timestamp": "2026-04-06 08:00", "stage": "ingest",     "rows": 32418, "status": "ok",    "duration_s": 12},
        {"timestamp": "2026-04-06 08:05", "stage": "preprocess", "rows": 32416, "status": "ok",    "duration_s": 8},
        {"timestamp": "2026-04-06 08:07", "stage": "sentiment",  "rows": 32416, "status": "ok",    "duration_s": 45},
        {"timestamp": "2026-04-06 08:10", "stage": "embeddings", "rows": 32416, "status": "ok",    "duration_s": 120},
        {"timestamp": "2026-04-05 08:00", "stage": "ingest",     "rows": 32404, "status": "ok",    "duration_s": 11},
        {"timestamp": "2026-04-05 08:07", "stage": "sentiment",  "rows": 32402, "status": "ok",    "duration_s": 44},
        {"timestamp": "2026-04-04 08:07", "stage": "sentiment",  "rows": 32388, "status": "error", "duration_s": 3},
        {"timestamp": "2026-04-04 08:10", "stage": "sentiment",  "rows": 32388, "status": "ok",    "duration_s": 43},
    ])
