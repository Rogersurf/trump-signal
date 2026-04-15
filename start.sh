#!/bin/bash
set -e

# Start background updater (optional)
if [ -f "backend_database/background_update.py" ]; then
    echo "[start.sh] Starting background updater..."
    python backend_database/background_update.py &
fi

# Start FastAPI
echo "[start.sh] Starting FastAPI on port 8000..."
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit
echo "[start.sh] Starting Streamlit on port 8501..."
streamlit run frontend/streamlitapp.py --server.port 8501 --server.address 0.0.0.0 &

# Wait for services to be ready
sleep 5

# Start Nginx (runs in foreground)
echo "[start.sh] Starting Nginx on port 7860..."
exec nginx -g "daemon off;"