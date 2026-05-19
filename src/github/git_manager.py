"""GitHub git manager – Git operations helper"""
import logging
import os
from pathlib import Path
from typing import Any

import git

logger = logging.getLogger(__name__)


class GitManager:
    """Helper cho các Git operations."""

    def __init__(self, repo_path: str = ".") -> None:
        self.repo = git.Repo(repo_path)
        self.base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")

    def get_current_branch(self) -> str:
        return self.repo.active_branch.name

    def create_branch(self, branch_name: str) -> None:
        """Tạo và checkout branch mới từ base branch."""
        self.repo.remotes.origin.fetch()
        base = self.repo.remotes.origin.refs[self.base_branch]
        new_branch = self.repo.create_head(branch_name, base)
        new_branch.checkout()
        logger.info(f"[STEP-D] Created and checked out branch: {branch_name}")

    def stage_and_commit(self, message: str) -> str:
        """Stage all changes và commit. Returns commit SHA."""
        self.repo.git.add(A=True)
        if not self.repo.is_dirty(untracked_files=True):
            logger.info("[STEP-D] Nothing to commit")
            return self.repo.head.commit.hexsha
        commit = self.repo.index.commit(message)
        logger.info(f"[STEP-D] Committed: {commit.hexsha[:8]}")
        return commit.hexsha

    def push(self, branch_name: str) -> None:
        """Push branch lên remote."""
        self.repo.remotes.origin.push(branch_name)
        logger.info(f"[STEP-D] Pushed: {branch_name}")

