# TrumpPulse — MLOps Semester Project

MSc BDS — Data Engineering and Machine Learning Operations in Business  
Aalborg University, 2026

## Group Members

Chenghao Luo  
Suchanya Baiyam  
Rogerio Braunschweiger de Freitas Lima

---

## Project Overview

TrumpPulse is an end-to-end MLOps pipeline that ingests, processes, and analyzes Trump Truth Social posts. The system correlates post content with real-time financial market data and geopolitical signals, enabling users to explore how political rhetoric relates to market behavior.

The primary focus is not model accuracy but the design of a robust, reproducible, and continuously operational MLOps system.

---

## Live Demo

https://huggingface.co/spaces/Ailee52/trump-signal

---

## Pipeline Overview

```
HuggingFace Dataset (32,429 posts)
        |
        v
Data Ingestion (init_db.py)
SQLite database with index on date and post_id
        |
        v
Daily Sync (backgroud_update.py)
APScheduler runs at 00:00 UTC, re-fetches dataset, rebuilds embeddings
        |
        v
Feature Layer (data_api.py)
TrumpDataClient: KPIs, stock series, GDELT trends, category distributions
        |
        v
Model Layer
  Sentiment: pre-labeled in dataset (cardiffnlp/twitter-roberta-base-sentiment)
  Semantic Search: all-MiniLM-L6-v2 embeddings, cosine similarity, pickle cache
  Market Predictor: XGBoost classifier, next-day market impact, TimeSeriesSplit CV
        |
        v
FastAPI (app/api/main.py)
Endpoints: /health /qa /posts /stocks /categories /gdelt /pipeline/status /metrics /feedback
        |
        v
Streamlit Frontend (frontend/streamlitapp.py)
Pages: Feed, Topics, Market, Geopolitical, Q&A, Developer Dashboard
        |
        v
Nginx Reverse Proxy (nginx.conf)
Single port 7860: /api/* to FastAPI (8000), /* to Streamlit (8501)
        |
        v
Docker Container
```

---

## How to Run Locally

**Requirements:** Docker installed on your machine.

Clone the repository:

```bash
git clone https://github.com/Rogersurf/trump-signal
cd trump-signal
```

Build and run:

```bash
docker build -t trump-pulse .
docker run -p 7860:7860 trump-pulse
```

Open in browser: http://localhost:7860

Note: The first build downloads the full dataset from HuggingFace (~32k posts) and builds the embeddings cache. This takes approximately 10 to 20 minutes.

---

## How to Run Without Docker

Install dependencies:

```bash
pip install -e .
pip install -r requirements.txt
```

Initialize the database:

```bash
python backend_database/init_db.py
```

Start FastAPI and Streamlit in two separate terminals:

```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
streamlit run frontend/streamlitapp.py --server.port 8501
```

Open in browser: http://localhost:8501

---

## How to Reproduce Results

The dataset is versioned with DVC. The pointer file is at data/trump_pulse.db.dvc.

To pull the exact dataset version used in this project:

```bash
dvc pull
```

The XGBoost model artifacts are stored in backend/model_artifacts/ and include the trained model, scaler, feature list, and evaluation metrics. To retrain from scratch:

```bash
python -m backend.model_training
```

Model performance on held-out test set (Dec 2025 to Mar 2026):

```
ROC-AUC (test):     0.639
ROC-AUC (CV mean):  0.607
CV std:             0.038
Test samples:       418 days
```

---

## Repository Structure

```
trump-signal/
    app/api/
        main.py               FastAPI application and all endpoints
        monitoring.py         Prometheus metrics endpoint
        soy_trump_rhetoric.py Rhetoric analysis router
    backend/
        model_training.py     XGBoost training pipeline with TimeSeriesSplit
        model_predict.py      Inference functions for latest and specific dates
        model_dashboard.py    Plotly Dash model visualization dashboard
        model_artifacts/      Saved model, scaler, feature list, metrics
    backend_database/
        init_db.py            First-time dataset download and SQLite creation
        daily_update.py       Scheduled daily sync (APScheduler)
        backgroud_update.py   Production background sync process
        embeddings.py         Sentence-transformer embedding cache and search
        build_embeddings.py   Rebuilds and uploads embeddings to HuggingFace
        incremental_embeddings.py  Updates only new posts in embedding cache
        data_api.py           TrumpDataClient: all SQL query functions
    frontend/
        streamlitapp.py       Entry point, routing, sidebar
        _pages/               feed, market, topics, geopolitical, qa, dev
        _data/api_client.py   HTTP client for all FastAPI calls
        _components/          Reusable post_card and charts components
        config.py             API URL, colors, stock options
    tests/                    Unit tests for all pipeline components
    .github/workflows/        Weekly CI/CD data update (Monday 03:00 UTC)
    .dvc/                     DVC configuration for data versioning
    Dockerfile                Single container build with Nginx + FastAPI + Streamlit
    nginx.conf                Reverse proxy routing on port 7860
    start.sh                  Startup script launching all three services
    requirements.txt          Python dependencies
    VERSION                   Current version (1.0.0)
    CHANGELOG.md              Version history
```

---

## Artifact Management

Each pipeline run produces the following artifacts:

Raw data: SQLite database downloaded from HuggingFace, versioned with DVC  
Embeddings: Precomputed pickle cache stored locally and on HuggingFace dataset repo (Rogersurf/trump-pulse-embeddings)  
Model artifacts: xgb_model.pkl, scaler.pkl, feature_cols.json, metrics.json stored in backend/model_artifacts/  
Feedback: User ratings on Q&A results stored in the SQLite feedback table  

---

## Monitoring and Versioning

The /metrics endpoint exposes Prometheus-formatted metrics including request counts per endpoint and database file size.

The /pipeline/status endpoint returns the current state of each pipeline stage including model name, embedding model, dataset version, and last update times.

Model versioning is handled by saving artifacts with fixed filenames in backend/model_artifacts/. Dataset versioning is handled by DVC with a pointer file tracking the SQLite database.

---

## Deployment

The system is deployed on HuggingFace Spaces using Docker (sdk: docker in README frontmatter). Nginx listens on port 7860 and routes traffic to FastAPI on port 8000 and Streamlit on port 8501 within the same container.

GitHub Actions runs a weekly pipeline update every Monday at 03:00 UTC, re-fetching the dataset and syncing the database. The workflow can also be triggered manually via workflow_dispatch.

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| /health | GET | Health check |
| /qa | GET | Semantic search over posts |
| /feedback | POST | Submit rating on Q&A result |
| /posts | GET | Fetch posts by date range |
| /stocks | GET | Stock series data |
| /categories | GET | Category distribution |
| /categories/impact | GET | Market impact per category |
| /gdelt/range | GET | GDELT geopolitical trend data |
| /gdelt/summary | GET | GDELT summary metrics |
| /pipeline/status | GET | Pipeline health and metadata |
| /metrics | GET | Prometheus-formatted metrics |