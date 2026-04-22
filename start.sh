#!/bin/bash
set -e

echo "[start.sh] Preparing environment..."

export TRUMPPULSE_DATA_DIR=/data
export HF_HOME=/data/.huggingface
export DB_PATH=/data/trump_pulse/trump_data.db

mkdir -p /data/trump_pulse
mkdir -p $HF_HOME

echo "[start.sh] DB_PATH=$DB_PATH"

# ---------------------------
# DOWNLOAD DB
# ---------------------------
if [ ! -f "$DB_PATH" ]; then
    echo "[start.sh] Downloading DB..."
    wget -q https://huggingface.co/datasets/Rogersurf/trump-signal-data/resolve/main/trump_data.db -O "$DB_PATH"
else
    echo "[start.sh] DB already exists."
fi

# ---------------------------
# START FASTAPI (background)
# ---------------------------
echo "[start.sh] Starting FastAPI..."
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

# ---------------------------
# WAIT API (robust)
# ---------------------------
echo "[start.sh] Waiting for API..."

for i in {1..30}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null; then
        echo "[start.sh] API ready!"
        break
    fi
    sleep 2
done

# ❌ REMOVE DEBUG CURLS (important)

# ---------------------------
# START STREAMLIT (MAIN PROCESS)
# ---------------------------
echo "[start.sh] Starting Streamlit..."

exec streamlit run frontend/streamlitapp.py \
    --server.port 7860 \
    --server.address 0.0.0.0