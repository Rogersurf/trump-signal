FROM python:3.12

WORKDIR /app

# Install system dependencies (curl is required for the health check)
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV HF_HOME=/data/.huggingface
ENV TRUMPPULSE_DATA_DIR=/data/trump_pulse
ENV CHROMA_DB_PATH=/data/chroma_db

# Create persistent directories
RUN mkdir -p $TRUMPPULSE_DATA_DIR $CHROMA_DB_PATH

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir 'uvicorn[standard]'

# Copy entire project
COPY . .

# Install the package itself (if setup.py/pyproject.toml exists)
RUN pip install -e .

# Initialize SQLite database
RUN python backend_database/init_db.py --db-path $TRUMPPULSE_DATA_DIR/trump_data.db

# Make the start script executable
RUN chmod +x start.sh

# Only port 7860 is exposed to the public (Hugging Face expects this)
EXPOSE 7860

# Start everything using the script
CMD ["./start.sh"]