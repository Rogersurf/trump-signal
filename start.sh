#!/bin/bash
set -e

echo "[start.sh] Downloading latest artifacts..."

# Clean old
rm -f /data/trump_pulse/trump_data.db

# DB
wget -O /data/trump_pulse/trump_data.db \
https://huggingface.co/datasets/Rogersurf/trump-signal-data/resolve/main/trump_data.db

# Model artifacts
mkdir -p /app/backend/model_artifacts

wget -O /app/backend/model_artifacts/xgb_model.pkl \
https://huggingface.co/datasets/Rogersurf/trump-signal-data/resolve/main/xgb_model.pkl

wget -O /app/backend/model_artifacts/scaler.pkl \
https://huggingface.co/datasets/Rogersurf/trump-signal-data/resolve/main/scaler.pkl

wget -O /app/backend/model_artifacts/feature_cols.json \
https://huggingface.co/datasets/Rogersurf/trump-signal-data/resolve/main/feature_cols.json

echo "[start.sh] Starting FastAPI..."

uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

echo "[start.sh] Waiting for API..."

for i in {1..30}; do
  if curl -s http://127.0.0.1:8000/health > /dev/null; then
    echo "[start.sh] API ready!"
    break
  fi
  sleep 2
done

echo "[start.sh] Starting Streamlit..."

streamlit run frontend/streamlitapp.py \
    --server.port 7860 \
    --server.address 0.0.0.0