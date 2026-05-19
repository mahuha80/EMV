*** Settings ***
Documentation    Mobile interaction keywords – tap, type, scroll, swipe, etc.
Resource         appium_base.robot

*** Keywords ***

# ═══════════════════════════════════════════════════════════════
#  TAP / CLICK
# ═══════════════════════════════════════════════════════════════

Tap Element By Accessibility ID
    [Documentation]    Tap element bằng accessibility_id (ưu tiên cao nhất)
    [Arguments]    ${acc_id}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait For Element Visible    accessibility_id=${acc_id}    ${timeout}
    Click Element    accessibility_id=${acc_id}
    Log    Tapped [accessibility_id]: ${acc_id}

Tap Element By ID
    [Documentation]    Tap element bằng resource-id
    [Arguments]    ${res_id}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait For Element Visible    id=${res_id}    ${timeout}
    Click Element    id=${res_id}
    Log    Tapped [id]: ${res_id}

Tap Element By Text
    [Documentation]    Tap element theo text hiển thị
    [Arguments]    ${text}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait For Element Visible    xpath=//*[@text='${text}' or @label='${text}']    ${timeout}
    Click Element    xpath=//*[@text='${text}' or @label='${text}']
    Log    Tapped [text]: ${text}

Tap Element By XPath
    [Documentation]    Tap element bằng XPath (LAST RESORT)
    [Arguments]    ${xpath}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait For Element Visible    xpath=${xpath}    ${timeout}
    Click Element    xpath=${xpath}
    Log    Tapped [xpath]: ${xpath}

Double Tap
    [Documentation]    Double tap element
    [Arguments]    ${locator}
    Click Element    ${locator}
    Sleep    0.1s
    Click Element    ${locator}

# ═══════════════════════════════════════════════════════════════
#  INPUT TEXT
# ═══════════════════════════════════════════════════════════════

Input Text To Field
    [Documentation]    Xóa và nhập text vào field
    [Arguments]    ${locator}    ${text}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait For Element Visible    ${locator}    ${timeout}
    Clear Text    ${locator}
    Input Text    ${locator}    ${text}
    Log    Input '${text}' → ${locator}

Input Text By Accessibility ID
    [Documentation]    Nhập text vào field tìm bằng accessibility_id
    [Arguments]    ${acc_id}    ${text}
    Input Text To Field    accessibility_id=${acc_id}    ${text}

Input Text By ID
    [Documentation]    Nhập text vào field tìm bằng resource-id
    [Arguments]    ${res_id}    ${text}
    Input Text To Field    id=${res_id}    ${text}

Clear Field
    [Documentation]    Xóa text trong field
    [Arguments]    ${locator}
    Click Element    ${locator}
    Clear Text    ${locator}

Hide Keyboard If Shown
    [Documentation]    Ẩn bàn phím nếu đang hiển thị
    Run Keyword And Ignore Error    Hide Keyboard

# ═══════════════════════════════════════════════════════════════
#  SCROLL / SWIPE
# ═══════════════════════════════════════════════════════════════

Scroll Down Once
    [Documentation]    Scroll xuống 1 lần từ giữa màn hình
    ${size}=    Get Window Size
    ${w}=       Evaluate    ${size['width']} // 2
    ${from_y}=  Evaluate    int(${size['height']} * 0.7)
    ${to_y}=    Evaluate    int(${size['height']} * 0.3)
    Swipe    ${w}    ${from_y}    ${w}    ${to_y}    500

Scroll Up Once
    [Documentation]    Scroll lên 1 lần từ giữa màn hình
    ${size}=    Get Window Size
    ${w}=       Evaluate    ${size['width']} // 2
    ${from_y}=  Evaluate    int(${size['height']} * 0.3)
    ${to_y}=    Evaluate    int(${size['height']} * 0.7)
    Swipe    ${w}    ${from_y}    ${w}    ${to_y}    500

Scroll Down Until Text Visible
    [Documentation]    Scroll xuống cho đến khi text xuất hiện (max 10 lần)
    [Arguments]    ${text}    ${max_swipes}=10
    FOR    ${i}    IN RANGE    ${max_swipes}
        ${visible}=    Run Keyword And Return Status
        ...    Page Should Contain Text    ${text}
        Exit For Loop If    ${visible}
        Scroll Down Once
    END
    Page Should Contain Text    ${text}

Swipe Left On Element
    [Documentation]    Swipe left trên element (ví dụ: delete item)
    [Arguments]    ${locator}
    ${elem}=      Get WebElement    ${locator}
    ${loc}=       Get Element Location    ${locator}
    ${size}=      Get Element Size    ${locator}
    ${start_x}=   Evaluate    ${loc['x']} + ${size['width']} - 10
    ${end_x}=     Evaluate    ${loc['x']} + 10
    ${mid_y}=     Evaluate    ${loc['y']} + ${size['height']} // 2
    Swipe    ${start_x}    ${mid_y}    ${end_x}    ${mid_y}    400

Swipe Right On Element
    [Documentation]    Swipe right trên element
    [Arguments]    ${locator}
    ${elem}=      Get WebElement    ${locator}
    ${loc}=       Get Element Location    ${locator}
    ${size}=      Get Element Size    ${locator}
    ${start_x}=   Evaluate    ${loc['x']} + 10
    ${end_x}=     Evaluate    ${loc['x']} + ${size['width']} - 10
    ${mid_y}=     Evaluate    ${loc['y']} + ${size['height']} // 2
    Swipe    ${start_x}    ${mid_y}    ${end_x}    ${mid_y}    400

# ═══════════════════════════════════════════════════════════════
#  NAVIGATION
# ═══════════════════════════════════════════════════════════════

Press Back Button
    [Documentation]    Nhấn nút Back (Android hardware back)
    Press Keycode    4

Press Home Button
    [Documentation]    Nhấn nút Home (Android)
    Press Keycode    3

Go To Background And Return
    [Documentation]    Đưa app vào background rồi quay lại
    [Arguments]    ${seconds}=3
    Background App    ${seconds}
    Log    App returned from background after ${seconds}s

# ═══════════════════════════════════════════════════════════════
#  APP STATE
# ═══════════════════════════════════════════════════════════════

Get Current Screen Text
    [Documentation]    Lấy toàn bộ text từ page source hiện tại
    ${source}=    Get Source
    RETURN    ${source}

App Should Be In Foreground
    [Documentation]    Verify app vẫn đang chạy ở foreground (không crash)
    ${source}=    Get Source
    Should Not Contain    ${source}    Unfortunately
    Should Not Contain    ${source}    has stopped
    Should Not Contain    ${source}    keeps stopping
    Log    ✅ App is running normally in foreground

