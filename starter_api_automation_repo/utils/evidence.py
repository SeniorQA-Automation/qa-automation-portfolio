import json
from datetime import datetime
from pathlib import Path

# Always resolve from package root
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "reports" / "evidence.json"


def now_clean():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def reset_evidence():
    if EVIDENCE_PATH.exists():
        print("[EVIDENCE] Deleting old evidence.json")
        EVIDENCE_PATH.unlink()
    else:
        print("[EVIDENCE] No evidence.json to delete")


def save_evidence(test, url, method, status_code, response):
    print("\n[EVIDENCE] save_evidence CALLED")
    print("[EVIDENCE] Path:", EVIDENCE_PATH)

    EVIDENCE_PATH.parent.mkdir(exist_ok=True)

    if EVIDENCE_PATH.exists():
        data = json.loads(EVIDENCE_PATH.read_text())
        print(f"[EVIDENCE] Existing entries: {len(data)}")
    else:
        print("[EVIDENCE] Creating new evidence.json")
        data = []

    entry = {
        "time": now_clean(),
        "test": test,
        "method": method,
        "url": url,
        "status": status_code,
        "response": response,
    }

    data.append(entry)
    EVIDENCE_PATH.write_text(json.dumps(data, indent=2))

    print(f"[EVIDENCE] Written entries now: {len(data)}")
