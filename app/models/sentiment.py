def predict_sentiment(text):
    text = text.lower()

    positive_words = ["great", "best", "strong", "secure", "respected"]
    negative_words = ["terrible", "weak", "disaster", "failing", "enemy"]

    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return {"label": "POSITIVE", "score": score}
    elif score < 0:
        return {"label": "NEGATIVE", "score": score}
    else:
        return {"label": "NEUTRAL", "score": 0}