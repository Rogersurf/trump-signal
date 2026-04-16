#!/usr/bin/env bash
set -e

echo "[start.sh] Starting services..."

uvicorn app.api.main:app \
  --host 0.0.0.0 \
  --port 8000 &

streamlit run frontend/streamlitapp.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true &

echo "[start.sh] Waiting for Streamlit..."
until curl -s http://localhost:8501/_stcore/health > /dev/null; do
  sleep 2
done

echo "[start.sh] Waiting for API..."
until curl -s http://localhost:8000/health > /dev/null; do
  sleep 2
done

echo "[start.sh] Starting nginx..."
exec nginx -g "daemon off;"