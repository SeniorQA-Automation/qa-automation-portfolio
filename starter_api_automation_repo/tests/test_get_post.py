import requests
from starter_api_automation_repo.utils.helpers import load_config, format_url
from starter_api_automation_repo.utils.evidence import save_evidence


def test_get_post_valid():
    cfg = load_config()
    post_id = cfg["test_data"]["valid_post_id"]

    url = format_url(cfg["base_url"], cfg["endpoints"]["get_post"], id=post_id)
    r = requests.get(url, headers=cfg.get("default_headers", {}))

    # evidence
    try:
        body = r.json()
    except Exception:
        body = {"raw": r.text}

    save_evidence("test_get_post_valid", url, "GET", r.status_code, body)

    assert r.status_code == 200
    assert body["id"] == post_id
    assert "title" in body
    assert "body" in body


def test_get_post_invalid_id():
    cfg = load_config()
    bad_id = cfg["test_data"]["invalid_post_id"]

    url = format_url(cfg["base_url"], cfg["endpoints"]["get_post"], id=bad_id)
    r = requests.get(url, headers=cfg.get("default_headers", {}))

    try:
        body = r.json()
    except Exception:
        body = {"raw": r.text}

    save_evidence("test_get_post_invalid_id", url, "GET", r.status_code, body)

    # JSONPlaceholder usually returns 200 and {} for unknown posts; real APIs often return 404
    assert r.status_code in (200, 404)
