# 🤖 AI Tool Interface - MCP Library Access Guide

## Overview

**AI Tool Interface** (`src/ai_tool_interface.py`) allows AI models (Claude, GPT-4, etc.) to directly call your MCP libraries (random-even-mcp and random-odd-mcp).

## Available Tools

### 1. `route_ticket`
**Route a ticket and call appropriate MCP server**

- **Input:**
  - `ticket_id` (string): Ticket ID like 'KAN-7' or 'PROJ-1234'
  - `mcp_method` (string): MCP method to call
  - `count` (integer, optional): For methods needing count parameter

- **Output:**
  ```json
  {
    "success": true,
    "ticket_id": "KAN-7",
    "mcp_server": "random-odd-mcp",
    "method": "get_random_odd",
    "value": 15
  }
  ```

- **Example:**
  ```python
  AIToolInterface.execute_tool('route_ticket', {
      'ticket_id': 'KAN-7',
      'mcp_method': 'get_random_odd'
  })
  ```

### 2. `determine_mcp_server`
**Just determine which MCP server handles a ticket**

- **Input:**
  - `ticket_id` (string): Ticket ID

- **Output:**
  ```json
  {
    "success": true,
    "ticket_id": "KAN-8",
    "last_digit": 8,
    "type": "EVEN",
    "mcp_server": "random-even-mcp",
    "reasoning": "..."
  }
  ```

### 3. `call_mcp_even`
**Call random-even-mcp library directly**

- **Available methods:**
  - `get_random_even` - Get 1 random even number
  - `get_random_evens` - Get N random even numbers (needs `count`)
  - `get_all_evens` - Get all even numbers [2,4,6,...,20]
  - `validate_even` - Validate if number is even (needs `number`)

- **Example:**
  ```python
  AIToolInterface.execute_tool('call_mcp_even', {
      'method': 'get_all_evens'
  })
  ```

### 4. `call_mcp_odd`
**Call random-odd-mcp library directly**

- **Available methods:**
  - `get_random_odd` - Get 1 random odd number
  - `get_random_odds` - Get N random odd numbers (needs `count`)
  - `get_all_odds` - Get all odd numbers [1,3,5,...,19]
  - `validate_odd` - Validate if number is odd (needs `number`)

---

## How to Use with Claude

### Option 1: Simple Python Integration

```python
from src.ai_tool_interface import AIToolInterface
import json

# Get tool schemas
tools = AIToolInterface.get_tool_schemas()

# Use tools directly
result = AIToolInterface.execute_tool('route_ticket', {
    'ticket_id': 'KAN-7',
    'mcp_method': 'get_random_odd'
})

print(json.dumps(result, indent=2))
```

### Option 2: Claude with Tool Use (Full Conversation)

```python
from anthropic import Anthropic
from src.ai_tool_interface import AIToolInterface
import json

client = Anthropic()
tools = AIToolInterface.get_tool_schemas()

messages = [
    {
        "role": "user",
        "content": "Route ticket KAN-7 and get a random number"
    }
]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# Process tool calls from Claude
for content_block in response.content:
    if content_block.type == "tool_use":
        result = AIToolInterface.execute_tool(
            content_block.name,
            content_block.input
        )
        print(f"Tool: {content_block.name}")
        print(f"Result: {json.dumps(result, indent=2)}")
```

### Option 3: OpenAI GPT-4 Integration

```python
from openai import OpenAI
from src.ai_tool_interface import AIToolInterface
import json

client = OpenAI()
tools = AIToolInterface.get_tool_schemas()

# Convert schemas to OpenAI format if needed
response = client.chat.completions.create(
    model="gpt-4-turbo",
    tools=tools,
    messages=[
        {
            "role": "user",
            "content": "Route ticket KAN-8 and check which MCP handles it"
        }
    ]
)

# Handle tool calls...
```

---

## Tool Schemas (For AI Models)

The tools use standard Anthropic/OpenAI compatible format:

```json
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
        ]
      },
      "count": {
        "type": "integer",
        "description": "Count parameter (optional)"
      }
    },
    "required": ["ticket_id", "mcp_method"]
  }
}
```

---

## Quick Start Example

### Command Line Test
```bash
# Test AI interface directly
python3 test_ai_interface.py

# Would show:
# ✅ Ticket: KAN-7
# ✅ MCP Server: random-odd-mcp
# ✅ Value: 3
```

### Python Code
```python
from src.ai_tool_interface import AIToolInterface

# Test 1: Route and call
result = AIToolInterface.execute_tool('route_ticket', {
    'ticket_id': 'KAN-7',
    'mcp_method': 'get_random_odd'
})
print(result['value'])  # 3

# Test 2: Check routing
result = AIToolInterface.execute_tool('determine_mcp_server', {
    'ticket_id': 'KAN-8'
})
print(result['mcp_server'])  # random-even-mcp

# Test 3: Call even MCP
result = AIToolInterface.execute_tool('call_mcp_even', {
    'method': 'get_all_evens'
})
print(result['result'])  # {'numbers': [2, 4, 6, ...]}
```

---

## Error Handling

All tool calls return a consistent format:

```json
{
  "success": true/false,
  "error": "error message if failed",
  "error_type": "exception type if failed",
  ...other results...
}
```

---

## Files

- **`src/ai_tool_interface.py`** - Main tool interface class
- **`test_ai_interface.py`** - Direct testing without API
- **`claude_integration_example.py`** - Full Claude integration example

---

## Usage Patterns

### Pattern 1: Direct Tool Calls
```python
result = AIToolInterface.execute_tool('call_mcp_even', {'method': 'get_all_evens'})
```

### Pattern 2: Through Claude
Claude calls tools automatically when given:
> "Route ticket KAN-7 and get a random number"

### Pattern 3: Get Tool Schemas
```python
tools = AIToolInterface.get_tool_schemas()  # For Claude/GPT-4 integration
```

---

## Summary

✅ **4 tools** available for AI to call  
✅ **Type-safe** input validation  
✅ **Consistent** output format  
✅ **Claude compatible** tool schemas  
✅ **Error handling** built-in  
✅ **Easy integration** with AI models  

**Status:** 🟢 Production Ready

---

**Next Step:** Use with Claude AI for intelligent ticket routing and MCP library calls!

