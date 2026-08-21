import os
from pathlib import Path
from typing import Dict, List
from app.schemas.repository import LanguageShare
from app.utils.helpers import get_language_color
from app.utils.logger import logger

EXTENSION_TO_LANGUAGE = {
    ".py": "Python",
    ".pyw": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "CSS",
    ".less": "CSS",
    ".md": "Markdown",
    ".markdown": "Markdown",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".ps1": "PowerShell",
    ".php": "PHP",
    ".rb": "Ruby",
    ".sql": "SQL",
    ".dockerfile": "Docker",
    ".toml": "TOML",
    ".xml": "XML",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".kts": "Kotlin"
}


class LanguageDetector:
    """Service to detect language breakdown and calculate percentage shares."""

    @classmethod
    def detect_languages(cls, repo_path: Path) -> List[LanguageShare]:
        """Scans all source code files in repository and computes normalized language distribution."""
        logger.info("Computing language distribution...")
        lang_bytes: Dict[str, int] = {}
        total_code_bytes = 0

        for root, dirs, files in os.walk(repo_path):
            # Ignore standard system/build folders
            dirs[:] = [d for d in dirs if d not in {
                ".git", "node_modules", "venv", ".venv", "dist", "build",
                "__pycache__", ".next", ".idea", ".vscode", "target"
            }]

            for f in files:
                file_path = Path(root) / f
                ext = file_path.suffix.lower()
                
                # Check special filenames
                if f.lower() in ["dockerfile", "dockerfile.dev", "dockerfile.prod"]:
                    lang = "Docker"
                elif ext in EXTENSION_TO_LANGUAGE:
                    lang = EXTENSION_TO_LANGUAGE[ext]
                else:
                    continue  # Skip unknown or non-code files

                try:
                    size = file_path.stat().st_size
                except Exception:
                    size = 0

                lang_bytes[lang] = lang_bytes.get(lang, 0) + size
                total_code_bytes += size

        if total_code_bytes == 0:
            return [LanguageShare(
                language="Other",
                percentage=100.0,
                color=get_language_color("Other"),
                bytes_count=0
            )]

        results: List[LanguageShare] = []
        for lang, count in lang_bytes.items():
            percentage = round((count / total_code_bytes) * 100, 2)
            if percentage > 0.0:
                results.append(LanguageShare(
                    language=lang,
                    percentage=percentage,
                    color=get_language_color(lang),
                    bytes_count=count
                ))

        # Sort descending by percentage
        results.sort(key=lambda x: x.percentage, reverse=True)

        logger.info(f"Language distribution calculation complete: {len(results)} languages detected.")
        return results
