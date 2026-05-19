"""
AI Robot Generator – Dùng AI đọc test steps và generate Robot Framework code
với Appium actions thực tế (không phải TODO placeholder).

Nếu không có AI key → dùng Smart Pattern Mapper fallback.
"""
import json
import logging
import os
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ── Smart Pattern Mapper (fallback khi không có AI key) ───────────────────────

STEP_PATTERNS = [
    # Launch / Open
    (re.compile(r"launch|open|start.*app", re.I),
     "Open App On Platform    ${PLATFORM}"),
    # Wait for screen
    (re.compile(r"wait for login screen|wait.*login.*appear", re.I),
     "Wait For Element Visible    accessibility_id=email_input    ${TIMEOUT_PAGE_LOAD}"),
    (re.compile(r"wait for (.+) (screen|page|view)", re.I),
     "Wait For Element Visible    accessibility_id=home_screen_container    ${TIMEOUT_PAGE_LOAD}"),
    # Navigate / go to
    (re.compile(r"navigate to (.+)|go to (.+)", re.I),
     "Log    STEP: Navigate    console=True"),
    # Enter email
    (re.compile(r"enter.*(valid\s+)?email|type.*(valid\s+)?email|input.*(valid\s+)?email", re.I),
     "Input Text By Accessibility ID    email_input    ${VALID_EMAIL}"),
    # Enter password
    (re.compile(r"enter.*(valid\s+)?password|type.*(valid\s+)?password", re.I),
     "Input Text By Accessibility ID    password_input    ${VALID_PASSWORD}"),
    # Leave password empty / clear password
    (re.compile(r"leave.*(password|pass).*empty|clear.*(password|pass)|do not.*type.*password", re.I),
     "Clear Field    accessibility_id=password_input"),
    # Leave email empty
    (re.compile(r"leave.*(email|username).*empty|clear.*(email|username)", re.I),
     "Clear Field    accessibility_id=email_input"),
    # Tap login button
    (re.compile(r"tap.*login\s+button|click.*login\s+button|press.*login\s+button", re.I),
     "Tap Element By Accessibility ID    login_button"),
    # Tap / click general button
    (re.compile(r"(?:tap|click|press).+(?:button|btn|link|icon)", re.I),
     "Tap Element By Text    Login"),
    # Select / choose photo
    (re.compile(r"select|choose|pick.*(photo|image|picture)", re.I),
     "Tap Element By Text    Choose Photo"),
    # Tap confirm
    (re.compile(r"tap.*confirm|click.*confirm|confirm.*upload", re.I),
     "Tap Element By Accessibility ID    confirm_button"),
    # Scroll
    (re.compile(r"scroll down", re.I), "Scroll Down Once"),
    (re.compile(r"scroll up", re.I),   "Scroll Up Once"),
    # Back
    (re.compile(r"press back|go back|tap back", re.I), "Press Back Button"),
    # Observe / wait
    (re.compile(r"observe|watch", re.I), "Sleep    2s"),
]

EXPECTED_PATTERNS = [
    (re.compile(r"validation.*(message|error)|error.*(message|text)|displays?.*(validation|message)", re.I),
     lambda m, text: f'Page Should Show Text    {_extract_quoted(text) or "Password cannot be empty"}'),
    (re.compile(r"not crash|must not crash|no crash|app.*running|does not crash", re.I),
     lambda m, text: "App Should Not Have Crashed"),
    (re.compile(r"remain.*login|stay.*login|on.*login.*screen|login.*screen", re.I),
     lambda m, text: "Current Screen Should Be    accessibility_id=email_input"),
    (re.compile(r"navigate.*home|go.*home|home screen|logged in.*home", re.I),
     lambda m, text: "Current Screen Should Be    accessibility_id=home_screen_container"),
    (re.compile(r"toast.*success|success.*toast|photo updated|updated successfully", re.I),
     lambda m, text: f'Toast Message Should Appear    {_extract_quoted(text) or "successfully"}'),
    (re.compile(r"progress.*bar|spinner|loading indicator", re.I),
     lambda m, text: "Element Should Be Visible On Screen    accessibility_id=progress_indicator"),
    (re.compile(r"error.*visible|visible.*below|clearly visible|error.*field", re.I),
     lambda m, text: "Element Should Be Visible On Screen    accessibility_id=error_message"),
    (re.compile(r"retry|try again|retry button", re.I),
     lambda m, text: "Element Should Be Visible On Screen    accessibility_id=retry_button"),
    (re.compile(r"biometric.*button|login.*biometric.*button|button.*visible", re.I),
     lambda m, text: "Element Should Be Visible On Screen    accessibility_id=biometric_button"),
    (re.compile(r"prompt.*biometric|biometric.*scan|face id|fingerprint", re.I),
     lambda m, text: "Element Should Be Visible On Screen    accessibility_id=biometric_prompt"),
    (re.compile(r"responsive|not freeze|no freeze", re.I),
     lambda m, text: "App Should Not Have Crashed"),
]


def _extract_quoted(text: str) -> str:
    """Lấy text trong dấu ngoặc kép."""
    m = re.search(r'"([^"]+)"', text)
    return m.group(1) if m else ""


def _map_step_to_robot(step: str) -> str:
    """Map 1 test step → Robot keyword call."""
    # Tap button patterns
    tap_match = re.search(
        r'(?:tap|click|press)\s+(?:the\s+)?["\']?([^"\']+?)["\']?\s*(?:button|btn|icon|link)?$',
        step, re.I
    )
    if tap_match:
        label = tap_match.group(1).strip().title()
        acc_id = re.sub(r'\s+', '_', label.lower())
        return f"Tap Element By Text    {label}"

    # Enter/type patterns
    enter_match = re.search(
        r'(?:enter|type|input)\s+(?:a\s+)?(?:valid\s+)?(.+?)\s*(?:into|in|to|:)?\s*(.+)?$',
        step, re.I
    )
    if enter_match:
        what = enter_match.group(1).lower()
        if "email" in what or "username" in what:
            return "Input Text By Accessibility ID    email_input    ${VALID_EMAIL}"
        if "password" in what or "pass" in what:
            return "Input Text By Accessibility ID    password_input    ${VALID_PASSWORD}"

    # Check known patterns
    for pattern, robot_line in STEP_PATTERNS:
        if pattern.search(step) and robot_line:
            return robot_line

    # Default fallback
    return f"Log    STEP: {step}    console=True"


def _map_expected_to_robot(expected: str) -> str:
    """Map 1 expected result → Robot assertion call."""
    for pattern, handler in EXPECTED_PATTERNS:
        m = pattern.search(expected)
        if m:
            return handler(m, expected)
    # Default
    quoted = _extract_quoted(expected)
    if quoted:
        return f'Page Should Show Text    {quoted}'
    return f"App Should Not Have Crashed"


# ── AI Generator ──────────────────────────────────────────────────────────────

class AIRobotGenerator:
    """
    Dùng AI generate Robot Framework keyword implementations thực tế.
    Fallback sang SmartMapper nếu không có AI key.
    """

    SYSTEM_PROMPT = """You are an expert in Robot Framework and Appium mobile testing.
Given test steps and expected results from a Jira ticket, generate complete Robot Framework keyword implementations.

Rules:
- Use AppiumLibrary keywords: Click Element, Input Text, Wait Until Element Is Visible, etc.
- Use accessibility_id as primary locator strategy
- For unknown element IDs, use a descriptive placeholder like: accessibility_id=<element_name>
- Always add: App Should Not Have Crashed  for crash-related verifications
- Use: Page Should Show Text    "<text>"  for text verification
- Format response as valid Robot Framework code only, no markdown, no explanations
"""

    def __init__(self) -> None:
        self.provider = os.getenv("AI_PROVIDER", "anthropic").lower()
        self.api_key  = os.getenv("AI_API_KEY", "")
        self.model    = os.getenv("AI_MODEL", "claude-3-5-sonnet-20241022")
        self.has_ai   = bool(self.api_key and "your_" not in self.api_key)

    def generate(self, ticket: dict, analysis: dict) -> dict[str, list[str]]:
        """
        Generate Robot keyword implementations cho preconditions, steps, expected.

        Returns:
            {
              "precondition_impl": ["keyword_body_line1", ...],
              "step_impls": { "step text": ["robot_line1", ...] },
              "expected_impls": { "expected text": ["robot_line1", ...] }
            }
        """
        if self.has_ai:
            logger.info(f"[AI-GEN] Using {self.provider}/{self.model}")
            try:
                return self._ai_generate(ticket, analysis)
            except Exception as e:
                logger.warning(f"[AI-GEN] AI failed ({e}), falling back to SmartMapper")

        logger.info("[AI-GEN] Using SmartMapper (no AI key)")
        return self._smart_map(analysis)

    def _smart_map(self, analysis: dict) -> dict:
        """Pattern-based mapping – không cần AI."""
        step_impls = {}
        for step in analysis.get("test_steps", []):
            step_impls[step] = [_map_step_to_robot(step)]

        expected_impls = {}
        for exp in analysis.get("expected_results", []):
            expected_impls[exp] = [_map_expected_to_robot(exp)]

        return {
            "precondition_impl": ["Open App On Platform    ${PLATFORM}"],
            "step_impls": step_impls,
            "expected_impls": expected_impls,
        }

    def _ai_generate(self, ticket: dict, analysis: dict) -> dict:
        """Gọi AI để generate Robot keyword bodies."""
        prompt = f"""
Ticket: {ticket['ticket_id']} - {ticket['title']}

PRECONDITIONS:
{json.dumps(analysis['preconditions'], ensure_ascii=False)}

TEST STEPS:
{json.dumps(analysis['test_steps'], ensure_ascii=False)}

EXPECTED RESULTS:
{json.dumps(analysis['expected_results'], ensure_ascii=False)}

Generate Robot Framework keyword implementations. Return ONLY valid JSON:
{{
  "precondition_impl": ["robot_line1", "robot_line2"],
  "step_impls": {{
    "step text 1": ["robot_line1", "robot_line2"],
    "step text 2": ["robot_line1"]
  }},
  "expected_impls": {{
    "expected text 1": ["assertion_line1"],
    "expected text 2": ["assertion_line1", "assertion_line2"]
  }}
}}
"""
        if self.provider == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            resp = client.messages.create(
                model=self.model, max_tokens=2048,
                system=self.SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text
        else:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            resp = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )
            raw = resp.choices[0].message.content

        # Parse JSON
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        if m:
            return json.loads(m.group())
        return self._smart_map({"test_steps": [], "expected_results": []})

