import requests
from utils.helpers import load_config, format_url

def test_create_post():
    cfg = load_config()
    url = format_url(cfg["base_url"], cfg["endpoints"]["create_post"])
    payload = cfg["test_data"]["new_post"]
    r = requests.post(url, headers=cfg["default_headers"], json=payload)
    assert r.status_code in (200, 201)
    data = r.json()
    assert "id" in data
    assert data.get("title") == payload["title"]
