"""
jira_flow.py – Fetch ticket thật từ Jira → Analyze → Generate Robot → Run dryrun
KHÔNG cần AI API key – dùng Jira REST API trực tiếp + TicketAnalyzer regex

Usage:
    python3 src/jira_flow.py --ticket KAN-4
    python3 src/jira_flow.py --ticket KAN-4 --platform android
"""
import argparse, json, logging, os, subprocess, sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import requests

load_dotenv()
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | %(message)s",
                    handlers=[logging.FileHandler("logs/jira_flow.log"),
                               logging.StreamHandler()])
logger = logging.getLogger(__name__)
console = Console()

BASE_URL = os.getenv("ATLASSIAN_BASE_URL", "").rstrip("/")
EMAIL    = os.getenv("ATLASSIAN_EMAIL", "")
TOKEN    = os.getenv("ATLASSIAN_API_TOKEN", "")
AUTH     = (EMAIL, TOKEN)
HEADERS  = {"Accept": "application/json"}


# ── STEP 1: Fetch ticket từ Jira REST API ─────────────────────────────────────

def fetch_ticket(ticket_id: str) -> dict:
    console.print(f"\n[bold blue]▶ STEP 1 – Fetching [cyan]{ticket_id}[/cyan] từ Jira[/bold blue]")
    url = f"{BASE_URL}/rest/api/3/issue/{ticket_id}?fields=summary,description,priority,status,issuetype,components,labels,assignee,reporter,attachment"
    r = requests.get(url, auth=AUTH, headers=HEADERS, timeout=15)
    if r.status_code == 404:
        console.print(f"  [red]❌ Ticket {ticket_id} không tồn tại![/red]")
        sys.exit(1)
    if r.status_code != 200:
        console.print(f"  [red]❌ Jira API error {r.status_code}: {r.text[:200]}[/red]")
        sys.exit(1)

    raw = r.json()
    fields = raw.get("fields", {})

    # Parse ADF description → plain text
    desc_raw = fields.get("description", {})
    description = _adf_to_text(desc_raw) if isinstance(desc_raw, dict) else (desc_raw or "")

    ticket = {
        "ticket_id":  raw["key"],
        "title":      fields.get("summary", ""),
        "description": description,
        "priority":   (fields.get("priority") or {}).get("name", "Medium"),
        "status":     (fields.get("status") or {}).get("name", ""),
        "issuetype":  (fields.get("issuetype") or {}).get("name", ""),
        "components": [c["name"] for c in (fields.get("components") or [])],
        "labels":     fields.get("labels", []),
        "assignee":   ((fields.get("assignee") or {}).get("emailAddress", "") or
                       (fields.get("assignee") or {}).get("displayName", "")),
        "reporter":   ((fields.get("reporter") or {}).get("emailAddress", "") or
                       (fields.get("reporter") or {}).get("displayName", "")),
        "acceptance_criteria": [],
        "attachments": [],
        "fetched_at": "",
    }

    # Print summary
    tbl = Table(title=f"🎫 {ticket['ticket_id']}", box=box.ROUNDED)
    tbl.add_column("Field", style="cyan", no_wrap=True)
    tbl.add_column("Value")
    tbl.add_row("Summary",    ticket["title"])
    tbl.add_row("Type",       ticket["issuetype"])
    tbl.add_row("Priority",   ticket["priority"])
    tbl.add_row("Status",     ticket["status"])
    tbl.add_row("Labels",     ", ".join(ticket["labels"]))
    console.print(tbl)

    # Save
    out = Path(f"reports/{ticket['ticket_id']}")
    out.mkdir(parents=True, exist_ok=True)
    (out / "ticket_data.json").write_text(
        json.dumps(ticket, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"  ✅ Saved → reports/{ticket['ticket_id']}/ticket_data.json")
    return ticket


def _adf_to_text(node: dict) -> str:
    """Convert Atlassian Document Format → plain text."""
    if not node:
        return ""
    if node.get("type") == "text":
        return node.get("text", "")
    parts = []
    for child in node.get("content", []):
        text = _adf_to_text(child)
        if text:
            parts.append(text)
        if child.get("type") in ("paragraph", "heading", "listItem", "orderedList", "bulletList"):
            parts.append("\n")
    return "".join(parts)


# ── STEP 2: Analyze ticket (không cần AI) ────────────────────────────────────

def analyze_ticket(ticket: dict) -> dict:
    console.print(f"\n[bold blue]▶ STEP 2 – Analyzing ticket (regex parser)[/bold blue]")
    sys.path.insert(0, str(Path(__file__).parent))
    from jira.ticket_analyzer import TicketAnalyzer

    analysis = TicketAnalyzer().analyze(ticket)

    console.print(f"  📌 Preconditions  ([cyan]{len(analysis['preconditions'])}[/cyan]):")
    for p in analysis["preconditions"]:
        console.print(f"     • {p}")

    console.print(f"\n  🪜 Test Steps     ([cyan]{len(analysis['test_steps'])}[/cyan]):")
    for i, s in enumerate(analysis["test_steps"], 1):
        console.print(f"     {i}. {s}")

    console.print(f"\n  ✅ Expected       ([cyan]{len(analysis['expected_results'])}[/cyan]):")
    for e in analysis["expected_results"]:
        console.print(f"     ➜ {e}")

    console.print(f"\n  🏷  Test Type: [cyan]{analysis['test_type']}[/cyan]  |  "
                  f"Platforms: [cyan]{', '.join(analysis['platforms'])}[/cyan]")
    return analysis


# ── STEP 3: Generate Robot test suite ────────────────────────────────────────

def generate_tests(ticket: dict, analysis: dict, platform: str) -> Path:
    console.print(f"\n[bold blue]▶ STEP 3 – Generating Robot test suite[/bold blue]")
    from testing.test_case_mapper import TestCaseMapper

    mapper = TestCaseMapper(platform=platform, dry_run=False)
    suite_path, test_cases = mapper.generate(ticket, analysis)

    console.print(f"  📝 Generated [bold]{len(test_cases)}[/bold] test cases:")
    for tc in test_cases:
        console.print(f"     [cyan]{tc['id']}[/cyan] – {tc['name']}")
    console.print(f"\n  📄 Suite: [green]{suite_path}[/green]")
    return suite_path


# ── STEP 4: Run Robot --dryrun ────────────────────────────────────────────────

def run_robot_dryrun(suite_path: Path, ticket_id: str, platform: str) -> None:
    console.print(f"\n[bold blue]▶ STEP 4 – Running Robot Framework (--dryrun)[/bold blue]")
    console.print(f"  ℹ️  Dryrun = validate syntax & keyword resolution (không cần device)\n")

    out_dir = Path(f"reports/{ticket_id}/robot_output")
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python3", "-m", "robot",
        "--dryrun", "--nostatusrc",
        "--outputdir", str(out_dir),
        "--variable", f"PLATFORM:{platform}",
        "--variable", f"TICKET_ID:{ticket_id}",
        "--variable", "APPIUM_URL:http://localhost:4723",
        "--variable", "ANDROID_DEVICE_NAME:emulator-5554",
        "--variable", "ANDROID_APP_PACKAGE:com.your.app",
        "--variable", "ANDROID_APP_ACTIVITY:.MainActivity",
        "--variable", "ANDROID_PLATFORM_NAME:Android",
        "--variable", "ANDROID_AUTOMATION:UiAutomator2",
        "--variable", "ANDROID_NO_RESET:False",
        "--variable", "TIMEOUT_DEFAULT:10s",
        "--variable", "TIMEOUT_SHORT:3s",
        "--variable", "TIMEOUT_LONG:30s",
        "--variable", "TIMEOUT_PAGE_LOAD:20s",
        "--variable", "VALID_EMAIL:test@example.com",
        "--variable", "VALID_PASSWORD:Test123",
        str(suite_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr

    # Parse pass/fail
    passed = output.count("| PASS |")
    failed = output.count("| FAIL |")
    total  = passed + failed

    # Print output line by line
    for line in output.splitlines():
        if "PASS" in line:
            console.print(f"  [green]{line.strip()}[/green]")
        elif "FAIL" in line or "ERROR" in line:
            console.print(f"  [red]{line.strip()}[/red]")
        elif "WARN" in line:
            console.print(f"  [yellow]{line.strip()}[/yellow]")
        elif line.strip().startswith(("==", "--")):
            console.print(f"  [dim]{line.strip()}[/dim]")

    # Summary
    color = "green" if failed == 0 else "red"
    icon  = "✅" if failed == 0 else "❌"
    console.print(Panel.fit(
        f"{icon} [bold {color}]{passed}/{total} PASS[/bold {color}]   Failed: {failed}\n"
        f"   Report: [cyan]{out_dir}/report.html[/cyan]",
        title="Robot Dryrun Result",
        border_style=color,
    ))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch Jira → Analyze → Generate → Run dryrun")
    parser.add_argument("--ticket",   required=True, help="Jira ticket ID, e.g. KAN-4")
    parser.add_argument("--platform", choices=["android","ios"], default="android")
    args = parser.parse_args()

    Path("logs").mkdir(exist_ok=True)

    console.print(Panel.fit(
        f"🚀 Jira Flow  (Real Jira + Regex Analyzer)\n"
        f"   Ticket  : [bold cyan]{args.ticket}[/bold cyan]\n"
        f"   Jira    : [dim]{BASE_URL}[/dim]\n"
        f"   Platform: [bold green]{args.platform}[/bold green]",
        title="QA Pipeline",
    ))

    if not all([BASE_URL, EMAIL, TOKEN]):
        console.print("[red]❌ Thiếu credentials! Kiểm tra .env[/red]")
        sys.exit(1)

    ticket   = fetch_ticket(args.ticket)
    analysis = analyze_ticket(ticket)
    suite    = generate_tests(ticket, analysis, args.platform)
    run_robot_dryrun(suite, args.ticket, args.platform)

    console.print(Panel.fit(
        f"🎉 Flow hoàn thành!\n\n"
        f"  Ticket : [cyan]{BASE_URL}/browse/{args.ticket}[/cyan]\n"
        f"  Suite  : [cyan]{suite}[/cyan]\n"
        f"  Report : [cyan]reports/{args.ticket}/robot_output/report.html[/cyan]\n\n"
        f"  Để chạy test thật (cần device + Appium):\n"
        f"  [bold]robot {suite}[/bold]",
        style="bold green",
    ))


if __name__ == "__main__":
    main()

