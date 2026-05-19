*** Settings ***
Documentation
...    Login Test Suite – Các test case liên quan đến màn hình Login
...    Precondition: App đã được cài, không có session đang active
...    Platform: Android / iOS
Library          AppiumLibrary
Resource         ../../resources/base/appium_base.robot
Resource         ../../resources/base/mobile_keywords.robot
Resource         ../../resources/base/assertions.robot
Resource         ../../resources/variables/android_variables.robot

Suite Setup      Open App On Platform    android
Suite Teardown   Close App On Platform
Test Teardown    Capture Screenshot On Failure

*** Variables ***
# ── Locators (thay bằng locator thực của app) ───────────────
${LOC_EMAIL_FIELD}         accessibility_id=email_input
${LOC_PASSWORD_FIELD}      accessibility_id=password_input
${LOC_LOGIN_BUTTON}        accessibility_id=login_button
${LOC_ERROR_MESSAGE}       accessibility_id=error_message
${LOC_FORGOT_PASSWORD}     accessibility_id=forgot_password_link
${LOC_HOME_SCREEN}         accessibility_id=home_screen_container
${LOC_LOADING_INDICATOR}   id=progress_indicator

# ── Test Data ────────────────────────────────────────────────
${WRONG_EMAIL}             notexist@example.com
${WRONG_PASSWORD}          WrongPass999!
${ERROR_INVALID_CRED}      Invalid email or password
${ERROR_EMPTY_EMAIL}       Email cannot be empty
${ERROR_EMPTY_PASSWORD}    Password cannot be empty
${ERROR_INVALID_FORMAT}    Please enter a valid email address

*** Test Cases ***

# ════════════════════════════════════════════════════════════
#  TC_001 – HAPPY PATH
# ════════════════════════════════════════════════════════════

TC_001 Login With Valid Credentials Should Navigate To Home
    [Documentation]
    ...    Precondition: User đã có account hợp lệ
    ...    Steps: Nhập email + password đúng → Tap Login
    ...    Expected: Chuyển sang màn hình Home
    [Tags]    login    smoke    P1    happy-path
    Given Login Screen Is Displayed
    When User Enters Valid Credentials
    And User Taps Login Button
    Then Home Screen Should Be Shown

# ══════════════════════════════════════════════════════════��═
#  TC_002 – TC_004: INVALID CREDENTIALS
# ════════════════════════════════════════════════════════════

TC_002 Login With Wrong Password Should Show Error
    [Documentation]
    ...    Steps: Nhập email đúng, password sai → Tap Login
    ...    Expected: Hiện error "Invalid email or password"
    [Tags]    login    regression    P1    negative
    Given Login Screen Is Displayed
    When User Enters Email    ${VALID_EMAIL}
    And User Enters Password    ${WRONG_PASSWORD}
    And User Taps Login Button
    Then Error Message Should Be Shown    ${ERROR_INVALID_CRED}
    And App Should Not Have Crashed

TC_003 Login With Non-Existent Account Should Show Error
    [Documentation]
    ...    Steps: Nhập email không tồn tại → Tap Login
    ...    Expected: Hiện error message
    [Tags]    login    regression    P2    negative
    Given Login Screen Is Displayed
    When User Enters Email    ${WRONG_EMAIL}
    And User Enters Password    ${VALID_PASSWORD}
    And User Taps Login Button
    Then Error Message Should Be Shown    ${ERROR_INVALID_CRED}

TC_004 Login With Wrong Email Format Should Show Validation Error
    [Documentation]
    ...    Steps: Nhập email sai format (thiếu @) → Tap Login
    ...    Expected: Hiện validation error về format email
    [Tags]    login    regression    P2    validation
    Given Login Screen Is Displayed
    When User Enters Email    invalid-email-format
    And User Enters Password    ${VALID_PASSWORD}
    And User Taps Login Button
    Then Error Message Should Be Shown    ${ERROR_INVALID_FORMAT}

# ════════════════════════════════════════════════════════════
#  TC_005 – TC_007: EMPTY FIELDS
# ══���═════════════════════════════════════════════════════════

TC_005 Login With Empty Email Should Show Validation Error
    [Documentation]
    ...    Steps: Để trống email, nhập password → Tap Login
    ...    Expected: Hiện "Email cannot be empty"
    ...    App KHÔNG được crash
    [Tags]    login    regression    P1    validation    empty-field
    Given Login Screen Is Displayed
    When User Enters Email    ${EMPTY_STRING}
    And User Enters Password    ${VALID_PASSWORD}
    And User Taps Login Button
    Then Error Message Should Be Shown    ${ERROR_EMPTY_EMAIL}
    And App Should Not Have Crashed

TC_006 Login With Empty Password Should Show Validation Error
    [Documentation]
    ...    Steps: Nhập email, để trống password → Tap Login
    ...    Expected: Hiện "Password cannot be empty"
    ...    App KHÔNG được crash
    [Tags]    login    regression    P1    validation    empty-field
    Given Login Screen Is Displayed
    When User Enters Email    ${VALID_EMAIL}
    And User Enters Password    ${EMPTY_STRING}
    And User Taps Login Button
    Then Error Message Should Be Shown    ${ERROR_EMPTY_PASSWORD}
    And App Should Not Have Crashed

TC_007 Login With Both Fields Empty Should Show Validation Error
    [Documentation]
    ...    Steps: Để trống cả 2 fields → Tap Login
    ...    Expected: Hiện validation error
    [Tags]    login    regression    P2    validation    empty-field
    Given Login Screen Is Displayed
    When User Taps Login Button
    Then App Should Not Have Crashed
    And Page Should Show Text    ${ERROR_EMPTY_EMAIL}

# ════════════════════════════════════════════════════════════
#  TC_008 – TC_009: UX / SECURITY
# ════════════════════════════════════════════════════════════

TC_008 Password Field Should Mask Input By Default
    [Documentation]
    ...    Expected: Password field hiển thị dạng ••••• (masked)
    [Tags]    login    regression    P2    security    ux
    Given Login Screen Is Displayed
    When User Enters Password    ${VALID_PASSWORD}
    Then Password Should Be Masked

TC_009 Forgot Password Link Should Navigate To Reset Screen
    [Documentation]
    ...    Steps: Tap "Forgot Password"
    ...    Expected: Chuyển sang màn hình Reset Password
    [Tags]    login    regression    P2    navigation
    Given Login Screen Is Displayed
    When User Taps Forgot Password Link
    Then Reset Password Screen Should Be Displayed

*** Keywords ***

# ── Given ────────────────────────────────────────────────────

Login Screen Is Displayed
    [Documentation]    Verify đang ở màn hình Login
    Current Screen Should Be    ${LOC_EMAIL_FIELD}
    Log    ✅ On Login Screen

# ── When ─────────────────────────────────────────────────────

User Enters Valid Credentials
    User Enters Email    ${VALID_EMAIL}
    User Enters Password    ${VALID_PASSWORD}

User Enters Email
    [Arguments]    ${email}
    Input Text To Field    ${LOC_EMAIL_FIELD}    ${email}
    Hide Keyboard If Shown

User Enters Password
    [Arguments]    ${password}
    Input Text To Field    ${LOC_PASSWORD_FIELD}    ${password}
    Hide Keyboard If Shown

User Taps Login Button
    Tap Element By Accessibility ID    login_button
    Wait For Loading Done    ${LOC_LOADING_INDICATOR}

User Taps Forgot Password Link
    Tap Element By Accessibility ID    forgot_password_link

# ── Then ─────────────────────────────────────────────────────

Home Screen Should Be Shown
    [Documentation]    Verify navigate thành công sang Home
    Wait For Element Visible    ${LOC_HOME_SCREEN}    ${TIMEOUT_PAGE_LOAD}
    Log    ✅ Navigated to Home Screen

Password Should Be Masked
    ${attr}=    Get Element Attribute    ${LOC_PASSWORD_FIELD}    password
    Should Be Equal    ${attr}    true    msg=Password field is NOT masked!
    Log    ✅ Password field is masked

Reset Password Screen Should Be Displayed
    Page Should Show Text    Reset Password
    Log    ✅ Reset Password screen displayed

