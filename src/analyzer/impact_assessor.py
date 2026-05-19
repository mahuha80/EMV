"""
Impact Assessor – Đánh giá impact của code fixes
"""
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

RISK_KEYWORDS = {
    "security": ["auth", "token", "password", "encrypt", "permission", "secret"],
    "payment": ["payment", "billing", "charge", "transaction", "stripe", "paypal"],
    "database": ["db", "database", "migration", "schema", "query", "orm"],
    "api": ["api", "endpoint", "route", "controller", "handler", "request"],
}


class ImpactAssessor:
    """Đánh giá risk và impact của fix patches."""

    def assess(
        self, patches: list[dict[str, Any]], raw_fixes: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Đánh giá tổng thể impact của tất cả patches.

        Args:
            patches: Enriched patch list từ FixGenerator
            raw_fixes: Raw AI suggestions

        Returns:
            dict: Impact assessment
        """
        files_changed = [p["file"] for p in patches if p.get("patch_applicable")]
        affected_components = self._detect_components(files_changed)
        risk_level = self._calculate_risk(files_changed, raw_fixes)
        breaking_change = self._detect_breaking_change(raw_fixes)

        impact = {
            "files_changed": len(files_changed),
            "files": files_changed,
            "risk_level": risk_level,
            "breaking_change": breaking_change,
            "affected_components": affected_components,
            "regression_risk": self._regression_risk(risk_level, breaking_change),
        }

        logger.debug(f"[STEP-C] Impact: risk={risk_level}, breaking={breaking_change}")
        return impact

    def _detect_components(self, files: list[str]) -> list[str]:
        """Detect components từ file paths."""
        components = set()
        for file in files:
            parts = Path(file).parts
            for part in parts[:-1]:  # Không tính tên file
                if part not in ("src", "lib", ".", "..", "main", "java", "kotlin", "swift"):
                    components.add(part)
        return sorted(components)

    def _calculate_risk(
        self, files: list[str], fixes: list[dict[str, Any]]
    ) -> str:
        """Tính risk level: Low, Medium, High, Critical."""
        score = 0
        all_text = " ".join(files + [f.get("explanation", "") for f in fixes]).lower()

        for category, keywords in RISK_KEYWORDS.items():
            if any(kw in all_text for kw in keywords):
                if category in ("security", "payment"):
                    score += 3
                else:
                    score += 1

        score += min(len(files), 5)  # Nhiều files thay đổi = rủi ro hơn

        if score >= 8:
            return "Critical"
        elif score >= 5:
            return "High"
        elif score >= 2:
            return "Medium"
        return "Low"

    def _detect_breaking_change(self, fixes: list[dict[str, Any]]) -> bool:
        """Phát hiện breaking change từ fix explanations."""
        breaking_keywords = [
            "remove", "delete", "rename", "breaking", "interface",
            "api change", "signature", "deprecated",
        ]
        for fix in fixes:
            explanation = fix.get("explanation", "").lower()
            if any(kw in explanation for kw in breaking_keywords):
                return True
        return False

    def _regression_risk(self, risk_level: str, breaking_change: bool) -> str:
        if breaking_change or risk_level == "Critical":
            return "High – Cần chạy full regression test"
        elif risk_level == "High":
            return "Medium – Cần chạy related component tests"
        return "Low – Chỉ cần chạy tests liên quan đến fix"

