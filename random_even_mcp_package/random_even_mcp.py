"""
RandomEvenLibrary MCP Server
Model Context Protocol server for random even numbers
"""

import json
import sys
import logging
from typing import Any
import random

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RandomEvenLibrary-MCP")

class RandomEvenMCP:
    """MCP Server for RandomEvenLibrary"""

    def __init__(self):
        self.even_numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        self.tools = {
            "get_random_even": self.get_random_even,
            "get_random_evens": self.get_random_evens,
            "get_all_evens": self.get_all_evens,
            "validate_even": self.validate_even,
        }

    def get_random_even(self):
        """Get a random even number"""
        return {"number": random.choice(self.even_numbers)}

    def get_random_evens(self, count: int = 5):
        """Get N random even numbers"""
        count = int(count)
        return {"numbers": [random.choice(self.even_numbers) for _ in range(count)]}

    def get_all_evens(self):
        """Get all even numbers"""
        return {"numbers": self.even_numbers}

    def validate_even(self, number: int):
        """Validate if number is even"""
        try:
            num = int(number)
            is_valid = num in self.even_numbers
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
    server = RandomEvenMCP()

    logger.info("RandomEvenLibrary MCP Server started")

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
            logger.info("RandomEvenLibrary MCP Server stopped")
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

