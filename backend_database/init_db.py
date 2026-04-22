import os
import json
import shutil
from datetime import datetime
from huggingface_hub import hf_hub_download, upload_file

# ==============================
# LOAD CONFIG
# ==============================
CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "config", "config_data.json")
)

print("CONFIG_PATH:", CONFIG_PATH)

with open(CONFIG_PATH) as f:
    config = json.load(f)

HF_DB_REPO = config["hf_db_repo"].replace(
    "https://huggingface.co/datasets/", ""
)

HF_FILENAME_LATEST = "trump_data_latest.db"


# ==============================
# PATH RESOLUTION (SAFE & DYNAMIC)
# ==============================
def resolve_db_path():
    """
    Single source of truth for DB path.
    Works for:
    - HF Spaces
    - Local dev
    """

    # 1️⃣ Priority: explicit env
    env_path = os.environ.get("DB_PATH")
    if env_path:
        print(f"[DB INIT] Using DB_PATH from env: {env_path}")
        return env_path

    # 2️⃣ HF / Docker persistent volume
    data_dir = os.environ.get("TRUMPPULSE_DATA_DIR")
    if data_dir:
        path = os.path.join(data_dir, "trump_data.db")
        print(f"[DB INIT] Using TRUMPPULSE_DATA_DIR: {path}")
        return path

    # 3️⃣ Local fallback
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "trump_data.db")
    print(f"[DB INIT] Using local fallback: {path}")
    return path


DB_PATH = os.path.abspath(resolve_db_path())

# ensure directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

DEFAULT_DB_PATH = DB_PATH

print(f"[DB INIT] FINAL DB_PATH: {DEFAULT_DB_PATH}")


# ==============================
# FILE NAMING
# ==============================
def generate_versioned_filename():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    return f"trump_data_{timestamp}.db"


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

        shutil.copy(file_path, DEFAULT_DB_PATH)

        print("✅ Loaded DB from HF (latest)")
        return True

    except Exception as e:
        print("⚠️ HF download failed:", e)
        return False


# ==============================
# DOWNLOAD FROM SOURCE DATASET
# ==============================
def download_from_chrissoria():
    try:
        print("📥 Downloading dataset from chrissoria...")

        file_path = hf_hub_download(
            repo_id="chrissoria/trump-truth-social",
            filename="data/train-00000-of-00001.parquet",
            repo_type="dataset"
        )

        import pandas as pd
        import sqlite3

        df = pd.read_parquet(file_path)

        conn = sqlite3.connect(DEFAULT_DB_PATH)
        df.to_sql("truth_social", conn, if_exists="replace", index=False)
        conn.close()

        print("✅ DB created from dataset")

    except Exception as e:
        print("❌ Failed to build DB:", e)
        raise


# ==============================
# UPLOAD TO HF
# ==============================
def upload_to_hf():
    try:
        print("📤 Uploading DB to HF...")

        versioned_name = generate_versioned_filename()

        upload_file(
            path_or_fileobj=DEFAULT_DB_PATH,
            path_in_repo=versioned_name,
            repo_id=HF_DB_REPO,
            repo_type="dataset"
        )

        upload_file(
            path_or_fileobj=DEFAULT_DB_PATH,
            path_in_repo=HF_FILENAME_LATEST,
            repo_id=HF_DB_REPO,
            repo_type="dataset"
        )

        print(f"✅ Uploaded as {versioned_name} + latest")

    except Exception as e:
        print("⚠️ Upload failed:", e)


# ==============================
# INIT DB
# ==============================
def init_db():
    print("🚀 Initializing database...")

    # 1️⃣ already exists
    if os.path.exists(DEFAULT_DB_PATH):
        print("✅ Using local DB")
        return DEFAULT_DB_PATH

    # 2️⃣ try HF
    if download_from_hf():
        return DEFAULT_DB_PATH

    # 3️⃣ fallback → build
    download_from_chrissoria()

    # 4️⃣ upload
    upload_to_hf()

    return DEFAULT_DB_PATH


if __name__ == "__main__":
    path = init_db()
    print(f"✅ DB initialized at: {path}")