#!/bin/bash
set -e

echo "[start.sh] Preparing environment..."

# DB path garantido
echo "[start.sh] DB_PATH=$DB_PATH"

# Download DB se não existir
if [ ! -f $DB_PATH ]; then
    echo "[start.sh] Downloading DB..."
    wget -q https://huggingface.co/datasets/Rogersurf/trump-signal-data/resolve/main/trump_data.db -O $DB_PATH
fi

echo "[start.sh] Starting FastAPI..."

# Start API em background
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

# Wait API
echo "[start.sh] Waiting for API..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null; then
        echo "[start.sh] API ready!"
        break
    fi
    echo "[start.sh] retry $i/30"
    sleep 2
done

echo "[start.sh] Testing endpoints..."

curl http://127.0.0.1:8000/health
curl "http://127.0.0.1:8000/data/max_date"
curl "http://127.0.0.1:8000/posts?start_date=2024-01-01&end_date=2024-01-02"

echo "[start.sh] Starting Streamlit..."

streamlit run frontend/streamlitapp.py \
    --server.port 7860 \
    --server.address 0.0.0.0