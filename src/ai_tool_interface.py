"""
AI Tool Interface - Allow AI models to call MCP libraries directly
Supports Claude, GPT-4, and other Claude models via tool definitions
"""

import json
from typing import Dict, Any, List
from src.ticket_router import TicketRouter

class AIToolInterface:
    """
    Defines all tools that AI models can call to interact with MCP libraries.
    Provides OpenAI/Anthropic compatible tool schemas.
    """

    # Tool definitions for Claude/GPT-4
    TOOLS = [
        {
            "name": "route_ticket",
            "description": "Route a ticket to appropriate MCP server based on last digit (even/odd)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "Ticket ID (e.g., 'PROJ-1234' or 'KAN-7')"
                    },
                    "mcp_method": {
                        "type": "string",
                        "enum": [
                            "get_random_even",
                            "get_random_evens",
                            "get_all_evens",
                            "validate_even",
                            "get_random_odd",
                            "get_random_odds",
                            "get_all_odds",
                            "validate_odd"
                        ],
                        "description": "MCP method to call (auto-selected based on ticket)"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Count parameter for methods like get_random_evens/get_random_odds (optional)"
                    }
                },
                "required": ["ticket_id", "mcp_method"]
            }
        },
        {
            "name": "determine_mcp_server",
            "description": "Determine which MCP server to use for a ticket ID based on last digit",
            "input_schema": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "Ticket ID (e.g., 'PROJ-1234' or 'KAN-7')"
                    }
                },
                "required": ["ticket_id"]
            }
        },
        {
            "name": "call_mcp_even",
            "description": "Call random-even-mcp library directly with specific method",
            "input_schema": {
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "enum": [
                            "get_random_even",
                            "get_random_evens",
                            "get_all_evens",
                            "validate_even"
                        ],
                        "description": "Method to call in random-even-mcp"
                    },
                    "number": {
                        "type": "integer",
                        "description": "Number parameter for validation methods (optional)"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Count parameter for get_random_evens (optional)"
                    }
                },
                "required": ["method"]
            }
        },
        {
            "name": "call_mcp_odd",
            "description": "Call random-odd-mcp library directly with specific method",
            "input_schema": {
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "enum": [
                            "get_random_odd",
                            "get_random_odds",
                            "get_all_odds",
                            "validate_odd"
                        ],
                        "description": "Method to call in random-odd-mcp"
                    },
                    "number": {
                        "type": "integer",
                        "description": "Number parameter for validation methods (optional)"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Count parameter for get_random_odds (optional)"
                    }
                },
                "required": ["method"]
            }
        }
    ]

    @staticmethod
    def route_ticket(ticket_id: str, mcp_method: str, count: int = None) -> Dict[str, Any]:
        """
        AI-callable function: Route ticket and call MCP method

        Args:
            ticket_id: Ticket ID (e.g., 'PROJ-1234')
            mcp_method: MCP method to call
            count: Optional count for methods needing it

        Returns:
            dict: MCP response with result
        """
        params = {}
        if count:
            params['count'] = count

        result = TicketRouter.route_and_generate(ticket_id, mcp_method, params)

        return {
            "success": True,
            "ticket_id": result['ticket_id'],
            "mcp_server": result['mcp_server'],
            "method": mcp_method,
            "value": result['mcp_value'],
            "full_response": result['mcp_response']
        }

    @staticmethod
    def determine_mcp_server(ticket_id: str) -> Dict[str, Any]:
        """
        AI-callable function: Just determine which MCP server for a ticket

        Args:
            ticket_id: Ticket ID (e.g., 'PROJ-1234')

        Returns:
            dict: MCP server name and reasoning
        """
        mcp_server = TicketRouter.determine_mcp_server(ticket_id)

        # Extract info for response
        last_digit = TicketRouter.extract_last_digit(ticket_id)
        is_even = last_digit % 2 == 0

        return {
            "success": True,
            "ticket_id": ticket_id,
            "last_digit": last_digit,
            "type": "EVEN" if is_even else "ODD",
            "mcp_server": mcp_server,
            "reasoning": f"Ticket {ticket_id} ends with {last_digit} which is {'even' if is_even else 'odd'}, so route to {mcp_server}"
        }

    @staticmethod
    def call_mcp_even(method: str, number: int = None, count: int = None) -> Dict[str, Any]:
        """
        AI-callable function: Call random-even-mcp directly

        Args:
            method: Method name (get_random_even, get_random_evens, etc)
            number: For validation
            count: For get_random_evens

        Returns:
            dict: MCP response
        """
        params = {}
        if number is not None:
            params['number'] = number
        if count is not None:
            params['count'] = count

        response = TicketRouter.call_mcp_server('random-even-mcp', method, params)

        return {
            "success": True,
            "mcp_server": "random-even-mcp",
            "method": method,
            "result": response['result'],
            "full_response": response
        }

    @staticmethod
    def call_mcp_odd(method: str, number: int = None, count: int = None) -> Dict[str, Any]:
        """
        AI-callable function: Call random-odd-mcp directly

        Args:
            method: Method name (get_random_odd, get_random_odds, etc)
            number: For validation
            count: For get_random_odds

        Returns:
            dict: MCP response
        """
        params = {}
        if number is not None:
            params['number'] = number
        if count is not None:
            params['count'] = count

        response = TicketRouter.call_mcp_server('random-odd-mcp', method, params)

        return {
            "success": True,
            "mcp_server": "random-odd-mcp",
            "method": method,
            "result": response['result'],
            "full_response": response
        }

    @staticmethod
    def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main handler for AI to execute any tool
        AI systems call this with tool_name and parameters

        Args:
            tool_name: Name of tool (route_ticket, call_mcp_even, etc)
            tool_input: Tool parameters as dict

        Returns:
            dict: Tool execution result

        Example:
            result = execute_tool('route_ticket', {
                'ticket_id': 'KAN-7',
                'mcp_method': 'get_random_odd'
            })
        """
        try:
            if tool_name == 'route_ticket':
                return AIToolInterface.route_ticket(
                    ticket_id=tool_input['ticket_id'],
                    mcp_method=tool_input['mcp_method'],
                    count=tool_input.get('count')
                )

            elif tool_name == 'determine_mcp_server':
                return AIToolInterface.determine_mcp_server(
                    ticket_id=tool_input['ticket_id']
                )

            elif tool_name == 'call_mcp_even':
                return AIToolInterface.call_mcp_even(
                    method=tool_input['method'],
                    number=tool_input.get('number'),
                    count=tool_input.get('count')
                )

            elif tool_name == 'call_mcp_odd':
                return AIToolInterface.call_mcp_odd(
                    method=tool_input['method'],
                    number=tool_input.get('number'),
                    count=tool_input.get('count')
                )

            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                    "available_tools": [t['name'] for t in AIToolInterface.TOOLS]
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

    @staticmethod
    def get_tool_schemas() -> List[Dict[str, Any]]:
        """
        Get all tool schemas for AI models (Claude, GPT-4, etc)

        Usage with Claude:
            client = Anthropic()
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                tools=AIToolInterface.get_tool_schemas(),
                messages=[{
                    "role": "user",
                    "content": "Route ticket KAN-7 and call the MCP"
                }]
            )
        """
        return AIToolInterface.TOOLS


if __name__ == "__main__":
    import sys

    # Test usage
    if len(sys.argv) < 2:
        print("Usage: python3 ai_tool_interface.py <tool_name> <tool_input_json>")
        print("\nExample:")
        print('  python3 ai_tool_interface.py route_ticket \'{"ticket_id":"KAN-7","mcp_method":"get_random_odd"}\'')
        sys.exit(1)

    tool_name = sys.argv[1]
    tool_input_str = sys.argv[2] if len(sys.argv) > 2 else "{}"

    try:
        tool_input = json.loads(tool_input_str)
        result = AIToolInterface.execute_tool(tool_name, tool_input)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

