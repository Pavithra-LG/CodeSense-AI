import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from app.schemas.repository import DirectoryNode, LargeFile, RepositoryStats
from app.utils.helpers import format_bytes
from app.utils.logger import logger

IGNORE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "env", ".env", "dist", "build",
    "__pycache__", ".next", ".nuxt", ".output", ".idea", ".vscode", "target",
    ".pytest_cache", ".tox", "coverage", ".egg-info", "eggs", "bin", "obj"
}

IGNORE_FILES = {
    ".gitignore", ".DS_Store", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "poetry.lock", "Cargo.lock"
}


class ParserService:
    """Service to parse repository file system, extract metadata and folder hierarchy."""

    @classmethod
    def parse_repository(cls, repo_path: Path) -> Tuple[RepositoryStats, DirectoryNode, Optional[str]]:
        """
        Traverses repository directory, calculates file statistics, hierarchy, and retrieves README content.
        """
        logger.info(f"Parsing codebase at {repo_path}...")
        
        total_files = 0
        total_folders = 0
        total_size = 0
        extensions: Dict[str, int] = {}
        all_file_sizes: List[Tuple[str, int]] = []
        readme_content: Optional[str] = None
        readme_found = False

        for root, dirs, files in os.walk(repo_path):
            # Exclude ignored directories in-place
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            total_folders += len(dirs)

            rel_root = os.path.relpath(root, repo_path)

            for f in files:
                if f in IGNORE_FILES:
                    continue

                full_path = Path(root) / f
                rel_path = f if rel_root == "." else os.path.join(rel_root, f)

                try:
                    size = full_path.stat().st_size
                except Exception:
                    size = 0

                total_files += 1
                total_size += size
                all_file_sizes.append((rel_path.replace("\\", "/"), size))

                # Extension tracking
                ext = full_path.suffix.lower()
                if not ext:
                    ext = "no_extension"
                extensions[ext] = extensions.get(ext, 0) + 1

                # Check for README
                if not readme_found and f.lower().startswith("readme"):
                    readme_found = True
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as rf:
                            readme_content = rf.read()
                            # Cap README content length if huge (e.g. 50 KB max)
                            if len(readme_content) > 50000:
                                readme_content = readme_content[:50000] + "\n\n... (README truncated for preview)"
                    except Exception as re_err:
                        logger.warning(f"Could not read README file at {full_path}: {str(re_err)}")
                        readme_content = None

        # Sort largest files
        all_file_sizes.sort(key=lambda x: x[1], reverse=True)
        top_largest = [
            LargeFile(path=path, size_bytes=size, size_formatted=format_bytes(size))
            for path, size in all_file_sizes[:5]
        ]

        stats = RepositoryStats(
            total_files=total_files,
            total_folders=total_folders,
            total_size_bytes=total_size,
            total_size_formatted=format_bytes(total_size),
            readme_available=readme_found,
            largest_files=top_largest,
            extensions_used=extensions
        )

        folder_tree = cls._build_tree(repo_path, max_depth=4)

        logger.info(f"Parse complete: {total_files} files, {total_folders} folders, total size {stats.total_size_formatted}")
        return stats, folder_tree, readme_content

    @classmethod
    def _build_tree(cls, current_path: Path, max_depth: int = 4, current_depth: int = 0) -> DirectoryNode:
        """Constructs a clean hierarchical directory tree representation."""
        node_name = current_path.name or "root"
        node_path = str(current_path)

        if not current_path.is_dir():
            return DirectoryNode(
                name=node_name,
                path=node_path,
                type="file",
                size=current_path.stat().st_size if current_path.exists() else 0
            )

        children: List[DirectoryNode] = []
        if current_depth < max_depth:
            try:
                entries = sorted(list(current_path.iterdir()), key=lambda e: (not e.is_dir(), e.name.lower()))
                for entry in entries:
                    if entry.name in IGNORE_DIRS or entry.name in IGNORE_FILES:
                        continue
                    if entry.is_dir():
                        children.append(cls._build_tree(entry, max_depth, current_depth + 1))
                    else:
                        children.append(DirectoryNode(
                            name=entry.name,
                            path=str(entry),
                            type="file",
                            size=entry.stat().st_size if entry.exists() else 0
                        ))
            except Exception as e:
                logger.warning(f"Error accessing directory {current_path}: {str(e)}")

        return DirectoryNode(
            name=node_name,
            path=node_path,
            type="directory",
            children=children
        )
