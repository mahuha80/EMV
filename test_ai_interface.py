#!/usr/bin/env python3
"""
Test AI Tool Interface
"""

import sys
import json
sys.path.insert(0, '/Users/vinhnt0111/Desktop/MCP')

from src.ai_tool_interface import AIToolInterface

print("\n" + "=" * 80)
print("🤖 AI TOOL INTERFACE - TESTING")
print("=" * 80)

# Test 1: Route ticket
print("\n[TEST 1] route_ticket - Route KAN-7 and call get_random_odd")
try:
    result = AIToolInterface.execute_tool('route_ticket', {
        'ticket_id': 'KAN-7',
        'mcp_method': 'get_random_odd'
    })
    print(f"✅ Ticket: {result['ticket_id']}")
    print(f"✅ MCP Server: {result['mcp_server']}")
    print(f"✅ Value: {result['value']}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Determine MCP server
print("\n[TEST 2] determine_mcp_server - Check which MCP for KAN-8")
try:
    result = AIToolInterface.execute_tool('determine_mcp_server', {
        'ticket_id': 'KAN-8'
    })
    print(f"✅ Ticket: {result['ticket_id']}")
    print(f"✅ Last Digit: {result['last_digit']}")
    print(f"✅ Type: {result['type']}")
    print(f"✅ MCP Server: {result['mcp_server']}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Call MCP even directly
print("\n[TEST 3] call_mcp_even - Get all even numbers")
try:
    result = AIToolInterface.execute_tool('call_mcp_even', {
        'method': 'get_all_evens'
    })
    print(f"✅ Even Numbers: {result['result']}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Call MCP odd directly
print("\n[TEST 4] call_mcp_odd - Get 3 random odd numbers")
try:
    result = AIToolInterface.execute_tool('call_mcp_odd', {
        'method': 'get_random_odds',
        'count': 3
    })
    print(f"✅ Odd Numbers: {result['result']}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ AI TOOL INTERFACE READY FOR CLAUDE/GPT-4")
print("=" * 80)
print("\n📊 Available Tools for AI:")
for tool in AIToolInterface.get_tool_schemas():
    print(f"  • {tool['name']}")
print("=" * 80 + "\n")

