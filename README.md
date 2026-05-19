# 🤖 AI-Powered QA Automation Pipeline

> **Hệ thống tự động hóa kiểm thử thông minh** – Tích hợp Jira MCP → Robot Framework + Appium → AI Code Analyzer → GitHub Submission

---

## 📋 Mục Lục

- [Tổng Quan](#tổng-quan)
- [Kiến Trúc Hệ Thống](#kiến-trúc-hệ-thống)
- [Cấu Trúc Project](#cấu-trúc-project)
- [Luồng Xử Lý](#luồng-xử-lý)
- [Cài Đặt](#cài-đặt)
- [Cấu Hình](#cấu-hình)
- [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)

---

## 🎯 Tổng Quan

Pipeline tự động hóa 4 bước:

| Bước | Tên | Mô Tả |
|------|-----|--------|
| **A** | Jira MCP Fetcher | Lấy thông tin ticket từ Jira qua MCP Protocol |
| **B** | Test Runner | Chạy test case tự động bằng Robot Framework + Appium |
| **C** | AI Code Analyzer | Đọc code, phân tích lỗi và đề xuất solution fix |
| **D** | GitHub Submitter | Submit code lên GitHub với đầy đủ thông tin fix, impact & test |

---

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI QA AUTOMATION PIPELINE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  STEP A  │───▶│  STEP B  │───▶│  STEP C  │───▶│  STEP D  │  │
│  │          │    │          │    │          │    │          │  │
│  │  Jira    │    │  Robot   │    │   AI     │    │  GitHub  │  │
│  │  MCP     │    │  +Appium │    │ Analyzer │    │ Submit   │  │
│  │ Fetcher  │    │  Runner  │    │  & Fix   │    │  & PR    │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │               │               │               │         │
│       ▼               ▼               ▼               ▼         │
│  ticket_data    test_results    fix_patches      pull_request   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Cấu Trúc Project

```
MCP/
├── 📄 README.md                    # Tài liệu chính (file này)
├── 📄 RULES.md                     # Quy tắc & convention của project
├── 📄 PIPELINE_FLOW.md             # Chi tiết luồng xử lý pipeline
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Template biến môi trường
├── 📄 .gitignore                   # Git ignore rules
│
├── 📁 config/                      # Cấu hình hệ thống
│   ├── jira_config.yaml            # Jira MCP settings
│   ├── appium_config.yaml          # Appium device settings
│   ├── github_config.yaml          # GitHub API settings
│   └── ai_config.yaml              # AI model settings
│
├── 📁 src/                         # Source code chính
│   ├── 📁 jira/                    # STEP A: Jira Integration
│   │   ├── __init__.py
│   │   ├── mcp_client.py           # MCP Protocol client
│   │   ├── ticket_fetcher.py       # Lấy thông tin ticket
│   │   └── ticket_parser.py        # Parse & validate ticket data
│   │
│   ├── 📁 testing/                 # STEP B: Test Execution
│   │   ├── __init__.py
│   │   ├── robot_runner.py         # Robot Framework runner
│   │   ├── appium_driver.py        # Appium WebDriver manager
│   │   ├── test_generator.py       # Tạo test case từ ticket
│   │   └── result_parser.py        # Parse kết quả test
│   │
│   ├── 📁 analyzer/                # STEP C: AI Code Analysis
│   │   ├── __init__.py
│   │   ├── code_reader.py          # Đọc & phân tích source code
│   │   ├── ai_analyzer.py          # AI engine phân tích lỗi
│   │   ├── fix_generator.py        # Tạo solution & patch
│   │   └── impact_assessor.py      # Đánh giá impact của fix
│   │
│   └── 📁 github/                  # STEP D: GitHub Submission
│       ├── __init__.py
│       ├── git_manager.py          # Git operations
│       ├── pr_creator.py           # Tạo Pull Request
│       ├── commit_formatter.py     # Format commit message
│       └── report_builder.py       # Build báo cáo PR
│
├── 📁 tests/                       # Unit & Integration tests
│   ├── test_jira_fetcher.py
│   ├── test_robot_runner.py
│   ├── test_ai_analyzer.py
│   └── test_github_submitter.py
│
├── 📁 robot_tests/                 # Robot Framework test suites
│   ├── resources/
│   │   ├── common.robot            # Keywords dùng chung
│   │   ├── appium_keywords.robot   # Appium-specific keywords
│   │   └── variables.robot         # Global variables
│   └── suites/
│       ├── mobile/                 # Mobile app test suites
│       └── web/                    # Web test suites
│
├── 📁 reports/                     # Kết quả test & báo cáo
│   ├── robot_output/               # Robot Framework output
│   ├── appium_logs/                # Appium session logs
│   └── ai_analysis/                # AI analysis reports
│
├── 📁 logs/                        # System logs
│   └── pipeline.log
│
└── 📁 docs/                        # Tài liệu bổ sung
    ├── setup_guide.md
    ├── jira_mcp_guide.md
    └── appium_setup.md
```

---

## 🔄 Luồng Xử Lý

### STEP A → Jira MCP Fetcher
```
[Input: Ticket ID]
      │
      ▼
MCP Client kết nối Jira Server
      │
      ▼
Lấy ticket data (title, description, acceptance criteria, attachments)
      │
      ▼
Parse & validate → ticket_data.json
```

### STEP B → Robot Framework + Appium Runner
```
[Input: ticket_data.json]
      │
      ▼
Generate test cases từ acceptance criteria
      │
      ▼
Khởi động Appium Server + Device
      │
      ▼
Chạy Robot Framework test suites
      │
      ▼
Thu thập kết quả → test_results.json
```

### STEP C → AI Code Analyzer
```
[Input: test_results.json (có FAIL)]
      │
      ▼
Đọc source code liên quan
      │
      ▼
AI phân tích root cause
      │
      ▼
Đề xuất & tạo fix patch
      │
      ▼
Đánh giá impact → fix_report.json
```

### STEP D → GitHub Submission
```
[Input: fix_report.json + patch files]
      │
      ▼
Tạo branch mới từ ticket ID
      │
      ▼
Apply fix patches
      │
      ▼
Commit với format chuẩn
      │
      ▼
Tạo Pull Request với đầy đủ thông tin
```

---

## ⚙️ Cài Đặt

```bash
# Clone repository
git clone <repo-url>
cd MCP

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

# Cài dependencies
pip install -r requirements.txt

# Cài Appium
npm install -g appium
appium driver install uiautomator2  # Android
appium driver install xcuitest      # iOS

# Copy & cấu hình env
cp .env.example .env
# Chỉnh sửa .env với thông tin thực
```

---

## 🔧 Cấu Hình

### Biến Môi Trường (.env)
```env
# Jira MCP
JIRA_MCP_URL=https://your-jira.atlassian.net
JIRA_API_TOKEN=your_jira_api_token
JIRA_EMAIL=your_email@company.com

# Appium
APPIUM_SERVER_URL=http://localhost:4723
ANDROID_DEVICE_NAME=emulator-5554
IOS_DEVICE_UDID=your_device_udid

# GitHub
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=owner/repository-name
GITHUB_BASE_BRANCH=main

# AI (OpenAI / Claude)
AI_API_KEY=your_ai_api_key
AI_MODEL=gpt-4o
```

---

## 🚀 Hướng Dẫn Sử Dụng

### Chạy toàn bộ pipeline
```bash
python src/main.py --ticket PROJ-1234
```

### Chạy từng bước riêng lẻ
```bash
# Chỉ fetch ticket
python src/main.py --ticket PROJ-1234 --step A

# Chỉ chạy test
python src/main.py --ticket PROJ-1234 --step B

# Chỉ analyze code
python src/main.py --ticket PROJ-1234 --step C

# Chỉ submit GitHub
python src/main.py --ticket PROJ-1234 --step D
```

---

## 📊 Output Mẫu Pull Request

```markdown
## 🎫 Ticket: PROJ-1234 – [Tên ticket]

### 🔍 Root Cause
Mô tả nguyên nhân gốc rễ...

### 🛠️ Solution & Changes
- File: `src/module/feature.py`
  - Thay đổi logic xử lý...

### ⚠️ Impact Assessment
| Area | Level | Notes |
|------|-------|-------|
| Performance | Low | Không ảnh hưởng |
| Security | None | - |
| Breaking Change | No | Backward compatible |

### ✅ How to Test
1. Chạy test suite: `robot robot_tests/suites/...`
2. Expected: All tests PASS
3. Test evidence: [link reports]
```

