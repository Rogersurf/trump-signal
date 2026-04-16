#!/bin/bash
set -e

uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &
streamlit run frontend/streamlitapp.py --server.port 8501 --server.address 0.0.0.0 &

echo "[start.sh] Waiting for Streamlit to be ready..."
until curl -s http://localhost:8501/_stcore/health > /dev/null 2>&1; do
    sleep 2
done
echo "[start.sh] Streamlit is ready!"

exec nginx -g "daemon off;"
