"""
PR Creator – Tạo Pull Request lên GitHub với đầy đủ thông tin (STEP D)
"""
import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import git
from github import Github, GithubException

from .commit_formatter import CommitFormatter
from .report_builder import ReportBuilder
from ..analyzer.fix_generator import FixGenerator

logger = logging.getLogger(__name__)


class PRCreator:
    """
    Orchestrates git operations và GitHub PR creation.
    """

    def __init__(self) -> None:
        self.gh_token = os.getenv("GITHUB_TOKEN", "")
        self.gh_repo_name = os.getenv("GITHUB_REPO", "")
        self.base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
        self.reviewers = [
            r.strip() for r in os.getenv("GITHUB_REVIEWERS", "").split(",") if r.strip()
        ]
        self.reports_base = Path(os.getenv("REPORTS_BASE_DIR", "reports"))

        if not self.gh_token or not self.gh_repo_name:
            raise ValueError(
                "GitHub credentials missing. Set GITHUB_TOKEN and GITHUB_REPO in .env"
            )

        self.gh = Github(self.gh_token)
        self.repo = self.gh.get_repo(self.gh_repo_name)
        self.commit_formatter = CommitFormatter()
        self.report_builder = ReportBuilder()
        self.fix_generator = FixGenerator()

    def create_pr(
        self,
        ticket_data: dict[str, Any],
        fix_report: dict[str, Any],
        test_results: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Tạo branch mới, apply fixes, commit và mở PR.

        Args:
            ticket_data: Ticket info từ STEP A
            fix_report: Fix analysis từ STEP C
            test_results: Test results từ STEP B

        Returns:
            dict: PR info bao gồm URL và số PR
        """
        ticket_id: str = ticket_data["ticket_id"]
        branch_name = self._create_branch_name(ticket_id, fix_report)

        logger.info(f"[STEP-D] Creating branch: {branch_name}")

        # Git operations
        git_repo = git.Repo(".")
        self._create_and_checkout_branch(git_repo, branch_name)

        # Apply patches
        applied = self._apply_patches(fix_report)
        logger.info(f"[STEP-D] Applied {applied} patches")

        if applied == 0:
            logger.warning("[STEP-D] No patches applied – committing report only")

        # Commit
        commit_msg = self.commit_formatter.format(ticket_data, fix_report)
        self._commit_changes(git_repo, commit_msg)

        # Push
        git_repo.remotes.origin.push(branch_name)
        logger.info(f"[STEP-D] Pushed branch: {branch_name}")

        # Create PR
        pr_body = self.report_builder.build(ticket_data, fix_report, test_results)
        pr = self._open_pr(branch_name, ticket_data, pr_body)

        pr_info = {
            "ticket_id": ticket_id,
            "branch": branch_name,
            "commit_sha": git_repo.head.commit.hexsha[:8],
            "pr_number": pr.number,
            "pr_url": pr.html_url,
            "status": pr.state,
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        }

        self._save_pr_info(ticket_id, pr_info)
        logger.info(f"[STEP-D] PR created: #{pr.number} – {pr.html_url}")
        return pr_info

    def _create_branch_name(self, ticket_id: str, fix_report: dict[str, Any]) -> str:
        """Tạo branch name từ ticket ID và root cause."""
        root_cause = fix_report.get("root_cause", "")
        # Lấy 5 từ đầu từ root cause
        words = re.sub(r"[^\w\s]", "", root_cause).lower().split()[:5]
        slug = "-".join(words) or "fix"
        return f"fix/{ticket_id}-{slug}"[:60]

    def _create_and_checkout_branch(self, repo: git.Repo, branch_name: str) -> None:
        """Tạo branch mới từ base branch."""
        repo.remotes.origin.fetch()
        base = repo.remotes.origin.refs[self.base_branch]
        new_branch = repo.create_head(branch_name, base)
        new_branch.checkout()

    def _apply_patches(self, fix_report: dict[str, Any]) -> int:
        """Apply tất cả patches trong fix report."""
        applied = 0
        for fix in fix_report.get("fixes", []):
            if self.fix_generator.apply_patch(fix):
                applied += 1
        return applied

    def _commit_changes(self, repo: git.Repo, message: str) -> None:
        """Stage all changes và commit."""
        repo.git.add(A=True)
        if not repo.index.diff("HEAD"):
            logger.info("[STEP-D] No changes to commit")
            return
        repo.index.commit(message)

    def _open_pr(
        self, branch_name: str, ticket_data: dict[str, Any], body: str
    ) -> Any:
        """Tạo GitHub Pull Request."""
        title = f"[{ticket_data['ticket_id']}] {ticket_data.get('title', 'Fix')}"
        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=branch_name,
                base=self.base_branch,
                draft=False,
            )
            if self.reviewers:
                pr.create_review_request(reviewers=self.reviewers)
            pr.add_to_labels("auto-fix", "qa-pipeline")
            return pr
        except GithubException as e:
            logger.error(f"[STEP-D] Failed to create PR: {e}")
            raise

    def _save_pr_info(self, ticket_id: str, pr_info: dict[str, Any]) -> None:
        output_path = self.reports_base / ticket_id / "pr_info.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(pr_info, f, indent=2, ensure_ascii=False)

