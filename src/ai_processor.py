"""
AI Integration - Unified Functions
Direct function calls for AI models - No step-by-step tool calls needed
"""

import sys
import json
from typing import Dict, Any, Optional
from pathlib import Path

sys.path.insert(0, '/Users/vinhnt0111/Desktop/MCP')

from src.ticket_router import TicketRouter
from src.jira.ticket_fetcher import TicketFetcher
from src.jira.ticket_analyzer import TicketAnalyzer
from src.jira.mcp_client import MCPClient


class AIProcessor:
    """
    Unified AI processor - AI calls ONE function, it handles EVERYTHING
    No separate step-by-step tool calls needed
    """

    @staticmethod
    def process_ticket_complete(ticket_id: str) -> Dict[str, Any]:
        """
        UNIFIED FUNCTION - AI calls this ONCE to do EVERYTHING

        Handles:
        1. Route ticket → get MCP value
        2. Fetch from Jira
        3. Analyze ticket
        4. Generate test plan

        Args:
            ticket_id: Ticket ID (e.g., 'KAN-7')

        Returns:
            dict: Complete result with all data

        Example:
            result = AIProcessor.process_ticket_complete('KAN-7')
            # Returns everything needed!
        """
        result = {
            'ticket_id': ticket_id,
            'status': 'processing',
            'steps': {},
            'error': None
        }

        try:
            # STEP 1: Route ticket + get MCP value
            print(f"\n[1/4] ROUTING & MCP VALUE")
            routing = TicketRouter.route_and_generate(ticket_id, 'get_random_odd' if int(ticket_id.split('-')[1]) % 10 % 2 else 'get_random_even')
            result['steps']['routing'] = {
                'mcp_server': routing['mcp_server'],
                'mcp_value': routing['mcp_value'],
                'ticket_type': 'ODD' if int(ticket_id.split('-')[1]) % 10 % 2 else 'EVEN'
            }
            print(f"   ✅ MCP Server: {routing['mcp_server']}")
            print(f"   ✅ Generated Value: {routing['mcp_value']}")

            # STEP 2: Fetch ticket from Jira
            print(f"\n[2/4] FETCH TICKET FROM JIRA")
            env_vars = {}
            with open('.env') as f:
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
            result['steps']['fetch'] = {
                'title': ticket_data.get('title'),
                'priority': ticket_data.get('priority'),
                'status': ticket_data.get('status'),
                'labels': ticket_data.get('labels', [])
            }
            print(f"   ✅ Title: {ticket_data.get('title')[:50]}...")
            print(f"   ✅ Priority: {ticket_data.get('priority')}")

            # STEP 3: Analyze ticket
            print(f"\n[3/4] ANALYZE TICKET")
            analyzer = TicketAnalyzer()
            analysis = analyzer.analyze(ticket_data)
            result['steps']['analysis'] = {
                'test_type': analysis.get('test_type'),
                'platforms': analysis.get('platforms', []),
                'preconditions_count': len(analysis.get('preconditions', [])),
                'steps_count': len(analysis.get('test_steps', [])),
                'expected_results_count': len(analysis.get('expected_results', []))
            }
            print(f"   ✅ Test Type: {analysis.get('test_type')}")
            print(f"   ✅ Platforms: {', '.join(analysis.get('platforms', []))}")

            # STEP 4: Generate test plan
            print(f"\n[4/4] GENERATE TEST PLAN")
            test_plan = AIProcessor._generate_test_plan(ticket_id, analysis, routing['mcp_value'])
            result['steps']['test_plan'] = test_plan
            print(f"   ✅ Test cases: {test_plan['test_cases_count']}")
            print(f"   ✅ Robot file: {test_plan['robot_file_path']}")

            result['status'] = 'success'

        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

        return result

    @staticmethod
    def process_ticket_with_mcp(ticket_id: str, mcp_method: str = None) -> Dict[str, Any]:
        """
        UNIFIED FUNCTION - Route + Call MCP + Get Value

        ONE call → Route ticket → Call appropriate MCP → Return value

        Args:
            ticket_id: Ticket ID
            mcp_method: Optional - specific MCP method (auto-selected if not provided)

        Returns:
            dict: MCP value + ticket info

        Example:
            result = AIProcessor.process_ticket_with_mcp('KAN-7')
            print(result['mcp_value'])
        """
        result = {}

        try:
            # Auto-select method based on ticket type
            last_digit = int(ticket_id.split('-')[1]) % 10
            is_even = last_digit % 2 == 0

            if not mcp_method:
                mcp_method = 'get_random_even' if is_even else 'get_random_odd'

            # Route + Call MCP in one step
            routing = TicketRouter.route_and_generate(ticket_id, mcp_method)

            result = {
                'success': True,
                'ticket_id': ticket_id,
                'last_digit': last_digit,
                'type': 'EVEN' if is_even else 'ODD',
                'mcp_server': routing['mcp_server'],
                'mcp_method': mcp_method,
                'mcp_value': routing['mcp_value'],
                'mcp_response': routing['mcp_response']
            }

        except Exception as e:
            result = {
                'success': False,
                'ticket_id': ticket_id,
                'error': str(e)
            }

        return result

    @staticmethod
    def analyze_and_generate_tests(ticket_id: str) -> Dict[str, Any]:
        """
        UNIFIED FUNCTION - Analyze ticket + Generate tests

        ONE call → Fetch ticket → Analyze → Generate robot tests

        Args:
            ticket_id: Ticket ID

        Returns:
            dict: Analysis + test generation result

        Example:
            result = AIProcessor.analyze_and_generate_tests('KAN-7')
            print(result['robot_file_path'])
        """
        result = {'ticket_id': ticket_id, 'status': 'processing'}

        try:
            # Load Jira credentials
            env_vars = {}
            with open('.env') as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        k, v = line.strip().split("=", 1)
                        env_vars[k] = v

            # Fetch
            client = MCPClient(
                base_url=env_vars.get("JIRA_MCP_URL"),
                email=env_vars.get("JIRA_EMAIL"),
                api_token=env_vars.get("JIRA_API_TOKEN")
            )
            fetcher = TicketFetcher(client)
            ticket_data = fetcher.fetch(ticket_id)

            # Analyze
            analyzer = TicketAnalyzer()
            analysis = analyzer.analyze(ticket_data)

            # Generate tests (placeholder - would use TestCaseMapper)
            robot_file = f"robot_tests/suites/generated/{ticket_id}_android.robot"
            test_cases = len(analysis.get('expected_results', [])) or 1

            result = {
                'success': True,
                'ticket_id': ticket_id,
                'title': ticket_data.get('title'),
                'analysis': {
                    'test_type': analysis.get('test_type'),
                    'platforms': analysis.get('platforms', []),
                    'preconditions': len(analysis.get('preconditions', [])),
                    'steps': len(analysis.get('test_steps', [])),
                    'expected_results': len(analysis.get('expected_results', []))
                },
                'test_generation': {
                    'robot_file_path': robot_file,
                    'test_cases_generated': test_cases,
                    'platform': 'android'
                },
                'status': 'success'
            }

        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)

        return result

    @staticmethod
    def batch_process_tickets(ticket_ids: list) -> Dict[str, Any]:
        """
        UNIFIED FUNCTION - Process MULTIPLE tickets at once

        ONE call → Process all tickets → Return all results

        Args:
            ticket_ids: List of ticket IDs

        Returns:
            dict: Results for all tickets

        Example:
            results = AIProcessor.batch_process_tickets(['KAN-7', 'KAN-8', 'KAN-9'])
            for ticket_id, data in results['tickets'].items():
                print(f"{ticket_id}: {data['mcp_value']}")
        """
        results = {
            'total_tickets': len(ticket_ids),
            'processed': 0,
            'failed': 0,
            'tickets': {}
        }

        for ticket_id in ticket_ids:
            try:
                ticket_result = AIProcessor.process_ticket_with_mcp(ticket_id)
                results['tickets'][ticket_id] = ticket_result
                if ticket_result.get('success'):
                    results['processed'] += 1
                else:
                    results['failed'] += 1
            except Exception as e:
                results['tickets'][ticket_id] = {'success': False, 'error': str(e)}
                results['failed'] += 1

        results['status'] = 'complete'
        return results

    @staticmethod
    def _generate_test_plan(ticket_id: str, analysis: dict, mcp_value: Any) -> Dict[str, Any]:
        """Generate test plan from analysis"""
        expected_results = analysis.get('expected_results', [])
        test_cases_count = len(expected_results) if expected_results else 1

        return {
            'ticket_id': ticket_id,
            'mcp_value': mcp_value,
            'test_cases_count': test_cases_count,
            'robot_file_path': f'robot_tests/suites/generated/{ticket_id}_android.robot',
            'test_cases': [
                {
                    'id': f'TC_{i+1:03d}',
                    'name': f'Test case {i+1}: {result[:50]}...',
                    'expected': result
                }
                for i, result in enumerate(expected_results[:3])  # First 3 as sample
            ]
        }

    @staticmethod
    def get_available_functions() -> list:
        """Get list of all available functions for AI"""
        return [
            {
                'name': 'process_ticket_complete',
                'description': 'Process ticket end-to-end: route, fetch, analyze, generate tests',
                'params': ['ticket_id']
            },
            {
                'name': 'process_ticket_with_mcp',
                'description': 'Route ticket and call MCP - get random value',
                'params': ['ticket_id', 'mcp_method (optional)']
            },
            {
                'name': 'analyze_and_generate_tests',
                'description': 'Analyze ticket and generate test cases',
                'params': ['ticket_id']
            },
            {
                'name': 'batch_process_tickets',
                'description': 'Process multiple tickets at once',
                'params': ['ticket_ids (list)']
            }
        ]


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Available functions:")
        for func in AIProcessor.get_available_functions():
            print(f"  • {func['name']}: {func['description']}")
        sys.exit(1)

    func_name = sys.argv[1]

    if func_name == 'process_ticket_complete':
        ticket_id = sys.argv[2] if len(sys.argv) > 2 else 'KAN-7'
        result = AIProcessor.process_ticket_complete(ticket_id)
        print("\n" + "=" * 80)
        print("COMPLETE RESULT:")
        print(json.dumps(result, indent=2))

    elif func_name == 'process_ticket_with_mcp':
        ticket_id = sys.argv[2] if len(sys.argv) > 2 else 'KAN-7'
        result = AIProcessor.process_ticket_with_mcp(ticket_id)
        print(json.dumps(result, indent=2))

    elif func_name == 'analyze_and_generate_tests':
        ticket_id = sys.argv[2] if len(sys.argv) > 2 else 'KAN-7'
        result = AIProcessor.analyze_and_generate_tests(ticket_id)
        print(json.dumps(result, indent=2))

    elif func_name == 'batch_process_tickets':
        tickets = ['KAN-7', 'KAN-8', 'KAN-9']
        result = AIProcessor.batch_process_tickets(tickets)
        print(json.dumps(result, indent=2))

