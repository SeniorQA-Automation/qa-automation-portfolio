import requests
from starter_api_automation_repo.utils.helpers import load_config, format_url
from starter_api_automation_repo.utils.evidence import save_evidence


def test_create_post():
    cfg = load_config()
    url = format_url(cfg["base_url"], cfg["endpoints"]["create_post"])
    payload = cfg["test_data"]["new_post"]

    r = requests.post(url, json=payload, headers=cfg.get("default_headers", {}))

    try:
        body = r.json()
    except Exception:
        body = {"raw": r.text}

    save_evidence("test_create_post", url, "POST", r.status_code, body)

    # JSONPlaceholder returns 201 for create
    assert r.status_code in (200, 201)
    # API echoes back what we sent (usually)
    assert "id" in body
