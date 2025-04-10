import json
import requests
from datetime import datetime
import socket

AUDIT_ENDPOINT = "http://localhost:5050/audit"

def log_event(event_type, user_id, detail=None):
    payload = {
        "event": event_type,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hostname": socket.gethostname(),
        "detail": detail or {}
    }
    try:
        r = requests.post(AUDIT_ENDPOINT, json=payload, timeout=5)
        return r.ok
    except Exception:
        return False
