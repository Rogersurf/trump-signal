#!/bin/bash
set -e

echo "[start.sh] Downloading database if needed..."

# Download DB from HF dataset if not present
if [ ! -f trump_data.db ]; then
    wget https://huggingface.co/datasets/Rogersurf/trump-signal-data/resolve/main/trump_data.db
fi

echo "[start.sh] Starting FastAPI..."

uvicorn app.api.main:app --host 0.0.0.0 --port 7860