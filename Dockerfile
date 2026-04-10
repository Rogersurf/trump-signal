# Use Python 3.10 as base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Initialize the SQLite database with real data
RUN python backend_database/init_db.py

# Expose ports for FastAPI (8000) and Streamlit (7860)
EXPOSE 8000 7860

# Start both services
CMD ["sh", "-c", "uvicorn app.api.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlitapp.py --server.port 7860 --server.address 0.0.0.0"]