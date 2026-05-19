"""
RandomOddLibrary MCP Server
Model Context Protocol server for random odd numbers
"""

import json
import sys
import logging
from typing import Any
import random

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RandomOddLibrary-MCP")

class RandomOddMCP:
    """MCP Server for RandomOddLibrary"""

    def __init__(self):
        self.odd_numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        self.tools = {
            "get_random_odd": self.get_random_odd,
            "get_random_odds": self.get_random_odds,
            "get_all_odds": self.get_all_odds,
            "validate_odd": self.validate_odd,
        }

    def get_random_odd(self):
        """Get a random odd number"""
        return {"number": random.choice(self.odd_numbers)}

    def get_random_odds(self, count: int = 5):
        """Get N random odd numbers"""
        count = int(count)
        return {"numbers": [random.choice(self.odd_numbers) for _ in range(count)]}

    def get_all_odds(self):
        """Get all odd numbers"""
        return {"numbers": self.odd_numbers}

    def validate_odd(self, number: int):
        """Validate if number is odd"""
        try:
            num = int(number)
            is_valid = num in self.odd_numbers
            return {"number": num, "is_valid": is_valid}
        except (ValueError, TypeError):
            return {"number": number, "is_valid": False, "error": "Invalid number"}

    def handle_request(self, request: dict) -> dict:
        """Handle MCP request"""
        try:
            method = request.get("method")
            params = request.get("params", {})

            if method not in self.tools:
                return {
                    "error": f"Method '{method}' not found",
                    "code": -32601
                }

            result = self.tools[method](**params) if params else self.tools[method]()
            return {
                "result": result,
                "jsonrpc": "2.0",
                "id": request.get("id")
            }
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "error": str(e),
                "code": -32603,
                "id": request.get("id")
            }

def main():
    """Main MCP server loop"""
    server = RandomOddMCP()

    logger.info("RandomOddLibrary MCP Server started")

    while True:
        try:
            line = input()
            if not line:
                continue

            request = json.loads(line)
            response = server.handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()

        except json.JSONDecodeError:
            error_response = {
                "error": "Invalid JSON",
                "code": -32700
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
        except KeyboardInterrupt:
            logger.info("RandomOddLibrary MCP Server stopped")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            error_response = {
                "error": str(e),
                "code": -32603
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()

