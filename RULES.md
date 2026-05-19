# 📏 RULES & CONVENTIONS

> Quy tắc bắt buộc cho toàn bộ project AI QA Automation Pipeline

---

## 🎯 1. Nguyên Tắc Chung

| # | Quy Tắc | Mô Tả |
|---|---------|--------|
| R01 | **Single Responsibility** | Mỗi file/class chỉ làm 1 nhiệm vụ duy nhất |
| R02 | **Fail Fast** | Phát hiện lỗi sớm, raise exception ngay khi có vấn đề |
| R03 | **Idempotent Steps** | Mỗi step có thể chạy lại mà không gây side effect |
| R04 | **Audit Trail** | Mọi hành động đều phải được log đầy đủ |
| R05 | **Config over Code** | Mọi giá trị có thể thay đổi phải nằm trong config/env |

---

## 🐍 2. Python Code Convention

### 2.1 Naming Convention
```python
# ✅ Module, file: snake_case
ticket_fetcher.py
robot_runner.py

# ✅ Class: PascalCase
class TicketFetcher:
class RobotRunner:

# ✅ Function, variable: snake_case
def fetch_ticket(ticket_id: str) -> dict:
ticket_data = {}

# ✅ Constant: UPPER_SNAKE_CASE
MAX_RETRY = 3
DEFAULT_TIMEOUT = 30

# ✅ Private: prefix underscore
def _parse_raw_data(self, raw: str) -> dict:
```

### 2.2 Type Hints – BẮT BUỘC
```python
# ✅ ĐÚNG – luôn dùng type hints
def run_tests(ticket_data: dict, platform: str = "android") -> TestResult:
    ...

# ❌ SAI – không có type hints
def run_tests(ticket_data, platform):
    ...
```

### 2.3 Docstring – BẮT BUỘC cho public methods
```python
def fetch_ticket(ticket_id: str) -> dict:
    """
    Lấy thông tin ticket từ Jira qua MCP Protocol.

    Args:
        ticket_id (str): ID của ticket, ví dụ: 'PROJ-1234'

    Returns:
        dict: Thông tin ticket bao gồm title, description, criteria

    Raises:
        JiraConnectionError: Khi không thể kết nối Jira MCP
        TicketNotFoundError: Khi ticket ID không tồn tại
    """
```

### 2.4 Error Handling
```python
# ✅ ĐÚNG – custom exceptions, có context
class JiraConnectionError(Exception):
    """Raised khi không thể kết nối Jira MCP server."""
    pass

try:
    ticket = fetcher.fetch_ticket(ticket_id)
except JiraConnectionError as e:
    logger.error(f"[STEP-A] Jira connection failed: {e}")
    raise

# ❌ SAI – catch-all không có xử lý
try:
    ticket = fetcher.fetch_ticket(ticket_id)
except:
    pass
```

### 2.5 Logging – BẮT BUỘC
```python
import logging

logger = logging.getLogger(__name__)

# Format log theo step
logger.info("[STEP-A] Fetching ticket: PROJ-1234")
logger.debug("[STEP-B] Appium session started: session_id=abc123")
logger.warning("[STEP-C] Low confidence fix suggestion: 65%")
logger.error("[STEP-D] GitHub PR creation failed: 403 Forbidden")
```

---

## 🤖 3. Robot Framework Convention

### 3.1 Cấu Trúc File .robot
```robot
*** Settings ***
Documentation    Mô tả ngắn gọn mục đích của test suite
Library          AppiumLibrary
Library          Collections
Resource         ../resources/common.robot
Resource         ../resources/appium_keywords.robot

*** Variables ***
${TICKET_ID}     PROJ-1234
${PLATFORM}      android

*** Test Cases ***
TC_001 Verify Feature Works As Expected
    [Documentation]    Test case mô tả từ acceptance criteria ticket
    [Tags]             smoke    regression    ${TICKET_ID}
    [Setup]            Open Application
    # Steps
    Given User Is On Home Screen
    When User Performs Action
    Then Expected Result Should Be Displayed
    [Teardown]         Close Application

*** Keywords ***
User Is On Home Screen
    [Documentation]    Verify user đang ở màn hình chính
    Wait Until Element Is Visible    ${HOME_SCREEN_ID}    timeout=10s
```

### 3.2 Naming Test Cases
```
# Format: TC_XXX <Action> <Expected>
TC_001 Login With Valid Credentials Should Succeed
TC_002 Login With Invalid Password Should Show Error
TC_003 Submit Empty Form Should Show Validation Message
```

### 3.3 Tag Convention
```robot
[Tags]    <type>    <priority>    <ticket_id>

# Types:
smoke           # Test cơ bản, chạy nhanh
regression      # Regression test
e2e             # End-to-end flow
ui              # UI specific

# Priority:
P1              # Critical
P2              # High
P3              # Medium
```

---

## 📱 4. Appium Convention

### 4.1 Locator Strategy (Ưu tiên theo thứ tự)
```
1. accessibility_id      ← ƯU TIÊN CAO NHẤT (stable, cross-platform)
2. id (resource-id)      ← stable
3. xpath                 ← CUỐI CÙNG, tránh dùng nếu có thể
```

### 4.2 Timeout & Wait
```python
# ✅ ĐÚNG – luôn dùng explicit wait
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "login_button", timeout=10)

# ❌ SAI – implicit wait hoặc hardcode sleep
time.sleep(3)
```

### 4.3 Appium Capabilities – Phải khai báo đầy đủ
```python
ANDROID_CAPS = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": os.getenv("ANDROID_DEVICE_NAME"),
    "appPackage": "com.your.app",
    "appActivity": ".MainActivity",
    "noReset": False,
    "fullReset": False,
    "newCommandTimeout": 300,
}
```

---

## 🔀 5. Git & GitHub Convention

### 5.1 Branch Naming
```
# Format: <type>/<ticket-id>-<short-description>
fix/PROJ-1234-login-crash-on-empty-password
feat/PROJ-5678-add-dark-mode-toggle
test/PROJ-9012-add-payment-flow-tests
```

### 5.2 Commit Message Format
```
<type>(<scope>): <subject> [TICKET-ID]

<body>

<footer>

# Ví dụ:
fix(auth): resolve null pointer on empty password input [PROJ-1234]

- Check for null/empty password before proceeding to authentication
- Add input validation at service layer
- Update unit tests to cover edge cases

Tested: Robot Framework + Appium | Android 13 | iOS 16
```

### 5.3 Commit Types
| Type | Khi nào dùng |
|------|-------------|
| `fix` | Bug fix |
| `feat` | Tính năng mới |
| `test` | Thêm/sửa test |
| `refactor` | Refactor không thay đổi behavior |
| `docs` | Cập nhật tài liệu |
| `chore` | Cấu hình, build scripts |

### 5.4 Pull Request Template – BẮT BUỘC
```markdown
## 🎫 Ticket
- **ID**: PROJ-XXXX
- **Link**: [Jira Ticket](https://jira.company.com/browse/PROJ-XXXX)
- **Type**: Bug Fix / Feature / Improvement

## 🔍 Root Cause Analysis
<!-- Mô tả nguyên nhân gốc rễ của vấn đề -->

## 🛠️ Solution & Changes
<!-- Mô tả những thay đổi đã thực hiện -->
| File | Change Description |
|------|--------------------|
| `src/...` | ... |

## ⚠️ Impact Assessment
| Impact Area | Level | Notes |
|------------|-------|-------|
| Functionality | - | |
| Performance | - | |
| Security | - | |
| Breaking Change | Yes/No | |

## ✅ How to Test
### Automated Tests
```bash
# Chạy test suite
robot --variable TICKET_ID:PROJ-XXXX robot_tests/suites/
```

### Manual Test Steps
1. Step 1
2. Step 2
3. Expected result

## 📊 Test Evidence
<!-- Attach screenshots, logs hoặc kết quả test -->
- [ ] Robot Framework report attached
- [ ] Appium logs attached
- [ ] Screenshots attached
```

---

## 🔐 6. Security Rules

| Rule | Mô Tả |
|------|--------|
| **No Hardcode Secrets** | KHÔNG hardcode token, password, key trong code |
| **Use .env** | Tất cả credentials phải lấy từ environment variables |
| **No .env in Git** | File .env phải có trong .gitignore |
| **Mask in Logs** | Không log sensitive data: `token=***MASKED***` |
| **Rotate Tokens** | API tokens phải có expiry và được rotate định kỳ |

```python
# ✅ ĐÚNG
import os
api_token = os.getenv("JIRA_API_TOKEN")
if not api_token:
    raise ValueError("JIRA_API_TOKEN environment variable is not set")

# ❌ SAI – TUYỆT ĐỐI không làm
api_token = "eyJhbGciOiJIUzI1NiJ9.abc123..."
```

---

## 🤖 9. MCP Integration Rules

### 9.1 Ticket Number Routing Rule
```
RULE: When processing a ticket, ALWAYS check the LAST DIGIT of ticket number.

┌─────────────────────────────────────────────────────┐
│  Ticket ID Format: <PROJECT>-<NUMBER>               │
│  Example: PROJ-1234 → Last digit = 4               │
└─────────────────────────────────────────────────────┘

|  Last Digit | Number Type | MCP Server to Call |
|-------------|-------------|-------------------|
| 0, 2, 4, 6, 8 | EVEN | random-even-mcp |
| 1, 3, 5, 7, 9 | ODD | random-odd-mcp |
```

### 9.2 MCP Calling Flow
```python
def determine_mcp_server(ticket_id: str) -> str:
    """
    Extract last digit from ticket ID and determine MCP server.
    
    Args:
        ticket_id (str): Ticket ID, e.g., 'PROJ-1234' or 'KAN-5'
    
    Returns:
        str: MCP server name ('random-even-mcp' or 'random-odd-mcp')
    
    Raises:
        ValueError: If ticket_id format is invalid
    """
    # Pattern: PROJ-1234
    match = re.search(r'-(\d+)$', ticket_id)
    if not match:
        raise ValueError(f"Invalid ticket ID format: {ticket_id}")
    
    last_number = int(match.group(1)) % 10  # Get last digit
    
    if last_number % 2 == 0:  # Even
        return 'random-even-mcp'
    else:  # Odd
        return 'random-odd-mcp'


def call_mcp_server(mcp_name: str, method: str, params: dict = None) -> dict:
    """
    Call appropriate MCP server based on routing rule.
    
    Args:
        mcp_name (str): 'random-even-mcp' or 'random-odd-mcp'
        method (str): Method name to call
        params (dict): Method parameters
    
    Returns:
        dict: MCP response
    
    Examples:
        # For even ticket (e.g., PROJ-1234)
        result = call_mcp_server('random-even-mcp', 'get_random_even')
        
        # For odd ticket (e.g., PROJ-1235)
        result = call_mcp_server('random-odd-mcp', 'get_random_odd', {'count': 5})
    """
    import subprocess
    import json
    
    process = subprocess.Popen(
        ['python3', f'/path/to/{mcp_name}.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1
    }
    
    try:
        process.stdin.write(json.dumps(request) + "\n")
        process.stdin.flush()
        response_line = process.stdout.readline()
        return json.loads(response_line)
    finally:
        process.terminate()
```

### 9.3 Available MCP Methods

**random-even-mcp (cho ticket có số cuối chẵn):**
- `get_random_even()` → Random số chẵn
- `get_random_evens(count)` → N số chẵn
- `get_all_evens()` → Tất cả [2,4,6,...,20]
- `validate_even(number)` → Check số chẵn

**random-odd-mcp (cho ticket có số cuối lẻ):**
- `get_random_odd()` → Random số lẻ
- `get_random_odds(count)` → N số lẻ
- `get_all_odds()` → Tất cả [1,3,5,...,19]
- `validate_odd(number)` → Check số lẻ

### 9.4 Integration Examples

**Example 1: PROJ-1234 (Even) → random-even-mcp**
```python
ticket_id = "PROJ-1234"  # Last digit: 4 (EVEN)
mcp_server = determine_mcp_server(ticket_id)  # → "random-even-mcp"

# Call MCP
result = call_mcp_server(mcp_server, 'get_random_even')
print(result)  # {'result': {'number': 6}, 'jsonrpc': '2.0', 'id': 1}

# Use result in test generation
random_even = result['result']['number']
test_data = generate_test_with_value(random_even)
```

**Example 2: KAN-5 (Odd) → random-odd-mcp**
```python
ticket_id = "KAN-5"  # Last digit: 5 (ODD)
mcp_server = determine_mcp_server(ticket_id)  # → "random-odd-mcp"

# Call MCP
result = call_mcp_server(mcp_server, 'get_random_odd')
print(result)  # {'result': {'number': 13}, 'jsonrpc': '2.0', 'id': 1}

# Use result
random_odd = result['result']['number']
test_data = generate_test_with_value(random_odd)
```

### 9.5 Updated Pipeline Flow

```
┌─────────────────────────────────────────┐
│  STEP 0: Extract & Route Ticket Number  │
│  ─────────────────────────────────────   │
│                                          │
│  Input: ticket_id = "PROJ-1234"          │
│                                          │
│  1. Extract last digit: 4                │
│  2. Check if even/odd: EVEN              │
│  3. Determine MCP: random-even-mcp       │
│  4. Log: [STEP-0] Routing to MCP...      │
│                                          │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌────────────┐  ┌─────────────────┐
│   EVEN     │  │      ODD        │
│  MCP Call  │  │    MCP Call     │
│            │  │                 │
│ get_random │  │ get_random_odd  │
│    even    │  │                 │
│  → value   │  │  → value        │
└────────────┘  └─────────────────┘
    │                     │
    └──────────┬──────────┘
               │
               ▼
    ┌──────────────────────┐
    │ STEP 1: FETCH TICKET │
    │ (add MCP value to... │
    │  test context)       │
    └──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ STEP 2: ANALYZE      │
    │ STEP 3: GENERATE     │
    │ STEP 4: RUN TEST     │
    └──────────────────────┘
```

### 9.6 Error Handling for MCP

```python
# ✅ ĐÚNG – Handle MCP errors
try:
    result = call_mcp_server(mcp_server, 'get_random_even')
    if 'error' in result:
        logger.error(f"[STEP-0] MCP error: {result['error']}")
        raise MCPError(result['error'])
except subprocess.TimeoutExpired:
    logger.error(f"[STEP-0] MCP timeout after 30s")
    raise MCPTimeoutError("MCP server timeout")
except Exception as e:
    logger.error(f"[STEP-0] Unexpected MCP error: {e}")
    raise

# ❌ SAI – Ignore MCP errors
result = call_mcp_server(mcp_server, 'get_random_even')
random_value = result['result']['number']  # May crash if error exists
```

### 9.7 Logging Format for MCP

```python
# Log format: [STEP-0] MCP routing & value generation
logger.info(f"[STEP-0] Ticket: {ticket_id}")
logger.info(f"[STEP-0] Last digit: {last_digit}")
logger.info(f"[STEP-0] Type: {'EVEN' if is_even else 'ODD'}")
logger.info(f"[STEP-0] MCP server: {mcp_server}")
logger.info(f"[STEP-0] Generated value: {random_value}")
logger.info(f"[STEP-0] Ready to proceed with test generation")
```


---

## 📊 7. Data & Output Rules

### 7.1 Intermediate Data Format
```json
// ticket_data.json – Output của STEP A
{
  "ticket_id": "PROJ-1234",
  "title": "App crashes on empty password",
  "description": "...",
  "acceptance_criteria": [...],
  "priority": "High",
  "components": ["auth", "login"],
  "fetched_at": "2026-05-18T10:00:00Z"
}

// test_results.json – Output của STEP B
{
  "ticket_id": "PROJ-1234",
  "run_id": "run-20260518-100500",
  "status": "FAIL",
  "total": 5,
  "passed": 3,
  "failed": 2,
  "test_cases": [...],
  "executed_at": "2026-05-18T10:05:00Z"
}

// fix_report.json – Output của STEP C
{
  "ticket_id": "PROJ-1234",
  "root_cause": "...",
  "fixes": [...],
  "impact": {...},
  "confidence": 0.92,
  "analyzed_at": "2026-05-18T10:10:00Z"
}
```

### 7.2 Report Storage
```
reports/
├── PROJ-1234/
│   ├── ticket_data.json        # STEP A output
│   ├── test_results.json       # STEP B output
│   ├── robot_output/           # Robot Framework reports
│   │   ├── output.xml
│   │   ├── log.html
│   │   └── report.html
│   ├── fix_report.json         # STEP C output
│   └── pr_info.json            # STEP D output
```

---

## ✅ 8. Checklist Trước Khi Merge

- [ ] Code tuân theo naming convention
- [ ] Tất cả functions có type hints
- [ ] Public methods có docstring
- [ ] Không có hardcoded credentials
- [ ] Tất cả tests PASS (`robot robot_tests/`)
- [ ] Không có `time.sleep()` trong test (dùng explicit wait)
- [ ] Log format theo chuẩn `[STEP-X]`
- [ ] PR description đầy đủ theo template
- [ ] Impact assessment đã được điền
- [ ] Reports đã được attach vào PR
