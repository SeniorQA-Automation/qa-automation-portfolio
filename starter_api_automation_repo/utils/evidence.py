import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_PATH = ROOT / "reports" / "evidence.json"

def now_clean():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_evidence(test, url, method, status_code, response):
    EVIDENCE_PATH.parent.mkdir(exist_ok=True)

    if EVIDENCE_PATH.exists():
        data = json.loads(EVIDENCE_PATH.read_text())
    else:
        data = []

    data.append({
        "time": now_clean(),
        "test": test,
        "method": method,
        "url": url,
        "status_code": status_code,   # ✅ changed key name
        "response": response
    })

    EVIDENCE_PATH.write_text(json.dumps(data, indent=2))