import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.getenv(
    "DB_PATH",
    f"{BASE_DIR}/../../trump_data.db"
)

MODEL_DIR = os.getenv(
    "MODEL_DIR",
    f"{BASE_DIR}/../../backend/model_artifacts"
)