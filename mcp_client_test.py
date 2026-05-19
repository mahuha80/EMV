#!/usr/bin/env python3
"""
MCP Client for RandomEvenLibrary and RandomOddLibrary
Demonstrates how to use the MCP servers
"""

import json
import subprocess
import sys
from pathlib import Path


class MCPClient:
    """Client for communicating with MCP servers"""

    def __init__(self, mcp_script_path):
        """Initialize MCP client"""
        self.process = subprocess.Popen(
            [sys.executable, mcp_script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def send_request(self, method, params=None, request_id=1):
        """Send a request to MCP server"""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": request_id
        }

        try:
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()

            response_line = self.process.stdout.readline()
            if response_line:
                return json.loads(response_line)
            return None
        except (json.JSONDecodeError, BrokenPipeError) as e:
            print(f"Error: {e}")
            return None

    def close(self):
        """Close the process"""
        self.process.terminate()
        self.process.wait(timeout=5)


def test_random_even_mcp():
    """Test RandomEvenLibrary MCP server"""
    print("=" * 60)
    print("Testing RandomEvenLibrary MCP Server")
    print("=" * 60)

    script_path = "/Users/vinhnt0111/Desktop/MCP/random_even_mcp_package/random_even_mcp.py"
    client = MCPClient(script_path)

    try:
        # Test 1: Get random even number
        print("\n1. Get Random Even Number:")
        response = client.send_request("get_random_even")
        print(f"   Response: {response}")

        # Test 2: Get multiple random even numbers
        print("\n2. Get 5 Random Even Numbers:")
        response = client.send_request("get_random_evens", {"count": 5})
        print(f"   Response: {response}")

        # Test 3: Get all even numbers
        print("\n3. Get All Even Numbers:")
        response = client.send_request("get_all_evens")
        print(f"   Response: {response}")

        # Test 4: Validate even number
        print("\n4. Validate Even Number (4):")
        response = client.send_request("validate_even", {"number": 4})
        print(f"   Response: {response}")

        print("\n5. Validate Even Number (5):")
        response = client.send_request("validate_even", {"number": 5})
        print(f"   Response: {response}")

    finally:
        client.close()


def test_random_odd_mcp():
    """Test RandomOddLibrary MCP server"""
    print("\n" + "=" * 60)
    print("Testing RandomOddLibrary MCP Server")
    print("=" * 60)

    script_path = "/Users/vinhnt0111/Desktop/MCP/random_odd_mcp_package/random_odd_mcp.py"
    client = MCPClient(script_path)

    try:
        # Test 1: Get random odd number
        print("\n1. Get Random Odd Number:")
        response = client.send_request("get_random_odd")
        print(f"   Response: {response}")

        # Test 2: Get multiple random odd numbers
        print("\n2. Get 5 Random Odd Numbers:")
        response = client.send_request("get_random_odds", {"count": 5})
        print(f"   Response: {response}")

        # Test 3: Get all odd numbers
        print("\n3. Get All Odd Numbers:")
        response = client.send_request("get_all_odds")
        print(f"   Response: {response}")

        # Test 4: Validate odd number
        print("\n4. Validate Odd Number (5):")
        response = client.send_request("validate_odd", {"number": 5})
        print(f"   Response: {response}")

        print("\n5. Validate Odd Number (4):")
        response = client.send_request("validate_odd", {"number": 4})
        print(f"   Response: {response}")

    finally:
        client.close()


if __name__ == "__main__":
    try:
        test_random_even_mcp()
        test_random_odd_mcp()
        print("\n" + "=" * 60)
        print("✅ All MCP tests completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()

