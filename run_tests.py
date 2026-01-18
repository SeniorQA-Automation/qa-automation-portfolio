import json
import pytest
import webbrowser
from datetime import datetime
from pathlib import Path

from starter_api_automation_repo.utils.evidence import EVIDENCE_PATH, reset_evidence


ROOT = Path(__file__).resolve().parent
REPORTS_DIR = ROOT / "reports"
REPORT_HTML = REPORTS_DIR / "report.html"


def now_clean():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def html_escape(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def load_evidence():
    print("[DEBUG] EVIDENCE_PATH =", EVIDENCE_PATH)
    if not EVIDENCE_PATH.exists():
        print("[DEBUG] evidence.json does not exist")
        return []

    raw = EVIDENCE_PATH.read_text(encoding="utf-8")
    print("[DEBUG] evidence.json bytes =", len(raw))

    try:
        data = json.loads(raw) if raw.strip() else []
    except Exception as e:
        print("[DEBUG] evidence.json parse error:", e)
        return []

    print("[DEBUG] evidence entries =", len(data))
    return data


def render_evidence_table(data):
    if not data:
        return "<p><b>No evidence was captured.</b> (evidence.json empty)</p>"

    rows = []
    for e in data:
        time_val = html_escape(e.get("time", ""))
        test_val = html_escape(e.get("test", ""))
        method_val = html_escape(e.get("method", ""))
        url_val = html_escape(e.get("url", ""))
        status_val = html_escape(e.get("status", e.get("status_code", "")))

        resp = e.get("response", {})
        try:
            resp_pretty = json.dumps(resp, indent=2, ensure_ascii=False)
        except Exception:
            resp_pretty = str(resp)

        rows.append(f"""
          <tr>
            <td>{time_val}</td>
            <td>{test_val}</td>
            <td>{method_val}</td>
            <td><a href="{url_val}" target="_blank" rel="noopener">{url_val}</a></td>
            <td>{status_val}</td>
            <td><pre>{html_escape(resp_pretty)}</pre></td>
          </tr>
        """)

    return f"""
    <h2>API Response Evidence</h2>
    <table>
      <thead>
        <tr>
          <th>Time</th>
          <th>Test</th>
          <th>Method</th>
          <th>URL</th>
          <th>Status</th>
          <th>Response</th>
        </tr>
      </thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
    """


def run_tests():
    REPORTS_DIR.mkdir(exist_ok=True)

    print("\n[RUN] Resetting evidence...")
    reset_evidence()

    started = now_clean()
    print("[RUN] pytest starting at", started)

    result = pytest.main(["-q"])

    finished = now_clean()
    print("[RUN] pytest finished at", finished)
    print("[RUN] exit code =", result)

    data = load_evidence()
    evidence_html = render_evidence_table(data)

    status_html = (
        "<div class='status pass'>ALL TESTS PASSED</div>"
        if result == 0
        else "<div class='status fail'>TEST FAILURES DETECTED</div>"
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>API Automation Test Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; }}
    h1 {{ color: #2c3e50; margin-bottom: 6px; }}
    .meta {{ color: #444; margin-bottom: 14px; }}
    .status {{ font-weight: bold; margin: 14px 0; font-size: 18px; }}
    .pass {{ color: green; }}
    .fail {{ color: red; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 14px; }}
    th, td {{ border: 1px solid #ccc; padding: 10px; vertical-align: top; }}
    th {{ background: #f1f1f1; text-align: left; }}
    pre {{ background: #f4f4f4; padding: 10px; white-space: pre-wrap; word-break: break-word; }}
  </style>
</head>
<body>
  <h1>API Automation Test Report</h1>

  <div class="meta"><b>Started:</b> {started} &nbsp;&nbsp; <b>Finished:</b> {finished}</div>

  {status_html}

  <hr />

  {evidence_html}
</body>
</html>
"""

    REPORT_HTML.write_text(html, encoding="utf-8")
    print("[RUN] wrote report.html ->", REPORT_HTML.resolve())

    webbrowser.open(REPORT_HTML.resolve().as_uri())

    raise SystemExit(result)


if __name__ == "__main__":
    run_tests()
