from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import traceback
import os
from groq import Groq

from backend_database.data_api import TrumpDataClient
from backend.model_predict import predict_for_date
from backend.model_training import load_posts

import pickle
from huggingface_hub import hf_hub_download

# ------------------------------------------------------------------------------
# 🔥 LOAD EMBEDDINGS FROM HF (DEBUG VERSION — CORRECT)
# ------------------------------------------------------------------------------
try:
    file_path = hf_hub_download(
        repo_id="Rogersurf/trump-pulse-embeddings",
        filename="trump_embeddings.pkl",
        repo_type="dataset",
        token=os.environ.get("HF_TOKEN")
    )

    print("FILE PATH:", file_path)
    print("FILE EXISTS:", os.path.exists(file_path))

    with open(file_path, "rb") as f:
        data = pickle.load(f)

    # 🔥 DEBUG FIRST (BEFORE ACCESSING KEYS)
    print("🔥 DATA TYPE:", type(data))

    if isinstance(data, dict):
        print("🔥 DATA KEYS:", data.keys())
    else:
        print("🔥 NOT A DICT — STRUCTURE:", data)

    # 🔥 SAFE EXTRACTION (NO CRASH)
    if isinstance(data, dict):
        texts = data["posts"]
        embeddings = np.array(data["embeddings"])

        print("LEN TEXTS:", len(texts))
        print("EMB SHAPE:", embeddings.shape)
    else:
        raise ValueError("Pickle is not a dict")

    if texts is None or embeddings is None:
        raise ValueError("Could not find text/embedding keys in dataset")

    embeddings = np.array(embeddings)

    print("✅ EMBEDDINGS LOADED:", len(texts))
    print("SHAPE:", embeddings.shape)
    print("SAMPLE TEXT:", texts[0][:100])

except Exception as e:
    print("🔥 FAILED TO LOAD EMBEDDINGS:", e)

    texts = ["fallback"]
    embeddings = np.random.rand(1, 384)

except Exception as e:
    print("🔥 FAILED TO LOAD EMBEDDINGS:", e)

    texts = ["fallback"]
    embeddings = np.random.rand(1, 384)


# ------------------------------------------------------------------------------
# 🔥 GROQ (SAFE INIT — FIXED)
# ------------------------------------------------------------------------------
groq_api_key = os.environ.get("GROQ_API_KEY")

if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)
    print("✅ GROQ CONNECTED")
else:
    groq_client = None
    print("⚠️ GROQ NOT CONFIGURED")

# ------------------------------------------------------------------------------
# APP
# ------------------------------------------------------------------------------
app = FastAPI()

DB_PATH = os.environ.get("DB_PATH", "/data/trump_pulse/trump_data.db")

# ------------------------------------------------------------------------------
# HEALTH
# ------------------------------------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "db_exists": os.path.exists(DB_PATH),
        "db_path": DB_PATH
    }

# ------------------------------------------------------------------------------
# MAX DATE
# ------------------------------------------------------------------------------
@app.get("/data/max_date")
def max_date():
    try:
        conn = sqlite3.connect(DB_PATH)
        date = conn.execute("SELECT MAX(date) FROM truth_social").fetchone()[0]
        conn.close()

        if date is None:
            return {"max_date": datetime.today().strftime("%Y-%m-%d")}

        return {"max_date": date}

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# POSTS
# ------------------------------------------------------------------------------
@app.get("/posts")
def get_posts(start_date: str = None, end_date: str = None):
    try:
        client = TrumpDataClient(DB_PATH)

        df = client.get_full_data(
            date_from=start_date,
            date_to=end_date
        )

        if df is None or df.empty:
            return []

        df = df.replace({np.nan: None})
        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# CATEGORIES (UNCHANGED — YOUR FIX IS GOOD)
# ------------------------------------------------------------------------------
@app.get("/categories")
def categories(date_from: str = None, date_to: str = None):
    try:
        conn = sqlite3.connect(DB_PATH)

        query = "SELECT * FROM truth_social WHERE 1=1"

        if date_from:
            query += f" AND DATE(date) >= '{date_from}'"
        if date_to:
            query += f" AND DATE(date) <= '{date_to}'"

        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            return []

        cat_cols = [c for c in df.columns if c.startswith("cat_")]

        df[cat_cols] = df[cat_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
        df = df[df[cat_cols].sum(axis=1) > 0]

        if df.empty:
            return []

        df["category"] = df[cat_cols].idxmax(axis=1)
        df["category"] = df["category"].str.replace("cat_", "")

        result = df["category"].value_counts().reset_index()
        result.columns = ["category", "count"]

        return result.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# MODEL
# ------------------------------------------------------------------------------
@app.get("/model/predict/date/{date}")
def predict_date(date: str):
    try:
        df = predict_for_date(date)

        if df is None or len(df) == 0:
            return {"status": "no_data", "date": date, "data": []}

        df = df.copy()

        for col in df.columns:
            if pd.api.types.is_integer_dtype(df[col]):
                df[col] = df[col].astype(int)
            elif pd.api.types.is_float_dtype(df[col]):
                df[col] = df[col].astype(float)
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)

        return {"status": "ok", "data": df.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------------------------------------------------------
# CATEGORY IMPACT (UNCHANGED — ALREADY FIXED)
# ------------------------------------------------------------------------------
@app.get("/categories/impact")
def get_category_impact(start: str, end: str):
    try:
        df, cat_cols, _ = load_posts()

        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        df = df[(df["date"] >= start) & (df["date"] <= end)].copy()

        if df.empty:
            return []

        df["impact"] = (df["sp500_close"] - df["sp500_open"]).fillna(0)
        df[cat_cols] = df[cat_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
        df = df[df[cat_cols].sum(axis=1) > 0]

        results = []

        for cat in cat_cols:
            weight = df[cat]
            if weight.sum() == 0:
                continue

            avg_impact = (df["impact"] * weight).sum() / weight.sum()

            results.append({
                "category": cat.replace("cat_", ""),
                "avg_impact": float(round(avg_impact, 6))
            })

        return results

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# QA (FIXED — REAL EMBEDDING + SAFE FALLBACK)
# ------------------------------------------------------------------------------
from backend_database.embeddings import get_search_engine

@app.get("/qa")
def qa(query: str, limit: int = 5):
    try:
        engine = get_search_engine(DB_PATH)
        results = engine.search(query, top_k=limit)

        import sqlite3
        import pandas as pd

        conn = sqlite3.connect(DB_PATH)

        enriched = []

        for r in results:
            post = r["post"]
            post_id = post.get("post_id")

            try:
                row = pd.read_sql(
                    """
                    SELECT 
                        url,
                        sp500_5min_before, sp500_5min_after,
                        qqq_5min_before, qqq_5min_after,
                        djt_5min_before, djt_5min_after,
                        during_market_hours
                    FROM truth_social
                    WHERE post_id = ?
                    LIMIT 1
                    """,
                    conn,
                    params=[str(post_id)]
                )

                if not row.empty:
                    extra = row.iloc[0].to_dict()
                    post.update(extra)

            except Exception as e:
                print("ENRICH ERROR:", e)

            enriched.append({
                "post": post,
                "score": r["score"]
            })

        conn.close()

        return {
            "query": query,
            "results": enriched
        }

    except Exception as e:
        return {"error": str(e)}