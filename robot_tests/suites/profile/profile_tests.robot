*** Settings ***
Documentation
...    Profile Test Suite – Xem, chỉnh sửa thông tin cá nhân
...    Precondition: User đã đăng nhập
Library          AppiumLibrary
Resource         ../../resources/base/appium_base.robot
Resource         ../../resources/base/mobile_keywords.robot
Resource         ../../resources/base/assertions.robot
Resource         ../../resources/variables/android_variables.robot
Resource         ../login/login_tests.robot

Suite Setup      Login And Navigate To Profile
Suite Teardown   Close App On Platform
Test Teardown    Capture Screenshot On Failure

*** Variables ***
${LOC_PROFILE_TAB}            accessibility_id=profile_tab
${LOC_EDIT_BUTTON}            accessibility_id=edit_profile_button
${LOC_FULLNAME_FIELD}         accessibility_id=fullname_input
${LOC_PHONE_FIELD}            accessibility_id=phone_input
${LOC_SAVE_BUTTON}            accessibility_id=save_button
${LOC_SUCCESS_MESSAGE}        accessibility_id=success_toast
${LOC_AVATAR}                 accessibility_id=profile_avatar
${LOC_LOGOUT_BUTTON}          accessibility_id=logout_button
${LOC_CONFIRM_LOGOUT}         accessibility_id=confirm_logout_button
${LOC_LOGIN_SCREEN}           accessibility_id=email_input

${NEW_FULLNAME}               QA Test User Updated
${INVALID_PHONE}              abc-not-a-phone
${ERROR_INVALID_PHONE}        Please enter a valid phone number
${MSG_PROFILE_UPDATED}        Profile updated successfully

*** Test Cases ***

TC_001 Profile Screen Should Display User Information
    [Documentation]
    ...    Expected: Màn hình Profile hiển thị đúng thông tin user
    [Tags]    profile    smoke    P1
    Current Screen Should Be    ${LOC_AVATAR}
    Page Should Show Text    ${VALID_EMAIL}
    Log    ✅ Profile info displayed correctly

TC_002 Edit Profile With Valid Name Should Save Successfully
    [Documentation]
    ...    Steps: Tap Edit → Sửa Full Name → Save
    ...    Expected: Toast "Profile updated successfully"
    [Tags]    profile    regression    P1    edit
    Given User Is On Profile Screen
    When User Taps Edit Button
    And User Updates Full Name    ${NEW_FULLNAME}
    And User Taps Save Button
    Then Success Message Should Appear    ${MSG_PROFILE_UPDATED}
    And Profile Name Should Be Updated    ${NEW_FULLNAME}

TC_003 Edit Profile With Invalid Phone Should Show Validation Error
    [Documentation]
    ...    Steps: Tap Edit → Nhập phone sai format → Save
    ...    Expected: Hiện validation error về phone
    [Tags]    profile    regression    P2    validation    negative
    Given User Is On Profile Screen
    When User Taps Edit Button
    And User Enters Phone Number    ${INVALID_PHONE}
    And User Taps Save Button
    Then Error Message Should Be Shown    ${ERROR_INVALID_PHONE}

TC_004 Cancel Edit Should Not Save Changes
    [Documentation]
    ...    Steps: Tap Edit → Sửa Name → Tap Cancel
    ...    Expected: Name KHÔNG thay đổi
    [Tags]    profile    regression    P2
    Given User Is On Profile Screen
    ${original_name}=    Get Element Text    ${LOC_FULLNAME_FIELD}
    When User Taps Edit Button
    And User Updates Full Name    SHOULD_NOT_SAVE_THIS
    And User Taps Back Without Saving
    Then Profile Name Should Be Updated    ${original_name}

TC_005 Logout Should Return To Login Screen
    [Documentation]
    ...    Steps: Tap Logout → Confirm
    ...    Expected: Quay về màn hình Login
    [Tags]    profile    regression    P1    logout
    Given User Is On Profile Screen
    When User Taps Logout
    And User Confirms Logout
    Then Login Screen Should Be Shown

*** Keywords ***

Login And Navigate To Profile
    Open App On Platform    android
    User Enters Valid Credentials
    User Taps Login Button
    Wait For Element Visible    ${LOC_PROFILE_TAB}    ${TIMEOUT_PAGE_LOAD}
    Tap Element By Accessibility ID    profile_tab

User Is On Profile Screen
    Current Screen Should Be    ${LOC_AVATAR}

User Taps Edit Button
    Tap Element By Accessibility ID    edit_profile_button

User Updates Full Name
    [Arguments]    ${name}
    Input Text To Field    ${LOC_FULLNAME_FIELD}    ${name}
    Hide Keyboard If Shown

User Enters Phone Number
    [Arguments]    ${phone}
    Input Text To Field    ${LOC_PHONE_FIELD}    ${phone}
    Hide Keyboard If Shown

User Taps Save Button
    Tap Element By Accessibility ID    save_button
    Wait For Loading Done

User Taps Back Without Saving
    Press Back Button

User Taps Logout
    Scroll Down Until Text Visible    Logout
    Tap Element By Accessibility ID    logout_button

User Confirms Logout
    Wait For Element Visible    ${LOC_CONFIRM_LOGOUT}
    Tap Element By Accessibility ID    confirm_logout_button

Success Message Should Appear
    [Arguments]    ${message}
    Toast Message Should Appear    ${message}
    Log    ✅ Success message: '${message}'

Profile Name Should Be Updated
    [Arguments]    ${expected_name}
    Element Text Should Equal    ${LOC_FULLNAME_FIELD}    ${expected_name}
    Log    ✅ Profile name: '${expected_name}'

Login Screen Should Be Shown
    Wait For Element Visible    ${LOC_LOGIN_SCREEN}    ${TIMEOUT_PAGE_LOAD}
    Log    ✅ Returned to Login screen

Get Element Text
    [Arguments]    ${locator}
    ${text}=    Get Text    ${locator}
    [Return]    ${text}

