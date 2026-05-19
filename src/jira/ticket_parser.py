"""
Ticket Parser – Parse và chuẩn hóa raw Jira ticket data
"""
import logging
import re
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


class TicketParser:
    """
    Chuyển đổi raw Jira API response thành structured ticket data.
    Trích xuất acceptance criteria từ description.
    """

    def parse(self, ticket_id: str, raw: dict[str, Any]) -> dict[str, Any]:
        """
        Parse Jira issue response thành structured data.

        Args:
            ticket_id: Jira ticket ID
            raw: Raw response từ Jira REST API

        Returns:
            dict: Structured ticket data
        """
        fields: dict = raw.get("fields", {})

        description_text = self._extract_description(fields.get("description", {}))
        acceptance_criteria = self._extract_acceptance_criteria(description_text)

        return {
            "ticket_id": ticket_id,
            "title": fields.get("summary", ""),
            "description": description_text,
            "acceptance_criteria": acceptance_criteria,
            "priority": self._extract_priority(fields.get("priority", {})),
            "status": fields.get("status", {}).get("name", ""),
            "components": [c.get("name", "") for c in fields.get("components", [])],
            "labels": fields.get("labels", []),
            "assignee": self._extract_user(fields.get("assignee")),
            "reporter": self._extract_user(fields.get("reporter")),
            "attachments": self._extract_attachments(fields.get("attachment", [])),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }

    def _extract_description(self, description: dict | str | None) -> str:
        """Xử lý Jira Atlassian Document Format (ADF) hoặc plain text."""
        if not description:
            return ""
        if isinstance(description, str):
            return description
        # ADF format
        if isinstance(description, dict) and description.get("type") == "doc":
            return self._adf_to_text(description)
        return str(description)

    def _adf_to_text(self, node: dict) -> str:
        """Đệ quy chuyển ADF node thành plain text."""
        text = ""
        if node.get("type") == "text":
            return node.get("text", "")
        for child in node.get("content", []):
            text += self._adf_to_text(child)
            if child.get("type") in ("paragraph", "heading", "listItem"):
                text += "\n"
        return text

    def _extract_acceptance_criteria(self, description: str) -> list[str]:
        """
        Trích xuất acceptance criteria từ description.
        Hỗ trợ nhiều format phổ biến.
        """
        criteria: list[str] = []

        # Tìm section Acceptance Criteria
        ac_pattern = re.compile(
            r"(?:acceptance criteria|ac|given|when|then)[:\s]*(.+?)(?=\n\n|\Z)",
            re.IGNORECASE | re.DOTALL,
        )
        match = ac_pattern.search(description)
        if match:
            section = match.group(1)
            # Parse bullet points
            for line in section.splitlines():
                line = line.strip().lstrip("•-*").strip()
                if line:
                    criteria.append(line)

        # Fallback: bullet points từ toàn bộ description
        if not criteria:
            for line in description.splitlines():
                line = line.strip()
                if line.startswith(("- ", "• ", "* ", "[ ] ", "[x] ")):
                    criteria.append(line.lstrip("-•*[ ]x").strip())

        return criteria or ["Verify feature works as described in ticket"]

    def _extract_priority(self, priority: dict | None) -> str:
        return (priority or {}).get("name", "Medium")

    def _extract_user(self, user: dict | None) -> str:
        if not user:
            return ""
        return user.get("emailAddress", user.get("displayName", ""))

    def _extract_attachments(self, attachments: list[dict]) -> list[dict[str, str]]:
        return [
            {"filename": a.get("filename", ""), "url": a.get("content", "")}
            for a in attachments
        ]

