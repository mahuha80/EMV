"""
Fix Generator – Tạo unified diff patches từ AI suggestions
"""
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class FixGenerator:
    """Tạo và validate code patches từ AI fix suggestions."""

    def create_patches(self, fixes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Tạo patch metadata từ AI fix suggestions.

        Args:
            fixes: List fix suggestions từ AI

        Returns:
            list: Enriched fix list với patch info
        """
        patches = []
        for fix in fixes:
            file_path = fix.get("file", "")
            if not file_path:
                continue

            patch = {
                **fix,
                "patch_applicable": self._check_applicable(fix),
                "unified_diff": self._create_unified_diff(fix),
            }
            patches.append(patch)
            logger.debug(f"[STEP-C] Created patch for: {file_path}")

        return patches

    def _check_applicable(self, fix: dict[str, Any]) -> bool:
        """Kiểm tra patch có thể áp dụng lên file hiện tại không."""
        file_path = fix.get("file", "")
        original = fix.get("original", "")

        if not file_path or not original:
            return False

        path = Path(file_path)
        if not path.exists():
            logger.warning(f"[STEP-C] Target file not found: {file_path}")
            return False

        content = path.read_text(encoding="utf-8")
        return original.strip() in content

    def _create_unified_diff(self, fix: dict[str, Any]) -> str:
        """Tạo unified diff string từ original và fixed code."""
        import difflib

        file_path = fix.get("file", "unknown")
        original_lines = (fix.get("original", "") + "\n").splitlines(keepends=True)
        fixed_lines = (fix.get("fixed", "") + "\n").splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            fixed_lines,
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            lineterm="",
        )
        return "\n".join(diff)

    def apply_patch(self, fix: dict[str, Any]) -> bool:
        """
        Áp dụng patch lên file thực tế.

        Args:
            fix: Fix dict với file, original, fixed

        Returns:
            bool: True nếu apply thành công
        """
        file_path = fix.get("file", "")
        original = fix.get("original", "")
        fixed_code = fix.get("fixed", "")

        if not fix.get("patch_applicable", False):
            logger.warning(f"[STEP-C] Patch not applicable: {file_path}")
            return False

        try:
            path = Path(file_path)
            content = path.read_text(encoding="utf-8")
            new_content = content.replace(original.strip(), fixed_code.strip(), 1)
            path.write_text(new_content, encoding="utf-8")
            logger.info(f"[STEP-C] Applied patch: {file_path}")
            return True
        except Exception as e:
            logger.error(f"[STEP-C] Failed to apply patch to {file_path}: {e}")
            return False

