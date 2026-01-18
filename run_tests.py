import json
import os
import pytest
import webbrowser
from datetime import datetime
from pathlib import Path

from starter_api_automation_repo.utils.evidence import EVIDENCE_PATH as EVIDENCE_JSON

ROOT = Path(__file__).resolve().parent
PKG_ROOT = ROOT / "starter_api_automation_repo"
REPORTS_DIR = PKG_ROOT / "reports"
REPORT_HTML = REPORTS_DIR / "report.html"


def now_clean() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
         .replace("'", "&#39;")
    )


def render_meta(start_time: str, end_time: str) -> str:
    return f"""
    <div class="meta">
      <div><b>Started:</b> {html_escape(start_time)}</div>
      <div><b>Finished:</b> {html_escape(end_time)}</div>
    </div>
    """


def render_status(passed: bool) -> str:
    if passed:
        return '<div class="status pass"><span class="dot"></span>ALL TESTS PASSED</div>'
    return '<div class="status fail"><span class="dot"></span>TEST FAILURES DETECTED</div>'


def status_badge_class(status_code: int) -> str:
    if 200 <= status_code <= 299:
        return "ok"
    if 300 <= status_code <= 399:
        return "warn"
    return "bad"


def render_evidence() -> str:
    print(f"[run_tests] REPORT_HTML   = {REPORT_HTML}")
    print(f"[run_tests] EVIDENCE_JSON = {EVIDENCE_JSON}")

    if not EVIDENCE_JSON.exists():
        return "<div class='card'><div class='small'><b>No evidence.json found.</b> Tests did not write evidence.</div></div>"

    try:
        data = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    except Exception as e:
        return f"<div class='card'><div class='small'><b>Could not parse evidence.json:</b> {html_escape(str(e))}</div></div>"

    if not data:
        return "<div class='card'><div class='small'><b>Evidence file is empty.</b></div></div>"

    rows = []
    for e in data:
        raw_status = e.get("status_code", e.get("status", 0))
        try:
            status_val = int(raw_status)
        except Exception:
            status_val = 0

        badge_class = status_badge_class(status_val)

        time_val = html_escape(str(e.get("time", "")))
        test_val = html_escape(str(e.get("test", "")))
        method_val = html_escape(str(e.get("method", "")))
        url_val = str(e.get("url", ""))
        url_safe = html_escape(url_val)

        resp_obj = e.get("response", {})
        try:
            resp_pretty = json.dumps(resp_obj, indent=2, ensure_ascii=False)
        except Exception:
            resp_pretty = str(resp_obj)

        resp_pretty = html_escape(resp_pretty)

        rows.append(f"""
        <tr>
          <td class="time">{time_val}</td>
          <td class="test">{test_val}</td>
          <td class="method">{method_val}</td>
          <td><a href="{url_safe}" target="_blank" rel="noreferrer">{url_safe}</a></td>
          <td><span class="badge {badge_class}">{status_val}</span></td>
          <td>
            <details>
              <summary>View JSON</summary>
              <pre>{resp_pretty}</pre>
            </details>
          </td>
        </tr>
        """)

    return f"""
    <div class="table-wrap">
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
    </div>
    """


def run_tests():
    os.chdir(ROOT)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if EVIDENCE_JSON.exists():
        print(f"[run_tests] Deleting old evidence: {EVIDENCE_JSON}")
        EVIDENCE_JSON.unlink()

    start_time = now_clean()
    result = pytest.main(["-q"])
    end_time = now_clean()
    passed = (result == 0)

    template = REPORT_HTML.read_text(encoding="utf-8")

    html = template.replace('<div id="meta"></div>', render_meta(start_time, end_time))
    html = html.replace('<div id="status"></div>', render_status(passed))
    html = html.replace('<div id="evidence"></div>', render_evidence())

    REPORT_HTML.write_text(html, encoding="utf-8")

    try:
        webbrowser.open(REPORT_HTML.resolve().as_uri())
        print(f"[run_tests] Opened report: {REPORT_HTML.resolve()}")
    except Exception as e:
        print(f"[run_tests] Could not auto-open report: {e}")
        print(f"[run_tests] Manually open: open {REPORT_HTML}")

    raise SystemExit(result)


if __name__ == "__main__":
    run_tests()
