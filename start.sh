#!/bin/bash
set -e

# Activate virtual environment if it exists (local development)
if [ -d "venv" ]; then
    echo "[start.sh] Activating virtual environment..."
    source venv/bin/activate
fi

echo "[start.sh] Starting FastAPI..."
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

# Wait for API to be ready
echo "[start.sh] Waiting for API to be ready..."

MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "[start.sh] API is ready!"
        break
    fi
    echo "[start.sh] API not ready yet... retrying ($((RETRY_COUNT+1))/$MAX_RETRIES)"
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT+1))
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "[start.sh] ERROR: API failed to start after $MAX_RETRIES attempts"
    exit 1
fi

echo "[DEBUG] Testing API..."
curl http://127.0.0.1:8000/health || echo "API FAILED"

echo "[DEBUG] CONFIG CONTENT:"
cat frontend/config.py

echo "[start.sh] Starting Streamlit..."
streamlit run frontend/streamlitapp.py \
    --server.port 7860 \
    --server.address 0.0.0.0