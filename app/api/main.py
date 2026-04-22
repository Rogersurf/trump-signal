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
# 🔥 LOAD EMBEDDINGS FROM HF (FIXED)
# ------------------------------------------------------------------------------
try:
    file_path = hf_hub_download(
        repo_id="Rogersurf/trump-pulse-embeddings",
        filename="trump_embeddings.pkl",
        repo_type="dataset",
        token=os.environ.get("HF_TOKEN")
    )

    with open(file_path, "rb") as f:
        data = pickle.load(f)

    texts = data["text"]
    embeddings = np.array(data["embedding"])

    print(f"✅ EMBEDDINGS LOADED: {len(texts)}")
    print("----- DEBUG EMBEDDINGS -----")
    print("texts type:", type(texts))
    print("embeddings type:", type(embeddings))

    print("len(texts):", len(texts))
    print("embeddings shape:", embeddings.shape)

    print("sample text:", texts[0][:200] if len(texts) > 0 else "EMPTY")
    print("sample embedding (first 5 values):", embeddings[0][:5] if len(embeddings) > 0 else "EMPTY")
    print("----------------------------")

except Exception as e:
    print("🔥 FAILED TO LOAD EMBEDDINGS:", e)

    texts = ["fallback"]
    embeddings = np.random.rand(1, 384)

# ------------------------------------------------------------------------------
# 🔥 EMBEDDING MODEL (SAFE ADD — THIS WAS MISSING)
# ------------------------------------------------------------------------------
try:
    from sentence_transformers import SentenceTransformer
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ EMBEDDING MODEL LOADED")
except Exception as e:
    print("🔥 EMBEDDING MODEL FAILED:", e)
    embedding_model = None

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
@app.get("/qa")
def qa(query: str, limit: int = 5):
    try:
        # 🔥 REAL embedding if possible
        if embedding_model is None:
            return {
                "answer": "Embedding model not available. Semantic search disabled.",
                "matches": []
            }

        query_vec = embedding_model.encode(query)

        def normalize(v):
            return v / (np.linalg.norm(v) + 1e-8)

        query_vec = normalize(query_vec)
        emb_norm = embeddings / (
            np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-8
        )

        sims = emb_norm @ query_vec
        top_idx = np.argsort(sims)[::-1][:limit]

        matches = [texts[i] for i in top_idx]
        context = "\n\n".join(matches)

        if groq_client is None:
            return {
                "answer": context[:1000],
                "matches": matches
            }

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "Analyze political posts."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
            ]
        )

        return {
            "answer": response.choices[0].message.content,
            "matches": matches
        }

    except Exception as e:
        print("🔥 QA ERROR:", e)
        return {"error": str(e)}