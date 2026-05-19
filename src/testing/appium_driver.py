"""
Appium Driver Manager – Khởi tạo và quản lý Appium WebDriver session

Hỗ trợ:
  - Android (UiAutomator2)
  - iOS (XCUITest)
  - Context switching (NATIVE_APP ↔ WEBVIEW)
  - Auto-screenshot on error
  - Session reuse / cleanup
"""
import logging
import os
import time
from pathlib import Path
from typing import Any

from appium import webdriver
from appium.options import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10
LONG_TIMEOUT = 30


class AppiumDriverError(Exception):
    """Raised khi Appium driver gặp lỗi không phục hồi được."""
    pass


class AppiumDriver:
    """
    Wrapper Appium WebDriver với các tiện ích cho mobile testing.

    Usage:
        driver = AppiumDriver(platform="android")
        driver.start_session()
        driver.tap(AppiumBy.ACCESSIBILITY_ID, "login_button")
        driver.quit()
    """

    def __init__(
        self,
        platform: str = "android",
        appium_url: str | None = None,
        screenshot_dir: str = "reports/screenshots",
    ) -> None:
        self.platform = platform.lower()
        self.appium_url = appium_url or os.getenv("APPIUM_SERVER_URL", "http://localhost:4723")
        self.screenshot_dir = Path(screenshot_dir)
        self._driver: webdriver.Remote | None = None

    # ── Session Management ────────────────────────────────────────

    def start_session(self, extra_caps: dict | None = None) -> webdriver.Remote:
        """
        Khởi tạo Appium session.

        Args:
            extra_caps: Capabilities bổ sung (override defaults)

        Returns:
            webdriver.Remote instance
        """
        caps = self._build_capabilities()
        if extra_caps:
            caps.update(extra_caps)

        options = AppiumOptions()
        for k, v in caps.items():
            options.set_capability(k, v)

        logger.info(f"[APPIUM] Starting {self.platform} session → {self.appium_url}")
        try:
            self._driver = webdriver.Remote(self.appium_url, options=options)
            logger.info(f"[APPIUM] Session ID: {self._driver.session_id}")
            return self._driver
        except Exception as e:
            raise AppiumDriverError(f"Cannot start Appium session: {e}") from e

    def quit(self) -> None:
        """Đóng Appium session."""
        if self._driver:
            try:
                self._driver.quit()
                logger.info("[APPIUM] Session closed")
            except Exception:
                pass
            finally:
                self._driver = None

    @property
    def driver(self) -> webdriver.Remote:
        if not self._driver:
            raise AppiumDriverError("No active Appium session. Call start_session() first.")
        return self._driver

    # ── Capabilities ─────────────────────────────────────────────

    def _build_capabilities(self) -> dict[str, Any]:
        if self.platform == "android":
            return self._android_caps()
        elif self.platform == "ios":
            return self._ios_caps()
        raise ValueError(f"Unsupported platform: {self.platform}")

    def _android_caps(self) -> dict[str, Any]:
        return {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": os.getenv("ANDROID_DEVICE_NAME", "emulator-5554"),
            "platformVersion": os.getenv("ANDROID_PLATFORM_VERSION", ""),
            "appPackage": os.getenv("ANDROID_APP_PACKAGE", ""),
            "appActivity": os.getenv("ANDROID_APP_ACTIVITY", ""),
            "noReset": False,
            "fullReset": False,
            "autoGrantPermissions": True,
            "newCommandTimeout": 300,
            "settings[waitForIdleTimeout]": 100,
            "settings[snapshotMaxDepth]": 50,
        }

    def _ios_caps(self) -> dict[str, Any]:
        return {
            "platformName": "iOS",
            "automationName": "XCUITest",
            "udid": os.getenv("IOS_DEVICE_UDID", ""),
            "bundleId": os.getenv("IOS_BUNDLE_ID", ""),
            "platformVersion": os.getenv("IOS_PLATFORM_VERSION", ""),
            "noReset": False,
            "newCommandTimeout": 300,
            "wdaLaunchTimeout": 120000,
            "wdaConnectionTimeout": 120000,
        }

    # ── Element Interaction ───────────────────────────────────────

    def find_element(
        self,
        by: str,
        value: str,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        Chờ và tìm element.

        Args:
            by: AppiumBy locator strategy
            value: Locator value
            timeout: Giây chờ tối đa

        Returns:
            WebElement

        Raises:
            TimeoutException: Element không xuất hiện trong timeout
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"[APPIUM] Found element: {by}={value}")
            return element
        except TimeoutException:
            self._screenshot(f"not_found_{value[:20]}")
            raise TimeoutException(f"Element not found: {by}='{value}' after {timeout}s")

    def find_element_visible(
        self,
        by: str,
        value: str,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Chờ element visible (không chỉ present)."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, value)))

    def tap(self, by: str, value: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Tìm và tap element."""
        element = self.find_element(by, value, timeout)
        element.click()
        logger.debug(f"[APPIUM] Tapped: {by}={value}")

    def type_text(
        self,
        by: str,
        value: str,
        text: str,
        clear_first: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """Nhập text vào field."""
        element = self.find_element(by, value, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.debug(f"[APPIUM] Typed '{text}' into {by}={value}")

    def get_text(self, by: str, value: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Lấy text của element."""
        element = self.find_element(by, value, timeout)
        return element.text

    def is_displayed(self, by: str, value: str, timeout: int = 3) -> bool:
        """Kiểm tra element có hiển thị không (không raise exception)."""
        try:
            element = self.find_element(by, value, timeout)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_element_gone(self, by: str, value: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Chờ element biến mất."""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.invisibility_of_element_located((by, value)))

    # ── Gestures ─────────────────────────────────────────────────

    def scroll_down(self, duration_ms: int = 500) -> None:
        """Scroll xuống giữa màn hình."""
        size = self.driver.get_window_size()
        w, h = size["width"], size["height"]
        self.driver.swipe(w // 2, int(h * 0.7), w // 2, int(h * 0.3), duration_ms)

    def scroll_up(self, duration_ms: int = 500) -> None:
        """Scroll lên."""
        size = self.driver.get_window_size()
        w, h = size["width"], size["height"]
        self.driver.swipe(w // 2, int(h * 0.3), w // 2, int(h * 0.7), duration_ms)

    def scroll_to_element(self, text: str) -> None:
        """Scroll đến element chứa text (Android UiScrollable)."""
        if self.platform == "android":
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true))'
                f'.scrollIntoView(new UiSelector().textContains("{text}"))',
            )

    def long_press(self, by: str, value: str, duration_ms: int = 1000) -> None:
        """Long press element."""
        element = self.find_element(by, value)
        action = self.driver.action_chains()
        action.long_press(element, duration=duration_ms).release().perform()

    def hide_keyboard(self) -> None:
        """Ẩn bàn phím nếu đang hiển thị."""
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    # ── App Control ───────────────────────────────────────────────

    def reset_app(self) -> None:
        """Reset app về trạng thái ban đầu."""
        self.driver.reset()
        logger.info("[APPIUM] App reset")

    def background_app(self, seconds: int = 3) -> None:
        """Đẩy app vào background."""
        self.driver.background_app(seconds)

    def terminate_app(self) -> None:
        """Force stop app (Android)."""
        pkg = os.getenv("ANDROID_APP_PACKAGE", "")
        if pkg and self.platform == "android":
            self.driver.terminate_app(pkg)

    def launch_app(self) -> None:
        """Launch lại app."""
        self.driver.launch_app()

    def get_app_state(self) -> str:
        """Lấy trạng thái app hiện tại."""
        pkg = os.getenv("ANDROID_APP_PACKAGE" if self.platform == "android" else "IOS_BUNDLE_ID", "")
        state = self.driver.query_app_state(pkg)
        return str(state)

    # ── Context / WebView ─────────────────────────────────────────

    def switch_to_webview(self, index: int = 0) -> None:
        """Chuyển sang WebView context."""
        contexts = self.driver.contexts
        webviews = [c for c in contexts if "WEBVIEW" in c]
        if not webviews:
            raise AppiumDriverError("No WebView context found")
        self.driver.switch_to.context(webviews[index])
        logger.debug(f"[APPIUM] Switched to context: {webviews[index]}")

    def switch_to_native(self) -> None:
        """Quay về NATIVE_APP context."""
        self.driver.switch_to.context("NATIVE_APP")

    # ── Assertion Helpers ─────────────────────────────────────────

    def assert_element_visible(self, by: str, value: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Assert element phải visible – raise nếu không thấy."""
        if not self.is_displayed(by, value, timeout):
            self._screenshot(f"assert_fail_{value[:20]}")
            raise AssertionError(f"Expected element visible: {by}='{value}'")

    def assert_text_present(self, expected: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Assert text xuất hiện ở đâu đó trong page source."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if expected in self.driver.page_source:
                logger.debug(f"[APPIUM] Text found: '{expected}'")
                return
            time.sleep(0.5)
        self._screenshot(f"text_not_found")
        raise AssertionError(f"Expected text not found in page: '{expected}'")

    def assert_element_text(self, by: str, value: str, expected_text: str) -> None:
        """Assert text của element bằng expected_text."""
        actual = self.get_text(by, value)
        if actual != expected_text:
            self._screenshot(f"text_mismatch")
            raise AssertionError(
                f"Text mismatch on {by}='{value}'\n"
                f"  Expected: '{expected_text}'\n"
                f"  Actual  : '{actual}'"
            )

    def assert_app_running(self) -> None:
        """Assert app vẫn đang chạy (không crash)."""
        source = self.driver.page_source
        crash_indicators = ["Unfortunately", "has stopped", "keeps stopping", "Force Close"]
        for indicator in crash_indicators:
            if indicator in source:
                self._screenshot("app_crash")
                raise AssertionError(f"App crash detected: '{indicator}' found in page source")
        logger.debug("[APPIUM] App running normally ✅")

    # ── Screenshot ────────────────────────────────────────────────

    def _screenshot(self, name: str = "screenshot") -> Path:
        """Chụp screenshot và lưu vào screenshot_dir."""
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        ts = int(time.time())
        filename = self.screenshot_dir / f"{ts}_{name}.png"
        try:
            self.driver.save_screenshot(str(filename))
            logger.info(f"[APPIUM] Screenshot saved: {filename}")
        except Exception as e:
            logger.warning(f"[APPIUM] Screenshot failed: {e}")
        return filename

    def screenshot(self, name: str = "manual") -> Path:
        """Public screenshot method."""
        return self._screenshot(name)

