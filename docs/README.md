# CodeSense AI - Architecture & System Design Documentation

CodeSense AI is a full-stack, AI-powered repository analysis application designed to enable developers, team leads, and reviewers to instantly understand unfamiliar GitHub codebases.

## Architectural Layers

### 1. Backend (FastAPI + Python 3.11)
- **Configuration Layer (`app/config/settings.py`)**: Uses Pydantic `BaseSettings` to manage environment variables (`OPENAI_API_KEY`, `MAX_CLONE_DEPTH`, `CORS_ORIGINS`).
- **Service Layer (`app/services/`)**:
  - `git_service.py`: Handles GitHub URL validation, directory sanitization, and git cloning via GitPython (`depth=1` shallow cloning).
  - `parser_service.py`: Performs filesystem traversal skipping build directories, calculates file/folder metrics, builds directory trees, and retrieves root `README.md`.
  - `tech_detector.py`: Scans configuration files (`package.json`, `requirements.txt`, `Dockerfile`, `pyproject.toml`, `pom.xml`, etc.) to detect technologies, frameworks, and build tools.
  - `lang_detector.py`: Maps file extensions to programming languages, sums line/byte counts, and calculates exact percentage breakdowns.
  - `ai_service.py`: Formats metadata and prompt for OpenAI API calls (`gpt-4o-mini`). Includes an algorithmic fallback generator if the API key is not present or if requests fail.
- **Router Layer (`app/routers/`)**:
  - `health.py`: Health check and system readiness endpoints.
  - `analysis.py`: Handles `POST /upload/github`, `GET /repository/info`, `GET /repository/summary`, `GET /repository/techstack`.

### 2. Frontend (React + Vite + Axios)
- **Design System (`src/App.css`)**: Glassmorphic dark design system with glowing indigo/cyan gradients, custom font integration (`Inter`, `JetBrains Mono`), and responsive UI grids.
- **Components (`src/components/`)**: Modular components for URL input with quick sample chips, step-by-step loading state, AI summary cards, technology badges grid, language percentage bars, directory explorer, and error banners.

## Data Flow Diagram

```
[ User Input (GitHub URL) ]
            │
            ▼
[ React Frontend (Axios POST /upload/github) ]
            │
            ▼
[ FastAPI Backend (app/main.py) ]
      ├──> [ GitService ] --------> Clones repo to backend/repositories/
      ├──> [ ParserService ] -----> Parses file tree & stats
      ├──> [ TechDetector ] ------> Scans manifest files
      ├──> [ LanguageDetector ] ---> Calculates language distribution
      └──> [ AIService ] ---------> Generates summary (OpenAI API / Fallback)
            │
            ▼
[ React Dashboard (State & Visual Cards) ]
```

## Security & Best Practices
- Shallow cloning (`depth=1`) minimizes bandwidth and disk usage.
- File system traversal strictly ignores `.git`, `node_modules`, `venv`, `.env`, and build outputs.
- Comprehensive error handling returns clear HTTP status codes (`400` for invalid URLs, `404` for private/missing repos, `500` for unexpected errors).
