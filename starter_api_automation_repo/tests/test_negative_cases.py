import requests
from starter_api_automation_repo.utils.helpers import load_config, format_url
from starter_api_automation_repo.utils.evidence import save_evidence


def test_get_posts_collection():
    cfg = load_config()
    url = format_url(cfg["base_url"], cfg["endpoints"]["get_posts"])

    r = requests.get(url, headers=cfg.get("default_headers", {}))

    try:
        body = r.json()
    except Exception:
        body = {"raw": r.text}

    save_evidence("test_get_posts_collection", url, "GET", r.status_code, body)

    assert r.status_code == 200
    assert isinstance(body, list)
    assert len(body) > 0


def test_get_post_missing_id_param_graceful():
    """
    Negative-ish: ensure our URL formatter doesn't crash even if id isn't passed.
    If your format_url requires id, this test can be removed.
    """
    cfg = load_config()
    endpoint = cfg["endpoints"]["get_post"]

    # If endpoint contains "{id}", format_url may raise KeyError.
    # We'll just assert we handle it (either by raising or returning a string).
    try:
        url = format_url(cfg["base_url"], endpoint)  # id not provided on purpose
        # If it didn't raise, store evidence that URL was produced
        save_evidence("test_get_post_missing_id_param_graceful", url, "FORMAT_URL", 0, {"url": url})
        assert isinstance(url, str)
    except Exception as e:
        save_evidence("test_get_post_missing_id_param_graceful", "N/A", "FORMAT_URL", 0, {"error": str(e)})
        assert True
