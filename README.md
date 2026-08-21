# CodeSense AI – AI-Powered GitHub Repository Analysis Assistant

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.1-646CFF.svg)](https://vitejs.dev/)

**CodeSense AI** is a production-style full-stack application that helps software engineers instantly analyze and understand unfamiliar GitHub repositories. 

Simply paste a public GitHub URL or repository slug (`owner/repo`), and CodeSense AI will clone the codebase, parse file statistics, detect framework technology stacks, calculate exact language breakdown percentages, and leverage OpenAI to generate developer-friendly architectural summaries.

---

## 🌟 Key Features

- **⚡ Fast Git Clone Engine**: Clones public GitHub repositories using GitPython with shallow depth (`depth=1`) for high-speed download.
- **🔍 Tech Stack Detection**: Automatically scans manifests (`package.json`, `requirements.txt`, `pyproject.toml`, `Dockerfile`, `pom.xml`, `tsconfig.json`, `tailwind.config.js`, etc.) to identify frameworks, databases, and build tools.
- **📊 Programming Language Breakdown**: Calculates exact line and byte share percentages for Python, JavaScript, TypeScript, Java, C++, Go, Rust, HTML, CSS, Markdown, JSON, YAML, and more.
- **🤖 AI Architectural Summary**: Sends extracted repository metadata to OpenAI (`gpt-4o-mini`) to generate structured JSON insights covering project purpose, architecture, technology rationale, folder roles, key features, and developer onboarding instructions. *(Includes an automatic algorithmic fallback mode if no API key is provided).*
- **📁 Interactive Directory & README Explorer**: Visualize codebase folder hierarchies and inspect `README.md` documentation directly inside a glassmorphic dark-mode dashboard.
- **🛡️ Robust Error Handling**: Clean user feedback for invalid URLs, private/missing repositories, clone failures, network errors, and unconfigured API keys.

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11**
- **FastAPI** (REST API Framework)
- **GitPython** (Git Cloning & Repository Management)
- **OpenAI API** (GPT-4o-mini Integration)
- **Pydantic v2 & Pydantic-Settings** (Data Validation & Environment Management)
- **Uvicorn** (ASGI Web Server)

### Frontend
- **React 18**
- **Vite** (Next-generation Frontend Tooling)
- **Axios** (HTTP Client)
- **React Router v6** (Client-side Routing)
- **Lucide React** (Modern Icons)
- **Vanilla CSS** (Custom Glassmorphic Dark Design System)

---

## 📂 Project Structure

```
CodeSense-AI/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── repository.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── repository.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── git_service.py
│   │   │   ├── parser_service.py
│   │   │   ├── tech_detector.py
│   │   │   ├── lang_detector.py
│   │   │   └── ai_service.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   └── analysis.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── helpers.py
│   │   └── main.py
│   ├── repositories/
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── UrlForm.jsx
│   │   │   ├── LoadingState.jsx
│   │   │   ├── SummaryCard.jsx
│   │   │   ├── TechStackCard.jsx
│   │   │   ├── LanguagesCard.jsx
│   │   │   ├── StatsCard.jsx
│   │   │   ├── FolderTreeCard.jsx
│   │   │   └── ErrorAlert.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   └── DashboardPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docs/
│   └── README.md
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API status and version greeting |
| `GET` | `/health` | Service health check |
| `POST` | `/upload/github` | Triggers repository clone, parsing, technology detection, language calculation, and AI summary generation |
| `GET` | `/repository/info` | Retrieves basic stats, file tree hierarchy, and README content |
| `GET` | `/repository/summary` | Retrieves AI architectural summary |
| `GET` | `/repository/techstack` | Retrieves detected technologies and language distribution |

---

## 🚀 Setup & Installation Instructions

### Prerequisites
- Python 3.11+ installed
- Node.js 18+ and npm installed
- Git installed on your local machine

---

### Step 1: Backend Setup

1. Open a terminal and navigate to the backend folder:
   ```bash
   cd CodeSense-AI/backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `backend/.env`:
   ```env
   PROJECT_NAME=CodeSense AI
   OPENAI_API_KEY=your-openai-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   MAX_CLONE_DEPTH=1
   ```
   *(Note: If you leave `OPENAI_API_KEY` blank, the app will run in Algorithmic Fallback mode without breaking).*

5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The backend API will be available at `http://localhost:8000` (Swagger UI at `http://localhost:8000/docs`).

---

### Step 2: Frontend Setup

1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd CodeSense-AI/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The application web interface will be running at `http://localhost:5173`.

---

## 📝 License

This project is open-source and built for portfolio and software engineering demonstration purposes.
