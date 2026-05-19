"""
MCP Flow Diagram – Minh họa đầy đủ kiến trúc AI + Jira MCP

Chạy file này để xem sơ đồ và kiểm tra cài đặt:
    python src/mcp_flow_diagram.py
"""
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box
from rich.table import Table
import os, sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
console = Console()


DIAGRAM = """
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     AI QA PIPELINE – Luồng đầy đủ với MCP                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Bạn chạy:  python src/flow_runner.py --ticket PROJ-1234                        │
│                           │                                                      │
│                           ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐                    │
│  │              STEP 1:  AI Agent + Jira MCP               │                    │
│  │                                                         │                    │
│  │   ┌──────────────┐  stdio/MCP   ┌───────────────────┐  │                    │
│  │   │  Python App  │◄────────────►│  mcp-atlassian    │  │                    │
│  │   │  (AI Agent)  │  tool calls  │  (npx subprocess) │  │                    │
│  │   └──────┬───────┘              └────────┬──────────┘  │                    │
│  │          │                               │              │                    │
│  │          │  AI decides to use tools      │ connects to  │                    │
│  │          ▼                               ▼              │                    │
│  │   ┌─────────────┐             ┌──────────────────────┐  │                    │
│  │   │  Claude /   │             │   Jira Cloud API     │  │                    │
│  │   │  OpenAI     │             │   (REST v3)          │  │                    │
│  │   │             │             │                      │  │                    │
│  │   │ Gọi tools:  │             │  GET /issue/PROJ-1234│  │                    │
│  │   │ jira_get_   │             │  ← ticket JSON       │  │                    │
│  │   │  _issue()   │             └──────────────────────┘  │                    │
│  │   │             │                                        │                    │
│  │   │ AI phân tích│                                        │                    │
│  │   │ → trả JSON  │                                        │                    │
│  │   └─────────────┘                                        │                    │
│  │                                                          │                    │
│  │   Output: ticket_analysis.json                           │                    │
│  │   {preconditions, test_steps, expected_results, ...}     │                    │
│  └─────────────────────────────────────────────────────────┘                    │
│                           │                                                      │
│                           ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐                    │
│  │              STEP 2:  Generate Robot Test Suite          │                    │
│  │                                                          │                    │
│  │   TestCaseMapper:                                        │                    │
│  │   • 1 expected result  →  1 TC_XXX                      │                    │
│  │   • preconditions      →  Suite Setup keywords          │                    │
│  │   • test_steps         →  Execute Step: keywords        │                    │
│  │                                                          │                    │
│  │   Output: robot_tests/suites/generated/PROJ-1234.robot  │                    │
│  └─────────────────────────────────────────────────────────┘                    │
│                           │                                                      │
│                           ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐                    │
│  │              STEP 3:  Robot Framework + Appium           │                    │
│  │                                                          │                    │
│  │   robot --outputdir reports/PROJ-1234/ ...robot         │                    │
│  │                  │                                       │                    │
│  │                  ▼                                       │                    │
│  │   AppiumLibrary  →  Appium Server  →  Device/Emulator   │                    │
│  │                                                          │                    │
│  │   Output: report.html, output.xml, screenshots          │                    │
│  └─────────────────────────────────────────────────────────┘                    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
"""

MCP_TOOLS = """
MCP Tools từ mcp-atlassian:
┌─────────────────────────┬──────────────────────────────────────────┐
│ Tool                    │ Mô tả                                    │
├─────────────────────────┼──────────────────────────────────────────┤
│ jira_get_issue          │ Lấy ticket theo ID → DÙNG CHÍNH          │
│ jira_search             │ JQL search nhiều tickets                 │
│ jira_get_issue_comments │ Lấy comments của ticket                  │
│ jira_get_transitions    │ Lấy workflow transitions                 │
│ jira_create_issue       │ Tạo ticket mới                           │
│ jira_update_issue       │ Update ticket                            │
│ jira_add_comment        │ Thêm comment vào ticket                  │
└─────────────────────────┴──────────────────────────────────────────┘
"""

AI_ROLE = """
AI Agent làm gì?
  1. Nhận request: "Fetch PROJ-1234 và analyze"
  2. Quyết định gọi tool: jira_get_issue(issue_key="PROJ-1234")
  3. Nhận ticket JSON thô từ Jira
  4. Phân tích description → tách preconditions/steps/expected
  5. Detect platform (android/ios) từ labels
  6. Detect test type (smoke/regression/functional)
  7. Trả về structured JSON cho pipeline
"""


def check_env() -> None:
    """Kiểm tra environment variables."""
    required = {
        "ATLASSIAN_BASE_URL":  os.getenv("ATLASSIAN_BASE_URL"),
        "ATLASSIAN_EMAIL":     os.getenv("ATLASSIAN_EMAIL"),
        "ATLASSIAN_API_TOKEN": os.getenv("ATLASSIAN_API_TOKEN"),
        "AI_PROVIDER":         os.getenv("AI_PROVIDER", "anthropic"),
        "AI_API_KEY":          os.getenv("AI_API_KEY"),
        "AI_MODEL":            os.getenv("AI_MODEL", "claude-3-5-sonnet-20241022"),
    }

    tbl = Table(title="⚙️  Environment Check", box=box.ROUNDED)
    tbl.add_column("Variable", style="cyan")
    tbl.add_column("Status")
    tbl.add_column("Value")

    all_ok = True
    for var, val in required.items():
        if val:
            status = "✅ Set"
            display = val[:30] + "..." if len(val) > 30 else val
            if "TOKEN" in var or "KEY" in var:
                display = val[:6] + "***" + val[-4:]
        else:
            status = "❌ MISSING"
            display = "(not set)"
            all_ok = False
        tbl.add_row(var, status, display)

    console.print(tbl)
    return all_ok


def check_npx() -> bool:
    """Kiểm tra npx và mcp-atlassian."""
    import subprocess
    try:
        result = subprocess.run(
            ["npx", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            console.print(f"  ✅ npx: [green]v{result.stdout.strip()}[/green]")
            return True
    except FileNotFoundError:
        pass
    console.print("  ❌ npx: [red]NOT FOUND[/red] – cần cài Node.js")
    return False


def main() -> None:
    console.print(Panel(DIAGRAM, title="🏗️  Kiến Trúc AI QA MCP Pipeline", border_style="blue"))
    console.print()
    console.print(Panel(MCP_TOOLS, title="🔧 MCP Tools", border_style="yellow"))
    console.print()
    console.print(Panel(AI_ROLE, title="🤖 Vai Trò AI Agent", border_style="green"))
    console.print()

    console.print("[bold]📋 Kiểm tra môi trường:[/bold]")
    env_ok = check_env()
    console.print()

    console.print("[bold]🔍 Kiểm tra dependencies:[/bold]")
    npx_ok = check_npx()

    # Check Python packages
    for pkg in ["mcp", "anthropic", "openai"]:
        try:
            __import__(pkg)
            console.print(f"  ✅ {pkg}: [green]installed[/green]")
        except ImportError:
            console.print(f"  ❌ {pkg}: [red]MISSING[/red]  →  pip install {pkg}")

    console.print()
    if env_ok and npx_ok:
        console.print(Panel.fit(
            "✅ [bold green]Sẵn sàng chạy![/bold green]\n\n"
            "  [bold]python src/flow_runner.py --ticket PROJ-1234 --skip-run[/bold]\n\n"
            "  Flags:\n"
            "    [cyan]--skip-run[/cyan]  = Chỉ fetch + analyze + generate (không chạy Appium)\n"
            "    [cyan]--dry-run[/cyan]   = Generate .robot file rồi in ra màn hình\n"
            "    [cyan]--platform ios[/cyan] = Chạy trên iOS thay vì Android",
            title="Next Steps",
        ))
    else:
        console.print(Panel.fit(
            "⚠️  [yellow]Cần cấu hình thêm trước khi chạy[/yellow]\n\n"
            "  1. Copy file cấu hình:\n"
            "     [cyan]cp .env.example .env[/cyan]\n\n"
            "  2. Điền thông tin vào .env:\n"
            "     [cyan]JIRA_MCP_URL, JIRA_EMAIL, JIRA_API_TOKEN[/cyan]\n"
            "     [cyan]AI_PROVIDER, AI_API_KEY[/cyan]\n\n"
            "  3. Chạy lại để kiểm tra:\n"
            "     [cyan]python src/mcp_flow_diagram.py[/cyan]",
            title="Setup Required",
            border_style="yellow",
        ))


if __name__ == "__main__":
    main()

