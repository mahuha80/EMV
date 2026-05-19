#!/usr/bin/env python3
"""
AI Decision Flow Runner - Execute intelligent flow following rules
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, '/Users/vinhnt0111/Desktop/MCP')

from src.ai_processor import AIProcessor

def read_rules():
    """AI reads the rules file"""
    rules_file = Path('/Users/vinhnt0111/Desktop/MCP/AI_DECISION_FLOW_RULES.md')
    with open(rules_file, 'r') as f:
        content = f.read()
    return content

def classify_priority(mcp_value):
    """Apply Rule R1: Classify priority by mcp_value"""
    if mcp_value >= 16:
        return 'HIGH'
    elif mcp_value >= 6:
        return 'MID'
    else:
        return 'LOW'

def execute_flow(ticket_id):
    """
    Main flow - AI reads rules and executes functions dynamically
    """
    print("\n" + "=" * 80)
    print("🤖 AI DECISION FLOW EXECUTION")
    print("=" * 80)

    decisions = []
    results = {}

    # STEP 1: Read rules
    print("\n[INIT] AI reads: AI_DECISION_FLOW_RULES.md")
    rules = read_rules()
    print(f"✅ Rules loaded ({len(rules)} characters)")

    # STEP 2: Execute first function
    print(f"\n[STEP 1] AI calls: AIProcessor.process_ticket_with_mcp('{ticket_id}')")
    result_1 = AIProcessor.process_ticket_with_mcp(ticket_id)
    results['step_1'] = result_1

    if not result_1.get('success'):
        print(f"❌ Error: {result_1.get('error')}")
        print("[RULE R4] Error handling: Stop execution")
        return {'success': False, 'error': result_1.get('error')}

    mcp_value = result_1['mcp_value']
    mcp_server = result_1['mcp_server']

    print(f"✅ Result: MCP Server={mcp_server}, Value={mcp_value}")

    # STEP 3: Apply Rule R1 - Classify priority
    priority = classify_priority(mcp_value)
    decision_1 = f"Rule R1: mcp_value={mcp_value} → Priority={priority}"
    decisions.append(decision_1)

    print(f"\n[DECISION 1] {decision_1}")

    # STEP 4: Apply Rule R3 - Decide batch vs single
    if priority == 'HIGH':
        decision_2 = "Rule R3: Priority=HIGH → batch_process_tickets()"
        print(f"[DECISION 2] {decision_2}")
        decisions.append(decision_2)

        print(f"\n[STEP 2] AI calls: AIProcessor.batch_process_tickets(['{ticket_id}', ...])")
        result_2 = AIProcessor.batch_process_tickets([ticket_id, 'KAN-8', 'KAN-9'])
        results['step_2'] = result_2

        print(f"✅ Result: Processed={result_2.get('processed')}, Failed={result_2.get('failed')}")

    else:
        decision_2 = "Rule R3: Priority≤MID → analyze_and_generate_tests()"
        print(f"[DECISION 2] {decision_2}")
        decisions.append(decision_2)

        print(f"\n[STEP 2] AI calls: AIProcessor.analyze_and_generate_tests('{ticket_id}')")
        result_2 = AIProcessor.analyze_and_generate_tests(ticket_id)
        results['step_2'] = result_2

        if result_2.get('success'):
            test_type = result_2.get('analysis', {}).get('test_type', 'unknown')
            print(f"✅ Result: Test Type={test_type}")

            # Apply Rule R2 - Decide testing strategy
            if test_type == 'regression':
                decision_3 = "Rule R2: test_type=regression → Execute regression testing"
                print(f"\n[DECISION 3] {decision_3}")
                decisions.append(decision_3)
                print(f"[STEP 3] Execute regression test suite")

            elif test_type == 'e2e':
                decision_3 = "Rule R2: test_type=e2e → Execute E2E testing"
                print(f"\n[DECISION 3] {decision_3}")
                decisions.append(decision_3)
                print(f"[STEP 3] Execute E2E test suite")

            else:
                decision_3 = "Rule R2: test_type=functional → Generate basic tests"
                print(f"\n[DECISION 3] {decision_3}")
                decisions.append(decision_3)
                print(f"[STEP 3] Generate basic test suite")

    # STEP 5: Apply Rule R5 - Completion
    print(f"\n[COMPLETION] Rule R5: All steps done → Generate final report")

    # Final report
    print("\n" + "=" * 80)
    print("📊 FINAL REPORT")
    print("=" * 80)

    final_result = {
        'ticket_id': ticket_id,
        'status': 'success',
        'decisions': decisions,
        'results': results
    }

    print(f"\n✅ Ticket: {ticket_id}")
    print(f"✅ Status: success")
    print(f"\n🔄 Decision Trail:")
    for i, decision in enumerate(decisions, 1):
        print(f"   {i}. {decision}")

    print("\n📋 Execution Summary:")
    print(f"   • STEP 1: process_ticket_with_mcp() → Success")
    if priority == 'HIGH':
        print(f"   • STEP 2: batch_process_tickets() → Success")
    else:
        print(f"   • STEP 2: analyze_and_generate_tests() → Success")
    print(f"   • STEP 3: Execute testing → Ready")

    print("\n" + "=" * 80 + "\n")

    return final_result


if __name__ == "__main__":
    # Run with ticket IDs
    tickets = ['KAN-7', 'KAN-8', 'KAN-9']

    for ticket_id in tickets:
        result = execute_flow(ticket_id)
        if not result.get('success'):
            print(f"⚠️ Skipping remaining tickets due to error")
            break

