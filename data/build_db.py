import sqlite3
import pandas as pd
from datasets import load_dataset
import kagglehub
import os

DB_PATH = "data/trump_pulse.db"

def build_db():
    conn = sqlite3.connect(DB_PATH)
    
    # --- Load Trump Truth Social (from Hugging Face) ---
    print("Loading Trump dataset from Hugging Face...")
    trump_dataset = load_dataset("chrissoria/trump-truth-social", split="train")
    trump_df = trump_dataset.to_pandas()
    trump_df.to_sql("trump_posts", conn, if_exists="replace", index=False)
    print(f"Saved {len(trump_df)} posts to 'trump_posts' table.")
    
    # --- Load Climate/Economic Impact (via kagglehub) ---
    print("Downloading Climate dataset from Kaggle...")
    path = kagglehub.dataset_download("uom190346a/global-climate-events-and-economic-impact-dataset")
    # O dataset pode conter vários arquivos; geralmente há um .csv principal.
    # Vamos listar os arquivos e pegar o primeiro .csv (ou você pode especificar o nome exato)
    files = os.listdir(path)
    csv_files = [f for f in files if f.endswith('.csv')]
    if not csv_files:
        print("No CSV found in downloaded dataset.")
        return
    climate_file = os.path.join(path, csv_files[0])
    print(f"Loading Climate data from: {climate_file}")
    climate_df = pd.read_csv(climate_file)
    climate_df.to_sql("climate_events", conn, if_exists="replace", index=False)
    print(f"Saved {len(climate_df)} events to 'climate_events' table.")
    
    # --- Create Empty Tables for MLOps Artifacts ---
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY,
            post_id TEXT,
            timestamp TEXT,
            sentiment TEXT,
            score REAL,
            model_version TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            metric_name TEXT,
            metric_value REAL
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database built at {DB_PATH}")

if __name__ == "__main__":
    build_db()