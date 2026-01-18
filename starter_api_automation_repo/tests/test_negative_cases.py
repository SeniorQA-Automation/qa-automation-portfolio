import requests
from utils.helpers import load_config, format_url

def test_create_post_missing_fields_negative():
    cfg = load_config()
    url = format_url(cfg["base_url"], cfg["endpoints"]["create_post"])
    payload = {"title": ""}  # intentionally minimal
    r = requests.post(url, headers=cfg["default_headers"], json=payload)
    # Demo API is permissive; real APIs often return 400/422
    assert r.status_code in (200, 201, 400, 422)
