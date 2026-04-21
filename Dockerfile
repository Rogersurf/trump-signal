FROM python:3.12

WORKDIR /app

# ─────────────────────────────────────
# System deps
# ─────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────
# ENV
# ─────────────────────────────────────
ENV HF_HOME=/data/.huggingface
ENV TRUMPPULSE_DATA_DIR=/data/trump_pulse
ENV CHROMA_DB_PATH=/data/chroma_db
ENV DB_PATH=/data/trump_pulse/trump_data.db

# ─────────────────────────────────────
# Create dirs
# ─────────────────────────────────────
RUN mkdir -p $TRUMPPULSE_DATA_DIR $CHROMA_DB_PATH

# ─────────────────────────────────────
# Install deps
# ─────────────────────────────────────
COPY requirements.txt .

RUN pip install --no-cache-dir torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────
# Copy code
# ─────────────────────────────────────
COPY . .
RUN pip install -e .

# ─────────────────────────────────────
# Start script
# ─────────────────────────────────────
RUN chmod +x start.sh

EXPOSE 7860

CMD ["bash", "start.sh"]