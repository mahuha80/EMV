"""
Result Parser – Parse Robot Framework output.xml thành structured test results
"""
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree  # type: ignore

logger = logging.getLogger(__name__)


class ResultParser:
    """Parse Robot Framework output.xml."""

    def parse(
        self,
        output_xml: Path,
        ticket_id: str,
        run_id: str,
        platform: str,
        duration_seconds: int,
        report_path: str,
    ) -> dict[str, Any]:
        """
        Parse output.xml và trả về structured test results.

        Args:
            output_xml: Path đến output.xml của Robot Framework
            ticket_id: Jira ticket ID
            run_id: Run identifier
            platform: Target platform
            duration_seconds: Tổng thời gian chạy test
            report_path: Path đến report.html

        Returns:
            dict: Structured test results
        """
        if not output_xml.exists():
            logger.warning(f"[STEP-B] output.xml not found: {output_xml}. Returning empty results.")
            return self._empty_result(ticket_id, run_id, platform, duration_seconds, report_path)

        try:
            tree = etree.parse(str(output_xml))
            root = tree.getroot()
        except Exception as e:
            logger.error(f"[STEP-B] Failed to parse output.xml: {e}")
            return self._empty_result(ticket_id, run_id, platform, duration_seconds, report_path)

        test_cases = []
        for test in root.iter("test"):
            status_elem = test.find("status")
            status = status_elem.get("status", "FAIL") if status_elem is not None else "FAIL"
            error_msg = ""
            if status == "FAIL":
                msg = status_elem.get("message", "") if status_elem is not None else ""
                error_msg = msg or self._find_failure_message(test)

            test_cases.append({
                "name": test.get("name", ""),
                "status": status,
                "duration": self._get_duration(status_elem),
                "error": error_msg,
            })

        passed = sum(1 for t in test_cases if t["status"] == "PASS")
        failed = len(test_cases) - passed

        return {
            "ticket_id": ticket_id,
            "run_id": run_id,
            "platform": platform,
            "status": "PASS" if failed == 0 else "FAIL",
            "total": len(test_cases),
            "passed": passed,
            "failed": failed,
            "duration_seconds": duration_seconds,
            "test_cases": test_cases,
            "report_path": report_path,
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }

    def _find_failure_message(self, test_elem: Any) -> str:
        for kw in test_elem.iter("kw"):
            status = kw.find("status")
            if status is not None and status.get("status") == "FAIL":
                return status.get("message", "")
        return ""

    def _get_duration(self, status_elem: Any) -> float:
        if status_elem is None:
            return 0.0
        start = status_elem.get("starttime", "")
        end = status_elem.get("endtime", "")
        if start and end:
            try:
                fmt = "%Y%m%d %H:%M:%S.%f"
                delta = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
                return delta.total_seconds()
            except ValueError:
                pass
        return 0.0

    def _empty_result(
        self, ticket_id: str, run_id: str, platform: str,
        duration_seconds: int, report_path: str
    ) -> dict[str, Any]:
        return {
            "ticket_id": ticket_id,
            "run_id": run_id,
            "platform": platform,
            "status": "ERROR",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "duration_seconds": duration_seconds,
            "test_cases": [],
            "report_path": report_path,
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }

