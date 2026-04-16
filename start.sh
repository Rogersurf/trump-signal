#!/bin/bash
set -e

echo "[start.sh] Starting FastAPI..."

uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

# WAIT UNTIL API IS ACTUALLY READY
echo "[start.sh] Waiting for API to be ready..."

for i in {1..30}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null; then
        echo "[start.sh] API is ready!"
        break
    fi
    echo "[start.sh] API not ready yet... retrying"
    sleep 2
done

echo "[start.sh] Starting Streamlit..."

streamlit run frontend/streamlitapp.py \
    --server.port 7860 \
    --server.address 0.0.0.0