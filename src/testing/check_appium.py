"""
Appium Connection Checker – Kiểm tra Appium server trước khi chạy tests
Chạy: python src/testing/check_appium.py
"""
import os
import sys
import requests
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

APPIUM_URL = os.getenv("APPIUM_SERVER_URL", "http://localhost:4723")


def check_appium_server() -> bool:
    """Kiểm tra Appium server có đang chạy không."""
    try:
        resp = requests.get(f"{APPIUM_URL}/status", timeout=5)
        data = resp.json()
        if resp.status_code == 200:
            console.print(f"  ✅ Appium server: [green]RUNNING[/green] at {APPIUM_URL}")
            version = data.get("value", {}).get("build", {}).get("version", "unknown")
            console.print(f"     Version: {version}")
            return True
    except Exception as e:
        console.print(f"  ❌ Appium server: [red]NOT REACHABLE[/red] at {APPIUM_URL}")
        console.print(f"     Error: {e}")
    return False


def check_env_vars() -> dict[str, bool]:
    """Kiểm tra các env var cần thiết."""
    required = {
        "APPIUM_SERVER_URL": os.getenv("APPIUM_SERVER_URL"),
        "ANDROID_DEVICE_NAME": os.getenv("ANDROID_DEVICE_NAME"),
        "ANDROID_APP_PACKAGE": os.getenv("ANDROID_APP_PACKAGE"),
        "ANDROID_APP_ACTIVITY": os.getenv("ANDROID_APP_ACTIVITY"),
        "JIRA_MCP_URL": os.getenv("JIRA_MCP_URL"),
        "JIRA_API_TOKEN": os.getenv("JIRA_API_TOKEN"),
    }
    return {k: bool(v) for k, v in required.items()}


def check_adb_devices() -> list[str]:
    """Lấy danh sách Android devices đang kết nối."""
    import subprocess
    try:
        result = subprocess.run(
            ["adb", "devices"], capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().splitlines()
        devices = [l.split("\t")[0] for l in lines[1:] if "device" in l and "offline" not in l]
        return devices
    except FileNotFoundError:
        return []
    except Exception:
        return []


def main() -> None:
    console.print("\n[bold cyan]🔍 Appium Environment Check[/bold cyan]\n")

    # Check env vars
    env_status = check_env_vars()
    table = Table(title="Environment Variables", box=box.ROUNDED)
    table.add_column("Variable", style="cyan")
    table.add_column("Status", style="white")
    for var, ok in env_status.items():
        status = "✅ Set" if ok else "❌ NOT SET"
        table.add_row(var, status)
    console.print(table)

    # Check ADB devices
    console.print("\n[bold]Android Devices (adb):[/bold]")
    devices = check_adb_devices()
    if devices:
        for d in devices:
            console.print(f"  📱 {d}")
    else:
        console.print("  ⚠️  No Android devices found (adb not available or no device)")

    # Check Appium server
    console.print("\n[bold]Appium Server:[/bold]")
    server_ok = check_appium_server()

    console.print()
    if server_ok:
        console.print("[bold green]✅ Ready to run tests![/bold green]")
        console.print("   Run: [cyan]python src/flow_runner.py --ticket PROJ-1234 --dry-run[/cyan]")
    else:
        console.print("[bold yellow]⚠️  Start Appium server first:[/bold yellow]")
        console.print("   [cyan]appium server --port 4723[/cyan]")
        console.print("   Or use --dry-run to skip actual test execution")
        sys.exit(1)


if __name__ == "__main__":
    main()

