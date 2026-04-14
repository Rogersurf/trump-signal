#!/bin/bash
set -e

# Start FastAPI in background
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on the public port
exec streamlit run frontend/streamlitapp.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.enableXsrfProtection false \
    --server.enableCORS false