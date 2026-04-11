"""Initialize the SQLite database with Trump Truth Social posts (all columns)."""
import sqlite3
import pandas as pd
from datasets import load_dataset
import os
import argparse

HF_REPO = "chrissoria/trump-truth-social"

# Default database location – always inside backend_database/ unless overridden
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.environ.get("TRUMPPULSE_DATA_DIR")
if _DATA_DIR:
    DEFAULT_DB_PATH = os.path.join(_DATA_DIR, "trump_data.db")
else:
    DEFAULT_DB_PATH = os.path.join(_BASE_DIR, "trump_data.db")


def initialize(db_path: str = None):
    """
    Download full dataset and create SQLite database.
    If db_path is provided, it is used exactly. Otherwise, the location is determined
    by TRUMPPULSE_DATA_DIR or the default backend_database/ directory.
    """
    if db_path is None:
        data_dir = os.environ.get("TRUMPPULSE_DATA_DIR")
        if data_dir:
            db_path = os.path.join(data_dir, "trump_data.db")
        else:
            db_path = DEFAULT_DB_PATH

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    if os.path.exists(db_path):
        print(f"Database {db_path} already exists. Skipping initialization.")
        return

    print("--- Starting first-time initialization ---")
    print(f"Downloading full dataset from Hugging Face: {HF_REPO}...")

    dataset = load_dataset(HF_REPO)
    df = dataset['train'].to_pandas()

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')

    print(f"Writing {len(df)} records with {len(df.columns)} columns to {db_path}...")
    with sqlite3.connect(db_path) as conn:
        df.to_sql("truth_social", conn, if_exists="replace", index=False)
        if 'date' in df.columns:
            conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON truth_social (date)")
        if 'post_id' in df.columns:
            conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_post_id ON truth_social (post_id)")

    print("--- Initialization successful! ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", default=None)
    args = parser.parse_args()
    initialize(args.db_path)