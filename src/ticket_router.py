"""
Ticket Number Router - MCP Integration Module
Check ticket number and route to appropriate MCP server (even/odd)
"""

import re
import json
import subprocess
import sys
import logging
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TicketRouter:
    """Route tickets based on last digit to appropriate MCP server"""
    
    EVEN_MCP = 'random-even-mcp'
    ODD_MCP = 'random-odd-mcp'
    
    EVEN_DIGITS = {0, 2, 4, 6, 8}
    ODD_DIGITS = {1, 3, 5, 7, 9}
    
    @staticmethod
    def extract_last_digit(ticket_id: str) -> int:
        """
        Extract last digit from ticket ID.
        
        Args:
            ticket_id (str): Ticket ID, e.g., 'PROJ-1234' or 'KAN-5'
        
        Returns:
            int: Last digit (0-9)
        
        Raises:
            ValueError: If ticket_id format is invalid
        """
        match = re.search(r'-(\d+)$', ticket_id)
        if not match:
            raise ValueError(f"Invalid ticket ID format: {ticket_id}. Expected format: PROJ-1234")
        
        number = int(match.group(1))
        last_digit = number % 10
        
        logger.debug(f"[ROUTE] Extracted last digit from {ticket_id}: {last_digit}")
        return last_digit
    
    @staticmethod
    def determine_mcp_server(ticket_id: str) -> str:
        """
        Determine which MCP server to call based on ticket number.
        
        Args:
            ticket_id (str): Ticket ID, e.g., 'PROJ-1234'
        
        Returns:
            str: MCP server name ('random-even-mcp' or 'random-odd-mcp')
        
        Examples:
            >>> determine_mcp_server('PROJ-1234')
            'random-even-mcp'  # Last digit: 4 (even)
            
            >>> determine_mcp_server('KAN-5')
            'random-odd-mcp'  # Last digit: 5 (odd)
        """
        last_digit = TicketRouter.extract_last_digit(ticket_id)
        
        if last_digit in TicketRouter.EVEN_DIGITS:
            mcp_server = TicketRouter.EVEN_MCP
            number_type = 'EVEN'
        else:
            mcp_server = TicketRouter.ODD_MCP
            number_type = 'ODD'
        
        logger.info(f"[STEP-0] Ticket: {ticket_id} | Last Digit: {last_digit} | Type: {number_type} | MCP: {mcp_server}")
        return mcp_server
    
    @staticmethod
    def call_mcp_server(mcp_name: str, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Call appropriate MCP server.
        
        Args:
            mcp_name (str): 'random-even-mcp' or 'random-odd-mcp'
            method (str): Method name to call
            params (dict): Method parameters
        
        Returns:
            dict: MCP response
        
        Raises:
            MCPError: If MCP call fails
            TimeoutError: If MCP server timeout
        
        Examples:
            >>> result = call_mcp_server('random-even-mcp', 'get_random_even')
            >>> print(result['result']['number'])
        """
        if params is None:
            params = {}
        
        import shutil
        
        # Find MCP script path
        # Convert 'random-even-mcp' to 'random_even_mcp_package/random_even_mcp.py'
        normalized_name = mcp_name.replace('-', '_')
        script_path = shutil.which(f'{mcp_name}_server') or f'/Users/vinhnt0111/Desktop/MCP/{normalized_name}_package/{normalized_name}.py'

        logger.debug(f"[STEP-0] Calling MCP: {mcp_name} | Method: {method} | Params: {params}")
        
        try:
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            request = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": 1
            }
            
            # Send request
            process.stdin.write(json.dumps(request) + "\n")
            process.stdin.flush()
            
            # Read response
            response_line = process.stdout.readline()
            
            if not response_line:
                stderr_output = process.stderr.read()
                logger.error(f"[STEP-0] MCP no response. Stderr: {stderr_output}")
                raise RuntimeError(f"MCP server returned no response: {stderr_output}")
            
            response = json.loads(response_line)
            
            # Check for errors
            if 'error' in response:
                error_msg = response['error']
                logger.error(f"[STEP-0] MCP error: {error_msg}")
                raise RuntimeError(f"MCP error: {error_msg}")
            
            logger.info(f"[STEP-0] MCP call successful | Response: {response['result']}")
            return response
            
        except subprocess.TimeoutExpired:
            logger.error(f"[STEP-0] MCP timeout after 30s")
            raise TimeoutError("MCP server timeout after 30 seconds")
        except json.JSONDecodeError as e:
            logger.error(f"[STEP-0] Invalid JSON response from MCP: {e}")
            raise RuntimeError(f"Invalid JSON from MCP: {e}")
        except Exception as e:
            logger.error(f"[STEP-0] Unexpected MCP error: {e}")
            raise
        finally:
            try:
                process.terminate()
                process.wait(timeout=2)
            except:
                process.kill()
    
    @staticmethod
    def route_and_generate(ticket_id: str, mcp_method: str = 'get_random_even', mcp_params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Complete routing and MCP call in one step.
        
        Args:
            ticket_id (str): Ticket ID
            mcp_method (str): MCP method to call (will use appropriate server based on routing)
            mcp_params (dict): MCP method parameters
        
        Returns:
            dict: Contains routing info and MCP response
        
        Examples:
            >>> result = route_and_generate('PROJ-1234', 'get_random_even')
            >>> print(f"Generated value: {result['mcp_value']}")
        """
        logger.info(f"[STEP-0] ========== TICKET ROUTING START ==========")
        logger.info(f"[STEP-0] Ticket ID: {ticket_id}")
        
        # Determine MCP server
        mcp_server = TicketRouter.determine_mcp_server(ticket_id)
        
        # Call MCP
        mcp_response = TicketRouter.call_mcp_server(mcp_server, mcp_method, mcp_params)
        
        # Extract value
        mcp_value = mcp_response['result'].get('number') or mcp_response['result'].get('numbers')
        
        result = {
            'ticket_id': ticket_id,
            'mcp_server': mcp_server,
            'mcp_method': mcp_method,
            'mcp_value': mcp_value,
            'mcp_response': mcp_response,
            'status': 'success'
        }
        
        logger.info(f"[STEP-0] Generated Value: {mcp_value}")
        logger.info(f"[STEP-0] ========== TICKET ROUTING COMPLETE ==========")
        
        return result


# CLI usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Route ticket to appropriate MCP server")
    parser.add_argument('ticket_id', help='Ticket ID (e.g., PROJ-1234)')
    parser.add_argument('--method', default='get_random_even', help='MCP method to call')
    parser.add_argument('--count', type=int, help='Count parameter for MCP methods')
    
    args = parser.parse_args()
    
    try:
        # Prepare params
        params = {}
        if args.count:
            params['count'] = args.count
        
        # Route and call
        result = TicketRouter.route_and_generate(args.ticket_id, args.method, params)
        
        # Output result
        print("\n" + "=" * 60)
        print("ROUTING RESULT")
        print("=" * 60)
        print(f"Ticket ID: {result['ticket_id']}")
        print(f"MCP Server: {result['mcp_server']}")
        print(f"Generated Value: {result['mcp_value']}")
        print("=" * 60 + "\n")
        
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)

