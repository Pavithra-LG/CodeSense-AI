from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Schema for repository analysis request."""
    url: str = Field(..., description="GitHub repository URL (e.g., https://github.com/fastapi/fastapi or fastapi/fastapi)")


class LargeFile(BaseModel):
    """Schema for large file metadata."""
    path: str
    size_bytes: int
    size_formatted: str


class LanguageShare(BaseModel):
    """Schema for language percentage breakdown."""
    language: str
    percentage: float
    color: str
    bytes_count: int


class DetectedTech(BaseModel):
    """Schema for detected technology items."""
    name: str
    category: str  # Framework, Database, Build Tool, Runtime, Config, etc.
    source_file: str


class RepositoryStats(BaseModel):
    """Schema for overall repository statistics."""
    total_files: int
    total_folders: int
    total_size_bytes: int
    total_size_formatted: str
    readme_available: bool
    largest_files: List[LargeFile]
    extensions_used: Dict[str, int]


class AISummary(BaseModel):
    """Schema for AI-generated summary results."""
    project_purpose: str
    architecture_overview: str
    technology_explanation: List[str]
    folder_explanation: List[str]
    main_features: List[str]
    developer_summary: str
    is_ai_generated: bool = True


class DirectoryNode(BaseModel):
    """Schema for tree representation of directories."""
    name: str
    path: str
    type: str  # 'file' or 'directory'
    children: Optional[List["DirectoryNode"]] = None
    size: Optional[int] = None


class RepositoryInfoResponse(BaseModel):
    """Response schema for repository info."""
    owner: str
    repo_name: str
    url: str
    stats: RepositoryStats
    folder_structure: DirectoryNode
    readme_content: Optional[str] = None


class TechStackResponse(BaseModel):
    """Response schema for technology stack and languages."""
    technologies: List[DetectedTech]
    languages: List[LanguageShare]


class AnalysisResult(BaseModel):
    """Complete response schema combining all analysis aspects."""
    owner: str
    repo_name: str
    url: str
    stats: RepositoryStats
    languages: List[LanguageShare]
    technologies: List[DetectedTech]
    summary: AISummary
    folder_structure: DirectoryNode
    readme_content: Optional[str] = None
