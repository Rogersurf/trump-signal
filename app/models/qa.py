def simple_qa(query, texts):
    query = query.lower()

    results = []
    for t in texts:
        if any(word in t.lower() for word in query.split()):
            results.append(t)

    return results[:3]