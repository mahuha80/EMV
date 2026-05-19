*** Settings ***
Documentation    Biến toàn cục cho toàn bộ test suite

*** Variables ***
# ── Appium ──────────────────────────────────────────────
${APPIUM_URL}               http://localhost:4723

# ── Android ─────────────────────────────────────────────
${ANDROID_DEVICE_NAME}      emulator-5554
${ANDROID_PLATFORM}         Android
${ANDROID_PLATFORM_VER}     13.0
${ANDROID_AUTOMATION}       UiAutomator2
${ANDROID_APP_PACKAGE}      com.your.app
${ANDROID_APP_ACTIVITY}     .MainActivity

# ── iOS ──────────────────────────────────────────────────
${IOS_DEVICE_NAME}          iPhone 15 Simulator
${IOS_PLATFORM}             iOS
${IOS_PLATFORM_VER}         17.0
${IOS_AUTOMATION}           XCUITest
${IOS_BUNDLE_ID}            com.your.app

# ── Timeouts ─────────────────────────────────────────────
${DEFAULT_TIMEOUT}          10s
${LONG_TIMEOUT}             30s
${SHORT_TIMEOUT}            5s

# ── Test Data ────────────────────────────────────────────
${VALID_USERNAME}           test_user@company.com
${VALID_PASSWORD}           TestPass123!
${INVALID_PASSWORD}         wrong_password
${EMPTY_STRING}             ${EMPTY}

