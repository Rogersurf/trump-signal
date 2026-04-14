import httpx
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response

app = FastAPI()

STREAMLIT_URL = "http://127.0.0.1:8501"
API_URL = "http://127.0.0.1:8000"


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def http_proxy(request: Request, path: str):
    """Proxy HTTP requests."""
    target = f"{API_URL}/{path}" if path.startswith("api/") else f"{STREAMLIT_URL}/{path}"

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


@app.websocket("/{path:path}")
async def websocket_proxy(websocket: WebSocket, path: str):
    """Proxy WebSocket connections (needed for Streamlit)."""
    await websocket.accept()

    target = f"{API_URL}/{path}" if path.startswith("api/") else f"{STREAMLIT_URL}/{path}"
    # Convert http:// to ws://
    target_ws = target.replace("http://", "ws://")

    async with httpx.AsyncClient() as client:
        async with client.stream("GET", target_ws, headers={"Connection": "upgrade", "Upgrade": "websocket"}) as upstream:
            async def forward_to_upstream():
                try:
                    while True:
                        data = await websocket.receive_text()
                        await upstream.write(data.encode())
                except WebSocketDisconnect:
                    pass

            async def forward_to_client():
                async for chunk in upstream.aiter_bytes():
                    await websocket.send_bytes(chunk)

            import asyncio
            await asyncio.gather(forward_to_upstream(), forward_to_client())