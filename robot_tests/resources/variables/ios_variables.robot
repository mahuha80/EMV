*** Settings ***
Documentation    iOS-specific variables và capabilities

*** Variables ***
# ── Appium Server ────────────────────────────────────────────
${APPIUM_URL}                 http://localhost:4723

# ── Platform ─────────────────────────────────────────────────
${PLATFORM}                   ios
${IOS_PLATFORM_NAME}          iOS
${IOS_AUTOMATION}             XCUITest
${IOS_UDID}                   %{IOS_DEVICE_UDID=auto}
${IOS_PLATFORM_VERSION}       %{IOS_PLATFORM_VERSION=17.0}

# ── App ──────────────────────────────────────────────────────
${IOS_BUNDLE_ID}              %{IOS_BUNDLE_ID=com.your.app}
${IOS_NO_RESET}               ${FALSE}

# ── Timeouts ─────────────────────────────────────────────────
${TIMEOUT_DEFAULT}            12s
${TIMEOUT_SHORT}              4s
${TIMEOUT_LONG}               40s
${TIMEOUT_PAGE_LOAD}          25s

# ── Test Data (Common) ────────────────────────────────────────
${VALID_EMAIL}                %{TEST_EMAIL=testuser@example.com}
${VALID_PASSWORD}             %{TEST_PASSWORD=TestPass123!}
${INVALID_PASSWORD}           wrong_password_123
${EMPTY_STRING}               ${EMPTY}
${SPECIAL_CHARS}              !@#$%^&*()
${VERY_LONG_TEXT}             AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

