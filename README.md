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
# TrumpSignal 📊
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
An MLOps pipeline that ingests Trump's Truth Social posts and generates market impact signals.
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
> **Disclaimer:** This project was developed solely for academic purposes as part of the Data Engineering and Machine Learning Operations in Business course at Aalborg University. It is not affiliated with, endorsed by, or intended to influence any political party, candidate, or movement. The analysis is purely technical and should not be interpreted as political commentary or financial advice.
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
---
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
## What it does
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
- Ingests Trump's Truth Social posts daily from HuggingFace
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
- Classifies posts by category (threatening, self-promotion, attacking, etc.)
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
- Predicts whether the next trading day will be high or low market impact
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
- Shows real-time stock price movements around each post
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
- Provides semantic search over all posts by topic
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
---
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
## Live Demo
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
[https://huggingface.co/spaces/Ailee52/trump-signal](https://huggingface.co/spaces/Ailee52/trump-signal)
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
---
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
## Pipeline
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
| Step | Component | Description |
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
|---|---|---|
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
| 1 | HuggingFace Dataset | Source of Trump's Truth Social posts |
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
| 2 | SQLite Database | Local storage, DVC tracked |
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
| 3 | Embeddings Cache | MiniLM-L6-v2 vectors for semantic search |
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
| 4 | XGBoost Classifier | Predicts next-day market impact |
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
| 5 | FastAPI | Serves predictions and search via API |
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
| 6 | Streamlit | Interactive frontend on port 7860 |
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
---
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
## Tech Stack
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
| Layer | Technology |
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
|---|---|
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
| Data | HuggingFace Datasets, SQLite, DVC |
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
| ML | XGBoost, scikit-learn, sentence-transformers |
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
| API | FastAPI, uvicorn |
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
| Frontend | Streamlit |
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
| Deployment | Docker, HuggingFace Spaces |
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
| Scheduling | APScheduler, GitHub Actions |
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
---
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
## Run Locally
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
**Requirements:** Docker
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
```bash
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
# Clone
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
git clone https://github.com/Rogersurf/trump-signal
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
cd trump-signal
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
# Build and run
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
docker build -t trump-signal .
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
docker run -p 8000:8000 -p 7860:7860 trump-signal
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
```
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
- Frontend: http://localhost:7860
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
- API docs: http://localhost:8000/docs
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
---
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
## Run without Docker
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
```bash
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
pip install -r requirements.txt
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
pip install -e .
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
# Terminal 1 — API
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
python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000
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
# Terminal 2 — Frontend
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
python -m streamlit run frontend/streamlitapp.py
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
```
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
---
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
## Project Structure
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
trump-signal/
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
├── app/api/          # FastAPI endpoints
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
├── backend/          # ML training and inference
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
├── backend_database/ # Data ingestion and SQLite
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
├── frontend/         # Streamlit pages
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
├── tests/            # Unit tests
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
├── Dockerfile        # Container setup
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
└── requirements.txt
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
---
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
## Dataset
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
[chrissoria/trump-truth-social](https://huggingface.co/datasets/chrissoria/trump-truth-social) — updated daily, includes post categories, engagement metrics, stock price snapshots, and GDELT global event indicators.
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
---
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
## Team
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
- Rogerio Braunschweiger De Freitas Lima
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
- Chenhao Lou  
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
- Suchanya Baiyam (Ailee)
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
MSc Economics and Business Administration (Business Data Science)  
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
Aalborg University, 2026
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
