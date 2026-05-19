b"""
Robot Runner – Chạy Robot Framework test suites (STEP B)
"""
import json
import logging
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .test_generator import TestGenerator
from .result_parser import ResultParser

logger = logging.getLogger(__name__)


class RobotRunner:
    """
    Orchestrates test generation and execution via Robot Framework + Appium.
    """

    def __init__(self, platform: str = "android") -> None:
        self.platform = platform
        self.reports_base = Path(os.getenv("REPORTS_BASE_DIR", "reports"))
        self.generator = TestGenerator()
        self.result_parser = ResultParser()

    def run(self, ticket_data: dict[str, Any]) -> dict[str, Any]:
        """
        Sinh và chạy test cases cho ticket.

        Args:
            ticket_data: Parsed ticket data từ STEP A

        Returns:
            dict: Test results bao gồm pass/fail counts và details
        """
        ticket_id: str = ticket_data["ticket_id"]
        run_id = f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        output_dir = self.reports_base / ticket_id / "robot_output"
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"[STEP-B] Starting test run: {run_id} for ticket {ticket_id}")

        # Generate test suite
        suite_path = self.generator.generate(ticket_data, self.platform)
        logger.info(f"[STEP-B] Generated test suite: {suite_path}")

        # Build robot command
        cmd = self._build_robot_command(
            suite_path=suite_path,
            output_dir=output_dir,
            ticket_id=ticket_id,
            run_id=run_id,
        )
        logger.info(f"[STEP-B] Executing: {' '.join(cmd)}")

        # Execute
        start_time = datetime.now(timezone.utc)
        returncode = self._execute(cmd)
        duration = (datetime.now(timezone.utc) - start_time).seconds

        # Parse results
        output_xml = output_dir / "output.xml"
        results = self.result_parser.parse(
            output_xml=output_xml,
            ticket_id=ticket_id,
            run_id=run_id,
            platform=self.platform,
            duration_seconds=duration,
            report_path=str(output_dir / "report.html"),
        )

        # Save results
        self._save_results(ticket_id, results)
        logger.info(
            f"[STEP-B] Test complete: {results['passed']}/{results['total']} PASS "
            f"| Status: {results['status']}"
        )
        return results

    def _build_robot_command(
        self,
        suite_path: Path,
        output_dir: Path,
        ticket_id: str,
        run_id: str,
    ) -> list[str]:
        return [
            "robot",
            "--outputdir", str(output_dir),
            "--output", "output.xml",
            "--log", "log.html",
            "--report", "report.html",
            "--variable", f"TICKET_ID:{ticket_id}",
            "--variable", f"PLATFORM:{self.platform}",
            "--variable", f"RUN_ID:{run_id}",
            "--variable", f"APPIUM_URL:{os.getenv('APPIUM_SERVER_URL', 'http://localhost:4723')}",
            str(suite_path),
        ]

    def _execute(self, cmd: list[str]) -> int:
        """Chạy robot command, stream output ra logger."""
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
            )
            for line in process.stdout:  # type: ignore
                line = line.rstrip()
                if line:
                    logger.info(f"[ROBOT] {line}")
            process.wait()
            return process.returncode
        except FileNotFoundError:
            raise RuntimeError(
                "robot command not found. Install via: pip install robotframework"
            )

    def _save_results(self, ticket_id: str, results: dict[str, Any]) -> None:
        output_path = self.reports_base / ticket_id / "test_results.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.debug(f"[STEP-B] Saved test results: {output_path}")

