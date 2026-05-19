# 🔄 MCP ROUTING FLOW - Chi Tiết Từng Bước

Khi chạy project, hệ thống sẽ kiểm tra số cuối của ticket ID, nếu là chẵn gọi MCP chẵn, lẻ gọi MCP lẻ, sau đó gọi các bước khác.

---

## 📋 FLOW DIAGRAM

```
┌───────────────────────────────────────────────────────────────────┐
│          ./run.sh --ticket PROJ-1234                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────▼────────────────────┐
        │  STEP 0: TICKET NUMBER ROUTING          │
        │  ─────────────────────────────────────   │
        │                                          │
        │  Input: ticket_id = "PROJ-1234"          │
        │                                          │
        │  1. Extract last digit: 4                │
        │     Regex: -(\d+)$ → Match: 1234         │
        │     Modulo 10: 1234 % 10 = 4             │
        │                                          │
        │  2. Check if even/odd:                   │
        │     4 is in {0,2,4,6,8}? YES → EVEN      │
        │                                          │
        │  3. Determine MCP server:                │
        │     Type = EVEN → "random-even-mcp"      │
        │                                          │
        │  4. Log routing:                         │
        │     [STEP-0] Ticket: PROJ-1234           │
        │     [STEP-0] Last Digit: 4               │
        │     [STEP-0] Type: EVEN                  │
        │     [STEP-0] MCP: random-even-mcp        │
        │                                          │
        └────────────────────┬────────────────────┘
                             │
        ┌────────────────────▼────────────────────┐
        │  STEP 0.5: CALL MCP SERVER               │
        │  ─────────────────────────────────────   │
        │                                          │
        │  Request JSON-RPC:                       │
        │  {                                       │
        │    "jsonrpc": "2.0",                     │
        │    "method": "get_random_even",          │
        │    "params": {},                         │
        │    "id": 1                               │
        │  }                                       │
        │                                          │
        │  MCP Server (random-even-mcp):           │
        │  • Nhận request từ stdin                  │
        │  • Generate random số chẵn               │
        │  • Return JSON response                  │
        │                                          │
        │  Response:                               │
        │  {                                       │
        │    "result": {"number": 18},             │
        │    "jsonrpc": "2.0",                     │
        │    "id": 1                               │
        │  }                                       │
        │                                          │
        │  Log:                                    │
        │  [STEP-0] Generated Value: 18            │
        │                                          │
        └────────────────────┬────────────────────┘
                             │
        ┌────────────────────▼────────────────────┐
        │  STEP 1: FETCH TICKET                    │
        │  ─────────────────────────────────────   │
        │                                          │
        │  ✅ MCP value available in context       │
        │                                          │
        │  - Fetch từ Jira API                     │
        │  - Parse description (ADF → Plain text)  │
        │  - Extract: preconditions, steps,        │
        │    expected_results                      │
        │  - Save to: reports/PROJ-1234/...        │
        │                                          │
        │  💡 MCP value có thể dùng trong:         │
        │    - Test data generation                │
        │    - Input validation tests              │
        │    - Custom scenarios                    │
        │                                          │
        └────────────────────┬────────────────────┘
                             │
        ┌────────────────────▼────────────────────┐
        │  STEP 2: ANALYZE TICKET                  │
        │  STEP 3: GENERATE ROBOT TESTS            │
        │  STEP 4: RUN ROBOT --DRYRUN              │
        │  ─────────────────────────────────────   │
        │                                          │
        │  Continue normal pipeline...             │
        │                                          │
        └────────────────────┬────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  ✅ SUCCESS     │
                    │  All steps OK   │
                    └─────────────────┘
```

---

## 🔄 Routing Examples

### Example 1: Chẵn (PROJ-1234 → random-even-mcp)

```python
ticket_id = "PROJ-1234"

# STEP 0: Extract & Route
last_digit = 1234 % 10  # = 4
is_even = 4 % 2 == 0    # True
mcp_server = "random-even-mcp"

# STEP 0.5: Call MCP
response = {
    "result": {"number": 18},
    "jsonrpc": "2.0",
    "id": 1
}
mcp_value = 18

# Log output
[STEP-0] Ticket: PROJ-1234
[STEP-0] Last Digit: 4
[STEP-0] Type: EVEN
[STEP-0] MCP: random-even-mcp
[STEP-0] Generated Value: 18
```

### Example 2: Lẻ (KAN-5 → random-odd-mcp)

```python
ticket_id = "KAN-5"

# STEP 0: Extract & Route
last_digit = 5 % 10     # = 5
is_even = 5 % 2 == 0    # False (ODD)
mcp_server = "random-odd-mcp"

# STEP 0.5: Call MCP
response = {
    "result": {"number": 13},
    "jsonrpc": "2.0",
    "id": 1
}
mcp_value = 13

# Log output
[STEP-0] Ticket: KAN-5
[STEP-0] Last Digit: 5
[STEP-0] Type: ODD
[STEP-0] MCP: random-odd-mcp
[STEP-0] Generated Value: 13
```

### Example 3: Edge case - Số cuối là 0

```python
ticket_id = "PROJ-1000"

# STEP 0: Extract & Route
last_digit = 1000 % 10  # = 0
is_even = 0 % 2 == 0    # True (EVEN)
mcp_server = "random-even-mcp"

# STEP 0.5: Call MCP
response = {
    "result": {"number": 2},
    "jsonrpc": "2.0",
    "id": 1
}
mcp_value = 2

# Log output
[STEP-0] Ticket: PROJ-1000
[STEP-0] Last Digit: 0
[STEP-0] Type: EVEN
[STEP-0] MCP: random-even-mcp
[STEP-0] Generated Value: 2
```

---

## 🐍 Python Implementation

### Usage 1: Import & Use Class

```python
from src.ticket_router import TicketRouter

# Determine which MCP to use
mcp_server = TicketRouter.determine_mcp_server('PROJ-1234')
print(mcp_server)  # → 'random-even-mcp'

# Call MCP and get result
result = TicketRouter.route_and_generate('PROJ-1234', 'get_random_even')
print(result['mcp_value'])  # → some even number
```

### Usage 2: Command Line

```bash
# Routing without additional parameters
python3 src/ticket_router.py PROJ-1234

# Routing with parameters (for methods like get_random_evens)
python3 src/ticket_router.py PROJ-1234 --count 5
```

### Usage 3: Integration with Flow Runner

```python
# In flow_runner.py or main.py
from src.ticket_router import TicketRouter

def run_pipeline(ticket_id):
    # STEP 0: Route ticket number
    try:
        routing_result = TicketRouter.route_and_generate(
            ticket_id,
            mcp_method='get_random_even'
        )
        mcp_value = routing_result['mcp_value']
        mcp_server = routing_result['mcp_server']
        
        logger.info(f"[MAIN] Routed to: {mcp_server}")
        logger.info(f"[MAIN] Generated value: {mcp_value}")
        
        # Store for use in subsequent steps
        context = {
            'ticket_id': ticket_id,
            'mcp_value': mcp_value,
            'mcp_server': mcp_server
        }
        
    except Exception as e:
        logger.error(f"[STEP-0] Routing failed: {e}")
        raise
    
    # STEP 1: Fetch ticket
    ticket_data = fetch_ticket(ticket_id)
    
    # STEP 2: Analyze
    analysis = analyze_ticket(ticket_data)
    
    # STEP 3: Generate tests (can use mcp_value)
    # Example: use mcp_value in test data generation
    tests = generate_tests(ticket_data, context['mcp_value'])
    
    # STEP 4: Run tests
    run_tests(tests)
```

---

## 📊 Routing Table  

| Ticket ID | Last Digit | Type | MCP Server | Sample Value |
|-----------|-----------|------|-----------|-------------|
| PROJ-1230 | 0 | EVEN | random-even-mcp | 8 |
| PROJ-1231 | 1 | ODD | random-odd-mcp | 17 |
| PROJ-1232 | 2 | EVEN | random-even-mcp | 14 |
| PROJ-1233 | 3 | ODD | random-odd-mcp | 5 |
| PROJ-1234 | 4 | EVEN | random-even-mcp | 20 |
| PROJ-1235 | 5 | ODD | random-odd-mcp | 11 |
| PROJ-1236 | 6 | EVEN | random-even-mcp | 2 |
| PROJ-1237 | 7 | ODD | random-odd-mcp | 19 |
| PROJ-1238 | 8 | EVEN | random-even-mcp | 12 |
| PROJ-1239 | 9 | ODD | random-odd-mcp | 9 |
| PROJ-1240 | 0 | EVEN | random-even-mcp | 6 |
| KAN-4 | 4 | EVEN | random-even-mcp | 18 |
| KAN-5 | 5 | ODD | random-odd-mcp | 13 |

---

## ⚠️ Error Handling

### Case 1: Invalid Ticket Format

```python
# ❌ Missing number
TicketRouter.determine_mcp_server('PROJ')  # ValueError

# ✅ Error handling
try:
    mcp = TicketRouter.determine_mcp_server('PROJ')
except ValueError as e:
    logger.error(f"[STEP-0] Invalid ticket format: {e}")
    raise
```

### Case 2: MCP Server Not Available

```python
# ❌ MCP script not found
call_mcp_server('random-even-mcp', 'get_random_even')  # FileNotFoundError

# ✅ Error handling
try:
    result = call_mcp_server(mcp_server, method)
except TimeoutError:
    logger.error("[STEP-0] MCP server timeout")
    raise
except Exception as e:
    logger.error(f"[STEP-0] MCP call failed: {e}")
    raise
```

### Case 3: Invalid MCP Response

```python
# ❌ MCP returns error
response = {
    "error": "Method not found",
    "code": -32601,
    "id": 1
}

# ✅ Error handling
if 'error' in response:
    logger.error(f"[STEP-0] MCP error: {response['error']}")
    raise RuntimeError(f"MCP error: {response['error']}")
```

---

## 📝 Logs Format

### Success case (PROJ-1234)

```
2026-05-18 23:12:29,289 - INFO - [STEP-0] ========== TICKET ROUTING START ==========
2026-05-18 23:12:29,290 - INFO - [STEP-0] Ticket ID: PROJ-1234
2026-05-18 23:12:29,291 - INFO - [STEP-0] Ticket: PROJ-1234 | Last Digit: 4 | Type: EVEN | MCP: random-even-mcp
2026-05-18 23:12:29,350 - INFO - [STEP-0] MCP call successful | Response: {'number': 18}
2026-05-18 23:12:29,351 - INFO - [STEP-0] Generated Value: 18
2026-05-18 23:12:29,352 - INFO - [STEP-0] ========== TICKET ROUTING COMPLETE ==========
```

### Error case (invalid format)

```
2026-05-18 23:12:29,289 - ERROR - Invalid ticket ID format: PROJ. Expected format: PROJ-1234
2026-05-18 23:12:29,290 - ERROR - Error: Invalid ticket ID format: PROJ
```

---

## 🎯 Summary

| Step | Action | Input | Output | Status |
|------|--------|-------|--------|--------|
| STEP-0A | Extract digit | PROJ-1234 | last_digit=4 | ✅ |
| STEP-0B | Check even/odd | 4 | type=EVEN | ✅ |
| STEP-0C | Route to MCP | type=EVEN | mcp=random-even-mcp | ✅ |
| STEP-0D | Call MCP | method=get_random_even | value=18 | ✅ |
| STEP-1+ | Fetch ticket | ticket_id | ticket_data | ✅ |
| ... | Continue pipeline | ... | ... | ✅ |

---

**File Location:** `/Users/vinhnt0111/Desktop/MCP/src/ticket_router.py`  
**Rules Location:** `/Users/vinhnt0111/Desktop/MCP/RULES.md` (Section 9)  
**Created:** May 18, 2026  
**Status:** ✅ Complete & Tested

