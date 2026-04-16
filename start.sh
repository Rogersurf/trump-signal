#!/bin/bash
set -e

echo "[start.sh] Starting Streamlit on port 7860..."

streamlit run frontend/streamlitapp.py \
    --server.port 7860 \
    --server.address 0.0.0.0