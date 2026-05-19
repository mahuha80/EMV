*** Settings ***
Documentation
...    Sample Generated Suite – Mẫu auto-generated từ Jira ticket
...    Đây là template cho ticket bất kỳ, sẽ được THAY THẾ
...    bởi TestCaseMapper khi chạy flow_runner.py
...
...    Cấu trúc:
...      Preconditions → Suite Setup
...      Test Steps    → Shared Keywords
...      Expected      → 1 TC mỗi expected result
Library          AppiumLibrary
Resource         ../../resources/base/appium_base.robot
Resource         ../../resources/base/mobile_keywords.robot
Resource         ../../resources/base/assertions.robot
Resource         ../../resources/variables/android_variables.robot

Suite Setup      Suite Setup For TICKET-SAMPLE
Suite Teardown   Close App On Platform
Test Teardown    Capture Screenshot On Failure

*** Variables ***
${TICKET_ID}     TICKET-SAMPLE
${PLATFORM}      android
${TEST_TYPE}     functional

*** Test Cases ***

TC_001 System Should Show Correct Feedback On Action
    [Documentation]    Expected: System hiển thị feedback đúng sau khi thực hiện action
    [Tags]             TICKET-SAMPLE    functional    P2    android
    Log    Running: TC_001    console=True
    Execute Step: User navigates to the feature screen
    Execute Step: User performs the main action
    Verify: System shows correct feedback

TC_002 App Should Not Crash During Operation
    [Documentation]    Expected: App không crash trong quá trình thực hiện
    [Tags]             TICKET-SAMPLE    functional    P1    android    smoke
    Log    Running: TC_002    console=True
    Execute Step: User navigates to the feature screen
    Execute Step: User performs the main action
    App Should Not Have Crashed

TC_003 Data Should Be Persisted After Action
    [Documentation]    Expected: Dữ liệu được lưu đúng sau khi thực hiện action
    [Tags]             TICKET-SAMPLE    functional    P2    android
    Log    Running: TC_003    console=True
    Execute Step: User navigates to the feature screen
    Execute Step: User performs the main action
    Execute Step: User navigates away and returns
    Verify: Data is correctly persisted

*** Keywords ***

# ─────────────────────────────────────────────────────────────
#  SUITE SETUP – Preconditions
# ─────────────────────────────────────────────────────────────

Suite Setup For TICKET-SAMPLE
    Log    ===== START: ${TICKET_ID} on ${PLATFORM} =====    console=True
    Open App On Platform    ${PLATFORM}
    Precondition: App is installed and launched
    Precondition: User is logged in with valid account

# ─────────────────────────────────────────────────────────────
#  PRECONDITION KEYWORDS
# ─────────────────────────────────────────────────────────────

Precondition: App is installed and launched
    [Documentation]    App phải được cài và launch thành công
    Log    PRECONDITION: App is installed and launched    console=True
    App Should Not Have Crashed
    # TODO: Verify app launch screen

Precondition: User is logged in with valid account
    [Documentation]    User phải đăng nhập trước khi test
    Log    PRECONDITION: User is logged in    console=True
    # TODO: Implement login precondition
    # Gợi ý: Gọi login keywords từ login_tests.robot

# ─────────────────────────────────────────────────────────────
#  STEP KEYWORDS
# ─────────────────────────────────────────────────────────────

Execute Step: User navigates to the feature screen
    [Documentation]    Step: Navigate đến feature cần test
    Log    STEP: Navigate to feature screen    console=True
    # TODO: Implement navigation step

Execute Step: User performs the main action
    [Documentation]    Step: Thực hiện action chính
    Log    STEP: Perform main action    console=True
    # TODO: Implement main action

Execute Step: User navigates away and returns
    [Documentation]    Step: Navigate ra rồi quay lại
    Log    STEP: Navigate away and return    console=True
    Press Back Button
    # TODO: Navigate back

# ─────────────────────────────────────────────────────────────
#  VERIFY KEYWORDS
# ─────────────────────────────────────────────────────────────

Verify: System shows correct feedback
    [Documentation]    Verify hệ thống phản hồi đúng
    Log    VERIFY: System feedback    console=True
    App Should Not Have Crashed
    # TODO: Verify specific feedback element

Verify: Data is correctly persisted
    [Documentation]    Verify dữ liệu được lưu đúng
    Log    VERIFY: Data persisted    console=True
    # TODO: Verify data after navigation

