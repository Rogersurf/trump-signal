"""
Daily sync script for Trump Truth Social posts.

Responsibilities:
- Incrementally update HF dataset (append only new posts)
- Maintain versioned DB + latest alias

This script is intended to be triggered by CI (GitHub Actions).
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime
from datasets import load_dataset
from huggingface_hub import hf_hub_download, upload_file

from backend_database.init_db import DB_PATH, HF_DB_REPO

HF_SOURCE = "chrissoria/trump-truth-social"
HF_FILENAME_LATEST = "trump_data_latest.db"


def sync_task():
    now = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    print(f"[{now}] Starting incremental sync...")

    try:
        # ─────────────────────────────
        # 1. LOAD CURRENT HF DB
        # ─────────────────────────────
        print("[1/5] Loading current HF database...")

        try:
            local_db = hf_hub_download(
                repo_id=HF_DB_REPO,
                filename=HF_FILENAME_LATEST,
                repo_type="dataset"
            )
            print(f"[INFO] Loaded existing DB from HF: {local_db}")
        except Exception:
            print("[WARN] No existing DB found on HF. Starting fresh.")
            local_db = None

        # ─────────────────────────────
        # 2. LOAD EXISTING DATA
        # ─────────────────────────────
        if local_db and os.path.exists(local_db):
            conn = sqlite3.connect(local_db)
            df_old = pd.read_sql("SELECT * FROM truth_social", conn)
            conn.close()
        else:
            df_old = pd.DataFrame()

        old_ids = set(df_old["post_id"]) if not df_old.empty else set()
        print(f"[INFO] Existing posts: {len(old_ids)}")

        # ─────────────────────────────
        # 3. LOAD NEW DATA (chrissoria)
        # ─────────────────────────────
        print("[2/5] Fetching new data from source dataset...")

        dataset = load_dataset(HF_SOURCE)
        df_new = dataset["train"].to_pandas()

        print(f"[INFO] Source dataset rows: {len(df_new)}")

        # ─────────────────────────────
        # 4. FILTER NEW POSTS
        # ─────────────────────────────
        df_new = df_new[~df_new["post_id"].isin(old_ids)]

        print(f"[INFO] New posts detected: {len(df_new)}")

        if df_new.empty:
            print("[INFO] No new data. Exiting.")
            return

        # ─────────────────────────────
        # 5. MERGE DATA
        # ─────────────────────────────
        df_all = pd.concat([df_old, df_new], ignore_index=True)

        print(f"[INFO] Total rows after merge: {len(df_all)}")

        # ─────────────────────────────
        # 6. SAVE LOCAL DB
        # ─────────────────────────────
        print("[3/5] Writing merged database...")

        with sqlite3.connect(DB_PATH) as conn:
            df_all.to_sql("truth_social", conn, if_exists="replace", index=False)

        # ─────────────────────────────
        # 7. UPLOAD TO HF
        # ─────────────────────────────
        print("[4/5] Uploading to Hugging Face...")

        versioned_name = f"trump_data_{now}.db"

        upload_file(
            path_or_fileobj=DB_PATH,
            path_in_repo=versioned_name,
            repo_id=HF_DB_REPO,
            repo_type="dataset"
        )

        upload_file(
            path_or_fileobj=DB_PATH,
            path_in_repo=HF_FILENAME_LATEST,
            repo_id=HF_DB_REPO,
            repo_type="dataset"
        )

        print("[5/5] Upload complete")
        print(f"[SUCCESS] Added {len(df_new)} new posts")

    except Exception as e:
        print(f"[ERROR] Sync failed: {e}")


if __name__ == "__main__":
    sync_task()