"""
Daily sync script for Trump Truth Social posts.
Fetches new data, updates SQLite, and refreshes ChromaDB vector index.
"""

import logging
import os
import sqlite3
import sys
import time

import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from datasets import load_dataset

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_database.embeddings import PostSearchEngine
from backend_database.init_db import DEFAULT_DB_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

HF_REPO = "chrissoria/trump-truth-social"


# ─────────────────────────────────────────────
# SYNC TASK
# ──────────��──────────────────────────────────
def sync_task() -> None:
    log.info("Sync started.")

    try:
        # 1. Fetch latest dataset from Hugging Face
        log.info("Fetching from %s ...", HF_REPO)
        dataset = load_dataset(HF_REPO)
        df_new  = dataset["train"].to_pandas()
        df_new["date"] = pd.to_datetime(df_new["date"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        log.info("Fetched %d records.", len(df_new))

        # 2. Update SQLite
        log.info("Updating SQLite at %s ...", DEFAULT_DB_PATH)
        with sqlite3.connect(DEFAULT_DB_PATH) as conn:
            df_new.to_sql("truth_social", conn, if_exists="replace", index=False)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON truth_social (date)")
        log.info("SQLite updated.")

        # 3. Rebuild ChromaDB vector index
        log.info("Rebuilding ChromaDB index ...")
        engine = PostSearchEngine(DEFAULT_DB_PATH)
        engine.build_index(force=True)

        log.info("Sync completed. Records: %d", len(df_new))

    except Exception:
        log.exception("Sync failed.")


# ───────────────────────────��─────────────────
if __name__ == "__main__":
    if not os.path.exists(DEFAULT_DB_PATH):
        log.error("Database not found at %s. Run init_db.py first.", DEFAULT_DB_PATH)
        sys.exit(1)

    # One-off mode: python sync.py --once
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        sync_task()
        log.info("One-off sync completed. Exiting.")
        sys.exit(0)

    # Scheduler mode: runs daily at midnight UTC
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_task, "cron", hour=0, minute=0)
    scheduler.start()
    log.info("Scheduler started. Daily sync at 00:00 UTC. Target: %s", DEFAULT_DB_PATH)

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        log.info("Scheduler stopped.")