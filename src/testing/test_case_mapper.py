"""
Test Case Mapper – Map ticket analysis → Robot Framework .robot test suite
với AI-generated Appium actions thực tế (không phải TODO placeholder).
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

SUITE_TEMPLATE = """\
*** Settings ***
Documentation    Auto-generated suite for {ticket_id}: {ticket_title}
...              Generated: {generated_at}
...              Platform : {platform}
Library          Collections
Library          String
Library          OperatingSystem
Resource         {rel_resources}/base/appium_base.robot
Resource         {rel_resources}/base/mobile_keywords.robot
Resource         {rel_resources}/base/assertions.robot
Resource         {rel_resources}/variables/{platform}_variables.robot

Suite Setup      Suite Setup For {ticket_id}
Suite Teardown   Suite Teardown For {ticket_id}
Test Teardown    Capture Screenshot On Failure

*** Variables ***
${{TICKET_ID}}        {ticket_id}
${{PLATFORM}}         {platform}
${{TEST_TYPE}}        {test_type}

*** Test Cases ***
{test_cases_block}
*** Keywords ***
Suite Setup For {ticket_id}
    [Documentation]    Khởi động app và thực hiện preconditions
    Log    ===== START: {ticket_id} on ${{PLATFORM}} =====    console=True
{precondition_body}

Suite Teardown For {ticket_id}
    [Documentation]    Dọn dẹp sau khi chạy xong
    Log    ===== END: {ticket_id} =====    console=True
    Close App On Platform

{shared_keywords}
"""

TEST_CASE_TEMPLATE = """\
{tc_id} {tc_name}
    [Documentation]    Expected: {expected}
    [Tags]             {ticket_id}    {test_type}    {priority_tag}    {platform}
    Log    Running: {tc_id} - {tc_name}    console=True
{step_calls}    {expected_keyword}
"""


class TestCaseMapper:
    """Chuyển đổi ticket analysis thành Robot Framework test suite với AI actions."""

    SUITES_DIR   = Path("robot_tests/suites/generated")
    RESOURCES_DIR = Path("robot_tests/resources")

    def __init__(self, platform: str = "android", dry_run: bool = False) -> None:
        self.platform = platform
        self.dry_run  = dry_run

    def generate(
        self, ticket_data: dict[str, Any], analysis: dict[str, Any]
    ) -> tuple[Path, list[dict]]:
        """Sinh .robot file với AI-generated Appium actions."""
        ticket_id    = ticket_data["ticket_id"]
        ticket_title = ticket_data.get("title", "")
        test_type    = analysis.get("test_type", "functional")
        priority     = ticket_data.get("priority", "Medium")
        steps        = analysis.get("test_steps", [])
        expected_list = analysis.get("expected_results", []) or [f"Feature works as described in {ticket_id}"]

        # ── Gọi AI Generator để lấy actions thực ──────────────────────────
        from testing.ai_robot_generator import AIRobotGenerator
        ai_gen   = AIRobotGenerator()
        ai_impls = ai_gen.generate(ticket_data, analysis)

        # ── Build test cases ───────────────────────────────────────────────
        test_cases: list[dict] = []
        tc_blocks: list[str]   = []

        for idx, expected in enumerate(expected_list, start=1):
            tc_id    = f"TC_{idx:03d}"
            tc_name  = self._to_title(expected)
            exp_kw   = self._to_kw(f"Verify: {expected}")
            step_calls = "".join(
                f"    Execute Step: {self._to_kw(s)}\n" for s in steps
            )
            tc_blocks.append(TEST_CASE_TEMPLATE.format(
                tc_id=tc_id, tc_name=tc_name, expected=expected,
                ticket_id=ticket_id, test_type=test_type,
                priority_tag=f"P{self._pri(priority)}", platform=self.platform,
                step_calls=step_calls or "    No Operation\n",
                expected_keyword=exp_kw,
            ))
            test_cases.append({"id": tc_id, "name": tc_name, "expected": expected})

        # ── Build keyword bodies ───────────────────────────────────────────
        precondition_body = self._build_precondition_body(analysis, ai_impls)
        shared_keywords   = self._build_shared_keywords(steps, expected_list, ai_impls)

        suite_content = SUITE_TEMPLATE.format(
            ticket_id=ticket_id, ticket_title=ticket_title,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
            platform=self.platform, test_type=test_type,
            rel_resources="../../resources",
            test_cases_block="\n".join(tc_blocks),
            precondition_body=precondition_body,
            shared_keywords=shared_keywords,
        )

        if self.dry_run:
            print(suite_content)
            suite_path = self.SUITES_DIR / f"{ticket_id}_{self.platform}.robot"
        else:
            suite_path = self._write(ticket_id, suite_content)
            self._save_meta(ticket_id, test_cases)

        return suite_path, test_cases

    # ── Keyword body builders ─────────────────────────────────────────────────

    def _build_precondition_body(self, analysis: dict, ai_impls: dict) -> str:
        """Build Suite Setup body: mở app + gọi precondition keywords."""
        lines = []
        pre_actions = ai_impls.get("precondition_impl", ["Open App On Platform    ${PLATFORM}"])
        for action in pre_actions:
            lines.append(f"    {action}")
        # Chỉ log preconditions, không gọi keyword riêng để tránh phải define thêm
        for p in analysis.get("preconditions", []):
            lines.append(f"    Log    PRECONDITION: {p}    console=True")
        return "\n".join(lines) if lines else "    Open App On Platform    ${PLATFORM}"

    def _build_shared_keywords(
        self, steps: list[str], expected_list: list[str], ai_impls: dict
    ) -> str:
        blocks: list[str] = []

        # Step keywords – dùng AI actions
        step_impls = ai_impls.get("step_impls", {})
        for s in steps:
            kw = self._to_kw(f"Execute Step: {s}")
            actions = step_impls.get(s, [f"Log    STEP: {s}    console=True"])
            body = "\n".join(f"    {a}" for a in actions)
            blocks.append(f"{kw}\n    [Documentation]    Step: {s}\n{body}\n")

        # Expected keywords – dùng AI assertions
        exp_impls = ai_impls.get("expected_impls", {})
        for e in expected_list:
            kw = self._to_kw(f"Verify: {e}")
            assertions = exp_impls.get(e, ["App Should Not Have Crashed"])
            body = "\n".join(f"    {a}" for a in assertions)
            blocks.append(f"{kw}\n    [Documentation]    Verify: {e}\n{body}\n")

        # Precondition keywords (individual)
        return "\n".join(blocks)

    # ── Utilities ─────────────────────────────────────────────────────────────

    def _write(self, ticket_id: str, content: str) -> Path:
        self.SUITES_DIR.mkdir(parents=True, exist_ok=True)
        path = self.SUITES_DIR / f"{ticket_id}_{self.platform}.robot"
        path.write_text(content, encoding="utf-8")
        logger.info(f"[MAPPER] Written: {path}")
        return path

    def _save_meta(self, ticket_id: str, test_cases: list[dict]) -> None:
        p = Path(f"reports/{ticket_id}/generated_tests.json")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(
            {"ticket_id": ticket_id, "platform": self.platform, "test_cases": test_cases},
            indent=2, ensure_ascii=False), encoding="utf-8")

    @staticmethod
    def _to_title(text: str) -> str:
        clean = re.sub(r"[^\w\s]", "", text).strip()
        return " ".join(w.capitalize() for w in clean.split()[:12])

    @staticmethod
    def _to_kw(text: str) -> str:
        clean = re.sub(r'[^\w\s:\'\"\-]', ' ', text).strip()
        return re.sub(r'\s+', ' ', clean)[:80]

    @staticmethod
    def _pri(priority: str) -> int:
        return {"Highest": 1, "High": 1, "Medium": 2, "Low": 3, "Lowest": 3}.get(priority, 2)

