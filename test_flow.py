#!/usr/bin/env python3
"""
Test Full Flow - STEP 0 & STEP 1
"""

import sys
sys.path.insert(0, '/Users/vinhnt0111/Desktop/MCP')

from src.ticket_router import TicketRouter
from src.jira.ticket_fetcher import TicketFetcher
from src.jira.mcp_client import MCPClient

ticket_id = "KAN-7"

print("\n" + "=" * 70)
print("🚀 RUNNING FULL FLOW TEST - STEP 0 & STEP 1")
print("=" * 70)

# ==================== STEP 0: ROUTING ====================
print(f"\n📋 STEP 0: TICKET ROUTING")
print("-" * 70)

try:
    routing_result = TicketRouter.route_and_generate(ticket_id, 'get_random_odd')
    print(f"✅ Ticket routed successfully!")
    print(f"   Ticket: {routing_result['ticket_id']}")
    print(f"   MCP Server: {routing_result['mcp_server']}")
    print(f"   Generated Value: {routing_result['mcp_value']}")
    mcp_value = routing_result['mcp_value']
except Exception as e:
    print(f"❌ Routing failed: {e}")
    sys.exit(1)

# ==================== STEP 1: FETCH TICKET ====================
print(f"\n📋 STEP 1: FETCH TICKET FROM JIRA")
print("-" * 70)

try:
    # Load credentials
    env_vars = {}
    with open(".env") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env_vars[k] = v

    # Create client and fetch
    client = MCPClient(
        base_url=env_vars.get("JIRA_MCP_URL"),
        email=env_vars.get("JIRA_EMAIL"),
        api_token=env_vars.get("JIRA_API_TOKEN")
    )

    fetcher = TicketFetcher(client)
    ticket_data = fetcher.fetch(ticket_id)

    print(f"✅ TICKET FETCHED SUCCESSFULLY!")
    print(f"   Ticket ID: {ticket_data.get('ticket_id')}")
    print(f"   Title: {ticket_data.get('title')[:50]}...")
    print(f"   Priority: {ticket_data.get('priority')}")
    print(f"   Status: {ticket_data.get('status')}")
    print(f"   Labels: {', '.join(ticket_data.get('labels', []))}")

except Exception as e:
    print(f"❌ Fetch failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ STEP 0 & STEP 1 COMPLETED SUCCESSFULLY!")
print("=" * 70 + "\n")

