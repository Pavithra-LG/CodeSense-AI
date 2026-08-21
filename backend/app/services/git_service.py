import shutil
from pathlib import Path
import git
from fastapi import HTTPException
from app.config.settings import settings
from app.utils.logger import logger
from app.utils.helpers import parse_github_url


class GitService:
    """Service to handle repository cloning and cleanup."""

    @staticmethod
    def clone_repository(url: str) -> tuple[Path, str, str, str]:
        """
        Validates GitHub URL, cleans existing repo folder, and clones specified repository.
        Returns tuple of (cloned_repo_path, clean_url, owner, repo_name).
        """
        try:
            clean_url, owner, repo_name = parse_github_url(url)
        except ValueError as e:
            logger.warning(f"URL validation failed for input '{url}': {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

        target_dir = settings.REPOSITORIES_DIR / f"{owner}_{repo_name}"

        # Clean existing folder if it exists
        if target_dir.exists():
            logger.info(f"Removing existing directory for '{owner}/{repo_name}' at {target_dir}")
            try:
                # Handle potential read-only git files on Windows
                def remove_readonly(func, path, excinfo):
                    import os, stat
                    os.chmod(path, stat.S_IWRITE)
                    func(path)

                shutil.rmtree(target_dir, onerror=remove_readonly)
            except Exception as e:
                logger.error(f"Failed to delete existing repository directory {target_dir}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Failed to clear previous repository clone: {str(e)}")

        logger.info(f"Cloning repository '{clean_url}' into {target_dir}...")
        try:
            git.Repo.clone_from(
                clean_url,
                target_dir,
                depth=settings.MAX_CLONE_DEPTH,
                single_branch=True
            )
            logger.info(f"Successfully cloned '{owner}/{repo_name}'")
            return target_dir, clean_url, owner, repo_name

        except git.exc.GitCommandError as ge:
            logger.error(f"Git clone command failed for '{clean_url}': {str(ge)}")
            if "not found" in str(ge).lower() or "repository not found" in str(ge).lower():
                raise HTTPException(
                    status_code=404, 
                    detail=f"Repository not found or private: '{clean_url}'. Make sure the repository is public."
                )
            elif "authentication failed" in str(ge).lower() or "permission denied" in str(ge).lower():
                raise HTTPException(
                    status_code=403,
                    detail=f"Access denied to repository '{clean_url}'. Private repositories require authentication."
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to clone repository: {ge.stderr if hasattr(ge, 'stderr') else str(ge)}"
                )
        except Exception as e:
            logger.error(f"Unexpected error while cloning '{clean_url}': {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred during git clone: {str(e)}"
            )
