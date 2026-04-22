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
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

# 🔥 Load HF dataset (your embeddings)
dataset = load_dataset("Rogersurf/trump-pulse-embeddings", split="train")

texts = dataset["text"]
embeddings = np.vstack(dataset["embedding"])

# 🔥 Model for query (must match how embeddings were created)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔥 Groq client
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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
# 🔥 FIXED CATEGORIES (THIS IS YOUR BUG)
# ------------------------------------------------------------------------------
@app.get("/categories")
def categories(date_from: str = None, date_to: str = None):
    try:
        # 🔥 BYPASS data_api completely
        conn = sqlite3.connect(DB_PATH)

        query = "SELECT * FROM truth_social WHERE 1=1"

        if date_from:
            query += f" AND DATE(date) >= '{date_from}'"
        if date_to:
            query += f" AND DATE(date) <= '{date_to}'"

        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print("⚠️ EMPTY RAW DATA")
            return []

        cat_cols = [c for c in df.columns if c.startswith("cat_")]

        if not cat_cols:
            print("⚠️ NO CATEGORY COLUMNS")
            return []

        # 🔥 FORCE numeric
        df[cat_cols] = df[cat_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

        # 🔥 KEEP ONLY rows with signal
        df = df[df[cat_cols].sum(axis=1) > 0]

        if df.empty:
            print("⚠️ ALL CATEGORY VALUES ZERO AFTER FILTER")
            return []

        # dominant category
        df["category"] = df[cat_cols].idxmax(axis=1)
        df["category"] = df["category"].str.replace("cat_", "")

        result = df["category"].value_counts().reset_index()
        result.columns = ["category", "count"]

        print("✅ FINAL CATEGORY OUTPUT:", result.head())

        return result.to_dict(orient="records")

    except Exception as e:
        print("🔥 CATEGORY ERROR:", e)
        traceback.print_exc()
        return {"error": str(e)}
# ------------------------------------------------------------------------------
# MODEL
# ------------------------------------------------------------------------------
@app.get("/model/predict/date/{date}")
def predict_date(date: str):
    try:
        df = predict_for_date(date)

        if df is None or len(df) == 0:
            return {
                "status": "no_data",
                "date": date,
                "data": []
            }

        df = df.copy()

        for col in df.columns:
            if pd.api.types.is_integer_dtype(df[col]):
                df[col] = df[col].astype(int)
            elif pd.api.types.is_float_dtype(df[col]):
                df[col] = df[col].astype(float)
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)

        return {
            "status": "ok",
            "data": df.to_dict(orient="records")
        }

    except Exception as e:
        print("🔥 PREDICT ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------------------------------------------------------
# GDELT
# ------------------------------------------------------------------------------
@app.get("/gdelt/range")
def gdelt_range(start: str, end: str):
    try:
        client = TrumpDataClient(DB_PATH)
        df = client.get_gdelt_trend(start, end)

        if df is None or df.empty:
            return []

        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.replace({np.nan: None})

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# STOCKS
# ------------------------------------------------------------------------------
@app.get("/stocks")
def stocks(index: str = "sp500", days: int = 30):
    try:
        dates = pd.date_range(end=datetime.today(), periods=days)

        df = pd.DataFrame({
            "date": dates.astype(str),
            "price": np.random.rand(days) * 100,
            "has_big_post": np.random.choice([True, False], days),
            "pct_change": np.random.randn(days)
        })

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# QA
# ------------------------------------------------------------------------------
@app.get("/categories/impact")
def get_category_impact(start: str, end: str):
    try:
        df, cat_cols, _ = load_posts()

        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        df = df[(df["date"] >= start) & (df["date"] <= end)].copy()

        if df.empty:
            print("⚠️ NO DATA IN DATE RANGE")
            return []

        # 🔥 CREATE IMPACT
        if "sp500_close" not in df.columns or "sp500_open" not in df.columns:
            print("⚠️ MISSING MARKET COLUMNS")
            return []

        df["impact"] = (df["sp500_close"] - df["sp500_open"]).fillna(0)

        # 🔥 FIX: force numeric
        df[cat_cols] = df[cat_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

        # 🔥 REMOVE rows with no category signal
        df = df[df[cat_cols].sum(axis=1) > 0]

        if df.empty:
            print("⚠️ ALL CATEGORY VALUES ZERO")
            return []

        results = []

        # 🔥 FIX: weighted average instead of threshold
        for cat in cat_cols:

            weight = df[cat]

            if weight.sum() == 0:
                continue

            avg_impact = (df["impact"] * weight).sum() / weight.sum()

            results.append({
                "category": cat.replace("cat_", ""),
                "avg_impact": float(round(avg_impact, 6))
            })

        print("✅ CATEGORY IMPACT:", results[:3])

        return results

    except Exception as e:
        print("🔥 CATEGORY IMPACT ERROR:", e)
        traceback.print_exc()
        return {"error": str(e)}
    
# ------------------------------------------------------------------------------
# QA (RAG WITH HF + GROQ)
# ------------------------------------------------------------------------------
@app.get("/qa")
def qa(query: str, limit: int = 5):
    try:
        if not query:
            return {"answer": "Empty query", "matches": []}

        # 🔥 embed query
        query_vec = embedding_model.encode([query], convert_to_numpy=True)[0]

        # 🔥 cosine similarity
        scores = np.dot(embeddings, query_vec) / (
            np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_vec)
        )

        # 🔥 top-k
        top_k_idx = np.argsort(scores)[-limit:][::-1]

        matches = [
            {
                "text": texts[i],
                "score": float(scores[i])
            }
            for i in top_k_idx
        ]

        context = "\n".join([texts[i] for i in top_k_idx])

        # 🔥 LLM
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Answer using Trump posts context."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion:\n{query}"
                }
            ],
            temperature=0.3
        )

        return {
            "answer": response.choices[0].message.content,
            "matches": matches
        }

    except Exception as e:
        print("🔥 QA ERROR:", e)
        return {"answer": str(e), "matches": []}