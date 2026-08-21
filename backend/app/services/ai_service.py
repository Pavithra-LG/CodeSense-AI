import json
from typing import List, Optional
from openai import OpenAI
from app.config.settings import settings
from app.schemas.repository import AISummary, DetectedTech, DirectoryNode, LanguageShare, RepositoryStats
from app.utils.logger import logger


class AIService:
    """Service to generate structured AI analysis summaries using OpenAI API."""

    @classmethod
    def generate_summary(
        cls,
        owner: str,
        repo_name: str,
        stats: RepositoryStats,
        languages: List[LanguageShare],
        technologies: List[DetectedTech],
        folder_tree: DirectoryNode,
        readme_content: Optional[str] = None
    ) -> AISummary:
        """
        Sends extracted repository metadata to OpenAI model and parses JSON response into AISummary.
        Provides a comprehensive fallback if OPENAI_API_KEY is not configured or request fails.
        """
        if not settings.OPENAI_API_KEY:
            logger.info("OPENAI_API_KEY not configured. Generating algorithmic fallback summary.")
            return cls._generate_fallback_summary(owner, repo_name, stats, languages, technologies, readme_content)

        logger.info(f"Initiating OpenAI API request using model '{settings.OPENAI_MODEL}'...")

        lang_str = ", ".join([f"{l.language} ({l.percentage}%)" for l in languages[:5]])
        tech_str = ", ".join([f"{t.name} ({t.category})" for t in technologies[:10]])
        readme_snippet = (readme_content[:1500] + "...") if readme_content else "No README file provided."

        system_prompt = (
            "You are CodeSense AI, a world-class senior software architect and code analyst. "
            "Analyze the provided repository information and generate a clear, highly accurate, "
            "developer-friendly project breakdown in pure JSON format.\n"
            "Do NOT include markdown formatting or triple backticks ``` in your response, return ONLY the raw JSON object."
        )

        user_prompt = f"""
Repository: {owner}/{repo_name}
Total Files: {stats.total_files} | Total Folders: {stats.total_folders} | Size: {stats.total_size_formatted}
Languages: {lang_str}
Detected Technologies: {tech_str}

README Snippet:
{readme_snippet}

Please respond with a JSON object containing the exact fields:
{{
  "project_purpose": "2-3 clear sentences summarizing what this application does and its core objective.",
  "architecture_overview": "Comprehensive breakdown of how the codebase is structured and the architectural pattern used.",
  "technology_explanation": ["List of strings explaining why each detected tech/framework is used in this repo."],
  "folder_explanation": ["List of strings explaining key directories and their functional roles."],
  "main_features": ["List of 4-6 key features provided by this repository."],
  "developer_summary": "A friendly 3-4 sentence quick-start summary for a software engineer joining the codebase."
}}
"""

        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )

            raw_content = response.choices[0].message.content.strip()
            # Clean possible markdown block markers
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.startswith("```"):
                raw_content = raw_content[3:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]
            raw_content = raw_content.strip()

            parsed_data = json.loads(raw_content)

            logger.info("OpenAI API request completed successfully.")
            return AISummary(
                project_purpose=parsed_data.get("project_purpose", f"{repo_name} is a software project built with {lang_str}."),
                architecture_overview=parsed_data.get("architecture_overview", "Modular application architecture."),
                technology_explanation=parsed_data.get("technology_explanation", [t.name for t in technologies]),
                folder_explanation=parsed_data.get("folder_explanation", ["Core repository directories and configuration files."]),
                main_features=parsed_data.get("main_features", ["Source code structure", "Configured build scripts"]),
                developer_summary=parsed_data.get("developer_summary", "Review the README and source code for details."),
                is_ai_generated=True
            )

        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}. Falling back to algorithmic summary.")
            return cls._generate_fallback_summary(owner, repo_name, stats, languages, technologies, readme_content)

    @classmethod
    def _generate_fallback_summary(
        cls,
        owner: str,
        repo_name: str,
        stats: RepositoryStats,
        languages: List[LanguageShare],
        technologies: List[DetectedTech],
        readme_content: Optional[str]
    ) -> AISummary:
        """Generates a rich algorithmic summary when OpenAI API is unavailable or unconfigured."""
        primary_lang = languages[0].language if languages else "Software"
        tech_names = [t.name for t in technologies] if technologies else [primary_lang]
        tech_list_formatted = ", ".join(tech_names[:6])

        # Purpose synthesis
        purpose = (
            f"'{repo_name}' is a {primary_lang} application developed by {owner}. "
            f"It leverages modern tools including {tech_list_formatted} to provide a modular solution across {stats.total_files} files."
        )

        # Architecture synthesis
        arch = (
            f"The project follows a standard {primary_lang} project structure with {stats.total_folders} directories. "
            f"Code files are organized into logical modules with clear separation between core logic, configuration assets, and dependencies."
        )

        # Tech explanations
        tech_explanations = []
        for t in technologies[:5]:
            tech_explanations.append(f"• {t.name} ({t.category}): Identified via '{t.source_file}' for core project functionality.")
        if not tech_explanations:
            tech_explanations.append(f"• {primary_lang}: Primary language used across {languages[0].percentage}% of codebase.")

        # Folder explanations
        folder_explanations = [
            f"• Root Directory: Contains configuration files, dependency manifests, and project documentation.",
            f"• Total Folders ({stats.total_folders}): Distributed across functional modules and source code trees."
        ]

        # Features synthesis
        features = [
            f"Built primarily with {primary_lang} ({languages[0].percentage}% of codebase)",
            f"Includes {len(technologies)} detected technology frameworks and build integration points",
            f"Repository size: {stats.total_size_formatted} spanning {stats.total_files} tracked files",
            f"README documentation is {'available' if stats.readme_available else 'not present in root'}"
        ]

        # Developer summary
        dev_summary = (
            f"To get started with '{repo_name}', clone the repo locally and inspect the project configuration files "
            f"({', '.join([t.source_file for t in technologies[:3]]) or 'root files'}). "
            f"Ensure runtime dependencies for {primary_lang} are installed before executing main entrypoints."
        )

        return AISummary(
            project_purpose=purpose,
            architecture_overview=arch,
            technology_explanation=tech_explanations,
            folder_explanation=folder_explanations,
            main_features=features,
            developer_summary=dev_summary,
            is_ai_generated=False
        )
