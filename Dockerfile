FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for Hugging Face cache and our data
ENV HF_HOME=/data/.huggingface
ENV TRUMPPULSE_DATA_DIR=/data/trump_pulse
ENV CHROMA_DB_PATH=/data/chroma_db

# Create necessary directories
RUN mkdir -p $TRUMPPULSE_DATA_DIR $CHROMA_DB_PATH

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize SQLite database (lightweight, can be on persistent storage or ephemeral)
RUN python backend_database/init_db.py --db-path $TRUMPPULSE_DATA_DIR/trump_data.db

# Build initial embeddings into ChromaDB (only if the collection is empty)
RUN python backend_database/build_embeddings.py

EXPOSE 8000 7860

CMD ["sh", "-c", "rm -rf /data/chroma_db/* && uvicorn app.api.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlitapp.py --server.port 7860 --server.address 0.0.0.0"]