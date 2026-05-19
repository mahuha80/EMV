h """
AI QA Automation Pipeline – Main Orchestrator
Usage: python src/main.py --ticket PROJ-1234 [--step A] [--platform android]
"""
import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)
console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI QA Automation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py --ticket PROJ-1234
  python src/main.py --ticket PROJ-1234 --step B
  python src/main.py --ticket PROJ-1234 --platform ios
        """,
    )
    parser.add_argument("--ticket", required=True, help="Jira ticket ID (e.g., PROJ-1234)")
    parser.add_argument(
        "--step",
        choices=["A", "B", "C", "D"],
        default="A",
        help="Starting step (default: A – run full pipeline)",
    )
    parser.add_argument(
        "--platform",
        choices=["android", "ios"],
        default="android",
        help="Target platform for Appium tests (default: android)",
    )
    return parser.parse_args()


def run_pipeline(ticket_id: str, start_step: str = "A", platform: str = "android") -> None:
    """
    Chạy toàn bộ AI QA pipeline từ bước được chỉ định.

    Args:
        ticket_id: Jira ticket ID
        start_step: Bước bắt đầu (A, B, C, D)
        platform: Target platform (android, ios)
    """
    console.print(Panel.fit(
        f"🚀 AI QA Automation Pipeline\n"
        f"   Ticket: [bold cyan]{ticket_id}[/bold cyan]\n"
        f"   Start Step: [bold yellow]{start_step}[/bold yellow]\n"
        f"   Platform: [bold green]{platform}[/bold green]",
        title="Pipeline Start",
    ))

    # Ensure reports directory exists
    Path(f"reports/{ticket_id}").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

    ticket_data = None
    test_results = None
    fix_report = None

    # ─── STEP A: Jira MCP Fetcher ────────────────────────────────
    if start_step <= "A":
        console.print("\n[bold blue]━━ STEP A: Jira MCP Fetcher ━━[/bold blue]")
        from jira.ticket_fetcher import TicketFetcher

        fetcher = TicketFetcher()
        ticket_data = fetcher.fetch(ticket_id)
        console.print(f"  ✅ Ticket fetched: [cyan]{ticket_data['title']}[/cyan]")

    # ─── STEP B: Robot Framework + Appium Runner ─────────────────
    if start_step <= "B":
        console.print("\n[bold blue]━━ STEP B: Test Runner (Robot + Appium) ━━[/bold blue]")
        from testing.robot_runner import RobotRunner

        runner = RobotRunner(platform=platform)
        test_results = runner.run(ticket_data)
        status_color = "green" if test_results["status"] == "PASS" else "red"
        console.print(
            f"  {'✅' if test_results['status'] == 'PASS' else '❌'} "
            f"Results: [{status_color}]{test_results['passed']}/{test_results['total']} PASS[/{status_color}]"
        )
        console.print(f"  📊 Report: {test_results.get('report_path', 'N/A')}")

    # ─── STEP C: AI Code Analyzer & Fix Generator ────────────────
    if start_step <= "C":
        if test_results and test_results["status"] == "FAIL":
            console.print("\n[bold blue]━━ STEP C: AI Code Analyzer ━━[/bold blue]")
            from analyzer.ai_analyzer import AIAnalyzer

            analyzer = AIAnalyzer()
            fix_report = analyzer.analyze(ticket_data, test_results)
            console.print(
                f"  ✅ Analysis complete | "
                f"Confidence: [yellow]{fix_report['confidence']:.0%}[/yellow] | "
                f"Files to fix: [cyan]{len(fix_report['fixes'])}[/cyan]"
            )
        else:
            console.print("\n[bold green]✅ STEP C: All tests passed – no fix needed![/bold green]")

    # ─── STEP D: GitHub Submission ───────────────────────────────
    if start_step <= "D" and fix_report:
        console.print("\n[bold blue]━━ STEP D: GitHub Submission ━━[/bold blue]")
        from github.pr_creator import PRCreator

        pr_creator = PRCreator()
        pr_info = pr_creator.create_pr(ticket_data, fix_report, test_results)
        console.print(f"  ✅ PR created: [link={pr_info['pr_url']}]{pr_info['pr_url']}[/link]")

    console.print(Panel.fit("🎉 Pipeline completed successfully!", style="bold green"))


def main() -> None:
    args = parse_args()
    try:
        run_pipeline(
            ticket_id=args.ticket,
            start_step=args.step,
            platform=args.platform,
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Pipeline interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        console.print(f"\n[red]❌ Pipeline failed: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()

