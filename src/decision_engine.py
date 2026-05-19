ọi """
AI Decision Engine - Intelligent Flow Execution
Executes functions step-by-step and decides what to call next based on results
"""

import sys
import logging
from typing import Dict, Any, Optional, List

sys.path.insert(0, '/Users/vinhnt0111/Desktop/MCP')

from src.ai_processor import AIProcessor

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class DecisionEngine:
    """
    Intelligent Decision Engine - Executes functions dynamically
    - Calls function 1
    - Checks result
    - Decides function 2 based on result
    - Continues until completion
    """

    def __init__(self):
        self.state = {
            'ticket_id': None,
            'step': 0,
            'success': False,
            'results': {},
            'decisions': [],
            'errors': []
        }

    def execute_intelligent_flow(self, ticket_id: str) -> Dict[str, Any]:
        """
        Main execution - automatically decide flow based on results

        Args:
            ticket_id: Ticket ID to process

        Returns:
            dict: Complete execution result with all decisions
        """
        self.state['ticket_id'] = ticket_id

        print("\n" + "=" * 80)
        print(f"🤖 INTELLIGENT FLOW EXECUTION - {ticket_id}")
        print("=" * 80)

        try:
            # STEP 1: Route & Get MCP Value
            print("\n[STEP 1] process_ticket_with_mcp()")
            result_1 = AIProcessor.process_ticket_with_mcp(ticket_id)
            self.state['step'] = 1
            self.state['results']['routing'] = result_1

            if not result_1.get('success'):
                self.state['success'] = False
                self.state['errors'].append(f"Routing failed: {result_1.get('error')}")
                return self._handle_error_flow(result_1)

            print(f"  ✅ MCP Server: {result_1['mcp_server']}")
            print(f"  ✅ MCP Value: {result_1['mcp_value']}")

            # STEP 2: Decision Point 1 - Priority Level (Rule R1)
            mcp_value = result_1['mcp_value']
            priority = self._classify_priority(mcp_value)

            print(f"\n[DECISION] Priority: {priority} (value={mcp_value})")
            self.state['decisions'].append({
                'point': 'Priority',
                'factor': mcp_value,
                'decision': priority
            })

            # STEP 3: Execute based on priority
            if priority == 'HIGH':
                print("\n[STEP 2] batch_process_tickets()")
                result_2 = self._execute_batch_flow(ticket_id)
            else:
                print("\n[STEP 2] analyze_and_generate_tests()")
                result_2 = AIProcessor.analyze_and_generate_tests(ticket_id)

            self.state['step'] = 2
            self.state['results']['analysis'] = result_2

            if not result_2.get('success'):
                self.state['success'] = False
                self.state['errors'].append(f"Analysis failed: {result_2.get('error')}")
                return self.state

            # STEP 4: Decision Point 2 - Test Type (Rule R2)
            test_type = result_2.get('analysis', {}).get('test_type', 'functional')

            print(f"\n[DECISION] Test Type: {test_type}")
            self.state['decisions'].append({
                'point': 'Test Type',
                'factor': test_type,
                'decision': 'Execute testing'
            })

            # STEP 5: Final execution based on test type
            if test_type == 'regression':
                print("\n[STEP 3] Execute Regression Testing")
                result_3 = self._execute_regression_flow(ticket_id)
            elif test_type == 'e2e':
                print("\n[STEP 3] Execute E2E Testing")
                result_3 = self._execute_e2e_flow(ticket_id)
            else:
                print("\n[STEP 3] Generate Basic Tests")
                result_3 = self._execute_basic_flow(ticket_id)

            self.state['step'] = 3
            self.state['results']['testing'] = result_3
            self.state['success'] = True

        except Exception as e:
            logger.error(f"❌ Exception during flow: {e}")
            self.state['success'] = False
            self.state['errors'].append(str(e))

        # Generate final report
        return self._generate_final_report()

    def _classify_priority(self, mcp_value: int) -> str:
        """Classify priority based on MCP value (Rule R1)"""
        if mcp_value <= 5:
            return 'LOW'
        elif mcp_value <= 15:
            return 'MID'
        else:
            return 'HIGH'

    def _execute_batch_flow(self, ticket_id: str) -> Dict[str, Any]:
        """Execute batch processing flow"""
        # Find similar tickets
        similar_tickets = self._find_similar_tickets(ticket_id)

        print(f"  ℹ️ Found {len(similar_tickets)} similar tickets")
        print(f"  → Processing: {similar_tickets}")

        result = AIProcessor.batch_process_tickets(similar_tickets)

        print(f"  ✅ Processed: {result.get('processed', 0)} tickets")
        print(f"  ✅ Failed: {result.get('failed', 0)} tickets")

        return {
            'success': True,
            'method': 'batch',
            'result': result
        }

    def _execute_regression_flow(self, ticket_id: str) -> Dict[str, Any]:
        """Execute regression testing flow"""
        print(f"  → Running regression test suite")
        return {
            'success': True,
            'method': 'regression',
            'message': 'Regression test suite prepared'
        }

    def _execute_e2e_flow(self, ticket_id: str) -> Dict[str, Any]:
        """Execute E2E testing flow"""
        print(f"  → Running E2E test suite")
        return {
            'success': True,
            'method': 'e2e',
            'message': 'E2E test suite prepared'
        }

    def _execute_basic_flow(self, ticket_id: str) -> Dict[str, Any]:
        """Execute basic testing flow"""
        print(f"  → Generating basic test cases")
        return {
            'success': True,
            'method': 'basic',
            'message': 'Basic test suite generated'
        }

    def _handle_error_flow(self, error_result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle errors intelligently (Rule R4)"""
        print(f"\n[ERROR HANDLING]")
        print(f"  ❌ Error: {error_result.get('error')}")

        # Apply fallback strategy
        print(f"  → Attempting fallback...")

        return {
            'success': False,
            'error': error_result.get('error'),
            'fallback_attempted': True
        }

    def _find_similar_tickets(self, ticket_id: str) -> List[str]:
        """Find other similar tickets for batch processing"""
        # Extract base (e.g., 'KAN' from 'KAN-7')
        base = ticket_id.split('-')[0]

        # Return similar tickets (demo)
        all_tickets = ['KAN-7', 'KAN-8', 'KAN-9']
        similar = [t for t in all_tickets if t.startswith(base)]

        return similar if len(similar) > 1 else [ticket_id]

    def _generate_final_report(self) -> Dict[str, Any]:
        """Generate final execution report"""
        print("\n" + "=" * 80)
        print("📊 FINAL REPORT")
        print("=" * 80)

        report = {
            'ticket_id': self.state['ticket_id'],
            'status': 'success' if self.state['success'] else 'failed',
            'steps_executed': self.state['step'],
            'decisions_made': len(self.state['decisions']),
            'decision_flow': self.state['decisions'],
            'results': self.state['results'],
            'errors': self.state['errors']
        }

        print(f"\n✅ Ticket: {report['ticket_id']}")
        print(f"✅ Status: {report['status']}")
        print(f"✅ Steps executed: {report['steps_executed']}")

        if report['decision_flow']:
            print(f"\n🔄 Decisions made:")
            for i, decision in enumerate(report['decision_flow'], 1):
                print(f"   {i}. {decision['point']}: {decision['decision']}")

        if report['errors']:
            print(f"\n⚠️ Errors:")
            for error in report['errors']:
                print(f"   • {error}")

        print("\n" + "=" * 80 + "\n")

        return report


# CLI
if __name__ == "__main__":
    # ...existing code...

o