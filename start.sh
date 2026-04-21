#!/bin/bash
set -e

echo "[start.sh] Preparing environment..."

# Ensure DB folder exists
mkdir -p /data/trump_pulse

# Download DB if not exists
if [ ! -f /data/trump_pulse/trump_data.db ]; then
    echo "[start.sh] Downloading DB..."
    wget -O /data/trump_pulse/trump_data.db \
    https://huggingface.co/datasets/Rogersurf/trump-signal-data/resolve/main/trump_data.db
fi

export DB_PATH=/data/trump_pulse/trump_data.db

echo "[start.sh] Starting FastAPI..."

# 🚀 START API (isso faltava)
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

echo "[start.sh] Waiting for API..."

for i in {1..30}; do
    sleep 2
    if curl -s http://127.0.0.1:8000/health > /dev/null; then
        echo "[start.sh] API ready!"
        break
    fi
    echo "[start.sh] retry $i/30"
done

echo "[start.sh] Starting Streamlit..."

streamlit run frontend/streamlitapp.py \
    --server.port 7860 \
    --server.address 0.0.0.0