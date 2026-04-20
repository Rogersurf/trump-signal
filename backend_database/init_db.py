import os
import json
import requests
from datetime import datetime
from huggingface_hub import hf_hub_download, upload_file
import shutil

# ==============================
# LOAD CONFIG
# ==============================
CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "config", "config_data.json")
)

print("CONFIG_PATH:", CONFIG_PATH)

with open(CONFIG_PATH) as f:
    config = json.load(f)

HF_DB_REPO = config["hf_db_repo"].replace("https://huggingface.co/datasets/", "")
HF_RAW_DATA = config["hf_raw_data"]

# ==============================
# FILE NAMING (NO HARDCODE VERSION)
# ==============================
HF_FILENAME_LATEST = "trump_data_latest.db"

def generate_versioned_filename():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    return f"trump_data_{timestamp}.db"

# ==============================
# PATHS
# ==============================
LOCAL_DB_DIR = os.environ.get("TRUMPPULSE_DATA_DIR", ".")
os.makedirs(LOCAL_DB_DIR, exist_ok=True)

DB_PATH = os.path.join(LOCAL_DB_DIR, "trump_data.db")
DEFAULT_DB_PATH = os.path.abspath(DB_PATH)


# ==============================
# DOWNLOAD FROM HF
# ==============================
def download_from_hf():
    try:
        print("📥 Trying HF latest DB...")
        file_path = hf_hub_download(
            repo_id=HF_DB_REPO,
            filename=HF_FILENAME_LATEST,
            repo_type="dataset"
        )
        shutil.copy(file_path, DB_PATH)
        print("✅ Loaded DB from HF (latest)")
        return True
    except Exception as e:
        print("⚠️ HF download failed:", e)
        return False


# ==============================
# DOWNLOAD FROM CHRISSORIA
# ==============================
def download_from_chrissoria():
    try:
        print("📥 Downloading dataset from chrissoria (HF API)...")

        file_path = hf_hub_download(
            repo_id="chrissoria/trump-truth-social",
            filename="data/train-00000-of-00001.parquet",
            repo_type="dataset"
        )

        print(f"✅ Downloaded: {file_path}")

        import pandas as pd
        import sqlite3

        df = pd.read_parquet(file_path)

        conn = sqlite3.connect(DB_PATH)
        df.to_sql("truth_social", conn, if_exists="replace", index=False)
        conn.close()

        print("✅ DB created from dataset")

    except Exception as e:
        print("❌ Failed:", e)
        raise

    except Exception as e:
        print("❌ Failed to process chrissoria data:", e)
        raise


# ==============================
# UPLOAD TO HF (VERSIONED + LATEST)
# ==============================
def upload_to_hf():
    try:
        print("📤 Uploading DB to HF...")

        versioned_name = generate_versioned_filename()

        # Upload versioned file
        upload_file(
            path_or_fileobj=DB_PATH,
            path_in_repo=versioned_name,
            repo_id=HF_DB_REPO,
            repo_type="dataset"
        )

        # Upload latest (overwrite)
        upload_file(
            path_or_fileobj=DB_PATH,
            path_in_repo=HF_FILENAME_LATEST,
            repo_id=HF_DB_REPO,
            repo_type="dataset"
        )

        print(f"✅ Uploaded as {versioned_name} + latest")

    except Exception as e:
        print("⚠️ Upload failed:", e)


# ==============================
# INIT DB (MAIN ENTRYPOINT)
# ==============================
def init_db():
    print("🚀 Initializing database...")

    # 1. Already exists locally
    if os.path.exists(DB_PATH):
        print("✅ Using local DB")
        return DB_PATH

    # 2. Try HF
    if download_from_hf():
        return DB_PATH

    # 3. Fallback → chrissoria
    download_from_chrissoria()

    # 4. Upload to YOUR HF
    upload_to_hf()

    return DB_PATH

if __name__ == "__main__":
    path = init_db()
    print(f"✅ DB initialized at: {path}")