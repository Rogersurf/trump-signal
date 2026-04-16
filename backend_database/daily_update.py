"""Daily sync script for Trump Truth Social posts.
Fetches new data, updates SQLite, and refreshes ChromaDB vector index.
"""
import sqlite3
import pandas as pd
import sys
import os
from datetime import datetime
from datasets import load_dataset
from apscheduler.schedulers.background import BackgroundScheduler

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_database.embeddings import PostSearchEngine
from backend_database.init_db import DEFAULT_DB_PATH

HF_REPO = "chrissoria/trump-truth-social"


def sync_task():
    """Fetch latest data, update SQLite, and rebuild ChromaDB index."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Triggering daily sync...")

    try:
        # 1. Fetch latest dataset from Hugging Face
        print("Fetching latest data from Hugging Face...")
        dataset = load_dataset(HF_REPO)
        df_new = dataset['train'].to_pandas()
        df_new['date'] = pd.to_datetime(df_new['date']).dt.strftime('%Y-%m-%d %H:%M:%S')

        # 2. Update SQLite (replace entire table for simplicity)
        print(f"Updating SQLite database at {DEFAULT_DB_PATH}...")
        with sqlite3.connect(DEFAULT_DB_PATH) as conn:
            df_new.to_sql("truth_social", conn, if_exists="replace", index=False)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON truth_social (date)")

        # 3. Rebuild ChromaDB index (force rebuild after full refresh)
        print("Rebuilding ChromaDB vector index...")
        engine = PostSearchEngine(DEFAULT_DB_PATH)
        engine.build_index(force=True)

        print(f"[{now}] Sync successful. Record count: {len(df_new)}")

    except Exception as e:
        print(f"[{now}] Sync error: {e}")


def activate():
    """Activate the daily sync scheduler."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_task, 'cron', hour=2, minute=0)
    print(f"Update scheduler started [Target: {DEFAULT_DB_PATH}]")
    print("Running in background...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == "__main__":
    # Check if database exists (should be created by init_db.py)
    if not os.path.exists(DEFAULT_DB_PATH):
        print(f"Error: Database not found at {DEFAULT_DB_PATH}. Run init_db.py first.")
        sys.exit(1)

    # One-off mode for CI/CD or manual execution
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        sync_task()
        print("One‑off sync completed. Exiting.")
        sys.exit(0)
    sync_task()
    # Scheduler mode (runs daily at 02:00)
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_task, 'cron', hour=2, minute=0)
    print(f"Update scheduler started [Target: {DEFAULT_DB_PATH}]")
    print("Running in background...")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")