FROM python:3.12

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ENV (🔥 CRÍTICO)
ENV HF_HOME=/data/.huggingface
ENV TRUMPPULSE_DATA_DIR=/data/trump_pulse
ENV CHROMA_DB_PATH=/data/chroma_db
ENV DB_PATH=/data/trump_pulse/trump_data.db

# Create dirs
RUN mkdir -p $TRUMPPULSE_DATA_DIR $CHROMA_DB_PATH

# Install deps
COPY requirements.txt .

RUN pip install --no-cache-dir torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .
RUN pip install -e .

# Init DB
RUN python backend_database/init_db.py --db-path $DB_PATH

# 🔥 DEBUG (pra nunca mais ficar cego)
RUN ls -lh /data/trump_pulse

# ⚠️ TREINO OPCIONAL (melhor tirar depois)
RUN python backend/model_training.py \
    --data-dir $TRUMPPULSE_DATA_DIR \
    --db-path $DB_PATH \
    --chroma-db-path $CHROMA_DB_PATH

# Start
RUN chmod +x start.sh

EXPOSE 7860

CMD ["bash", "start.sh"]