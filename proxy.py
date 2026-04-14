# proxy.py
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()

STREAMLIT_URL = "http://127.0.0.1:8501"
API_URL = "http://127.0.0.1:8000"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy(request: Request, path: str):
    # Determine target backend
    if path.startswith("api/"):
        target = f"{API_URL}/{path}"
    else:
        target = f"{STREAMLIT_URL}/{path}"

    # Remove hop-by-hop headers
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "content-length")}

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=target,
            headers=headers,
            content=await request.body(),
            follow_redirects=True,
        )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers),
        )