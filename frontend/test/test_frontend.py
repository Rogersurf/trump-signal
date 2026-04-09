"""
tests/test_frontend.py
======================
Smoke tests สำหรับ frontend — GitHub Actions จะรันทุกครั้งที่ push
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.data.api_client import (
    get_posts, get_category_summary, get_stock_series,
    get_gdelt_summary, get_gdelt_timeseries,
    ask_question, get_pipeline_status, get_artifact_log,
)
from frontend.config import TRANSLATIONS, TIMEZONES, CATEGORY_COLORS

def test_config_has_all_languages():
    for lang in ["English", "Thai", "Chinese"]:
        assert lang in TRANSLATIONS, f"Missing language: {lang}"
        T = TRANSLATIONS[lang]
        required_keys = ["app_title", "tagline", "daily_feed", "market", "geo", "qa"]
        for k in required_keys:
            assert k in T, f"Missing key '{k}' in {lang}"

def test_get_posts_returns_data():
    df = get_posts()
    assert len(df) > 0, "get_posts() returned empty"
    required_cols = ["text", "sentiment", "dominant_category", "market_impact_pct"]
    for col in required_cols:
        assert col in df.columns, f"Missing column: {col}"

def test_get_posts_date_filter():
    df = get_posts("2026-04-05", "2026-04-06")
    assert len(df) > 0
    assert all(df["date"] >= "2026-04-05"), "Date filter failed"

def test_category_summary():
    for period in ["week", "month", "year"]:
        df = get_category_summary(period)
        assert len(df) > 0, f"Empty category summary for {period}"
        assert "category" in df.columns
        assert "count" in df.columns

def test_stock_series():
    for index in ["sp500", "djt", "qqq"]:
        df = get_stock_series(index, 7)
        assert len(df) == 7, f"Wrong length for {index}"
        assert "price" in df.columns
        assert "has_big_post" in df.columns

def test_gdelt():
    g = get_gdelt_summary()
    assert "avg_tone" in g
    assert "interpretation" in g
    df = get_gdelt_timeseries(4)
    assert len(df) == 4

def test_semantic_search():
    results = ask_question("Iran", top_k=2)
    assert len(results) == 2
    assert "post" in results[0]
    assert "score" in results[0]

def test_pipeline_status():
    s = get_pipeline_status()
    assert "status" in s
    assert "total_posts" in s

def test_artifact_log():
    df = get_artifact_log()
    assert len(df) > 0
    assert "stage" in df.columns
    assert "status" in df.columns

if __name__ == "__main__":
    tests = [
        test_config_has_all_languages,
        test_get_posts_returns_data,
        test_get_posts_date_filter,
        test_category_summary,
        test_stock_series,
        test_gdelt,
        test_semantic_search,
        test_pipeline_status,
        test_artifact_log,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
