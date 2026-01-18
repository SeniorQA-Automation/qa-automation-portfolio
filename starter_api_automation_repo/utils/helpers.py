import json
from pathlib import Path

def load_config():
    # Always resolve config relative to the package folder:
    # starter_api_automation_repo/config/config.json
    package_root = Path(__file__).resolve().parents[1]   # starter_api_automation_repo/
    config_path = package_root / "config" / "config.json"
    return json.loads(config_path.read_text())

def format_url(base_url: str, endpoint: str, **kwargs):
    # Supports endpoints like "/posts/{id}"
    if kwargs:
        endpoint = endpoint.format(**kwargs)
    return base_url.rstrip("/") + "/" + endpoint.lstrip("/")
