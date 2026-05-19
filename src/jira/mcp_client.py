"""
MCP Protocol Client – Kết nối Jira qua Model Context Protocol
"""
import logging
import os
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)


class JiraConnectionError(Exception):
    """Raised khi không thể kết nối Jira MCP server."""
    pass


class JiraAuthError(Exception):
    """Raised khi authentication với Jira thất bại."""
    pass


class MCPClient:
    """
    Client kết nối Jira Server qua MCP Protocol.
    Hỗ trợ retry với exponential backoff.
    """

    def __init__(
        self,
        base_url: str | None = None,
        email: str | None = None,
        api_token: str | None = None,
        max_retries: int = 3,
    ) -> None:
        self.base_url = (base_url or os.getenv("JIRA_MCP_URL", "")).rstrip("/")
        self.email = email or os.getenv("JIRA_EMAIL", "")
        self.api_token = api_token or os.getenv("JIRA_API_TOKEN", "")
        self.max_retries = max_retries
        self._session: requests.Session | None = None

        if not all([self.base_url, self.email, self.api_token]):
            raise ValueError(
                "Jira credentials missing. Set JIRA_MCP_URL, JIRA_EMAIL, JIRA_API_TOKEN in .env"
            )

    def _get_session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
            self._session.auth = (self.email, self.api_token)
            self._session.headers.update(
                {"Accept": "application/json", "Content-Type": "application/json"}
            )
        return self._session

    def get(self, endpoint: str, params: dict | None = None) -> dict[str, Any]:
        """
        Thực hiện GET request đến Jira API với retry logic.

        Args:
            endpoint: API endpoint (e.g., '/rest/api/3/issue/PROJ-1234')
            params: Query parameters

        Returns:
            dict: Response JSON

        Raises:
            JiraAuthError: 401/403 response
            JiraConnectionError: Network error hoặc sau max retries
        """
        url = f"{self.base_url}{endpoint}"
        session = self._get_session()

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"[STEP-A] GET {url} (attempt {attempt}/{self.max_retries})")
                response = session.get(url, params=params, timeout=30)

                if response.status_code in (401, 403):
                    raise JiraAuthError(
                        f"Authentication failed ({response.status_code}). "
                        "Check JIRA_EMAIL and JIRA_API_TOKEN."
                    )
                if response.status_code == 404:
                    return {}  # Caller handles not-found

                response.raise_for_status()
                return response.json()

            except JiraAuthError:
                raise
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"[STEP-A] Connection error on attempt {attempt}: {e}")
                if attempt == self.max_retries:
                    raise JiraConnectionError(f"Cannot connect to Jira after {self.max_retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
            except requests.exceptions.RequestException as e:
                logger.error(f"[STEP-A] Request failed: {e}")
                raise JiraConnectionError(f"Jira request failed: {e}")

        raise JiraConnectionError("Max retries exceeded")

