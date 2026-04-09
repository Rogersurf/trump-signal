FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000 8501

CMD uvicorn app.api.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0