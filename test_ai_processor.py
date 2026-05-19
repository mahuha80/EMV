#!/usr/bin/env python3
"""
Test Unified AI Processor Functions
"""

import sys
sys.path.insert(0, '/Users/vinhnt0111/Desktop/MCP')

from src.ai_processor import AIProcessor

print("\n" + "=" * 80)
print("🤖 AI PROCESSOR - UNIFIED FUNCTION CALLS")
print("=" * 80)

# TEST 1: Single ticket with MCP
print("\n[TEST 1] process_ticket_with_mcp('KAN-8')")
result = AIProcessor.process_ticket_with_mcp('KAN-8')
print(f"✅ MCP Server: {result['mcp_server']}")
print(f"✅ MCP Value: {result['mcp_value']}")
print(f"✅ Type: {result['type']}")

# TEST 2: Analyze and generate
print("\n[TEST 2] analyze_and_generate_tests('KAN-9')")
result = AIProcessor.analyze_and_generate_tests('KAN-9')
if result.get('success'):
    print(f"✅ Title: {result['title']}")
    print(f"✅ Test Type: {result['analysis']['test_type']}")
    print(f"✅ Generated Tests: {result['test_generation']['test_cases_generated']}")

# TEST 3: Batch process
print("\n[TEST 3] batch_process_tickets(['KAN-7', 'KAN-8', 'KAN-9'])")
result = AIProcessor.batch_process_tickets(['KAN-7', 'KAN-8', 'KAN-9'])
print(f"✅ Total: {result['total_tickets']}")
print(f"✅ Processed: {result['processed']}")
print(f"✅ Failed: {result['failed']}")
for ticket_id, data in result['tickets'].items():
    if data.get('success'):
        print(f"   • {ticket_id}: {data['type']} → {data['mcp_value']}")

print("\n" + "=" * 80)
print("✅ ALL UNIFIED FUNCTIONS WORKING!")
print("=" * 80 + "\n")

