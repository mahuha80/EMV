"""
Code Reader – Đọc source code liên quan đến lỗi từ stack trace
"""
import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

CONTEXT_LINES = 25  # Số dòng context xung quanh lỗi


class CodeReader:
    """Đọc và index source code liên quan đến test failures."""

    def gather_context(self, failed_tests: list[dict[str, Any]]) -> str:
        """
        Thu thập code context từ tất cả failed tests.

        Args:
            failed_tests: List test cases FAIL với error messages

        Returns:
            str: Formatted code context string
        """
        context_parts: list[str] = []
        visited_files: set[str] = set()

        for test in failed_tests:
            error = test.get("error", "")
            if not error:
                continue

            file_locations = self._extract_file_locations(error)
            for file_path, line_no in file_locations:
                if file_path in visited_files:
                    continue
                visited_files.add(file_path)

                snippet = self._read_snippet(file_path, line_no)
                if snippet:
                    context_parts.append(
                        f"--- File: {file_path} (around line {line_no}) ---\n{snippet}"
                    )

        if not context_parts:
            context_parts.append("No source code context available from stack trace.")

        return "\n\n".join(context_parts)

    def _extract_file_locations(self, error: str) -> list[tuple[str, int]]:
        """
        Parse stack trace để tìm file paths và line numbers.
        Hỗ trợ Python, Java, Kotlin, Swift stack trace formats.
        """
        locations: list[tuple[str, int]] = []

        # Python: File "path/to/file.py", line 42
        python_pattern = re.compile(r'File "([^"]+\.py)", line (\d+)')
        for match in python_pattern.finditer(error):
            locations.append((match.group(1), int(match.group(2))))

        # Java/Kotlin: at com.example.Class.method(File.java:145)
        java_pattern = re.compile(r'at [\w.$]+\((\w+\.\w+):(\d+)\)')
        for match in java_pattern.finditer(error):
            filename = match.group(1)
            line_no = int(match.group(2))
            # Tìm file trong project
            found = self._find_file(filename)
            if found:
                locations.append((found, line_no))

        # Swift: path/to/File.swift:42
        swift_pattern = re.compile(r'([\w/.-]+\.swift):(\d+)')
        for match in swift_pattern.finditer(error):
            locations.append((match.group(1), int(match.group(2))))

        return locations

    def _find_file(self, filename: str) -> str | None:
        """Tìm file theo tên trong project directory."""
        for path in Path(".").rglob(filename):
            if ".git" not in str(path) and "node_modules" not in str(path):
                return str(path)
        return None

    def _read_snippet(self, file_path: str, line_no: int) -> str:
        """Đọc code snippet xung quanh dòng lỗi."""
        path = Path(file_path)
        if not path.exists():
            logger.debug(f"[STEP-C] File not found: {file_path}")
            return ""

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
            start = max(0, line_no - CONTEXT_LINES - 1)
            end = min(len(lines), line_no + CONTEXT_LINES)
            snippet_lines = []
            for i, line in enumerate(lines[start:end], start=start + 1):
                marker = ">>>" if i == line_no else "   "
                snippet_lines.append(f"{marker} {i:4d} | {line}")
            return "\n".join(snippet_lines)
        except Exception as e:
            logger.warning(f"[STEP-C] Cannot read {file_path}: {e}")
            return ""

