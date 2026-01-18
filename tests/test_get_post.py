import requests
from utils.helpers import load_config, format_url

def test_get_post_valid():
    cfg = load_config()
    url = format_url(cfg["base_url"], cfg["endpoints"]["get_post"], id=cfg["test_data"]["valid_post_id"])
    r = requests.get(url, headers=cfg["default_headers"])
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == cfg["test_data"]["valid_post_id"]
    assert "title" in data
    assert "body" in data

def test_get_post_invalid_id():
    cfg = load_config()
    url = format_url(cfg["base_url"], cfg["endpoints"]["get_post"], id=cfg["test_data"]["invalid_post_id"])
    r = requests.get(url, headers=cfg["default_headers"])
    # JSONPlaceholder returns {} for unknown posts with 200; real APIs often return 404
    assert r.status_code in (200, 404)
