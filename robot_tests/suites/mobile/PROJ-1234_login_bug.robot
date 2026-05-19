*** Settings ***
Documentation    Example test suite cho Login Bug – PROJ-1234
...              Mẫu test suite được viết thủ công (không auto-generated)
Library          AppiumLibrary
Resource         ../../resources/common.robot
Resource         ../../resources/appium_keywords.robot
Resource         ../../resources/variables.robot
Suite Setup      Open Mobile App
Suite Teardown   Close Mobile App
Test Teardown    Run Keyword If Test Failed    Take Screenshot On Failure

*** Variables ***
${LOGIN_USERNAME_FIELD}    accessibility_id=username_input
${LOGIN_PASSWORD_FIELD}    accessibility_id=password_input
${LOGIN_BUTTON}            accessibility_id=login_button
${ERROR_MESSAGE_LABEL}     accessibility_id=error_message
${HOME_SCREEN}             accessibility_id=home_screen

*** Test Cases ***
TC_001 Show Validation Message When Password Is Empty
    [Documentation]    Khi user submit login với password trống phải hiện thông báo lỗi
    [Tags]             PROJ-1234    regression    P1    android
    Given User Is On Login Screen
    When User Enters Username Only
    And User Taps Login Button
    Then Validation Error Should Be Shown    Password cannot be empty

TC_002 App Must Not Crash When Password Is Empty
    [Documentation]    App không được crash khi password field trống
    [Tags]             PROJ-1234    regression    P1    android    smoke
    Given User Is On Login Screen
    When User Enters Username Only
    And User Taps Login Button
    Then App Should Still Be Running

TC_003 Error Message Text Should Match Expected
    [Documentation]    Error message phải đúng text: 'Password cannot be empty'
    [Tags]             PROJ-1234    regression    P2    android
    Given User Is On Login Screen
    When User Enters Username Only
    And User Taps Login Button
    Then Error Message Should Display    Password cannot be empty

*** Keywords ***
User Is On Login Screen
    Wait For Element    ${LOGIN_USERNAME_FIELD}
    Log    [TC] User is on Login Screen

User Enters Username Only
    Type In Field    ${LOGIN_USERNAME_FIELD}    ${VALID_USERNAME}
    Clear Field    ${LOGIN_PASSWORD_FIELD}
    Hide Keyboard If Visible
    Log    [TC] Entered username, left password empty

User Taps Login Button
    Tap Element    ${LOGIN_BUTTON}
    Log    [TC] Tapped Login button

Validation Error Should Be Shown
    [Arguments]    ${expected_message}
    Verify Text Displayed    ${expected_message}    timeout=${DEFAULT_TIMEOUT}
    Log    [TC] ✅ Validation message shown: ${expected_message}

App Should Still Be Running
    Verify App Did Not Crash
    Log    [TC] ✅ App is still running after empty password submit

Error Message Should Display
    [Arguments]    ${expected_text}
    ${actual_text}=    Get Element Text    ${ERROR_MESSAGE_LABEL}
    Should Be Equal    ${actual_text}    ${expected_text}
    Log    [TC] ✅ Error message text matches: ${actual_text}

