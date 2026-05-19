"""
Ticket Fetcher – Lấy dữ liệu ticket từ Jira qua MCP Client (STEP A)
"""
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .mcp_client import MCPClient, JiraConnectionError
from .ticket_parser import TicketParser

logger = logging.getLogger(__name__)


class TicketNotFoundError(Exception):
    """Raised khi ticket ID không tồn tại trên Jira."""
    pass


class TicketFetcher:
    """
    Lấy và lưu trữ thông tin ticket từ Jira.
    Output: ticket_data.json trong thư mục reports/{ticket_id}/
    """

    FIELDS = [
        "summary", "description", "priority", "status",
        "assignee", "reporter", "components", "labels",
        "attachment", "comment", "customfield_10016",  # Story points
        "customfield_10014",  # Epic link
    ]

    def __init__(self, client: MCPClient | None = None) -> None:
        self.client = client or MCPClient()
        self.parser = TicketParser()
        self.reports_dir = Path(os.getenv("REPORTS_BASE_DIR", "reports"))

    def fetch(self, ticket_id: str) -> dict[str, Any]:
        """
        Fetch toàn bộ thông tin ticket từ Jira.

        Args:
            ticket_id: Jira ticket ID (e.g., 'PROJ-1234')

        Returns:
            dict: Parsed ticket data

        Raises:
            TicketNotFoundError: Ticket không tồn tại
            JiraConnectionError: Lỗi kết nối
        """
        logger.info(f"[STEP-A] Fetching ticket: {ticket_id}")

        # Fetch issue
        raw = self.client.get(
            f"/rest/api/3/issue/{ticket_id}",
            params={"fields": ",".join(self.FIELDS)},
        )
        if not raw:
            raise TicketNotFoundError(f"Ticket '{ticket_id}' not found on Jira")

        # Parse raw data
        ticket_data = self.parser.parse(ticket_id, raw)

        # Save to disk
        self._save(ticket_id, ticket_data)

        logger.info(f"[STEP-A] Ticket {ticket_id} fetched successfully: {ticket_data['title']}")
        return ticket_data

    def _save(self, ticket_id: str, data: dict[str, Any]) -> None:
        """Lưu ticket_data.json vào reports directory."""
        output_dir = self.reports_dir / ticket_id
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "ticket_data.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.debug(f"[STEP-A] Saved ticket data: {output_path}")

