---
title: TrumpSignal
emoji: 📊
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
---

# TrumpSignal 📊

An MLOps pipeline that ingests Trump's Truth Social posts and generates market impact signals.

> **Disclaimer:** This project was developed solely for academic purposes as part of the Data Engineering and Machine Learning Operations in Business course at Aalborg University. It is not affiliated with, endorsed by, or intended to influence any political party, candidate, or movement. The analysis is purely technical and should not be interpreted as political commentary or financial advice.

---

## What it does

- Ingests Trump's Truth Social posts daily from HuggingFace
- Classifies posts by category (threatening, self-promotion, attacking, etc.)
- Predicts whether the next trading day will be high or low market impact
- Shows real-time stock price movements around each post
- Provides semantic search over all posts by topic

---

## Live Demo

[https://huggingface.co/spaces/Ailee52/trump-signal](https://huggingface.co/spaces/Ailee52/trump-signal)

---

## Pipeline

| Step | Component | Description |
|---|---|---|
| 1 | HuggingFace Dataset | Source of Trump's Truth Social posts |
| 2 | SQLite Database | Local storage, DVC tracked |
| 3 | Embeddings Cache | MiniLM-L6-v2 vectors for semantic search |
| 4 | XGBoost Classifier | Predicts next-day market impact |
| 5 | FastAPI | Serves predictions and search via API |
| 6 | Streamlit | Interactive frontend on port 7860 |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data | HuggingFace Datasets, SQLite, DVC |
| ML | XGBoost, scikit-learn, sentence-transformers |
| API | FastAPI, uvicorn |
| Frontend | Streamlit |
| Deployment | Docker, HuggingFace Spaces |
| Scheduling | APScheduler, GitHub Actions |

---

## Run Locally

**Requirements:** Docker

```bash
# Clone
git clone https://github.com/Rogersurf/trump-signal
cd trump-signal

# Build and run
docker build -t trump-signal .
docker run -p 8000:8000 -p 7860:7860 trump-signal
```

- Frontend: http://localhost:7860
- API docs: http://localhost:8000/docs

---

## Run without Docker

```bash
pip install -r requirements.txt
pip install -e .

# Terminal 1 — API
python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000

# Terminal 2 — Frontend
python -m streamlit run frontend/streamlitapp.py
```

---

## Project Structure
trump-signal/
├── app/api/          # FastAPI endpoints
├── backend/          # ML training and inference
├── backend_database/ # Data ingestion and SQLite
├── frontend/         # Streamlit pages
├── tests/            # Unit tests
├── Dockerfile        # Container setup
└── requirements.txt
---

## Dataset

[chrissoria/trump-truth-social](https://huggingface.co/datasets/chrissoria/trump-truth-social) — updated daily, includes post categories, engagement metrics, stock price snapshots, and GDELT global event indicators.

---

## Team

- Rogerio Braunschweiger De Freitas Lima
- Chenhao Lou  
- Suchanya Baiyam (Ailee)

MSc Economics and Business Administration (Business Data Science)  
Aalborg University, 2026
