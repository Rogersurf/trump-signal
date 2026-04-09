"""Prometheus metrics endpoint for monitoring."""
import time
from fastapi import APIRouter, Response
from app.utils import DB_PATH
import os
import json

router = APIRouter()

# In-memory counters (reset on restart)
request_counts = {
    "sentiment_requests": 0,
    "qa_requests": 0,
    "pipeline_triggers": 0
}

def increment_counter(endpoint: str):
    if endpoint in request_counts:
        request_counts[endpoint] += 1

@router.get("/metrics")
def get_metrics():
    """Expose Prometheus-formatted metrics."""
    lines = []
    
    # Request counters
    for name, value in request_counts.items():
        lines.append(f"trump_pulse_{name}_total {value}")
    
    # Database file size
    if os.path.exists(DB_PATH):
        size_bytes = os.path.getsize(DB_PATH)
        lines.append(f"trump_pulse_db_size_bytes {size_bytes}")
    
    # Pipeline status from status.json
    status_path = "artifacts/status.json"
    if os.path.exists(status_path):
        with open(status_path, "r") as f:
            status = json.load(f)
        for step, state in status.items():
            value = 1 if state == "ok" else 0
            lines.append(f'trump_pulse_step_status{{step="{step}"}} {value}')
    
    # Return in Prometheus text format
    return Response(content="\n".join(lines), media_type="text/plain")