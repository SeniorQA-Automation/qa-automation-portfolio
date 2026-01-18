import json
import os
import pytest
import webbrowser
from datetime import datetime
from pathlib import Path

from starter_api_automation_repo.utils.evidence import EVIDENCE_PATH as EVIDENCE_JSON

ROOT = Path(__file__).resolve().parent
REPORTS_DIR = ROOT / "reports"

REPORT_TEMPLATE = REPORTS_DIR / "template.html"   # ✅ static template (never overwritten)
REPORT_HTML = REPORTS_DIR / "report.html"         # ✅ generated output
REPORT_CSS = REPORTS_DIR / "report.css"           # ✅ stylesheet


def now_clean():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_css_file():
    REPORTS_DIR.mkdir(exist_ok=True)
    if REPORT_CSS.exists():
        return

    REPORT_CSS.write_text(
        """body { font-family: Arial, sans-serif; margin: 24px; color: #111; }
h1 { margin-bottom: 8px; }
.meta { color: #444; margin-bottom: 12px; }
.status { font-weight: 700; margin: 12px 0 18px 0; padding: 10px 12px; border-radius: 8px; display: inline-block; }
.pass { background: #eaffea; border: 1px solid #b6f2b6; color: #0a6b0a; }
.fail { background: #ffecec; border: 1px solid #ffb8b8; color: #8a0a0a; }
hr { border: none; border-top: 1px solid #ddd; margin: 18px 0; }
table { width: 100%; border-collapse: collapse; margin-top: 12px; table-layout: fixed; }
th, td { border: 1px solid #ddd; padding: 10px; vertical-align: top; word-wrap: break-word; }
th { background: #f6f6f6; text-align: left; }
pre { white-space: pre-wrap; margin: 0; background: #f4f4f4; padding: 10px; border-radius: 6px; font-size: 12px; line-height: 1.35; }
a { color: #0b66c3; text-decoration: none; }
a:hover { text-decoration: underline; }
.small { font-size: 12px; color: #666; }""",
        encoding="utf-8",
    )


def render_evidence():
    if not EVIDENCE_JSON.exists():
        return "<p><b>No evidence.json found.</b> Tests did not write evidence.</p>"

    try:
        data = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    except Exception as e:
        return f"<p><b>Could not parse evidence.json:</b> {e}</p>"

    if not data:
        return "<p><b>Evidence file is empty.</b></p>"

    rows = []
    for e in data:
        status_val = e.get("status_code", e.get("status", ""))  # supports both keys
        resp = e.get("response", {})
        rows.append(
            f"""
            <tr>
              <td>{e.get('time','')}</td>
              <td>{e.get('test','')}</td>
              <td>{e.get('method','')}</td>
              <td><a href="{e.get('url','')}" target="_blank">{e.get('url','')}</a></td>
              <td>{status_val}</td>
              <td><pre>{json.dumps(resp, indent=2)}</pre></td>
            </tr>
            """
        )

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
    os.chdir(ROOT)
    REPORTS_DIR.mkdir(exist_ok=True)
    ensure_css_file()

    # ✅ delete evidence each run (fresh run)
    if EVIDENCE_JSON.exists():
       EVIDENCE_JSON.unlink()

    start_time = now_clean()
    result = pytest.main(["-q"])
    end_time = now_clean()

    passed = (result == 0)
    status_html = (
        '<div class="status pass">ALL TESTS PASSED</div>'
        if passed
        else '<div class="status fail">TEST FAILURES DETECTED</div>'
    )

    meta_html = f"""
    <div class="meta">
      <div><b>Started at:</b> {start_time}</div>
      <div><b>Finished at:</b> {end_time}</div>
    </div>
    """

    evidence_html = render_evidence()

    # ✅ Read STATIC template (placeholders always exist)
    template = REPORT_TEMPLATE.read_text(encoding="utf-8")

    html = template.replace('<div id="meta"></div>', meta_html)
    html = html.replace('<div id="status"></div>', status_html)
    html = html.replace('<div id="evidence"></div>', evidence_html)

    REPORT_HTML.write_text(html, encoding="utf-8")
    webbrowser.open(REPORT_HTML.resolve().as_uri())

    raise SystemExit(result)


if __name__ == "__main__":
    run_tests()
