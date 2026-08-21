import json
import os
from pathlib import Path
from typing import List, Set
from app.schemas.repository import DetectedTech
from app.utils.logger import logger


class TechDetector:
    """Service to analyze repository configuration files and detect frameworks, databases, and dependencies."""

    @classmethod
    def detect_technologies(cls, repo_path: Path) -> List[DetectedTech]:
        """Scans codebase files for tech signatures."""
        logger.info("Detecting technologies and frameworks...")
        detected: List[DetectedTech] = []
        found_keys: Set[str] = set()

        def add_tech(name: str, category: str, source: str):
            if name not in found_keys:
                found_keys.add(name)
                detected.append(DetectedTech(name=name, category=category, source_file=source))

        # Check file existence signatures
        for root, _, files in os.walk(repo_path):
            rel_dir = os.path.relpath(root, repo_path)
            if any(part in {".git", "node_modules", "venv", ".venv", "dist", "build"} for part in Path(rel_dir).parts):
                continue

            for f in files:
                file_lower = f.lower()
                full_file_path = Path(root) / f
                rel_file_path = f if rel_dir == "." else os.path.join(rel_dir, f).replace("\\", "/")

                # Docker & Containers
                if file_lower in ["dockerfile", "dockerfile.dev", "dockerfile.prod"]:
                    add_tech("Docker", "Containerization", rel_file_path)
                elif file_lower in ["docker-compose.yml", "docker-compose.yaml", "compose.yml"]:
                    add_tech("Docker Compose", "Orchestration", rel_file_path)

                # TypeScript / JavaScript Build Configs
                elif file_lower == "tsconfig.json":
                    add_tech("TypeScript", "Language / Compiler", rel_file_path)
                elif "vite.config" in file_lower:
                    add_tech("Vite", "Build Tool", rel_file_path)
                elif "next.config" in file_lower:
                    add_tech("Next.js", "Framework", rel_file_path)
                elif "tailwind.config" in file_lower:
                    add_tech("Tailwind CSS", "Styling Framework", rel_file_path)

                # Java / Kotlin
                elif file_lower == "pom.xml":
                    add_tech("Maven / Java", "Build System", rel_file_path)
                elif file_lower in ["build.gradle", "build.gradle.kts"]:
                    add_tech("Gradle / Java", "Build System", rel_file_path)

                # Go & Rust
                elif file_lower == "go.mod":
                    add_tech("Go", "Runtime & Modules", rel_file_path)
                elif file_lower == "cargo.toml":
                    add_tech("Rust / Cargo", "Package Manager", rel_file_path)

                # Parse package.json
                if file_lower == "package.json":
                    cls._parse_package_json(full_file_path, rel_file_path, add_tech)

                # Parse requirements.txt / pyproject.toml
                elif file_lower == "requirements.txt":
                    cls._parse_requirements_txt(full_file_path, rel_file_path, add_tech)
                elif file_lower == "pyproject.toml":
                    cls._parse_pyproject_toml(full_file_path, rel_file_path, add_tech)

        logger.info(f"Tech detection finished. Found {len(detected)} technology signatures.")
        return detected

    @staticmethod
    def _parse_package_json(file_path: Path, rel_path: str, add_tech):
        """Parse package.json dependencies."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                deps = {}
                deps.update(data.get("dependencies", {}))
                deps.update(data.get("devDependencies", {}))

                add_tech("Node.js", "Runtime", rel_path)

                mapping = {
                    "react": ("React", "Frontend Library"),
                    "react-dom": ("React", "Frontend Library"),
                    "vue": ("Vue.js", "Frontend Framework"),
                    "svelte": ("Svelte", "Frontend Framework"),
                    "@angular/core": ("Angular", "Frontend Framework"),
                    "next": ("Next.js", "Fullstack Framework"),
                    "express": ("Express.js", "Backend Framework"),
                    "nest": ("NestJS", "Backend Framework"),
                    "@nestjs/core": ("NestJS", "Backend Framework"),
                    "tailwindcss": ("Tailwind CSS", "Styling"),
                    "typescript": ("TypeScript", "Language"),
                    "axios": ("Axios", "HTTP Client"),
                    "mongoose": ("MongoDB / Mongoose", "Database ORM"),
                    "pg": ("PostgreSQL", "Database Driver"),
                    "mysql2": ("MySQL", "Database Driver"),
                    "redis": ("Redis", "In-Memory Data Store"),
                    "prisma": ("Prisma", "Database ORM"),
                    "sequelize": ("Sequelize", "Database ORM"),
                    "graphql": ("GraphQL", "API Query Language")
                }

                for key, (tech_name, category) in mapping.items():
                    if key in deps:
                        add_tech(tech_name, category, rel_path)
        except Exception as e:
            logger.warning(f"Error reading package.json at {file_path}: {str(e)}")

    @staticmethod
    def _parse_requirements_txt(file_path: Path, rel_path: str, add_tech):
        """Parse Python requirements.txt."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()

                add_tech("Python", "Runtime", rel_path)

                mapping = {
                    "fastapi": ("FastAPI", "Web Framework"),
                    "flask": ("Flask", "Web Framework"),
                    "django": ("Django", "Web Framework"),
                    "pydantic": ("Pydantic", "Data Validation"),
                    "uvicorn": ("Uvicorn", "ASGI Server"),
                    "gunicorn": ("Gunicorn", "WSGI Server"),
                    "openai": ("OpenAI API", "AI Integration"),
                    "sqlalchemy": ("SQLAlchemy", "Database ORM"),
                    "psycopg2": ("PostgreSQL", "Database Adapter"),
                    "pymongo": ("MongoDB", "Database Driver"),
                    "redis": ("Redis", "Cache / Queue"),
                    "celery": ("Celery", "Task Queue"),
                    "torch": ("PyTorch", "Machine Learning"),
                    "tensorflow": ("TensorFlow", "Machine Learning"),
                    "pandas": ("Pandas", "Data Processing"),
                    "numpy": ("NumPy", "Data Computation"),
                    "gitpython": ("GitPython", "Git Automation")
                }

                for pkg, (tech_name, category) in mapping.items():
                    if pkg in content:
                        add_tech(tech_name, category, rel_path)
        except Exception as e:
            logger.warning(f"Error reading requirements.txt at {file_path}: {str(e)}")

    @staticmethod
    def _parse_pyproject_toml(file_path: Path, rel_path: str, add_tech):
        """Parse Python pyproject.toml."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()

                add_tech("Python", "Runtime", rel_path)

                mapping = {
                    "fastapi": ("FastAPI", "Web Framework"),
                    "poetry": ("Poetry", "Dependency Management"),
                    "flit": ("Flit", "Packaging Tool"),
                    "hatchling": ("Hatch", "Build Backend"),
                    "django": ("Django", "Web Framework"),
                    "flask": ("Flask", "Web Framework"),
                    "openai": ("OpenAI API", "AI Integration")
                }

                for pkg, (tech_name, category) in mapping.items():
                    if pkg in content:
                        add_tech(tech_name, category, rel_path)
        except Exception as e:
            logger.warning(f"Error reading pyproject.toml at {file_path}: {str(e)}")
