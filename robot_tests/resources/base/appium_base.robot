*** Settings ***
Documentation
...    appium_base.robot – Khởi tạo và quản lý Appium session
...    Tất cả test suites đều Resource file này
Library     AppiumLibrary    run_on_failure=Capture Screenshot On Failure
Library     Collections
Library     String
Library     OperatingSystem
Resource    ../variables/android_variables.robot
Resource    ../variables/ios_variables.robot

*** Keywords ***

# ═══════════════════════════════════════════════════════════════
#  SESSION MANAGEMENT
# ═══════════════════════════════════════════════════════════════

Open App On Platform
    [Documentation]    Mở app tương ứng với platform (android/ios)
    [Arguments]    ${platform}=${PLATFORM}
    Run Keyword If    '${platform}' == 'android'    Open Android App
    ...    ELSE IF    '${platform}' == 'ios'         Open iOS App
    ...    ELSE       Fail    Unsupported platform: ${platform}
    Log    ✅ App opened on ${platform}    console=True

Open Android App
    [Documentation]    Khởi động app Android với UiAutomator2
    Open Application    ${APPIUM_URL}
    ...    platformName=${ANDROID_PLATFORM_NAME}
    ...    automationName=${ANDROID_AUTOMATION}
    ...    deviceName=${ANDROID_DEVICE_NAME}
    ...    appPackage=${ANDROID_APP_PACKAGE}
    ...    appActivity=${ANDROID_APP_ACTIVITY}
    ...    noReset=${ANDROID_NO_RESET}
    ...    autoGrantPermissions=${TRUE}
    ...    newCommandTimeout=300

Open iOS App
    [Documentation]    Khởi động app iOS với XCUITest
    Open Application    ${APPIUM_URL}
    ...    platformName=${IOS_PLATFORM_NAME}
    ...    automationName=${IOS_AUTOMATION}
    ...    udid=${IOS_UDID}
    ...    bundleId=${IOS_BUNDLE_ID}
    ...    noReset=${IOS_NO_RESET}
    ...    newCommandTimeout=300
    ...    wdaLaunchTimeout=120000

Close App On Platform
    [Documentation]    Đóng Appium session
    Run Keyword And Ignore Error    Close Application
    Log    App session closed    console=True

Restart App
    [Documentation]    Restart app về trạng thái fresh
    Close Application
    Sleep    1s
    Open App On Platform

Reset App State
    [Documentation]    Reset app data mà không restart session
    Reset Application

# ═══════════════════════════════════════════════════════════════
#  WAIT UTILITIES
# ═══════════════════════════════════════════════════════════════

Wait For Element Visible
    [Documentation]    Chờ element visible trong timeout
    [Arguments]    ${locator}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait Until Element Is Visible    ${locator}    timeout=${timeout}
    Log    Element visible: ${locator}

Wait For Element Gone
    [Documentation]    Chờ element biến mất
    [Arguments]    ${locator}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait Until Element Is Not Visible    ${locator}    timeout=${timeout}

Wait For Text Present
    [Documentation]    Chờ text xuất hiện trong page source
    [Arguments]    ${text}    ${timeout}=${TIMEOUT_DEFAULT}
    Wait Until Page Contains    ${text}    timeout=${timeout}

Wait For Loading Done
    [Documentation]    Chờ loading spinner biến mất (nếu có)
    [Arguments]    ${spinner_locator}=id=loading_spinner    ${timeout}=${TIMEOUT_LONG}
    Run Keyword And Ignore Error
    ...    Wait Until Element Is Not Visible    ${spinner_locator}    timeout=${timeout}

# ═══════════════════════════════════════════════════════════════
#  SCREENSHOT
# ═══════════════════════════════════════════════════════════════

Capture Screenshot On Failure
    [Documentation]    Chụp screenshot khi test case FAIL (dùng cho Test Teardown)
    Run Keyword If Test Failed    Capture Page Screenshot

