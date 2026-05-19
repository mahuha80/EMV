# 🔄 PIPELINE FLOW – Chi Tiết Luồng Xử Lý

> Tài liệu mô tả chi tiết từng bước trong pipeline AI QA Automation

---

## 📌 Tổng Quan Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   INPUT: python src/main.py --ticket PROJ-1234                              │
│                                                                              │
│   ┌─────────────┐                                                            │
│   │   STEP A    │  Jira MCP → Lấy ticket info                               │
│   │ ticket_data │                                                            │
│   └──────┬──────┘                                                            │
│          │ ticket_data.json                                                  │
│          ▼                                                                   │
│   ┌─────────────┐                                                            │
│   │   STEP B    │  Robot + Appium → Chạy test cases                         │
│   │test_results │                                                            │
│   └──────┬──────┘                                                            │
│          │ test_results.json                                                 │
│          ▼                                                                   │
│   ┌─────────────┐  All PASS? ──YES──▶ Done (no fix needed)                 │
│   │   STEP C    │                                                            │
│   │ fix_report  │  Has FAIL? ──▶ AI analyze + generate fix                  │
│   └──────┬──────┘                                                            │
│          │ fix_report.json + patch files                                     │
│          ▼                                                                   │
│   ┌─────────────┐                                                            │
│   │   STEP D    │  Git → Create branch → Apply fix → PR                     │
│   │  pr_info    │                                                            │
│   └─────────────┘                                                            │
│                                                                              │
│   OUTPUT: Pull Request URL                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🅰️ STEP A – Jira MCP Fetcher

### Mục Tiêu
Kết nối Jira qua **Model Context Protocol (MCP)** để lấy đầy đủ thông tin ticket.

### Input
```
ticket_id: "PROJ-1234"
```

### Các Module

#### `src/jira/mcp_client.py`
```python
"""
Quản lý kết nối MCP đến Jira server.
- Authenticate với Jira API token
- Duy trì session MCP
- Handle reconnect khi timeout
"""
```

#### `src/jira/ticket_fetcher.py`
```python
"""
Lấy dữ liệu ticket từ Jira qua MCP client.
- fetch_ticket(ticket_id) → raw ticket data
- fetch_attachments(ticket_id) → danh sách file đính kèm
- fetch_comments(ticket_id) → comments & discussion
"""
```

#### `src/jira/ticket_parser.py`
```python
"""
Parse và chuẩn hóa dữ liệu ticket thô.
- Trích xuất acceptance criteria
- Xác định components liên quan
- Map priority → test priority
"""
```

### Output
```json
{
  "ticket_id": "PROJ-1234",
  "title": "App crashes when submitting empty password",
  "description": "When user taps Login with empty password field, app force closes",
  "acceptance_criteria": [
    "Show validation message when password is empty",
    "App must NOT crash",
    "Error message: 'Password cannot be empty'"
  ],
  "priority": "High",
  "components": ["authentication", "login-screen"],
  "labels": ["bug", "android", "ios"],
  "assignee": "dev@company.com",
  "reporter": "qa@company.com",
  "attachments": ["screenshot_crash.png"],
  "fetched_at": "2026-05-18T10:00:00Z"
}
```

### Error Scenarios
| Lỗi | Xử lý |
|-----|--------|
| Jira server unreachable | Retry 3 lần, sau đó raise `JiraConnectionError` |
| Invalid ticket ID | Raise `TicketNotFoundError` |
| Auth failed | Raise `JiraAuthError`, yêu cầu kiểm tra token |
| Network timeout | Retry với exponential backoff |

---

## 🅱️ STEP B – Robot Framework + Appium Runner

### Mục Tiêu
Tự động sinh và thực thi test cases dựa trên acceptance criteria từ STEP A.

### Input
```json
ticket_data.json (từ STEP A)
```

### Các Module

#### `src/testing/test_generator.py`
```python
"""
Sinh robot test cases tự động từ acceptance criteria.
- Map criteria → test case structure
- Chọn appium keywords phù hợp với platform
- Sinh file .robot tạm thời cho ticket
"""
```

#### `src/testing/appium_driver.py`
```python
"""
Quản lý Appium WebDriver session.
- Khởi động Appium server
- Tạo và quản lý device session
- Screenshot on failure
- Cleanup sau khi test xong
"""
```

#### `src/testing/robot_runner.py`
```python
"""
Chạy Robot Framework test suites.
- Execute via subprocess: robot --outputdir ...
- Monitor realtime output
- Parse kết quả từ output.xml
"""
```

#### `src/testing/result_parser.py`
```python
"""
Parse kết quả test từ Robot Framework output.xml.
- Tổng hợp PASS/FAIL
- Trích xuất error messages
- Xác định test case nào FAIL và tại sao
"""
```

### Flow Chi Tiết
```
ticket_data.json
      │
      ▼
test_generator.py
├── Đọc acceptance_criteria
├── Map criteria → robot keywords
├── Sinh file: robot_tests/suites/generated/PROJ-1234.robot
└── Output: test_suite_path

      │
      ▼
appium_driver.py
├── Load config từ appium_config.yaml
├── Khởi động Appium server (nếu chưa chạy)
├── Tạo session với device
└── Output: driver instance

      │
      ▼
robot_runner.py
├── Build command:
│   robot
│   --outputdir reports/PROJ-1234/robot_output/
│   --variable TICKET_ID:PROJ-1234
│   --variable PLATFORM:android
│   robot_tests/suites/generated/PROJ-1234.robot
├── Execute subprocess
└── Monitor output

      │
      ▼
result_parser.py
├── Đọc output.xml
├── Parse từng test case result
└── Output: test_results.json
```

### Output
```json
{
  "ticket_id": "PROJ-1234",
  "run_id": "run-20260518-100500",
  "platform": "android",
  "device": "emulator-5554",
  "status": "FAIL",
  "total": 3,
  "passed": 1,
  "failed": 2,
  "duration_seconds": 145,
  "test_cases": [
    {
      "name": "TC_001 Show Validation Message On Empty Password",
      "status": "PASS",
      "duration": 23
    },
    {
      "name": "TC_002 App Must Not Crash On Empty Password",
      "status": "FAIL",
      "error": "Application crashed: NullPointerException in AuthService.java:145",
      "screenshot": "reports/PROJ-1234/screenshots/TC_002_fail.png"
    },
    {
      "name": "TC_003 Error Message Should Match Expected Text",
      "status": "FAIL",
      "error": "Element 'error_message_label' not found after crash"
    }
  ],
  "report_path": "reports/PROJ-1234/robot_output/report.html",
  "executed_at": "2026-05-18T10:05:00Z"
}
```

---

## 🅲 STEP C – AI Code Analyzer & Fix Generator

### Mục Tiêu
Phân tích lỗi từ kết quả test, đọc source code liên quan, đề xuất và tạo fix patch.

### Khi nào kích hoạt
- STEP B có ít nhất 1 test case **FAIL**
- Có error message / stack trace

### Các Module

#### `src/analyzer/code_reader.py`
```python
"""
Đọc và index source code liên quan đến lỗi.
- Parse stack trace → xác định file & line số
- Đọc file source code
- Trích xuất context xung quanh lỗi (±20 lines)
- Scan các file liên quan (imports, dependencies)
"""
```

#### `src/analyzer/ai_analyzer.py`
```python
"""
AI engine phân tích lỗi và đề xuất fix.
- Gửi context (error + code) đến AI model
- Parse AI response → structured fix
- Confidence scoring
- Fallback nếu AI không chắc chắn
"""
```

#### `src/analyzer/fix_generator.py`
```python
"""
Tạo fix patches từ AI suggestions.
- Tạo unified diff patches
- Validate patch áp dụng được
- Dry-run test patch
"""
```

#### `src/analyzer/impact_assessor.py`
```python
"""
Đánh giá impact của fix đề xuất.
- Scan các file import module bị sửa
- Check có breaking change không
- Estimate risk level
"""
```

### AI Prompt Template
```
CONTEXT:
- Ticket: {ticket_id} - {ticket_title}
- Failed Test: {test_case_name}
- Error: {error_message}
- Stack Trace: {stack_trace}

SOURCE CODE ({file_path}):
{code_snippet}

TASK:
1. Phân tích root cause của lỗi
2. Đề xuất fix code cụ thể
3. Giải thích tại sao fix này giải quyết vấn đề
4. List các file cần thay đổi

OUTPUT FORMAT: JSON
```

### Output
```json
{
  "ticket_id": "PROJ-1234",
  "root_cause": "NullPointerException tại AuthService.java:145 do không kiểm tra null trước khi gọi password.trim()",
  "confidence": 0.94,
  "fixes": [
    {
      "file": "src/auth/AuthService.java",
      "line_start": 143,
      "line_end": 147,
      "original": "String trimmed = password.trim();",
      "fixed": "if (password == null || password.isEmpty()) {\n    throw new ValidationException(\"Password cannot be empty\");\n}\nString trimmed = password.trim();",
      "explanation": "Thêm null check và empty check trước khi gọi trim()"
    }
  ],
  "impact": {
    "files_changed": 1,
    "risk_level": "Low",
    "breaking_change": false,
    "affected_components": ["authentication"],
    "regression_risk": "Minimal – chỉ thêm validation, không thay đổi logic hiện có"
  },
  "analyzed_at": "2026-05-18T10:10:00Z"
}
```

---

## 🅳 STEP D – GitHub Submitter

### Mục Tiêu
Tạo branch, commit fix, và mở Pull Request với đầy đủ thông tin.

### Các Module

#### `src/github/git_manager.py`
```python
"""
Quản lý Git operations.
- Tạo branch: fix/PROJ-1234-<short-desc>
- Apply patches từ fix_report.json
- Stage và commit changes
"""
```

#### `src/github/commit_formatter.py`
```python
"""
Format commit message theo convention.
- Sinh commit message từ fix_report
- Tuân theo Conventional Commits format
"""
```

#### `src/github/pr_creator.py`
```python
"""
Tạo Pull Request qua GitHub API.
- Build PR body từ template
- Set labels, reviewers, milestone
- Link Jira ticket trong PR
"""
```

#### `src/github/report_builder.py`
```python
"""
Build PR description đầy đủ.
- Root cause analysis
- Changes made
- Impact assessment table
- Test evidence & instructions
"""
```

### PR Body Template
```markdown
## 🎫 Ticket: {ticket_id} – {ticket_title}
**Jira**: [{ticket_id}]({jira_url}) | **Priority**: {priority}

---

## 🔍 Root Cause Analysis
{root_cause}

---

## 🛠️ Changes Made
| File | Change |
|------|--------|
{changes_table}

---

## ⚠️ Impact Assessment
| Area | Level | Notes |
|------|-------|-------|
| Risk Level | {risk_level} | {risk_notes} |
| Breaking Change | {breaking_change} | {bc_notes} |
| Affected Components | {components} | |

---

## ✅ How to Test

### Run Automated Tests
```bash
robot --variable TICKET_ID:{ticket_id} \
      --outputdir reports/{ticket_id}/ \
      robot_tests/suites/
```

### Expected Results
- TC_001: PASS ✅
- TC_002: PASS ✅  
- TC_003: PASS ✅

### Test Evidence
- 📊 Robot Report: `reports/{ticket_id}/robot_output/report.html`
- 📱 Platform: Android {android_version}
- 🕐 Executed: {executed_at}

---
*🤖 Auto-generated by AI QA Pipeline v1.0*
```

### Output
```json
{
  "ticket_id": "PROJ-1234",
  "branch": "fix/PROJ-1234-null-pointer-on-empty-password",
  "commit_sha": "abc123def456",
  "pr_number": 42,
  "pr_url": "https://github.com/owner/repo/pull/42",
  "status": "open",
  "submitted_at": "2026-05-18T10:15:00Z"
}
```

---

## ⚡ Entry Point – `src/main.py`

```python
"""
Main pipeline orchestrator.
Usage: python src/main.py --ticket PROJ-1234 [--step A|B|C|D] [--platform android|ios]
"""

def run_pipeline(ticket_id: str, start_step: str = "A", platform: str = "android"):
    # STEP A
    if start_step <= "A":
        ticket_data = step_a_fetch_ticket(ticket_id)

    # STEP B
    if start_step <= "B":
        test_results = step_b_run_tests(ticket_data, platform)

    # STEP C – chỉ chạy nếu có FAIL
    if start_step <= "C" and test_results["status"] == "FAIL":
        fix_report = step_c_analyze_and_fix(ticket_data, test_results)

    # STEP D
    if start_step <= "D" and fix_report:
        pr_info = step_d_submit_github(ticket_data, fix_report, test_results)
        print(f"✅ PR created: {pr_info['pr_url']}")
```

