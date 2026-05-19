*** Settings ***
Documentation    Assertion keywords – verify UI state, text, elements, app health
Library          String
Resource         appium_base.robot

*** Keywords ***

# ═══════════════════════════════════════════════════════════════
#  ELEMENT ASSERTIONS
# ═══════════════════════════════════════════════════════════════

Element Should Be Visible On Screen
    [Documentation]    Assert element visible trên màn hình hiện tại
    [Arguments]    ${locator}    ${timeout}=${TIMEOUT_DEFAULT}    ${message}=${EMPTY}
    ${msg}=    Set Variable If    '${message}' == '${EMPTY}'
    ...    Element should be visible: ${locator}    ${message}
    Run Keyword And Continue On Failure
    ...    Wait Until Element Is Visible    ${locator}    timeout=${timeout}    error=${msg}
    Log    ✅ Verified visible: ${locator}

Element Should NOT Be Visible On Screen
    [Documentation]    Assert element KHÔNG visible
    [Arguments]    ${locator}    ${timeout}=3s
    Run Keyword And Continue On Failure
    ...    Wait Until Element Is Not Visible    ${locator}    timeout=${timeout}
    Log    ✅ Verified NOT visible: ${locator}

Element Should Exist In Page
    [Documentation]    Assert element tồn tại trong DOM (không cần visible)
    [Arguments]    ${locator}
    Page Should Contain Element    ${locator}
    Log    ✅ Element exists: ${locator}

Element Count Should Be
    [Documentation]    Verify số lượng element match locator
    [Arguments]    ${locator}    ${expected_count}
    ${count}=    Get Element Count    ${locator}
    Should Be Equal As Integers    ${count}    ${expected_count}
    ...    msg=Expected ${expected_count} elements but found ${count}: ${locator}
    Log    ✅ Element count verified: ${count}

# ═══════════════════════════════════════════════════════════════
#  TEXT ASSERTIONS
# ═══════════════════════════════════════════════════════════════

Page Should Show Text
    [Documentation]    Verify text xuất hiện ở đâu đó trên screen
    [Arguments]    ${text}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait Until Page Contains    ${text}    timeout=${timeout}
    Log    ✅ Text found: '${text}'

Page Should NOT Show Text
    [Documentation]    Verify text KHÔNG xuất hiện trên screen
    [Arguments]    ${text}
    Page Should Not Contain Text    ${text}
    Log    ✅ Text not present: '${text}'

Element Text Should Equal
    [Documentation]    Verify text của element bằng expected value
    [Arguments]    ${locator}    ${expected}
    ${actual}=    Get Text    ${locator}
    Should Be Equal    ${actual}    ${expected}
    ...    msg=Text mismatch → Expected: '${expected}' | Actual: '${actual}'
    Log    ✅ Text matched: '${actual}'

Element Text Should Contain
    [Documentation]    Verify text của element chứa substring
    [Arguments]    ${locator}    ${substring}
    ${actual}=    Get Text    ${locator}
    Should Contain    ${actual}    ${substring}
    ...    msg=Expected '${substring}' in '${actual}'
    Log    ✅ Text contains: '${substring}'

Element Text Should Not Be Empty
    [Documentation]    Verify element có text (không rỗng)
    [Arguments]    ${locator}
    ${text}=    Get Text    ${locator}
    Should Not Be Empty    ${text}    msg=Element text is empty: ${locator}
    Log    ✅ Text not empty: '${text}'

# ═══════════════════════════════════════════════════════════════
#  ATTRIBUTE ASSERTIONS
# ═══════════════════════════════════════════════════════════════

Element Should Be Enabled
    [Documentation]    Verify element ở trạng thái enabled (clickable)
    [Arguments]    ${locator}
    ${enabled}=    Get Element Attribute    ${locator}    enabled
    Should Be Equal    ${enabled}    true
    ...    msg=Element is disabled: ${locator}
    Log    ✅ Element enabled: ${locator}

Element Should Be Disabled
    [Documentation]    Verify element ở trạng thái disabled
    [Arguments]    ${locator}
    ${enabled}=    Get Element Attribute    ${locator}    enabled
    Should Be Equal    ${enabled}    false
    ...    msg=Element should be disabled: ${locator}

Element Should Be Checked
    [Documentation]    Verify checkbox/toggle đang được check
    [Arguments]    ${locator}
    ${checked}=    Get Element Attribute    ${locator}    checked
    Should Be Equal    ${checked}    true
    ...    msg=Element is NOT checked: ${locator}
    Log    ✅ Element is checked

Element Should NOT Be Checked
    [Documentation]    Verify checkbox/toggle KHÔNG được check
    [Arguments]    ${locator}
    ${checked}=    Get Element Attribute    ${locator}    checked
    Should Be Equal    ${checked}    false
    ...    msg=Element should NOT be checked: ${locator}

# ═══════════════════════════════════════════════════════════════
#  APP HEALTH ASSERTIONS
# ═══════════════════════════════════════════════════════════════

App Should Not Have Crashed
    [Documentation]    Verify app không bị crash (không hiện dialog lỗi)
    ${source}=    Get Source
    ${crash_strings}=    Create List
    ...    Unfortunately    has stopped    keeps stopping
    ...    Force Close      ANR            Application Error
    FOR    ${crash_str}    IN    @{crash_strings}
        Run Keyword And Continue On Failure
        ...    Should Not Contain    ${source}    ${crash_str}
        ...    msg=⚠️ Crash detected: '${crash_str}' found in page source
    END
    Log    ✅ App is healthy – no crash detected

Error Message Should Be Shown
    [Documentation]    Verify error/validation message hiển thị
    [Arguments]    ${expected_message}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait Until Page Contains    ${expected_message}    timeout=${timeout}
    Log    ✅ Error message shown: '${expected_message}'

Error Message Should NOT Be Shown
    [Documentation]    Verify KHÔNG có error message
    [Arguments]    ${message}
    Page Should Not Contain Text    ${message}
    Log    ✅ No error message: '${message}'

Toast Message Should Appear
    [Documentation]    Verify toast message xuất hiện và biến mất (Android)
    [Arguments]    ${expected_text}    ${timeout}=5s
    Wait Until Page Contains    ${expected_text}    timeout=${timeout}
    Log    ✅ Toast shown: '${expected_text}'

# ═══════════════════════════════════════════════════════════════
#  NAVIGATION ASSERTIONS
# ═══════════════════════════════════════════════════════════════

Current Screen Should Be
    [Documentation]    Verify đang ở màn hình đúng bằng cách kiểm tra unique element
    [Arguments]    ${screen_identifier}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait Until Element Is Visible    ${screen_identifier}    timeout=${timeout}
    Log    ✅ Current screen verified: ${screen_identifier}

URL Should Contain
    [Documentation]    Verify URL hiện tại (WebView context)
    [Arguments]    ${expected_url_part}
    ${url}=    Get Location
    Should Contain    ${url}    ${expected_url_part}
    Log    ✅ URL contains: ${expected_url_part}

