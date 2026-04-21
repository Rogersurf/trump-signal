from huggingface_hub import HfApi
import os

api = HfApi()

REPO_ID = "Rogersurf/trump-signal-data"

files_to_upload = [
    "trump_data.db",
    "backend/model_artifacts/xgb_model.pkl",
    "backend/model_artifacts/scaler.pkl",
    "backend/model_artifacts/feature_cols.json",
    "backend/model_artifacts/metrics.json",
]

for file in files_to_upload:
    if os.path.exists(file):
        print(f"Uploading {file}...")

        api.upload_file(
            path_or_fileobj=file,
            path_in_repo=os.path.basename(file),
            repo_id=REPO_ID,
            repo_type="dataset",
        )
    else:
        print(f"⚠️ Missing file: {file}")