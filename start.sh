#!/usr/bin/env bash
set -e

echo "[start.sh] Starting services..."

# Start FastAPI (background)
uvicorn app.api.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 1 &

# Start Streamlit (background)
streamlit run frontend/streamlitapp.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true &

# Wait for Streamlit to be ready
echo "[start.sh] Waiting for Streamlit..."
until curl -s http://localhost:8501/_stcore/health > /dev/null; do
  sleep 2
done
echo "[start.sh] Streamlit is ready!"

# Wait for API to be ready
echo "[start.sh] Waiting for API..."
until curl -s http://localhost:8000/health > /dev/null; do
  sleep 2
done
echo "[start.sh] API is ready!"

# Start nginx (foreground → keeps container alive)
echo "[start.sh] Starting nginx..."
exec nginx -g "daemon off;"