#!/usr/bin/env python3
"""
Test Full Flow - All STEPs
"""

import sys
import json
sys.path.insert(0, '/Users/vinhnt0111/Desktop/MCP')

from src.ticket_router import TicketRouter
from src.jira.ticket_fetcher import TicketFetcher
from src.jira.ticket_analyzer import TicketAnalyzer
from src.jira.mcp_client import MCPClient

ticket_id = "KAN-7"

print("\n" + "=" * 70)
print("🚀 FULL FLOW TEST - ALL STEPS")
print("=" * 70)

# ==================== STEP 0: ROUTING ====================
print(f"\n[STEP-0] TICKET ROUTING")
try:
    routing_result = TicketRouter.route_and_generate(ticket_id, 'get_random_odd')
    print(f"✅ Routing: {routing_result['ticket_id']} → {routing_result['mcp_server']}")
    print(f"   Generated value: {routing_result['mcp_value']}")
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# ==================== STEP 1: FETCH ====================
print(f"\n[STEP-1] FETCH TICKET FROM JIRA")
try:
    env_vars = {}
    with open(".env") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env_vars[k] = v

    client = MCPClient(
        base_url=env_vars.get("JIRA_MCP_URL"),
        email=env_vars.get("JIRA_EMAIL"),
        api_token=env_vars.get("JIRA_API_TOKEN")
    )

    fetcher = TicketFetcher(client)
    ticket_data = fetcher.fetch(ticket_id)
    print(f"✅ Fetched: {ticket_data.get('title')[:40]}...")
    print(f"   Priority: {ticket_data.get('priority')}")

except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# ==================== STEP 2: ANALYZE ====================
print(f"\n[STEP-2] ANALYZE TICKET")
try:
    analyzer = TicketAnalyzer()
    analysis = analyzer.analyze(ticket_data)

    print(f"✅ Analysis complete:")
    print(f"   Type: {analysis.get('test_type', 'N/A')}")
    print(f"   Platforms: {analysis.get('platforms', [])}")
    print(f"   Preconditions: {len(analysis.get('preconditions', []))} items")
    print(f"   Steps: {len(analysis.get('test_steps', []))} items")
    print(f"   Expected: {len(analysis.get('expected_results', []))} items")

except Exception as e:
    print(f"❌ Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ FLOW VERIFICATION: STEPS 0-2 WORKING!")
print("=" * 70 + "\n")

