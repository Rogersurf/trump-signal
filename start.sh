#!/bin/bash
set -e

# ----------------------------------------------------------------------
# 1. Background updater (if it exists)
# ----------------------------------------------------------------------
if [ -f "backend_database/background_update.py" ]; then
    echo "[start.sh] Starting background updater..."
    python backend_database/background_update.py &
fi

# ----------------------------------------------------------------------
# 2. FastAPI backend (internal only – port 8000)
# ----------------------------------------------------------------------
echo "[start.sh] Starting FastAPI on port 8000..."
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

# ----------------------------------------------------------------------
# 3. Wait for FastAPI health endpoint
# ----------------------------------------------------------------------
echo "[start.sh] Waiting for API to be ready..."
max_retries=30
counter=0
while ! curl -s -f http://localhost:8000/health > /dev/null 2>&1; do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge $max_retries ]; then
        echo "[start.sh] ERROR: FastAPI failed to start after $max_retries seconds"
        exit 1
    fi
done
echo "[start.sh] FastAPI is healthy."

# ----------------------------------------------------------------------
# 4. Streamlit frontend (internal only – port 8501)
# ----------------------------------------------------------------------
echo "[start.sh] Starting Streamlit on port 8501..."
streamlit run frontend/streamlitapp.py --server.port 8501 --server.address 0.0.0.0 &

# ----------------------------------------------------------------------
# 5. Proxy (public port 7860) – routes /api → FastAPI, everything else → Streamlit
# ----------------------------------------------------------------------
echo "[start.sh] Starting proxy on port 7860..."
exec uvicorn proxy:app --host 0.0.0.0 --port 7860