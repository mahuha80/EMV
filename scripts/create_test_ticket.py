#!/usr/bin/env python3
"""
Create a test Jira ticket - Demo script
This script creates a new test issue on Jira for testing purposes.
"""

import json
import logging
import os
import sys
from datetime import datetime
import requests
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Get Jira credentials
JIRA_URL = os.getenv("JIRA_MCP_URL", "").rstrip("/")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN", "")

if not all([JIRA_URL, JIRA_EMAIL, JIRA_TOKEN]):
    logger.error("❌ Missing Jira credentials! Set JIRA_MCP_URL, JIRA_EMAIL, JIRA_API_TOKEN in .env")
    sys.exit(1)


def create_test_ticket(project_key="PROJ", issue_type="Bug"):
    """
    Create a test ticket on Jira.

    Args:
        project_key: Jira project key (e.g., 'PROJ', 'KAN')
        issue_type: Issue type (e.g., 'Bug', 'Task', 'Story')

    Returns:
        dict: Created ticket information
    """

    # Generate unique summary with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary = f"[TEST] MCP Router Test Ticket - {timestamp}"

    # Create description using ADF format
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
                "content": [{"type": "text", "text": "This is a test ticket created by the MCP Router system to verify Jira integration and MCP server routing functionality."}]
            },
            {
                "type": "heading",
                "attrs": {"level": 3},
                "content": [{"type": "text", "text": "Test Scenario"}]
            },
            {
                "type": "bulletList",
                "content": [
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": f"Created: {datetime.now().isoformat()}"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Purpose: Test MCP ticket routing based on last digit"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Expected: Last digit determines which MCP server to call (even/odd)"}]}]}
                ]
            },
            {
                "type": "heading",
                "attrs": {"level": 3},
                "content": [{"type": "text", "text": "Steps"}]
            },
            {
                "type": "orderedList",
                "content": [
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Extract last digit from ticket number"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Check if even or odd"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Route to appropriate MCP server (random-even-mcp or random-odd-mcp)"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Generate random number and use in test"}]}]}
                ]
            }
        ]
    }

    # Prepare issue payload
    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": issue_type
            },
            "priority": {
                "name": "Medium"
            },
            "labels": ["test", "mcp-router", "automated"]
        }
    }

    # Create issue via Jira REST API v3
    endpoint = f"{JIRA_URL}/rest/api/3/issue"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    logger.info(f"🚀 Creating test ticket in project: {project_key}")
    logger.info(f"📝 Summary: {summary}")

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            auth=(JIRA_EMAIL, JIRA_TOKEN),
            timeout=30
        )

        if response.status_code in (401, 403):
            logger.error(f"❌ Authentication failed ({response.status_code})")
            logger.error(f"Response: {response.text}")
            raise Exception("Authentication failed. Check JIRA_EMAIL and JIRA_API_TOKEN")

        if response.status_code >= 400:
            logger.error(f"❌ Request failed ({response.status_code})")
            logger.error(f"Response: {response.text}")
            raise Exception(f"Failed to create ticket: {response.text}")

        result = response.json()
        ticket_id = result.get("key", "UNKNOWN")
        issue_id = result.get("id", "UNKNOWN")

        logger.info(f"✅ Ticket created successfully!")
        logger.info(f"📌 Ticket ID: {ticket_id}")
        logger.info(f"🔗 Link: {JIRA_URL}/browse/{ticket_id}")

        return {
            "ticket_id": ticket_id,
            "issue_id": issue_id,
            "project_key": project_key,
            "summary": summary,
            "created_at": datetime.now().isoformat(),
            "status": "success",
            "url": f"{JIRA_URL}/browse/{ticket_id}"
        }

    except requests.exceptions.ConnectionError as e:
        logger.error(f"❌ Connection error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Request error: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise


def save_result(result):
    """Save ticket creation result to file."""
    output_dir = Path("/Users/vinhnt0111/Desktop/MCP/reports/test_tickets")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{result['ticket_id']}_creation_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"💾 Result saved to: {output_file}")


if __name__ == "__main__":
    import sys

    # Get project key from command line or use default
    project_key = sys.argv[1] if len(sys.argv) > 1 else "PROJ"

    print("\n" + "=" * 70)
    print("🎫 JIRA TEST TICKET CREATION")
    print("=" * 70)
    print(f"Jira URL: {JIRA_URL}")
    print(f"Email: {JIRA_EMAIL}")
    print(f"Project: {project_key}")
    print("=" * 70 + "\n")

    try:
        result = create_test_ticket(project_key=project_key, issue_type="Bug")
        save_result(result)

        print("\n" + "=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print(f"Ticket ID: {result['ticket_id']}")
        print(f"URL: {result['url']}")
        print(f"Created: {result['created_at']}")
        print("=" * 70 + "\n")

        sys.exit(0)

    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ ERROR: {e}")
        print("=" * 70 + "\n")
        sys.exit(1)

