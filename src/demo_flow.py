"""
Demo Flow – Simulate full pipeline với mock Jira data (không cần token thật).
Dùng để test logic generate test cases trước khi có MCP token.

Usage:
    python src/demo_flow.py --ticket PROJ-1234
    python src/demo_flow.py --ticket PROJ-1234 --platform ios
"""
import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

# ── Mock Jira Ticket Data ─────────────────────────────────────────────────────
# Thay thế bằng data thật khi có MCP token
MOCK_TICKETS: dict[str, dict] = {
    "PROJ-1234": {
        "ticket_id": "PROJ-1234",
        "title": "App crashes when submitting login with empty password",
        "description": """
Preconditions:
- App is installed on device
- User is on the Login screen
- User has a valid account

Steps:
1. Launch the app
2. Navigate to Login screen
3. Enter a valid email address
4. Leave the Password field EMPTY
5. Tap the "Login" button

Expected Results:
- App should display validation message: "Password cannot be empty"
- App must NOT crash or force close
- User should remain on the Login screen
- Error message should be clearly visible below the password field
        """,
        "priority": "High",
        "status": "In Progress",
        "components": ["authentication", "login"],
        "labels": ["bug", "android", "ios", "regression"],
        "assignee": "dev@company.com",
        "reporter": "qa@company.com",
        "acceptance_criteria": [],
        "attachments": [],
        "fetched_at": "2026-05-18T10:00:00Z",
    },
    "PROJ-5678": {
        "ticket_id": "PROJ-5678",
        "title": "Profile photo upload fails on slow network",
        "description": """
Preconditions:
- User is logged in
- User is on Profile screen
- Network speed is throttled (3G/slow)

Steps:
1. Tap on the profile avatar
2. Select "Change Photo" option
3. Choose a photo from gallery (size > 2MB)
4. Wait for upload to complete

Expected Results:
- Upload progress indicator should be shown
- App should NOT timeout without feedback
- On success: show toast "Photo updated successfully"
- On failure: show retry option with error message
- App must stay responsive during upload
        """,
        "priority": "Medium",
        "status": "Open",
        "components": ["profile", "media-upload", "network"],
        "labels": ["bug", "android", "performance"],
        "assignee": "dev2@company.com",
        "reporter": "qa@company.com",
        "acceptance_criteria": [],
        "attachments": [],
        "fetched_at": "2026-05-18T10:00:00Z",
    },
    "PROJ-9999": {
        "ticket_id": "PROJ-9999",
        "title": "Add biometric login support",
        "description": """
Given user has biometric authentication set up on device
And user is on the Login screen

When user taps "Login with Biometric" button
Then system should prompt biometric scan (fingerprint/face)

When biometric scan succeeds
Then user should be logged in and navigate to Home screen

When biometric scan fails or is cancelled
Then user should see error message and remain on Login screen
        """,
        "priority": "High",
        "status": "In Development",
        "components": ["authentication", "biometric", "security"],
        "labels": ["feature", "android", "ios", "smoke"],
        "assignee": "dev3@company.com",
        "reporter": "pm@company.com",
        "acceptance_criteria": [],
        "attachments": [],
        "fetched_at": "2026-05-18T10:00:00Z",
    },
}


def get_mock_ticket(ticket_id: str) -> dict:
    if ticket_id in MOCK_TICKETS:
        return MOCK_TICKETS[ticket_id]
    # Tạo generic mock nếu ticket không có trong list
    return {
        "ticket_id": ticket_id,
        "title": f"[MOCK] Test ticket {ticket_id}",
        "description": """
Preconditions:
- App is installed
- User is logged in

Steps:
1. Navigate to the feature
2. Perform the action
3. Observe the result

Expected Results:
- Feature works as expected
- No crash occurs
- Data is saved correctly
        """,
        "priority": "Medium",
        "status": "Open",
        "components": ["general"],
        "labels": ["android"],
        "assignee": "",
        "reporter": "",
        "acceptance_criteria": [],
        "attachments": [],
        "fetched_at": "2026-05-18T10:00:00Z",
    }


def run_demo(ticket_id: str, platform: str) -> None:
    Path("logs").mkdir(exist_ok=True)
    Path(f"reports/{ticket_id}").mkdir(parents=True, exist_ok=True)

    console.print(Panel.fit(
        f"🎭 [bold yellow]DEMO MODE[/bold yellow] – Mock Jira Data\n"
        f"   Ticket: [bold cyan]{ticket_id}[/bold cyan] | Platform: [bold green]{platform}[/bold green]\n"
        f"   (Thay thế bằng MCP token thật khi sẵn sàng)",
        title="QA Demo Flow",
    ))

    # ── STEP 1: Mock Fetch ────────────────────────────────────────
    console.print("\n[bold blue]▶ STEP 1 – Loading mock ticket data[/bold blue]")
    ticket_data = get_mock_ticket(ticket_id)
    console.print(f"  📋 Title   : [white]{ticket_data['title']}[/white]")
    console.print(f"  🏷  Priority: [yellow]{ticket_data['priority']}[/yellow]")
    console.print(f"  🧩 Components: {', '.join(ticket_data['components'])}")

    # Save mock data
    with open(f"reports/{ticket_id}/ticket_data.json", "w") as f:
        json.dump(ticket_data, f, indent=2)

    # ── STEP 2: Analyze ───────────────────────────────────────────
    console.print("\n[bold blue]▶ STEP 2 – Analyzing ticket[/bold blue]")
    sys.path.insert(0, str(Path(__file__).parent))
    from jira.ticket_analyzer import TicketAnalyzer

    analyzer = TicketAnalyzer()
    analysis = analyzer.analyze(ticket_data)

    console.print(f"\n  📌 Preconditions ({len(analysis['preconditions'])}):")
    for p in analysis["preconditions"]:
        console.print(f"     • {p}")

    console.print(f"\n  🪜 Test Steps ({len(analysis['test_steps'])}):")
    for i, s in enumerate(analysis["test_steps"], 1):
        console.print(f"     {i}. {s}")

    console.print(f"\n  ✅ Expected Results ({len(analysis['expected_results'])}):")
    for e in analysis["expected_results"]:
        console.print(f"     ➜ {e}")

    console.print(f"\n  🏷  Test Type : [cyan]{analysis['test_type']}[/cyan]")
    console.print(f"  📱 Platforms  : [cyan]{', '.join(analysis['platforms'])}[/cyan]")

    # ── STEP 3: Generate ──────────────────────────────────────────
    console.print("\n[bold blue]▶ STEP 3 – Generating Robot test suite[/bold blue]")
    from testing.test_case_mapper import TestCaseMapper

    mapper = TestCaseMapper(platform=platform, dry_run=False)
    suite_path, test_cases = mapper.generate(ticket_data, analysis)

    console.print(f"\n  📝 Generated [bold]{len(test_cases)}[/bold] test cases")
    for tc in test_cases:
        console.print(f"     [cyan]{tc['id']}[/cyan] – {tc['name']}")

    # ── Print generated robot file ────────────────────────────────
    console.print(f"\n  📄 Suite file: [green]{suite_path}[/green]")
    console.print("\n[bold]Generated .robot content:[/bold]")
    if suite_path.exists():
        content = suite_path.read_text()
        syntax = Syntax(content, "robotframework", theme="monokai", line_numbers=True)
        console.print(syntax)

    console.print(Panel.fit(
        f"✅ [bold green]Done![/bold green]\n\n"
        f"  Suite: [cyan]{suite_path}[/cyan]\n\n"
        f"  Run tests:\n"
        f"  [bold white]robot --variable PLATFORM:{platform} {suite_path}[/bold white]\n\n"
        f"  Or full pipeline (needs MCP token):\n"
        f"  [bold white]python src/flow_runner.py --ticket {ticket_id}[/bold white]",
        title="Next Steps",
    ))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo QA Flow với mock Jira data")
    parser.add_argument("--ticket", default="PROJ-1234",
                        help="Ticket ID (PROJ-1234, PROJ-5678, PROJ-9999 hoặc bất kỳ)")
    parser.add_argument("--platform", choices=["android", "ios"], default="android")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_demo(ticket_id=args.ticket, platform=args.platform)

