"""
Claude AI Integration Example
Shows how Claude can call MCP libraries through the AI Tool Interface
"""

# Installation:
# pip install anthropic

from anthropic import Anthropic
import json
import sys

sys.path.insert(0, '/Users/vinhnt0111/Desktop/MCP')
from src.ai_tool_interface import AIToolInterface

def process_tool_call(tool_name: str, tool_input: dict):
    """Process tool calls from Claude"""
    return AIToolInterface.execute_tool(tool_name, tool_input)

def main():
    """Main Claude conversation with MCP tools"""
    client = Anthropic()
    
    # Get tool schemas from our interface
    tools = AIToolInterface.get_tool_schemas()
    
    print("\n" + "=" * 80)
    print("🤖 CLAUDE AI - MCP LIBRARY INTEGRATION")
    print("=" * 80)
    print("\nClaude can now call these tools:")
    for tool in tools:
        print(f"  • {tool['name']}: {tool['description']}")
    
    # Example conversation
    messages = [
        {
            "role": "user",
            "content": """Please help me with the following tasks:
1. Route ticket KAN-7 to the appropriate MCP server and get a random number
2. Check which MCP server handles ticket KAN-9
3. Get all even numbers from the even MCP library"""
        }
    ]
    
    print("\n" + "=" * 80)
    print("USER REQUEST:")
    print(messages[0]['content'])
    print("=" * 80)
    
    # Start conversation with Claude
    print("\n🚀 Claude is processing...\n")
    
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Check if Claude wants to use tools
        if response.stop_reason == "tool_use":
            # Process tool calls
            tool_results = []
            
            for content_block in response.content:
                if content_block.type == "tool_use":
                    tool_name = content_block.name
                    tool_input = content_block.input
                    tool_use_id = content_block.id
                    
                    print(f"🔧 Claude calling: {tool_name}")
                    print(f"   Input: {json.dumps(tool_input)}")
                    
                    # Execute the tool
                    result = process_tool_call(tool_name, tool_input)
                    
                    print(f"   Result: {json.dumps(result, indent=2)}")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": json.dumps(result)
                    })
            
            # Add assistant response and tool results to messages
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        
        else:
            # Claude has finished and provided final response
            print("\n" + "=" * 80)
            print("📝 CLAUDE'S RESPONSE:")
            print("=" * 80)
            
            for content_block in response.content:
                if hasattr(content_block, 'text'):
                    print(content_block.text)
            
            break
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║  CLAUDE AI + MCP LIBRARY INTEGRATION EXAMPLE                              ║
╚════════════════════════════════════════════════════════════════════════════╝

This example shows how to enable Claude to call your MCP libraries directly.

To use this:
1. Set ANTHROPIC_API_KEY environment variable
2. Run: python3 claude_integration_example.py

Features:
✅ Claude automatically calls the right MCP library
✅ AI Tool Interface handles all complexity
✅ Type-safe tool definitions
✅ Full conversation context management
    """)
    
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: This requires ANTHROPIC_API_KEY to be set in environment")
        print("      For testing without API, use the test_ai_interface.py instead")

