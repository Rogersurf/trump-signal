from fastapi import FastAPI
from data.sample import get_sample_data
from app.services.sentiment_service import analyze_dataset
from app.models.qa import simple_qa

app = FastAPI()

texts = get_sample_data()
sentiments = analyze_dataset(texts)


@app.get("/")
def health():
    return {"status": "running"}


@app.get("/sentiments")
def get_sentiments():
    return sentiments


@app.get("/qa")
def qa(query: str):
    return simple_qa(query, texts)