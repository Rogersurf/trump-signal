"""
Local daily sync script for Trump Truth Social posts.

Responsibilities:
- Fetch latest dataset from source (chrissoria)
- Refresh LOCAL SQLite database (full snapshot)

IMPORTANT:
- This script is LOCAL ONLY
- It does NOT upload to Hugging Face
- It does NOT perform incremental updates
- It does NOT rebuild embeddings
"""

import sqlite3
import pandas as pd
import sys
import os
from datetime import datetime
from datasets import load_dataset

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_database.data_api import DB_PATH

HF_SOURCE = "chrissoria/trump-truth-social"


# ─────────────────────────────────────────────
# SYNC TASK (LOCAL ONLY)
# ─────────────────────────────────────────────
def sync_task():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 60)
    print(f"[{now}] LOCAL SYNC START")
    print(f"[DEBUG] DB_PATH: {DB_PATH}")

    try:
        # ─────────────────────────────
        # 1. FETCH DATASET
        # ─────────────────────────────
        print("[1/3] Fetching dataset from Hugging Face source...")

        dataset = load_dataset(HF_SOURCE)
        df = dataset["train"].to_pandas()

        print(f"[INFO] Rows fetched: {len(df)}")

        # Normalize datetime columns
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

        # ─────────────────────────────
        # 2. WRITE LOCAL DB (FULL REFRESH)
        # ─────────────────────────────
        print("[2/3] Writing LOCAL SQLite database (full refresh)...")

        with sqlite3.connect(DB_PATH) as conn:
            df.to_sql(
                "truth_social",
                conn,
                if_exists="replace",  # full overwrite (intentional)
                index=False
            )

            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_date ON truth_social (date)"
            )

        print("[INFO] Local database updated successfully")

        # ─────────────────────────────
        # 3. SUMMARY
        # ─────────────────────────────
        print("[3/3] Validation check...")

        with sqlite3.connect(DB_PATH) as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM truth_social"
            ).fetchone()[0]

        print(f"[INFO] Total rows in DB: {count}")

        print(f"[{now}] LOCAL SYNC COMPLETE")
        print("=" * 60)

    except Exception as e:
        print(f"[ERROR] Local sync failed: {e}")
        print("=" * 60)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print(f"[INIT] Checking DB at: {DB_PATH}")

    if not os.path.exists(DB_PATH):
        print("[ERROR] Database not found. Run init_db.py first.")
        sys.exit(1)

    sync_task()