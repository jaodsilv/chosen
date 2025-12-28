# CHOSEN

**C**andidate's **H**elper for **O**ptimized **S**eeker-**E**mployer **N**etworking

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A multi-agent AI assistant that helps job seekers optimize their communication with employers and recruiters.

## Features

- **AI-Powered Response Generation** - Generate professional, context-aware responses using Claude AI
- **Conversation Tracking** - Manage and track multiple recruiter conversations
- **Context Analysis** - Analyze conversation sentiment, patterns, and stage
- **Job Fit Scoring** - Evaluate job-candidate fit based on requirements
- **Follow-up Optimization** - Get intelligent timing recommendations for follow-ups
- **Secure Data Storage** - File-based YAML storage with git-crypt encryption
- **CLI Interface** (P1) - Command-line tool for generating responses and managing conversations
- **AI Resilience** (P0) - Graceful handling of API outages with retry and fallback mechanisms

## Current Status

| Milestone | Issues | Status |
|-----------|--------|--------|
| P0: Minimal Backend | 5 | 2 Done (#66, #67), 3 Pending |
| P1: Core + CLI | 9 | Pending |
| P2: Intelligence | 8 | Pending |
| P3: Polish | 16 | Pending |

**Completed:**
- FileHandler (#66): File operations with read/write/lock
- YAMLHandler (#67): YAML serialization with validation

See [ROADMAP.md](ROADMAP.md) for details.

## Quick Start

### Prerequisites

- Python 3.11+
- Git
- [Anthropic API key](https://console.anthropic.com/)

### Setup

**Windows:**
```powershell
.\scripts\setup.ps1
```

**Unix/macOS:**
```bash
./scripts/setup.sh
```

### Configuration

1. Copy `.env.example` to `.env`
2. Add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```

### Run the Server

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11+, FastAPI |
| AI/ML | Anthropic Claude SDK |
| Data Validation | Pydantic v2 |
| Data Storage | YAML files with git-crypt encryption |
| Testing | pytest with coverage |
| Code Quality | black, isort, flake8, mypy |

## Project Structure

```
chosen/
├── backend/
│   ├── app/
│   │   ├── api/          # REST endpoints
│   │   ├── agents/       # AI agent orchestration
│   │   ├── data/         # File-based repositories
│   │   ├── models/       # Domain models
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI entry point
│   └── tests/            # Unit, integration, e2e tests
├── data/                 # Encrypted data (git-crypt)
├── docs/                 # Design documentation
├── scripts/              # Setup scripts
├── ROADMAP.md           # Development roadmap
└── CLAUDE.md            # Development guidance
```

## Documentation

- [ROADMAP.md](ROADMAP.md) - Development milestones and issue tracking
- [docs/](docs/) - Design documentation
  - [SYSTEM-DESIGN.md](docs/SYSTEM-DESIGN.md) - Technical architecture
  - [DEV-PLAN.md](docs/DEV-PLAN.md) - Development process
  - [INTERFACE-DESIGN.md](docs/INTERFACE-DESIGN.md) - UI/UX specification
  - [requirements.md](docs/requirements.md) - Product requirements
  - [planning/RISKS.md](docs/planning/RISKS.md) - Risk analysis and mitigations
- [CLAUDE.md](CLAUDE.md) - Development commands and patterns
- [DATA_SETUP.md](DATA_SETUP.md) - Data repository setup guide

## Development

### Running Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test types
pytest -m unit
pytest -m integration
```

### Code Quality

```bash
cd backend

# Format code
black app/
isort app/

# Lint
flake8 app/
mypy app/
```

Pre-commit hooks are configured to run these automatically.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/docs` | Swagger UI |
| GET | `/api/redoc` | ReDoc |

See [ROADMAP.md](ROADMAP.md) for planned endpoints.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
