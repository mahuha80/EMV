#!/usr/bin/env python3
"""
Create a real Jira test ticket - Updated version with correct project ID
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import sys

def main():
    # Read .env file
    env_vars = {}
    try:
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("❌ .env file not found!")
        sys.exit(1)

    JIRA_URL = env_vars.get("JIRA_MCP_URL", "").rstrip("/")
    JIRA_EMAIL = env_vars.get("JIRA_EMAIL", "")
    JIRA_TOKEN = env_vars.get("JIRA_API_TOKEN", "")

    if not all([JIRA_URL, JIRA_EMAIL, JIRA_TOKEN]):
        print("❌ Missing Jira credentials in .env")
        sys.exit(1)

    # Generate unique summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary = f"[TEST] MCP Router Test - {timestamp}"

    # Create description
    description = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "heading",
                "attrs": {"level": 3},
                "content": [{"type": "text", "text": "Purpose"}]
            },
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Test ticket for MCP Router - verifies Jira integration and MCP routing (even/odd by last digit)."}]
            },
            {
                "type": "heading",
                "attrs": {"level": 3},
                "content": [{"type": "text", "text": "Routing Info"}]
            },
            {
                "type": "bulletList",
                "content": [
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Created by MCP Router test script"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Last digit of ticket determines which MCP to use"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Even = random-even-mcp, Odd = random-odd-mcp"}]}]}
                ]
            }
        ]
    }

    # Prepare payload
    payload = {
        "fields": {
            "project": {"id": "10000"},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"},
            "priority": {"name": "Medium"},
            "labels": ["test", "mcp-router", "automated"]
        }
    }

    # Display info
    print("\n" + "=" * 70)
    print("🎫 CREATING JIRA TEST TICKET")
    print("=" * 70)
    print(f"Project: My Software Team (KAN)")
    print(f"Issue Type: Bug")
    print(f"Summary: {summary}")
    print("=" * 70)

    # Create issue
    try:
        response = requests.post(
            f"{JIRA_URL}/rest/api/3/issue",
            json=payload,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=(JIRA_EMAIL, JIRA_TOKEN),
            timeout=30
        )

        if response.status_code >= 400:
            print(f"\n❌ Error ({response.status_code}): {response.text}")
            sys.exit(1)

        result = response.json()
        ticket_id = result.get("key")
        issue_id = result.get("id")

        print(f"\n✅ TICKET CREATED!")
        print("=" * 70)
        print(f"📌 Ticket ID: {ticket_id}")
        print(f"🔗 URL: {JIRA_URL}/browse/{ticket_id}")
        print("=" * 70)

        # Extract routing info
        import re
        match = re.search(r'-(\d+)$', ticket_id)
        if match:
            last_digit = int(match.group(1)) % 10
            is_even = last_digit % 2 == 0
            mcp_server = "random-even-mcp" if is_even else "random-odd-mcp"

            print(f"\n🔄 MCP ROUTING:")
            print(f"   Last Digit: {last_digit}")
            print(f"   Type: {'EVEN' if is_even else 'ODD'}")
            print(f"   MCP Server: {mcp_server}")
            print("=" * 70)

        # Save result
        output_dir = Path("reports/test_tickets")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{ticket_id}_creation.json"

        with open(output_file, "w") as f:
            json.dump({
                "ticket_id": ticket_id,
                "issue_id": issue_id,
                "summary": summary,
                "url": f"{JIRA_URL}/browse/{ticket_id}",
                "created_at": datetime.now().isoformat(),
                "status": "success"
            }, f, indent=2)

        print(f"\n💾 Saved to: {output_file}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

