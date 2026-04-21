import requests

API = "https://rogersurf-trump-signal-api-v2.hf.space"

print("POSTS:", requests.get(f"{API}/posts").json())
print("QA:", requests.get(f"{API}/qa", params={"query": "test"}).json())