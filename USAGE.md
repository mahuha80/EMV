# 🚀 Chạy QA Pipeline – Hướng Dẫn Sử Dụng

## 1️⃣ Setup Ban Đầu (chỉ làm 1 lần)

### Bước 1: Kiểm tra Prerequisites
```bash
python3 --version          # Python 3.10+
robot --version            # Robot Framework
npx --version              # Node.js + npx
```

### Bước 2: Cài đặt (nếu chưa có)
```bash
# Python packages
pip3 install robotframework robotframework-appiumlibrary python-dotenv rich

# mcp-atlassian (Jira MCP server)
npm install -g mcp-atlassian

# Cài AppiumLibrary cho Robot
robot_data=$(python3 -c "import robot; print(robot.__file__.split('lib')[0] + 'lib')")
```

### Bước 3: Điền credentials vào `.env`
```bash
# Xem file hiện tại
cat .env

# Điền:
ATLASSIAN_BASE_URL=https://xuanhieu0423.atlassian.net
ATLASSIAN_EMAIL=xuanhieu0423@gmail.com
ATLASSIAN_API_TOKEN=ATATT3x...C38B0680    # Lấy từ https://id.atlassian.com/...
```

---

## 2️⃣ Chạy Flow – 4 Cách

### 🟢 Cách 1: Full Pipeline (RECOMM ENDED) – Fetch + Parse + Generate + Dryrun
```bash
cd /Users/vinhnt0111/Desktop/MCP
./run.sh --ticket KAN-4 --platform android
```

**Output:**
```
▶ STEP 1 – Fetching KAN-4 từ Jira
  ✅ Ticket data saved

▶ STEP 2 – Analyzing ticket
  📌 3 Preconditions / 5 Steps / 4 Expected

▶ STEP 3 – Generating Robot test suite
  📝 Generated 4 test cases
     TC_001 – App Should Display Validation...
     TC_002 – App Must Not Crash...
     ...

▶ STEP 4 – Running Robot Framework (--dryrun)
  TC_001 ... | PASS |
  TC_002 ... | PASS |
  ...
  ✅ 5/5 PASS   Failed: 0
```

### 🟡 Cách 2: Chỉ Generate (không chạy test)
```bash
./run.sh --ticket KAN-4 --platform android --skip-run
```

File robot sẽ được generate trong: `robot_tests/suites/generated/KAN-4_android.robot`

### 🔵 Cách 3: Dry-run (in file robot ra stdout)
```bash
./run.sh --ticket KAN-4 --platform android --dry-run
```

### 🔴 Cách 4: Chạy Direct Python
```bash
cd /Users/vinhnt0111/Desktop/MCP
PYTHONPATH=src python3 src/jira_flow.py --ticket KAN-4 --platform android
```

---

## 3️⃣ Chạy Actual Test (trên Device/Emulator)

### Yêu cầu:
- ✅ Appium server đang chạy: `appium --port 4723`
- ✅ Android device/emulator connected
- ✅ App đã được cài trên device

### Chạy:
```bash
# Cách 1: Robot command trực tiếp
robot robot_tests/suites/generated/KAN-4_android.robot

# Cách 2: Với variables
robot \
  --variable PLATFORM:android \
  --variable APPIUM_URL:http://localhost:4723 \
  --variable ANDROID_DEVICE_NAME:emulator-5554 \
  --variable ANDROID_APP_PACKAGE:com.your.app \
  --variable ANDROID_APP_ACTIVITY:.MainActivity \
  robot_tests/suites/generated/KAN-4_android.robot

# Cách 3: Với output directory
robot \
  --outputdir reports/KAN-4/actual_run \
  robot_tests/suites/generated/KAN-4_android.robot
```

### Output:
```
Test Execution
==============================================================================
KAN-4 android
TC_001 App Displays Validation Message                         | PASS |
TC_002 App Must Not Crash                                       | PASS |
TC_003 User Remains On Login Screen                             | PASS |
TC_004 Error Message Visible                                    | PASS |
==============================================================================
Test Execution
4 tests, 4 passed, 0 failed
```

---

## 4️⃣ Các Tùy Chọn Khác

### Chạy Multiple Tickets
```bash
for TICKET in KAN-4 KAN-5 KAN-6; do
  ./run.sh --ticket $TICKET
done
```

### Chạy trên iOS
```bash
./run.sh --ticket KAN-4 --platform ios
```

### Xem báo cáo
```bash
# Report HTML
open reports/KAN-4/robot_output/report.html

# Ticket data JSON
cat reports/KAN-4/ticket_data.json

# Robot log
open reports/KAN-4/robot_output/log.html
```

---

## 5️⃣ Troubleshooting

### ❌ "Jira credentials invalid"
```bash
# Kiểm tra .env
cat .env | grep ATLASSIAN

# Test kết nối
curl -u "email@example.com:token" \
  https://your.atlassian.net/rest/api/3/myself
```

### ❌ "Appium server not reachable"
```bash
# Khởi động Appium
appium --port 4723

# Test connection
curl http://localhost:4723/status
```

### ❌ "Device not found"
```bash
# Check adb devices
adb devices

# Use correct device name
./run.sh --ticket KAN-4 --variable ANDROID_DEVICE_NAME:192.168.1.100:5555
```

### ❌ "Robot keyword not found"
```bash
# Check Robot installation
robot --version
robot --list-profiles

# Reinstall AppiumLibrary
pip3 install --force-reinstall robotframework-appiumlibrary
```

---

## 6️⃣ Flow Diagram

```
┌─────────────┐
│ ./run.sh    │  --ticket KAN-4 --platform android
└──────┬──────┘
       │
       ▼ STEP 1: Fetch từ Jira
┌─────────────────────────────────┐
│ Jira REST API                   │
│ KAN-4: [Android] Login crashes  │
└──────┬──────────────────────────┘
       │
       ▼ STEP 2: Analyze
┌─────────────────────────────────┐
│ TicketAnalyzer (regex)          │
│ → 3 precond / 5 steps / 4 exp   │
└──────┬──────────────────────────┘
       │
       ▼ STEP 3: Generate
┌─────────────────────────────────┐
│ TestCaseMapper + AIRobotGenerator│
│ → SmartMapper (Appium keywords) │
│ → KAN-4_android.robot (4 TCs)   │
└──────┬──────────────────────────┘
       │
       ▼ STEP 4A: Dryrun
┌─────────────────────────────────┐
│ Robot Framework --dryrun        │
│ Validate syntax & keywords      │
│ ✅ 5/5 PASS                      │
└──────┬──────────────────────────┘
       │
       ├─────────────────────────────┐
       │                             │
       ▼ STEP 4B: Actual (opt)       ▼ Reports
  ┌────────────────┐           ┌──────────────┐
  │Robot + Appium  │           │reports/KAN-4/│
  │ on device      │           │ ├─ ticket_data.json
  │✅ PASS/FAIL    │           │ ├─ report.html
  └────────────────┘           │ └─ output.xml
                                └──────────────┘
```

---

## 📝 Ví Dụ Thực Tế

### Scenario 1: QA vừa nhận ticket KAN-4, cần chạy test ngay
```bash
cd /Users/vinhnt0111/Desktop/MCP
./run.sh --ticket KAN-4

# Kết quả: file robot được generate + dryrun qua chạy ✅
```

### Scenario 2: Có device setup xong, chạy test thật
```bash
# Bước 1: Generate (không chạy device chưa sẵn sàng)
./run.sh --ticket KAN-4 --skip-run

# [Chuẩn bị device, kết nối Appium]

# Bước 2: Chạy test thật
robot robot_tests/suites/generated/KAN-4_android.robot

# Xem kết quả
open reports/KAN-4/robot_output/report.html
```

### Scenario 3: Batch run 3 tickets
```bash
for TICKET in KAN-4 KAN-5 KAN-6; do
  echo "=== Running $TICKET ==="
  ./run.sh --ticket $TICKET --platform android || true
done
```

---

## 🆘 Help
```bash
./run.sh --help
```


