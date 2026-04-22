#!/bin/bash
set -e

echo "[start.sh] Preparing environment..."

# 🔥 ENV PRIMEIRO
export TRUMPPULSE_DATA_DIR=/data
export HF_HOME=/data/.huggingface

# 🔥 DEFINE DB_PATH CORRETAMENTE (AQUI ESTÁ O BUG)
export DB_PATH=/data/trump_pulse/trump_data.db

# 🔥 CRIA PASTA CERTA
mkdir -p /data/trump_pulse
mkdir -p $HF_HOME

echo "[start.sh] DB_PATH=$DB_PATH"