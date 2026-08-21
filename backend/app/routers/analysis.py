from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.repository import analysis_store
from app.schemas.repository import (
    AISummary,
    AnalysisResult,
    AnalyzeRequest,
    RepositoryInfoResponse,
    TechStackResponse,
)
from app.services.ai_service import AIService
from app.services.git_service import GitService
from app.services.lang_detector import LanguageDetector
from app.services.parser_service import ParserService
from app.services.tech_detector import TechDetector
from app.utils.logger import logger

router = APIRouter(tags=["Analysis"])


@router.post("/upload/github", response_model=AnalysisResult, summary="Analyze GitHub Repository")
def analyze_github_repository(payload: AnalyzeRequest):
    """
    Accepts GitHub Repository URL, clones it, parses file structure,
    detects languages and technology stack, generates AI summary, and returns JSON.
    """
    logger.info(f"API Request received for repository analysis: {payload.url}")

    # Step 1: Clone Repository
    repo_path, clean_url, owner, repo_name = GitService.clone_repository(payload.url)
    store_key = f"{owner}/{repo_name}"

    # Step 2: Parse File System & Structure
    stats, folder_tree, readme_content = ParserService.parse_repository(repo_path)

    # Step 3: Detect Technologies & Frameworks
    technologies = TechDetector.detect_technologies(repo_path)

    # Step 4: Detect Languages & Distribution
    languages = LanguageDetector.detect_languages(repo_path)

    # Step 5: Generate AI Summary
    summary = AIService.generate_summary(
        owner=owner,
        repo_name=repo_name,
        stats=stats,
        languages=languages,
        technologies=technologies,
        folder_tree=folder_tree,
        readme_content=readme_content
    )

    result = AnalysisResult(
        owner=owner,
        repo_name=repo_name,
        url=clean_url,
        stats=stats,
        languages=languages,
        technologies=technologies,
        summary=summary,
        folder_structure=folder_tree,
        readme_content=readme_content
    )

    # Store result in memory
    analysis_store.save(store_key, result)

    return result


@router.get("/repository/info", response_model=RepositoryInfoResponse, summary="Get Repository Info & Stats")
def get_repository_info(repo: Optional[str] = Query(None, description="Repository identifier in 'owner/repo' format")):
    """Retrieves basic stats, folder hierarchy, and README for the analyzed repository."""
    result = analysis_store.get(repo)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No repository analysis found. Please run analysis on a repository first via POST /upload/github."
        )

    return RepositoryInfoResponse(
        owner=result.owner,
        repo_name=result.repo_name,
        url=result.url,
        stats=result.stats,
        folder_structure=result.folder_structure,
        readme_content=result.readme_content
    )


@router.get("/repository/summary", response_model=AISummary, summary="Get AI Repository Summary")
def get_repository_summary(repo: Optional[str] = Query(None, description="Repository identifier in 'owner/repo' format")):
    """Retrieves AI-generated summary for the analyzed repository."""
    result = analysis_store.get(repo)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No repository summary found. Please analyze a repository first via POST /upload/github."
        )

    return result.summary


@router.get("/repository/techstack", response_model=TechStackResponse, summary="Get Repository Tech Stack & Languages")
def get_repository_techstack(repo: Optional[str] = Query(None, description="Repository identifier in 'owner/repo' format")):
    """Retrieves technology stack and programming language distribution for the analyzed repository."""
    result = analysis_store.get(repo)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No repository technology details found. Please analyze a repository first via POST /upload/github."
        )

    return TechStackResponse(
        technologies=result.technologies,
        languages=result.languages
    )
