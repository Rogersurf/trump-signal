import sqlite3
import pandas as pd
import sys
from datetime import datetime
from datasets import load_dataset
from apscheduler.schedulers.blocking import BlockingScheduler
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "trump_data.db")
HF_REPO = "chrissoria/trump-truth-social"


def sync_task():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Triggering daily sync...")

    try:
        # Fetch latest data
        dataset = load_dataset(HF_REPO)
        df_new = dataset['train'].to_pandas()
        df_new['date'] = pd.to_datetime(df_new['date']).dt.strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DB_PATH) as conn:
            # Strategy: replace local table.
            # For very large datasets, consider "INSERT OR IGNORE" for true incremental updates.
            df_new.to_sql("truth_social", conn, if_exists="replace", index=False)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON truth_social (date)")

        print(f"[{now}] Sync successful. Record count: {len(df_new)}")
    except Exception as e:
        print(f"[{now}] Sync error: {e}")


if __name__ == "__main__":
    # Check if database was created by init_db.py
    if not os.path.exists(DB_PATH):
        print("Error: Database file not found. Please run 'python init_db.py' first.")
        exit(1)

    # One-off mode for CI/CD
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        sync_task()
        print("One‑off sync completed. Exiting.")
        exit(0)

    # Scheduler mode (original behavior)
    scheduler = BlockingScheduler()

    # Run daily at 02:00
    scheduler.add_job(sync_task, 'cron', hour=2, minute=0)

    print(f"Update scheduler started [Target: {DB_PATH}]")
    print("Running in background...")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")