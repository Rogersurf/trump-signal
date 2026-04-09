import os
from huggingface_hub import hf_hub_download

DB_PATH = "data/trump_pulse.db"

def ensure_database():
    """Download the versioned SQLite database from Hugging Face if missing."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DB_PATH):
        print("Downloading trump_pulse.db from Hugging Face Dataset...")
        hf_hub_download(
            repo_id="Rogersurf/trump_pulse_data",
            filename="trump_pulse.db",
            local_dir="data/",
            repo_type="dataset",
            revision="main"
        )
        print("Database downloaded successfully.")
    else:
        print("Database already exists locally.")
    return DB_PATH