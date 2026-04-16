FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl nginx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV HF_HOME=/data/.huggingface
ENV TRUMPPULSE_DATA_DIR=/data/trump_pulse
ENV CHROMA_DB_PATH=/data/chroma_db

RUN mkdir -p $TRUMPPULSE_DATA_DIR $CHROMA_DB_PATH

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

# 🔥 Create DB
RUN python backend_database/init_db.py

# 🔥 Populate DB (CRITICAL FIX)
RUN python backend_database/daily_update.py --once

# (optional) remove if slow
# RUN python -m backend.model_training

COPY nginx.conf /etc/nginx/nginx.conf
RUN chmod +x start.sh

EXPOSE 8000
EXPOSE 8501

CMD ["bash", "start.sh"]