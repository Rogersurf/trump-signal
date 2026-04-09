# Use Python 3.10 as base image (standard, not slim)
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the SQLite database is downloaded from Hugging Face Dataset
# This runs during image build so the container starts with data ready
RUN python -c "from app.utils import ensure_database; ensure_database()"

# Expose ports for FastAPI (8000) and Streamlit (7860)
EXPOSE 8000 7860

# Start both services in parallel
CMD uvicorn app.api.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run frontend/streamlitapp.py --server.port 7860 --server.address 0.0.0.0