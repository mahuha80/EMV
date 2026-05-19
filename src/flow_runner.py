"""
Flow Runner – Main entry point cho luồng:
  [STEP 1] AI Agent + Jira MCP Server  → Fetch & analyze ticket
  [STEP 2] TestCaseMapper              → Generate Robot .robot file
  [STEP 3] Robot Framework + Appium    → Run tests (optional)

Usage:
    python src/flow_runner.py --ticket PROJ-1234
    python src/flow_runner.py --ticket PROJ-1234 --platform ios --skip-run
    python src/flow_runner.py --ticket PROJ-1234 --dry-run
"""
import argparse
import json
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/flow.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)
console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI QA Flow: Jira MCP → Analyze → Generate Robot Tests → Run",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Cần set trong .env:
  JIRA_MCP_URL       = https://your.atlassian.net
  JIRA_EMAIL         = you@company.com
  JIRA_API_TOKEN     = your_jira_token
  AI_PROVIDER        = anthropic | openai
  AI_API_KEY         = your_ai_key
  AI_MODEL           = claude-3-5-sonnet-20241022 | gpt-4o
        """,
    )
    parser.add_argument("--ticket",   required=True,  help="Jira ticket ID, e.g. PROJ-1234")
    parser.add_argument("--platform", choices=["android", "ios"], default="android")
    parser.add_argument("--dry-run",  action="store_true", help="Generate .robot nhưng không chạy Appium")
    parser.add_argument("--skip-run", action="store_true", help="Chỉ fetch+analyze+generate, không chạy test")
    return parser.parse_args()


def print_analysis_summary(analysis: dict) -> None:
    """In bảng tóm tắt phân tích ticket."""
    tbl = Table(title=f"🎫 {analysis.get('ticket_id')} – {analysis.get('title', '')[:60]}", box=box.ROUNDED)
    tbl.add_column("Field", style="cyan", no_wrap=True)
    tbl.add_column("Value")
    tbl.add_row("Priority",   analysis.get("priority", ""))
    tbl.add_row("Status",     analysis.get("status", ""))
    tbl.add_row("Components", ", ".join(analysis.get("components", [])))
    tbl.add_row("Platforms",  ", ".join(analysis.get("platforms", [])))
    tbl.add_row("Test Type",  analysis.get("test_type", ""))
    console.print(tbl)

    prec  = analysis.get("preconditions", [])
    steps = analysis.get("test_steps", [])
    exp   = analysis.get("expected_results", [])

    console.print(f"\n  📌 Preconditions ([cyan]{len(prec)}[/cyan])")
    for p in prec:
        console.print(f"     • {p}")

    console.print(f"\n  🪜 Test Steps ([cyan]{len(steps)}[/cyan])")
    for i, s in enumerate(steps, 1):
        console.print(f"     {i}. {s}")

    console.print(f"\n  ✅ Expected ([cyan]{len(exp)}[/cyan])")
    for e in exp:
        console.print(f"     ➜ {e}")


def run_flow(ticket_id: str, platform: str, dry_run: bool, skip_run: bool) -> None:
    Path("logs").mkdir(exist_ok=True)
    Path(f"reports/{ticket_id}").mkdir(parents=True, exist_ok=True)

    console.print(Panel.fit(
        f"🚀 AI QA Flow  (Jira MCP + AI Agent)\n"
        f"   Ticket  : [bold cyan]{ticket_id}[/bold cyan]\n"
        f"   Platform: [bold green]{platform}[/bold green]"
        + (" | [yellow]DRY RUN[/yellow]" if dry_run else ""),
        title="QA Pipeline",
    ))

    # ── STEP 1: AI Agent + Jira MCP ──────────────────────────────
    console.print("\n[bold blue]▶ STEP 1 – AI Agent fetching ticket via Jira MCP[/bold blue]")
    console.print("  🔌 Connecting to mcp-atlassian server (npx)...")

    from jira.ai_jira_agent import JiraMCPAgent
    agent = JiraMCPAgent()
    analysis = agent.fetch_and_analyze(ticket_id)

    # Save full analysis
    with open(f"reports/{ticket_id}/ticket_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    print_analysis_summary(analysis)

    # ── STEP 2: Generate Robot test suite ────────────────────────
    console.print("\n[bold blue]▶ STEP 2 – Generating Robot test cases[/bold blue]")
    from testing.test_case_mapper import TestCaseMapper

    mapper = TestCaseMapper(platform=platform, dry_run=dry_run)
    suite_path, test_cases = mapper.generate(analysis, analysis)
    console.print(f"  📝 Generated [cyan]{len(test_cases)}[/cyan] test cases → [green]{suite_path}[/green]")
    for tc in test_cases:
        console.print(f"     [cyan]{tc['id']}[/cyan] – {tc['name']}")

    if skip_run or dry_run:
        console.print(Panel.fit(
            f"✅ Done!\n"
            f"   Suite: [cyan]{suite_path}[/cyan]\n"
            f"   Run:   [bold]robot {suite_path}[/bold]",
            style="green",
        ))
        return

    # ─�� STEP 3: Run Robot + Appium ────────────────────────────────
    console.print("\n[bold blue]▶ STEP 3 – Running Robot Framework + Appium[/bold blue]")
    from testing.robot_runner import RobotRunner

    runner  = RobotRunner(platform=platform)
    results = runner.run(analysis)
    color   = "green" if results["status"] == "PASS" else "red"
    console.print(
        f"  [{color}]{'✅' if results['status']=='PASS' else '❌'} "
        f"{results['passed']}/{results['total']} PASS[/{color}]"
        f"  →  {results.get('report_path','')}"
    )

    console.print(Panel.fit("🎉 Flow completed!", style="bold green"))


def main() -> None:
    args = parse_args()
    try:
        run_flow(
            ticket_id=args.ticket,
            platform=args.platform,
            dry_run=args.dry_run,
            skip_run=args.skip_run,
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠  Interrupted[/yellow]")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Flow failed: {e}")
        console.print(f"\n[red]❌ ERROR: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
