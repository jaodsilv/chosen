# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CHOSEN - Candidate's Helper for Optimized Seeker-Employer Networking. Multi-agent AI assistant for recruitment communication. Python/FastAPI backend with React frontend (planned). Uses file-based YAML storage with git-crypt encryption for sensitive data.

## Development Commands

```bash
# Setup (from project root)
.\scripts\setup.ps1                    # Windows
./scripts/setup.sh                     # Unix

# Activate virtual environment
.\venv\Scripts\Activate.ps1            # Windows
source venv/bin/activate               # Unix

# Start development server
cd backend && uvicorn app.main:app --reload

# Install dependencies
pip install -r backend/requirements.txt -r backend/requirements-dev.txt
```

### Testing

```bash
# Run all tests with coverage
cd backend && pytest

# Run single test file
pytest tests/unit/test_example.py

# Run single test
pytest tests/unit/test_example.py::test_function_name

# Run tests by marker
pytest -m unit
pytest -m integration
pytest -m e2e
```

### Code Quality

```bash
# All commands run from backend/ directory
black app/                             # Format code
isort app/                             # Sort imports
flake8 app/                            # Lint
mypy app/                              # Type check

# Pre-commit hooks (auto-run on commit)
pre-commit run --all-files             # Manual run
```

## Architecture

```
v2/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI entry point, CORS, exception handlers
│       ├── config.py            # Pydantic Settings (env vars → Settings object)
│       ├── dependencies.py      # FastAPI dependency injection
│       ├── api/
│       │   ├── routes/          # REST endpoints (conversations, messages, etc.)
│       │   ├── schemas/         # Pydantic request/response models
│       │   └── middleware/      # Custom middleware
│       ├── services/            # Business logic layer
│       ├── agents/              # AI agent orchestration (multi-model)
│       ├── data/                # File-based repositories (YAML storage)
│       ├── models/              # Domain models
│       ├── utils/               # Utilities
│       └── core/
│           └── exceptions.py    # AppException hierarchy
├── data/                        # Junction to encrypted data repo (git-crypt)
├── scripts/                     # Setup scripts
└── venv/                        # Python virtual environment
```

### Key Patterns

1. **Configuration**: `get_settings()` returns cached `Settings` instance from env vars
2. **Exceptions**: All app errors inherit from `AppException` with status_code, error_type, details
3. **Testing**: `conftest.py` provides `client` (sync) and `async_client` fixtures

### Agent System (Planned)

Multi-model orchestration using Anthropic SDK:
- MessageParserAgent (Haiku) - Parse LinkedIn/email messages
- CompanyResearcherAgent (Sonnet) - Research companies
- ResponseGeneratorAgent (User-selectable) - Generate responses
- FollowupJudgeAgent (Haiku) - Determine follow-up timing

### Data Storage

File-based YAML in `data/` directory (encrypted via git-crypt):
- `data/conversations/` - Conversation threads
- `data/settings/` - User profiles and preferences
- `data/cache/` - Research cache

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/docs` | Swagger UI |
| GET | `/api/redoc` | ReDoc |

Planned routes: `/api/v1/conversations`, `/api/v1/messages`, `/api/v1/analysis`, `/api/v1/settings`

## Environment Variables

Key variables in `.env` (copy from `.env.example`):
- `ANTHROPIC_API_KEY` - Required for AI features
- `DEFAULT_MODEL` - Claude model (sonnet/haiku/opus)
- `DATA_DIR` - Path to data directory
- `CORS_ORIGINS` - Allowed origins for CORS

## Pre-commit Hooks

Configured hooks (run automatically on commit):
- trailing-whitespace, end-of-file-fixer, check-yaml
- black (Python formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
