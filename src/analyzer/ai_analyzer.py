"""
AI Analyzer – Phân tích lỗi và đề xuất fix solution (STEP C)
"""
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .code_reader import CodeReader
from .fix_generator import FixGenerator
from .impact_assessor import ImpactAssessor

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """
    Orchestrates AI-powered code analysis và fix generation.
    Hỗ trợ OpenAI và Anthropic.
    """

    SYSTEM_PROMPT = """You are an expert software engineer and QA specialist.
Analyze the provided test failure and source code, then suggest precise fixes.
Always respond in valid JSON format as specified."""

    def __init__(self) -> None:
        self.provider = os.getenv("AI_PROVIDER", "openai").lower()
        self.api_key = os.getenv("AI_API_KEY", "")
        self.model = os.getenv("AI_MODEL", "gpt-4o")
        self.max_tokens = int(os.getenv("AI_MAX_TOKENS", "4096"))
        self.confidence_threshold = float(os.getenv("AI_CONFIDENCE_THRESHOLD", "0.7"))
        self.reports_base = Path(os.getenv("REPORTS_BASE_DIR", "reports"))

        self.code_reader = CodeReader()
        self.fix_generator = FixGenerator()
        self.impact_assessor = ImpactAssessor()

    def analyze(
        self, ticket_data: dict[str, Any], test_results: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Phân tích test failures và tạo fix report.

        Args:
            ticket_data: Ticket info từ STEP A
            test_results: Test results từ STEP B

        Returns:
            dict: Fix report với root cause, fixes, và impact
        """
        ticket_id: str = ticket_data["ticket_id"]
        failed_tests = [t for t in test_results.get("test_cases", []) if t["status"] == "FAIL"]

        logger.info(f"[STEP-C] Analyzing {len(failed_tests)} failed tests for {ticket_id}")

        # Đọc source code liên quan
        code_context = self.code_reader.gather_context(failed_tests)

        # Gọi AI
        prompt = self._build_prompt(ticket_data, failed_tests, code_context)
        ai_response = self._call_ai(prompt)

        # Parse AI response
        analysis = self._parse_ai_response(ai_response)

        # Tạo patches
        patches = self.fix_generator.create_patches(analysis.get("fixes", []))

        # Đánh giá impact
        impact = self.impact_assessor.assess(patches, analysis.get("fixes", []))

        fix_report: dict[str, Any] = {
            "ticket_id": ticket_id,
            "root_cause": analysis.get("root_cause", ""),
            "confidence": analysis.get("confidence", 0.0),
            "fixes": patches,
            "impact": impact,
            "ai_model": f"{self.provider}/{self.model}",
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
        }

        self._save_report(ticket_id, fix_report)
        logger.info(
            f"[STEP-C] Analysis complete | "
            f"Confidence: {fix_report['confidence']:.0%} | "
            f"Fixes: {len(patches)}"
        )
        return fix_report

    def _build_prompt(
        self,
        ticket_data: dict[str, Any],
        failed_tests: list[dict],
        code_context: str,
    ) -> str:
        failures_text = "\n".join(
            f"- {t['name']}: {t.get('error', 'No error message')}"
            for t in failed_tests
        )
        return f"""
TICKET: {ticket_data['ticket_id']} - {ticket_data.get('title', '')}
DESCRIPTION: {ticket_data.get('description', '')[:500]}

FAILED TESTS:
{failures_text}

SOURCE CODE CONTEXT:
{code_context}

Respond with ONLY valid JSON in this exact format:
{{
  "root_cause": "Clear explanation of root cause",
  "confidence": 0.0-1.0,
  "fixes": [
    {{
      "file": "relative/path/to/file.py",
      "line_start": 10,
      "line_end": 15,
      "original": "original code block",
      "fixed": "fixed code block",
      "explanation": "Why this fixes the issue"
    }}
  ]
}}
"""

    def _call_ai(self, prompt: str) -> str:
        """Gọi AI API (OpenAI hoặc Anthropic)."""
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _call_openai(self, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content or "{}"

    def _call_anthropic(self, prompt: str) -> str:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def _parse_ai_response(self, response: str) -> dict[str, Any]:
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"[STEP-C] Failed to parse AI response as JSON: {e}")
            return {"root_cause": response, "confidence": 0.5, "fixes": []}

    def _save_report(self, ticket_id: str, report: dict[str, Any]) -> None:
        output_path = self.reports_base / ticket_id / "fix_report.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logger.debug(f"[STEP-C] Saved fix report: {output_path}")

