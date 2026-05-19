*** Settings ***
Documentation    Shared keywords dùng chung cho tất cả test suites
Library          AppiumLibrary
Library          Collections
Library          String
Library          OperatingSystem
Resource         variables.robot

*** Keywords ***
# ── Setup / Teardown ────────────────────────────────────

Open Mobile App
    [Documentation]    Mở app trên device (Android hoặc iOS) dựa vào ${PLATFORM}
    [Arguments]    ${platform}=${PLATFORM}
    Run Keyword If    '${platform}' == 'android'
    ...    Open Android App
    ...    ELSE
    ...    Open iOS App

Open Android App
    [Documentation]    Khởi động app trên Android với UiAutomator2
    Open Application    ${APPIUM_URL}
    ...    platformName=${ANDROID_PLATFORM}
    ...    automationName=${ANDROID_AUTOMATION}
    ...    deviceName=${ANDROID_DEVICE_NAME}
    ...    platformVersion=${ANDROID_PLATFORM_VER}
    ...    appPackage=${ANDROID_APP_PACKAGE}
    ...    appActivity=${ANDROID_APP_ACTIVITY}
    ...    noReset=True
    ...    newCommandTimeout=300
    Log    [ROBOT] Android app opened: ${ANDROID_APP_PACKAGE}

Open iOS App
    [Documentation]    Khởi động app trên iOS với XCUITest
    Open Application    ${APPIUM_URL}
    ...    platformName=${IOS_PLATFORM}
    ...    automationName=${IOS_AUTOMATION}
    ...    deviceName=${IOS_DEVICE_NAME}
    ...    platformVersion=${IOS_PLATFORM_VER}
    ...    bundleId=${IOS_BUNDLE_ID}
    ...    noReset=True
    ...    newCommandTimeout=300
    Log    [ROBOT] iOS app opened: ${IOS_BUNDLE_ID}

Close Mobile App
    [Documentation]    Đóng app và cleanup session
    Close Application
    Log    [ROBOT] App closed

Take Screenshot On Failure
    [Documentation]    Chụp screenshot khi test fail
    Capture Page Screenshot

# ── Wait Utilities ───────────────────────────────────────

Wait For Element
    [Documentation]    Chờ element xuất hiện trong timeout
    [Arguments]    ${locator}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait Until Element Is Visible    ${locator}    timeout=${timeout}
    Log    [ROBOT] Element visible: ${locator}

Wait For Element To Be Gone
    [Documentation]    Chờ element biến mất
    [Arguments]    ${locator}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait Until Element Is Not Visible    ${locator}    timeout=${timeout}

# ── Actions ──────────────────────────────────────────────

Tap Element
    [Documentation]    Tap vào element
    [Arguments]    ${locator}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait For Element    ${locator}    ${timeout}
    Click Element    ${locator}
    Log    [ROBOT] Tapped: ${locator}

Input Text To Field
    [Documentation]    Clear và nhập text vào field
    [Arguments]    ${locator}    ${text}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait For Element    ${locator}    ${timeout}
    Clear Text    ${locator}
    Input Text    ${locator}    ${text}
    Log    [ROBOT] Input text to ${locator}: ${text}

Scroll Down
    [Documentation]    Scroll xuống màn hình
    Swipe    500    1000    500    300    500

Scroll Up
    [Documentation]    Scroll lên màn hình
    Swipe    500    300    500    1000    500

# ── Assertions ───────────────────────────────────────────

Verify Text Displayed
    [Documentation]    Kiểm tra text hiển thị trên màn hình
    [Arguments]    ${text}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait Until Page Contains    ${text}    timeout=${timeout}
    Log    [ROBOT] Text verified: ${text}

Verify Element Exists
    [Documentation]    Kiểm tra element tồn tại
    [Arguments]    ${locator}    ${timeout}=${DEFAULT_TIMEOUT}
    Wait For Element    ${locator}    ${timeout}
    Element Should Be Visible    ${locator}

Verify Element Does Not Exist
    [Documentation]    Kiểm tra element không tồn tại
    [Arguments]    ${locator}
    Element Should Not Be Visible    ${locator}

Verify App Did Not Crash
    [Documentation]    Kiểm tra app vẫn đang chạy bình thường
    ${source}=    Get Source
    Should Not Contain    ${source}    Unfortunately
    Should Not Contain    ${source}    has stopped
    Should Not Contain    ${source}    crash
    Log    [ROBOT] App is still running normally

