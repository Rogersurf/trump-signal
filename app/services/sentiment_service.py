from app.models.sentiment import predict_sentiment

def analyze_dataset(texts):
    results = []
    for t in texts:
        results.append(predict_sentiment(t))
    return results