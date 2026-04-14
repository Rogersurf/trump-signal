"""
data/api_client.py
==================
จุดเดียวที่ติดต่อกับ API ทั้งหมด
ใช้ TrumpDataClient จาก backend_database/data_api.py
fallback เป็น mock data ถ้า client ไม่พร้อม
"""

import random
import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from frontend.config import API_URL
import sqlite3

_DB_PATH = os.environ.get("TRUMP_DB_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend_database", "trump_data.db")))

def _get_conn():
    return sqlite3.connect(_DB_PATH)

random.seed(42)
np.random.seed(42)

# ── Load TrumpDataClient ──────────────────────────────────────────────────────
try:
    from backend_database.data_api import TrumpDataClient
    _client = TrumpDataClient()
    _client.get_kpis()  # test connection
    _USE_REAL = True
    print("[api_client] TrumpDataClient connected — using real data")
except Exception as e:
    _client = None
    _USE_REAL = False
    print(f"[api_client] TrumpDataClient not available — using mock data ({e})")


def is_api_alive() -> bool:
    return _USE_REAL


# ─────────────────────────────────────────────────────────────────────────────
# POSTS
# ─────────────────────────────────────────────────────────────────────────────

def get_posts(start_date=None, end_date=None) -> pd.DataFrame:
    if _USE_REAL:
        try:
            # use DATE() to handle datetime format in DB
            import sqlite3, os
            db = os.environ.get("TRUMP_DB_PATH",
                 os.path.abspath(os.path.join(os.path.dirname(__file__),
                 "..", "..", "backend_database", "trump_data.db")))
            conn = sqlite3.connect(db)
            query = "SELECT * FROM truth_social WHERE 1=1"
            params = []
            if start_date:
                query += " AND DATE(date) >= ?"
                params.append(str(start_date))
            if end_date:
                query += " AND DATE(date) <= ?"
                params.append(str(end_date))
            query += " ORDER BY datetime DESC LIMIT 500"
            df = pd.read_sql(query, conn, params=params)
            conn.close()
            if df.empty:
                return pd.DataFrame()  # no mock — show empty

            # rename columns ให้ตรงกับ frontend
            df = df.rename(columns={
                "replies_count":    "replies",
                "reblogs_count":    "reblogs",
                "favourites_count": "favourites",
            })

            df = _add_dominant_category(df)
            df = _add_market_impact(df)
            df = _add_engagement(df)

            # sentiment — pending Chenghao
            if "sentiment" not in df.columns:
                df["sentiment"]       = "NEUTRAL"
                df["sentiment_score"] = 0.5

            df["post_type"] = df["text"].apply(
                lambda x: "repost" if str(x).startswith("RT") else "original"
            )
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
            df["date"]     = pd.to_datetime(df["date"],     errors="coerce")

            return df.sort_values("datetime", ascending=False).reset_index(drop=True)

        except Exception as e:
            print(f"get_posts error: {e}")

    return pd.DataFrame()  # empty = no data


def get_sentiments() -> pd.DataFrame:
    return get_posts()


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY SUMMARY — pie chart
# ─────────────────────────────────────────────────────────────────────────────

def get_category_summary(period: str = "month", date_from: str = None, date_to: str = None) -> pd.DataFrame:
    if _USE_REAL:
        try:
            from datetime import date, timedelta
            if not date_from or not date_to:
                period_days = {'week': 7, 'month': 30, 'year': 365}.get(period, 30)
                date_to   = date.today().strftime('%Y-%m-%d')
                date_from = (date.today() - timedelta(days=period_days)).strftime('%Y-%m-%d')
            result = _client.get_category_distribution(date_from=date_from, date_to=date_to)
            if isinstance(result, pd.Series):
                return pd.DataFrame({
                    "category": [_CAT_MAP.get(k, k) for k in result.index],
                    "count":    [round(float(v) * 100, 1) for v in result.values],
                })
            elif isinstance(result, pd.DataFrame):
                if "category" not in result.columns:
                    result.columns = ["category", "count"]
                return result
        except Exception as e:
            print(f"get_category_summary error: {e}")

    return pd.DataFrame(columns=["category", "count"])


# ─────────────────────────────────────────────────────────────────────────────
# STOCK SERIES
# ─────────────────────────────────────────────────────────────────────────────

def get_stock_series(index: str = "sp500", days: int = 30) -> pd.DataFrame:
    if _USE_REAL:
        try:
            # use dataset max date dynamically — no hardcode
            all_df   = _client.get_full_data()
            max_date = pd.to_datetime(all_df["date"]).max() if not all_df.empty else datetime.now()
            end   = max_date.strftime("%Y-%m-%d")
            start = (max_date - timedelta(days=days)).strftime("%Y-%m-%d")
            df    = _client.get_market_impact(start=start, end=end)

            if not df.empty:
                # get_market_impact returns _5min_pct columns for sp500/qqq/dia only
                col_map = {
                    "sp500": "sp500_5min_pct",
                    "qqq":   "qqq_5min_pct",
                    "dia":   "dia_5min_pct",
                }
                col = col_map.get(index)

                if col and col in df.columns:
                    result = df[["date", col]].copy()
                    result = result.rename(columns={col: "price"})
                    result["price"]        = pd.to_numeric(result["price"], errors="coerce")
                    result["has_big_post"] = result["price"].abs() > 0.3   # flag big moves
                    result["pct_change"]   = result["price"].round(4)
                    return result.dropna(subset=["price"]).reset_index(drop=True)

                # fallback for djt/gld/tlt — use get_daily_metrics which has close prices
                close_map = {
                    "djt": "djt_close",
                    "gld": "gld_close",
                    "tlt": "tlt_close",
                }
                close_col = close_map.get(index)
                if close_col:
                    dm = _client.get_daily_metrics(date_from=start, date_to=end)
                    if not dm.empty and close_col in dm.columns:
                        result = dm[["day", close_col]].copy()
                        result = result.rename(columns={"day": "date", close_col: "price"})
                        result["price"]        = pd.to_numeric(result["price"], errors="coerce")
                        result["has_big_post"] = False
                        result["pct_change"]   = result["price"].pct_change().fillna(0).round(4)
                        return result.dropna(subset=["price"]).reset_index(drop=True)

        except Exception as e:
            print(f"get_stock_series error: {e}")

    return pd.DataFrame(columns=["date", "price", "has_big_post", "pct_change"])


# ─────────────────────────────────────────────────────────────────────────────
# GDELT
# ─────────────────────────────────────────────────────────────────────────────

def get_gdelt_summary() -> dict:
    if _USE_REAL:
        try:
            # use get_gdelt_trend — dynamic max date, no hardcode
            all_df = _client.get_gdelt_trend(start="2020-01-01", end="2099-12-31")
            if not all_df.empty:
                max_date = pd.to_datetime(all_df["day"]).max()
                start    = (max_date - timedelta(days=7)).strftime("%Y-%m-%d")
                df       = _client.get_gdelt_trend(
                    start=start,
                    end=max_date.strftime("%Y-%m-%d")
                )
                if not df.empty:
                    row  = df.iloc[-1]
                    tone = float(row.get("gdelt_avg_tone", 0) or 0)
                    interp = (
                        "Global tension elevated — verbal conflict high."
                        if tone < -2 else
                        "Moderate tension detected this week." if tone < -1 else
                        "Global tone relatively neutral this week."
                    )
                    return {
                        "week_of":            str(max_date.strftime("%d %b %Y")),
                        "military_events":    int(row.get("gdelt_military",           0) or 0),
                        "verbal_conflict":    int(row.get("gdelt_verbal_conflict",    0) or 0),
                        "verbal_cooperation": int(row.get("gdelt_verbal_cooperation", 0) or 0),
                        "material_conflict":  int(row.get("gdelt_material_conflict",  0) or 0),
                        "diplomatic":         int(row.get("gdelt_diplomatic",         0) or 0),
                        "goldstein_avg":      round(float(row.get("gdelt_goldstein_avg", 0) or 0), 2),
                        "avg_tone":           round(tone, 2),
                        "total_events":       int(row.get("gdelt_total_events",       0) or 0),
                        "interpretation":     interp,
                    }
        except Exception as e:
            print(f"get_gdelt_summary error: {e}")
    return {}


def get_gdelt_timeseries(weeks: int = 8) -> pd.DataFrame:
    if _USE_REAL:
        try:
            weeks = max(weeks, 4)
            # get latest date from dataset dynamically — no hardcode
            all_df = _client.get_gdelt_trend(start="2020-01-01", end="2099-12-31")
            if all_df.empty:
                return pd.DataFrame(columns=["week", "avg_tone", "verbal_conflict"])
            max_date = pd.to_datetime(all_df["day"]).max()
            end   = max_date.strftime("%Y-%m-%d")
            start = (max_date - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
            df    = _client.get_gdelt_trend(start=start, end=end)
            if not df.empty:
                # get_gdelt_trend returns: day, gdelt_avg_tone, gdelt_verbal_conflict, ...
                df["day"] = pd.to_datetime(df["day"]).dt.strftime("%d %b")
                df = df.rename(columns={
                    "day":                   "week",
                    "gdelt_avg_tone":        "avg_tone",
                    "tone":                  "avg_tone",
                    "gdelt_verbal_conflict": "verbal_conflict",
                    "protest":               "verbal_conflict",
                })
                # keep only what geopolitical.py needs
                keep = [c for c in ["week", "avg_tone", "verbal_conflict"] if c in df.columns]
                return df[keep].tail(weeks).reset_index(drop=True)
        except Exception as e:
            print(f"get_gdelt_timeseries error: {e}")

    return pd.DataFrame(columns=["week", "avg_tone", "verbal_conflict"])


# ─────────────────────────────────────────────────────────────────────────────
# Q&A
# ─────────────────────────────────────────────────────────────────────────────

def ask_question(query: str, top_k: int = 4) -> list:
    # ลองเรียก FastAPI ก่อน
    try:
        r = requests.get(f"{API_URL}/qa", params={"query": query, "top_k": top_k}, timeout=8)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data and isinstance(data[0], dict) and "post" in data[0]:
                return data
            if isinstance(data, dict) and "results" in data:
                return data["results"]
    except:
        pass
    # Semantic search + DB lookup
    try:
        from backend_database.embeddings import get_search_engine
        engine  = get_search_engine()
        results = engine.search(query, top_k=top_k)
        if results:
            formatted = []
            for r in results:
                post  = r.get("post", {})
                score = r.get("score", 0)
                row   = {}
                try:
                    conn = _get_conn()
                    rows = pd.read_sql(
                        "SELECT * FROM truth_social WHERE post_id = ?",
                        conn, params=[str(post.get("post_id", ""))]
                    )
                    if not rows.empty:
                        row = rows.iloc[0].to_dict()
                    conn.close()
                except Exception as db_e:
                    print(f"[QA] DB lookup error: {db_e}")
                try:
                    b      = float(row.get("sp500_5min_before", 0) or 0)
                    a      = float(row.get("sp500_5min_after",  0) or 0)
                    impact = round((a - b) / b * 100, 2) if b != 0 else 0
                except:
                    impact = 0
                formatted.append({
                    "post": {
                        "post_id":           str(post.get("post_id", "")),
                        "date":              str(post.get("date", "")),
                        "text":              str(row.get("text", "") or post.get("text", "")),
                        "sentiment":         "NEUTRAL",
                        "sentiment_score":   0.5,
                        "dominant_category": "Other",
                        "market_impact_pct": impact,
                        "sp500_5min_before": row.get("sp500_5min_before", 0),
                        "sp500_5min_after":  row.get("sp500_5min_after",  0),
                        "qqq_5min_before":   row.get("qqq_5min_before",   0),
                        "qqq_5min_after":    row.get("qqq_5min_after",    0),
                        "djt_5min_before":   row.get("djt_5min_before",   0),
                        "djt_5min_after":    row.get("djt_5min_after",    0),
                        "gld_5min_before":   row.get("gld_5min_before",   0),
                        "gld_5min_after":    row.get("gld_5min_after",    0),
                        "tlt_5min_before":   row.get("tlt_5min_before",   0),
                        "tlt_5min_after":    row.get("tlt_5min_after",    0),
                        "uso_5min_before":   row.get("uso_5min_before",   0),
                        "uso_5min_after":    row.get("uso_5min_after",    0),
                        "ibit_5min_before":  row.get("ibit_5min_before",  0),
                        "ibit_5min_after":   row.get("ibit_5min_after",   0),
                        "lmt_5min_before":   row.get("lmt_5min_before",   0),
                        "lmt_5min_after":    row.get("lmt_5min_after",    0),
                        "uup_5min_before":   row.get("uup_5min_before",   0),
                        "uup_5min_after":    row.get("uup_5min_after",    0),
                        "url":               str(row.get("url", "")),
                        "replies":           int(row.get("replies_count",    0) or 0),
                        "reblogs":           int(row.get("reblogs_count",    0) or 0),
                        "favourites":        int(row.get("favourites_count", 0) or 0),
                    },
                    "score": round(float(score) / 100, 2),
                })
            return formatted
    except Exception as e:
        print(f"[QA] Semantic search error: {e}")

    if _USE_REAL:
        try:
            df = _client.get_top_posts()
            if not df.empty:
                keywords = [w for w in query.lower().split() if len(w) > 2]
                mask     = df["text"].str.lower().apply(
                    lambda t: any(kw in str(t) for kw in keywords)
                )
                matched = df[mask].head(top_k)
                if not matched.empty:
                    matched = _add_dominant_category(matched)
                    matched = _add_market_impact(matched)
                    results = []
                    for _, row in matched.iterrows():
                        score = round(
                            min(sum(1 for kw in keywords if kw in str(row.get("text", "")).lower())
                                / max(len(keywords), 1), 1.0), 2
                        )
                        results.append({
                            "post": {
                                "post_id":           str(row.get("post_id", "")),
                                "date":              str(row.get("date", "")),
                                "text":              str(row.get("text", "")),
                                "sentiment":         "NEUTRAL",
                                "sentiment_score":   0.5,
                                "dominant_category": row.get("dominant_category", "Other"),
                                "market_impact_pct": float(row.get("market_impact_pct", 0)),
                                "replies":           int(row.get("replies_count", 0) or 0),
                                "reblogs":           int(row.get("reblogs_count", 0) or 0),
                                "favourites":        int(row.get("favourites_count", 0) or 0),
                            },
                            "score": score,
                        })
                    return results
        except Exception as e:
            print(f"ask_question error: {e}")

    return []  # no mock — show empty


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE STATUS
# ─────────────────────────────────────────────────────────────────────────────

def get_pipeline_status() -> dict:
    if _USE_REAL:
        try:
            kpis = _client.get_kpis()
            total = int(kpis.get("total_posts", 0))
            pct_mh = float(kpis.get("pct_market_hours", 0) or 0)
            return {
                "last_ingest":          "daily @ 02:00 UTC (APScheduler)",
                "last_preprocess":      "on ingest",
                "last_sentiment_run":   "pre-labeled in dataset",
                "last_embedding_build": "on ingest (ChromaDB)",
                "last_gdelt_update":    "weekly",
                "total_posts":          total,
                "posts_today":          0,
                "rows_dropped_today":   0,
                "pct_market_hours":     round(pct_mh, 1),
                "model_name":           "cardiffnlp/twitter-roberta-base-sentiment",
                "embedding_model":      "all-MiniLM-L6-v2",
                "dataset_version":      "chrissoria/trump-truth-social @ main",
                "artifact_path":        "backend_database/trump_data.db",
                "status":               "healthy",
                "errors":               [],
            }
        except Exception as e:
            print(f"get_pipeline_status error: {e}")

    return {
        "last_ingest": "N/A", "last_preprocess": "N/A",
        "last_sentiment_run": "N/A", "last_embedding_build": "N/A",
        "last_gdelt_update": "N/A", "total_posts": 0, "posts_today": 0,
        "rows_dropped_today": 0, "model_name": "N/A", "embedding_model": "N/A",
        "dataset_version": "N/A", "artifact_path": "N/A", "status": "mock", "errors": ["Not connected"],
    }


def get_artifact_log() -> pd.DataFrame:
    if _USE_REAL:
        try:
            metrics = _client.get_daily_metrics()
            if not metrics.empty:
                return pd.DataFrame([{
                    "timestamp": str(metrics.iloc[0].get("day", "N/A")),
                    "stage":     "daily_update",
                    "rows":      int(metrics.iloc[0].get("posts", 0) or 0),
                    "status":    "ok",
                    "duration_s": 0,
                }])
        except Exception as e:
            print(f"get_artifact_log error: {e}")

    return pd.DataFrame([{
        "timestamp": "N/A", "stage": "not connected",
        "rows": 0, "status": "error", "duration_s": 0
    }])


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

_CAT_MAP = {
    "cat_self_promotion":         "Self-promotion",
    "cat_attacking_opposition":   "Attacking opposition",
    "cat_attacking_individual":   "Attacking individual",
    "cat_threatening_intl":       "Threatening intl.",
    "cat_enacting_nonaggressive": "Enacting non-agg.",
    "cat_enacting_aggressive":    "Enacting aggressive",
    "cat_praising_endorsing":     "Praising/endorsing",
    "cat_deescalating":           "De-escalating",
    "cat_other":                  "Other",
}

def _add_dominant_category(df):
    cols = [c for c in _CAT_MAP if c in df.columns]
    if not cols:
        df["dominant_category"] = "Other"
        return df
    df["dominant_category"] = (
        df[cols].apply(pd.to_numeric, errors="coerce")
        .fillna(0).idxmax(axis=1).map(_CAT_MAP).fillna("Other")
    )
    return df

def _add_market_impact(df):
    b = pd.to_numeric(df.get("sp500_5min_before", pd.Series(dtype=float)), errors="coerce")
    a = pd.to_numeric(df.get("sp500_5min_after",  pd.Series(dtype=float)), errors="coerce")
    df["market_impact_pct"] = ((a - b) / b.replace(0, np.nan) * 100).round(3).fillna(0)
    return df

def _add_engagement(df):
    r  = pd.to_numeric(df.get("replies",   pd.to_numeric(df.get("replies_count",   0), errors="coerce")), errors="coerce").fillna(0)
    rb = pd.to_numeric(df.get("reblogs",   pd.to_numeric(df.get("reblogs_count",   0), errors="coerce")), errors="coerce").fillna(0)
    f  = pd.to_numeric(df.get("favourites",pd.to_numeric(df.get("favourites_count",0), errors="coerce")), errors="coerce").fillna(0)
    df["engagement_score"] = (r + rb * 2 + f).astype(int)
    return df

