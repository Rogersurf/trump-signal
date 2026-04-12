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
            df = _client.get_full_data(
                date_from=str(start_date) if start_date else None,
                date_to=str(end_date) if end_date else None,
            )
            if df.empty:
                return _mock_posts(start_date, end_date)

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

    return _mock_posts(start_date, end_date)


def get_sentiments() -> pd.DataFrame:
    return get_posts()


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY SUMMARY — pie chart
# ─────────────────────────────────────────────────────────────────────────────

def get_category_summary(period: str = "month") -> pd.DataFrame:
    if _USE_REAL:
        try:
            result = _client.get_category_distribution()
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

    return pd.DataFrame({
        "category": ["Self-promotion", "Attacking opposition", "Threatening intl.",
                     "Enacting non-agg.", "Praising/endorsing", "De-escalating", "Other"],
        "count":    [72, 44, 38, 35, 21, 8, 14],
    })


# ─────────────────────────────────────────────────────────────────────────────
# STOCK SERIES
# ─────────────────────────────────────────────────────────────────────────────

def get_stock_series(index: str = "sp500", days: int = 30) -> pd.DataFrame:
    if _USE_REAL:
        try:
            end   = datetime.now().strftime("%Y-%m-%d")
            start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
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

    return _mock_stock(index, days)


# ─────────────────────────────────────────────────────────────────────────────
# GDELT
# ─────────────────────────────────────────────────────────────────────────────

def get_gdelt_summary() -> dict:
    if _USE_REAL:
        try:
            df = _client.get_gdelt_events()
            if not df.empty:
                row  = df.iloc[-1]
                # get_gdelt_events returns: military, sanctions, protest, tone, total_events
                tone = float(row.get("tone", 0) or row.get("gdelt_avg_tone", 0) or 0)
                interp = (
                    "Global tension elevated — verbal conflict high, world already tense when Trump posted."
                    if tone < -2 else
                    "Moderate tension detected this week." if tone < -1 else
                    "Global tone relatively neutral this week."
                )
                return {
                    "week_of":            str(row.get("day", "Latest")),
                    "military_events":    int(row.get("military",          row.get("gdelt_military", 0)) or 0),
                    "verbal_conflict":    int(row.get("protest",           row.get("gdelt_verbal_conflict", 0)) or 0),
                    "verbal_cooperation": int(row.get("gdelt_verbal_cooperation", 0) or 0),
                    "material_conflict":  int(row.get("sanctions",         row.get("gdelt_material_conflict", 0)) or 0),
                    "diplomatic":         int(row.get("gdelt_diplomatic",  0) or 0),
                    "goldstein_avg":      round(float(row.get("gdelt_goldstein_avg", 0) or 0), 2),
                    "avg_tone":           round(tone, 2),
                    "total_events":       int(row.get("total_events",      row.get("gdelt_total_events", 0)) or 0),
                    "interpretation":     interp,
                }
        except Exception as e:
            print(f"get_gdelt_summary error: {e}")

    return {
        "week_of": "Latest", "military_events": 2326, "verbal_conflict": 7642,
        "verbal_cooperation": 1710, "material_conflict": 1625, "diplomatic": 0,
        "goldstein_avg": 0.11, "avg_tone": -2.28, "total_events": 13303,
        "interpretation": "Global tension was elevated this week.",
    }


def get_gdelt_timeseries(weeks: int = 8) -> pd.DataFrame:
    if _USE_REAL:
        try:
            end   = datetime.now().strftime("%Y-%m-%d")
            start = (datetime.now() - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
            df    = _client.get_gdelt_trend(start=start, end=end)
            if not df.empty:
                # get_gdelt_trend returns: day, gdelt_avg_tone, gdelt_verbal_conflict, ...
                df = df.rename(columns={
                    "day":                   "week",
                    "gdelt_avg_tone":        "avg_tone",
                    "tone":                  "avg_tone",        # fallback alias
                    "gdelt_verbal_conflict": "verbal_conflict",
                    "protest":               "verbal_conflict",  # fallback alias
                })
                # keep only what geopolitical.py needs
                keep = [c for c in ["week", "avg_tone", "verbal_conflict"] if c in df.columns]
                return df[keep].tail(weeks).reset_index(drop=True)
        except Exception as e:
            print(f"get_gdelt_timeseries error: {e}")

    dates = [datetime(2026, 4, 6) - timedelta(weeks=i) for i in range(weeks - 1, -1, -1)]
    return pd.DataFrame({
        "week":           [d.strftime("%b %d") for d in dates],
        "avg_tone":       [-1.2, -1.8, -2.1, -0.9, -1.5, -2.8, -2.1, -2.28][:weeks],
        "verbal_conflict": [5200, 6100, 7200, 4800, 6500, 8900, 7100, 7642][:weeks],
    })


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

    return _mock_search(query, top_k)


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


# ─────────────────────────────────────────────────────────────────────────────
# MOCK FALLBACKS
# ─────────────────────────────────────────────────────────────────────────────

def _mock_posts(start_date=None, end_date=None):
    posts = [
        {"post_id":"p001","date":"2026-04-06","time":"11:08","datetime":datetime(2026,4,6,11,8),"text":"Great going Freedom Caucus. Proud of you!!! President DJT","sentiment":"POSITIVE","sentiment_score":0.94,"dominant_category":"Self-promotion","engagement_score":22825,"replies":1574,"reblogs":4835,"favourites":16414,"has_media":True,"is_president":True,"sp500_5min_before":6581.56,"sp500_5min_after":6590.99,"market_impact_pct":0.14,"post_type":"original"},
        {"post_id":"p002","date":"2026-04-05","time":"12:03","datetime":datetime(2026,4,5,12,3),"text":"Open the Strait, you crazy bastards, or you'll be living in Hell - JUST WATCH!","sentiment":"NEGATIVE","sentiment_score":0.97,"dominant_category":"Threatening intl.","engagement_score":125335,"replies":22306,"reblogs":19346,"favourites":83683,"has_media":False,"is_president":True,"sp500_5min_before":6581.56,"sp500_5min_after":6562.50,"market_impact_pct":-0.29,"post_type":"original"},
        {"post_id":"p003","date":"2026-04-04","time":"13:32","datetime":datetime(2026,4,4,13,32),"text":"178,000 new jobs, TRADE DEFICIT down 55%. THANK YOU MR. TARIFF! MAGA!!!","sentiment":"POSITIVE","sentiment_score":0.91,"dominant_category":"Enacting non-agg.","engagement_score":60557,"replies":3150,"reblogs":9820,"favourites":47587,"has_media":False,"is_president":True,"sp500_5min_before":6560.00,"sp500_5min_after":6572.00,"market_impact_pct":0.18,"post_type":"original"},
        {"post_id":"p004","date":"2026-04-04","time":"14:05","datetime":datetime(2026,4,4,14,5),"text":"Remember when I gave Iran ten days to MAKE A DEAL or OPEN UP THE HORMUZ STRAIT.","sentiment":"NEGATIVE","sentiment_score":0.93,"dominant_category":"Threatening intl.","engagement_score":65339,"replies":6841,"reblogs":10745,"favourites":47753,"has_media":False,"is_president":True,"sp500_5min_before":6572.00,"sp500_5min_after":6553.00,"market_impact_pct":-0.29,"post_type":"original"},
    ]
    df = pd.DataFrame(posts)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"]     = pd.to_datetime(df["date"])
    if start_date: df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:   df = df[df["date"] <= pd.to_datetime(end_date)]
    return df.sort_values("datetime", ascending=False).reset_index(drop=True)

def _mock_stock(index, days):
    base = {"sp500":6500.0,"djt":8.80,"qqq":570.0,"gld":425.0,"tlt":86.0}
    p = base.get(index, 6500.0); prices = [p]; dates = []
    for i in range(days-1,-1,-1):
        dates.append((datetime(2026,4,6)-timedelta(days=i)).strftime("%Y-%m-%d"))
    for _ in range(days-1):
        prices.append(round(prices[-1]*(1+np.random.normal(0,0.008)),2))
    df = pd.DataFrame({"date":dates,"price":prices,"has_big_post":[False]*days})
    df["pct_change"] = df["price"].pct_change().fillna(0).round(4)
    return df

def _mock_search(query, top_k):
    posts = _mock_posts().to_dict("records")
    kws   = query.lower().split()
    scored = [(sum(1 for kw in kws if kw in p["text"].lower()) + random.uniform(0,.3), p) for p in posts]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"post":p,"score":round(min(s/max(len(kws),1),1.0),2)} for s,p in scored[:top_k]]