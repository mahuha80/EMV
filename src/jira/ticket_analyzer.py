"""
Ticket Analyzer – Parse precondition, test steps, expected results từ Jira ticket.

Hỗ trợ các format phổ biến:
  - Jira Description với sections: Precondition / Steps / Expected
  - Gherkin style: Given / When / Then
  - Numbered list steps
  - Acceptance Criteria bullet points
"""
import json
import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ── Regex patterns cho từng section ──────────────────────────────────────────

_SECTION_HEADERS = {
    "preconditions": re.compile(
        r"(?:precondition[s]?|pre-condition[s]?|prerequisite[s]?|setup|given)[:\s]*",
        re.IGNORECASE,
    ),
    "test_steps": re.compile(
        r"(?:test\s*steps?|steps?\s*to\s*reproduce|steps?|reproduction\s*steps?|how\s*to\s*reproduce|when)[:\s]*",
        re.IGNORECASE,
    ),
    "expected_results": re.compile(
        r"(?:expected\s*results?|expected\s*behavior|expected\s*outcome|then|acceptance\s*criteria)[:\s]*",
        re.IGNORECASE,
    ),
    # Các section này sẽ DỪNG việc thêm vào expected_results
    "actual_results": re.compile(
        r"(?:actual\s*results?|actual\s*behavior|actual\s*outcome|current\s*behavior)[:\s]*",
        re.IGNORECASE,
    ),
}

_NUMBERED_STEP = re.compile(r"^\s*\d+[.)]\s+(.+)$")
_BULLET_STEP = re.compile(r"^\s*[-•*]\s+(.+)$")
_GHERKIN_LINE = re.compile(r"^\s*(given|when|then|and|but)\s+(.+)$", re.IGNORECASE)


class TicketAnalyzer:
    """
    Parse ticket description thành structured test analysis.

    Output structure:
        {
          "preconditions": [...],
          "test_steps": [...],
          "expected_results": [...],
          "test_type": "functional|regression|smoke",
          "platforms": ["android","ios"],
          "components": [...]
        }
    """

    def analyze(self, ticket_data: dict[str, Any]) -> dict[str, Any]:
        """
        Phân tích ticket data để trích xuất thông tin test.

        Args:
            ticket_data: Dict từ TicketFetcher

        Returns:
            dict: Structured test analysis
        """
        description: str = ticket_data.get("description", "")
        criteria: list[str] = ticket_data.get("acceptance_criteria", [])
        labels: list[str] = [l.lower() for l in ticket_data.get("labels", [])]
        components: list[str] = ticket_data.get("components", [])

        # Parse từng section từ description
        sections = self._parse_sections(description)

        # Fallback: dùng acceptance_criteria nếu không tìm được steps
        if not sections["test_steps"] and criteria:
            sections["test_steps"] = criteria

        # Detect từ Gherkin nếu không có section rõ ràng
        if not any(sections.values()):
            sections = self._parse_gherkin(description)

        # Detect platforms từ labels
        platforms = self._detect_platforms(labels)

        # Detect test type
        test_type = self._detect_test_type(labels, ticket_data.get("priority", ""))

        analysis: dict[str, Any] = {
            "ticket_id": ticket_data["ticket_id"],
            "preconditions": sections["preconditions"],
            "test_steps": sections["test_steps"],
            "expected_results": sections["expected_results"],
            "test_type": test_type,
            "platforms": platforms,
            "components": components,
        }

        # Save analysis
        self._save(ticket_data["ticket_id"], analysis)
        logger.info(
            f"[ANALYZE] {ticket_data['ticket_id']} → "
            f"precond={len(analysis['preconditions'])} "
            f"steps={len(analysis['test_steps'])} "
            f"expected={len(analysis['expected_results'])}"
        )
        return analysis

    # ── Private: Section Parsing ──────────────────────────────────

    def _parse_sections(self, text: str) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {
            "preconditions": [],
            "test_steps": [],
            "expected_results": [],
        }
        if not text:
            return result

        lines = text.splitlines()
        current_section: str | None = None

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Phát hiện header
            detected = self._detect_section_header(stripped)
            if detected:
                # "actual_results" → dừng collect, không map vào result
                current_section = detected if detected in result else None
                content = _SECTION_HEADERS[detected].sub("", stripped).strip()
                if content and current_section:
                    result[current_section].append(content)
                continue

            if current_section:
                item = self._clean_line(stripped)
                if item:
                    result[current_section].append(item)

        return result

    def _detect_section_header(self, line: str) -> str | None:
        for section, pattern in _SECTION_HEADERS.items():
            if pattern.match(line):
                return section
        return None

    def _clean_line(self, line: str) -> str:
        """Strip bullet points, numbers từ dòng."""
        m = _NUMBERED_STEP.match(line)
        if m:
            return m.group(1).strip()
        m = _BULLET_STEP.match(line)
        if m:
            return m.group(1).strip()
        return line

    def _parse_gherkin(self, text: str) -> dict[str, list[str]]:
        """Parse Gherkin-style description (Given/When/Then)."""
        result: dict[str, list[str]] = {
            "preconditions": [],
            "test_steps": [],
            "expected_results": [],
        }
        for line in text.splitlines():
            m = _GHERKIN_LINE.match(line.strip())
            if not m:
                continue
            keyword = m.group(1).lower()
            content = m.group(2).strip()
            if keyword == "given":
                result["preconditions"].append(content)
            elif keyword in ("when", "and"):
                result["test_steps"].append(content)
            elif keyword == "then":
                result["expected_results"].append(content)
        return result

    # ── Private: Detection Helpers ────────────────────────────────

    def _detect_platforms(self, labels: list[str]) -> list[str]:
        platforms = []
        if any(l in labels for l in ("android", "android-only")):
            platforms.append("android")
        if any(l in labels for l in ("ios", "ios-only")):
            platforms.append("ios")
        if not platforms:
            platforms = ["android", "ios"]  # default: all platforms
        return platforms

    def _detect_test_type(self, labels: list[str], priority: str) -> str:
        if "smoke" in labels:
            return "smoke"
        if priority.lower() in ("highest", "critical"):
            return "smoke"
        if "regression" in labels:
            return "regression"
        return "functional"

    def _save(self, ticket_id: str, analysis: dict[str, Any]) -> None:
        output_dir = Path(f"reports/{ticket_id}")
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir / "ticket_analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

