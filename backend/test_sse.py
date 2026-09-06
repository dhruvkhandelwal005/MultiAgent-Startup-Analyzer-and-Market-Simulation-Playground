import httpx
import json

url = "http://127.0.0.1:8000/simulations/1/events/stream"
payload = {"event_type": "general", "current_event": "Test SSE: new feature request from users."}

with httpx.stream("POST", url, json=payload, timeout=120) as response:
    for line in response.iter_lines():
        if line.startswith("data: "):
            data = json.loads(line[6:])
            print(data)