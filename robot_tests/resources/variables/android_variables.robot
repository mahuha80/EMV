*** Settings ***
Documentation    Android-specific variables và capabilities

*** Variables ***
# ── Appium Server ────────────────────────────────────────────
${APPIUM_URL}                 http://localhost:4723

# ── Platform ─────────────────────────────────────────────────
${PLATFORM}                   android
${ANDROID_PLATFORM_NAME}      Android
${ANDROID_AUTOMATION}         UiAutomator2
${ANDROID_DEVICE_NAME}        %{ANDROID_DEVICE_NAME=emulator-5554}
${ANDROID_PLATFORM_VERSION}   %{ANDROID_PLATFORM_VERSION=13.0}

# ── App ──────────────────────────────────────────────────────
${ANDROID_APP_PACKAGE}        %{ANDROID_APP_PACKAGE=com.your.app}
${ANDROID_APP_ACTIVITY}       %{ANDROID_APP_ACTIVITY=.MainActivity}
${ANDROID_NO_RESET}           ${FALSE}
${ANDROID_FULL_RESET}         ${FALSE}

# ── Timeouts ─────────────────────────────────────────────────
${TIMEOUT_DEFAULT}            10s
${TIMEOUT_SHORT}              3s
${TIMEOUT_LONG}               30s
${TIMEOUT_PAGE_LOAD}          20s

# ── Test Data (Common) ────────────────────────────────────────
${VALID_EMAIL}                %{TEST_EMAIL=testuser@example.com}
${VALID_PASSWORD}             %{TEST_PASSWORD=TestPass123!}
${INVALID_PASSWORD}           wrong_password_123
${EMPTY_STRING}               ${EMPTY}
${SPECIAL_CHARS}              !@#$%^&*()
${VERY_LONG_TEXT}             AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

