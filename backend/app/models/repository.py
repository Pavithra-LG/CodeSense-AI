from typing import Dict, Optional
from app.schemas.repository import AnalysisResult


class InMemoryAnalysisStore:
    """In-memory data store to hold recent analysis results."""

    def __init__(self):
        self._store: Dict[str, AnalysisResult] = {}
        self._latest_key: Optional[str] = None

    def save(self, key: str, data: AnalysisResult) -> None:
        """Save analysis result for a repo key (e.g. 'owner/repo')."""
        normalized_key = key.lower().strip()
        self._store[normalized_key] = data
        self._latest_key = normalized_key

    def get(self, key: Optional[str] = None) -> Optional[AnalysisResult]:
        """Retrieve analysis result by repo key or return latest analyzed repository."""
        if not key:
            if self._latest_key and self._latest_key in self._store:
                return self._store[self._latest_key]
            return None
        
        normalized_key = key.lower().strip()
        return self._store.get(normalized_key)

    def clear(self) -> None:
        """Clear store."""
        self._store.clear()
        self._latest_key = None


# Singleton instance for the backend session
analysis_store = InMemoryAnalysisStore()
