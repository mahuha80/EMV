"""
Commit Formatter – Format commit messages theo Conventional Commits
"""
import re
from typing import Any


class CommitFormatter:
    """Format commit message theo chuẩn Conventional Commits."""

    def format(
        self, ticket_data: dict[str, Any], fix_report: dict[str, Any]
    ) -> str:
        """
        Tạo commit message đầy đủ.

        Args:
            ticket_data: Ticket info
            fix_report: Fix analysis

        Returns:
            str: Formatted commit message
        """
        ticket_id = ticket_data["ticket_id"]
        title = ticket_data.get("title", "fix issue")
        root_cause = fix_report.get("root_cause", "")
        fixes = fix_report.get("fixes", [])
        impact = fix_report.get("impact", {})

        # Subject line
        scope = self._detect_scope(fixes)
        subject = self._to_slug(title)[:60]
        subject_line = f"fix({scope}): {subject} [{ticket_id}]"

        # Body
        body_lines = [
            f"Root Cause: {root_cause[:200]}",
            "",
            "Changes:",
        ]
        for fix in fixes[:5]:  # Max 5 fixes trong commit msg
            body_lines.append(f"  - {fix.get('file', '')}: {fix.get('explanation', '')[:80]}")

        # Footer
        platform = ticket_data.get("labels", [])
        tested_on = ", ".join(platform) if platform else "mobile"
        footer = (
            f"Impact: {impact.get('risk_level', 'Low')} risk | "
            f"Files: {impact.get('files_changed', 0)} | "
            f"Breaking: {'Yes' if impact.get('breaking_change') else 'No'}\n"
            f"Tested: Robot Framework + Appium | {tested_on}"
        )

        return f"{subject_line}\n\n{chr(10).join(body_lines)}\n\n{footer}"

    def _detect_scope(self, fixes: list[dict[str, Any]]) -> str:
        """Detect scope từ file paths được fix."""
        if not fixes:
            return "app"
        components = set()
        for fix in fixes:
            parts = fix.get("file", "").split("/")
            if len(parts) > 1:
                components.add(parts[-2])
        return ",".join(sorted(components))[:20] or "app"

    def _to_slug(self, text: str) -> str:
        """Chuyển text thành lowercase slug."""
        text = re.sub(r"[^\w\s-]", "", text.lower())
        return re.sub(r"\s+", " ", text).strip()

