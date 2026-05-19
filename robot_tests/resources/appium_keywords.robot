*** Settings ***
Documentation    Appium-specific keywords cho mobile testing
Library          AppiumLibrary
Resource         common.robot
Resource         variables.robot

*** Keywords ***
# ── Locator Strategies ───────────────────────────────────

Find By Accessibility ID
    [Documentation]    Tìm element bằng accessibility_id (cross-platform, ưu tiên cao nhất)
    [Arguments]    ${acc_id}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait Until Element Is Visible    accessibility_id=${acc_id}    timeout=${timeout}
    [Return]    accessibility_id=${acc_id}

Find By Resource ID
    [Documentation]    Tìm element bằng Android resource-id
    [Arguments]    ${resource_id}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait Until Element Is Visible    id=${resource_id}    timeout=${timeout}
    [Return]    id=${resource_id}

Find By XPath
    [Documentation]    Tìm element bằng XPath (LAST RESORT – dùng khi không có cách khác)
    [Arguments]    ${xpath}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait Until Element Is Visible    xpath=${xpath}    timeout=${timeout}
    [Return]    xpath=${xpath}

# ── Input ─────────────────────────────────────────────────

Type In Field
    [Documentation]    Nhập text vào field, hỗ trợ cả Android và iOS
    [Arguments]    ${locator}    ${text}
    Wait Until Element Is Visible    ${locator}    timeout=${DEFAULT_TIMEOUT}
    Click Element    ${locator}
    Input Text    ${locator}    ${text}

Clear Field
    [Documentation]    Xóa nội dung trong field
    [Arguments]    ${locator}
    Click Element    ${locator}
    Clear Text    ${locator}

Hide Keyboard If Visible
    [Documentation]    Ẩn bàn phím nếu đang hiển thị
    Run Keyword And Ignore Error    Hide Keyboard

# ── Navigation ────────────────────────────────────────────

Press Back Button
    [Documentation]    Nhấn nút Back (Android)
    Press Keycode    4

Go To Background
    [Documentation]    Đưa app vào background
    [Arguments]    ${seconds}=3
    Background App    ${seconds}

Launch App Again
    [Documentation]    Launch lại app
    Launch Application

# ── Verification ─────────────────────────────────────────

Verify Toast Message
    [Documentation]    Kiểm tra Toast message hiển thị (Android)
    [Arguments]    ${expected_text}    ${timeout}=${SHORT_TIMEOUT}
    Wait Until Page Contains    ${expected_text}    timeout=${timeout}

Verify Alert Displayed
    [Documentation]    Kiểm tra alert dialog hiển thị với text
    [Arguments]    ${expected_text}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait Until Page Contains    ${expected_text}    timeout=${timeout}

Dismiss Alert
    [Documentation]    Đóng alert dialog
    Run Keyword And Ignore Error    Click Element    accessibility_id=OK
    Run Keyword And Ignore Error    Click Element    accessibility_id=Dismiss

Get Element Text
    [Documentation]    Lấy text của element
    [Arguments]    ${locator}
    Wait Until Element Is Visible    ${locator}    timeout=${DEFAULT_TIMEOUT}
    ${text}=    Get Text    ${locator}
    [Return]    ${text}

# ── App State ────────────────────────────────────────────

Verify App Running
    [Documentation]    Kiểm tra app vẫn đang foreground (không crash)
    ${state}=    Query App State    ${ANDROID_APP_PACKAGE}
    Should Be Equal As Strings    ${state}    RUNNING_IN_FOREGROUND
    Log    [ROBOT] App state: RUNNING_IN_FOREGROUND ✅

Reset App State
    [Documentation]    Reset app về trạng thái ban đầu
    Reset Application

