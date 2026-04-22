#!/bin/bash
set -e

echo "[start.sh] Preparing environment..."

# 🔥 ENV PRIMEIRO (ANTES DE TUDO)
export TRUMPPULSE_DATA_DIR=/data
export HF_HOME=/data/.huggingface

mkdir -p $TRUMPPULSE_DATA_DIR
mkdir -p $HF_HOME

# DB path
echo "[start.sh] DB_PATH=$DB_PATH"

# ---------------------------
# DOWNLOAD DB (se não existir)
# ---------------------------
if [ ! -f "$DB_PATH" ]; then
    echo "[start.sh] Downloading DB..."
    wget -q https://huggingface.co/datasets/Rogersurf/trump-signal-data/resolve/main/trump_data.db -O "$DB_PATH"
else
    echo "[start.sh] DB already exists."
fi

# ---------------------------
# START FASTAPI
# ---------------------------
echo "[start.sh] Starting FastAPI..."

uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

# ---------------------------
# WAIT API
# ---------------------------
echo "[start.sh] Waiting for API..."

for i in {1..30}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null; then
        echo "[start.sh] API ready!"
        break
    fi
    echo "[start.sh] retry $i/30"
    sleep 2
done

# ---------------------------
# DEBUG TESTS
# ---------------------------
echo "[start.sh] Testing endpoints..."

curl -s http://127.0.0.1:8000/health || true
curl -s "http://127.0.0.1:8000/data/max_date" || true
curl -s "http://127.0.0.1:8000/posts?start_date=2024-01-01&end_date=2024-01-02" || true

# ---------------------------
# START STREAMLIT
# ---------------------------
echo "[start.sh] Starting Streamlit..."

streamlit run frontend/streamlitapp.py \
    --server.port 7860 \
    --server.address 0.0.0.0