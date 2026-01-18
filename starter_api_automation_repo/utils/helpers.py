import json
from pathlib import Path

def load_config(path: str = "config/config.json") -> dict:
    return json.loads(Path(path).read_text())

def format_url(base_url: str, endpoint: str, **kwargs) -> str:
    return base_url.rstrip("/") + endpoint.format(**kwargs)
