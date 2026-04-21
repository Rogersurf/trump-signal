FROM python:3.12

WORKDIR /app

# Install system dependencies including nginx
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV HF_HOME=/data/.huggingface
ENV TRUMPPULSE_DATA_DIR=/data/trump_pulse
ENV CHROMA_DB_PATH=/data/chroma_db

# Create directories
RUN mkdir -p $TRUMPPULSE_DATA_DIR $CHROMA_DB_PATH

# Python dependencies
COPY requirements.txt .
# Install CPU-only torch FIRST
RUN pip install --no-cache-dir torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu

# Then install the rest
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .
RUN pip install -e .

# Initialize database
RUN python backend_database/init_db.py --db-path $TRUMPPULSE_DATA_DIR/trump_data.db

# train the model
RUN python backend/model_training.py --data-dir $TRUMPPULSE_DATA_DIR --db-path $TRUMPPULSE_DATA_DIR/trump_data.db --chroma-db-path $CHROMA_DB_PATH

# Make start script executable
RUN chmod +x start.sh

EXPOSE 7860

CMD ["bash", "start.sh"]

RUN ls -l