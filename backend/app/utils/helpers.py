import re
from typing import Tuple


def parse_github_url(url: str) -> Tuple[str, str, str]:
    """
    Validates and parses a GitHub repository URL or slug.
    Returns a tuple of (clean_url, owner, repo_name).
    """
    clean_input = url.strip().rstrip("/")
    if clean_input.endswith(".git"):
        clean_input = clean_input[:-4]

    # Handle standard full URL: https://github.com/owner/repo
    url_pattern = r"^https?://(?:www\.)?github\.com/([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-\.]+)"
    match = re.match(url_pattern, clean_input)
    if match:
        owner, repo = match.group(1), match.group(2)
        clean_url = f"https://github.com/{owner}/{repo}"
        return clean_url, owner, repo

    # Handle short form: owner/repo
    short_pattern = r"^([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-\.]+)$"
    match = re.match(short_pattern, clean_input)
    if match:
        owner, repo = match.group(1), match.group(2)
        clean_url = f"https://github.com/{owner}/{repo}"
        return clean_url, owner, repo

    raise ValueError("Invalid GitHub URL. Format must be 'https://github.com/owner/repo' or 'owner/repo'.")


def format_bytes(size: int) -> str:
    """Format size in bytes into human readable string."""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"


LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Java": "#b07219",
    "C++": "#f34b7d",
    "C": "#555555",
    "C#": "#178600",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Markdown": "#083fa1",
    "JSON": "#292929",
    "YAML": "#cb171e",
    "Shell": "#89e051",
    "PHP": "#4F5D95",
    "Ruby": "#701516",
    "SQL": "#e38c00",
    "Docker": "#384d54",
    "Other": "#8b949e"
}


def get_language_color(lang: str) -> str:
    """Return color hex code for a programming language."""
    return LANGUAGE_COLORS.get(lang, "#8b949e")
