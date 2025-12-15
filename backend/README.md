# AI Message Writer Assistant v2 - Backend

Python FastAPI backend for the AI Message Writer Assistant.

## Quick Start

### Prerequisites

- Python 3.11+
- pip
- git-crypt (for data encryption)

### Installation

```bash
# From the project root directory

# Option 1: Use setup script (recommended)
# Unix/macOS:
./scripts/setup.sh

# Windows PowerShell:
.\scripts\setup.ps1

# Option 2: Manual setup
python -m venv venv
source venv/bin/activate  # Unix/macOS
# or: .\venv\Scripts\Activate.ps1  # Windows

pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt
```

### Running the Server

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at:

- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/api/docs>
- ReDoc: <http://localhost:8000/api/redoc>

### Health Check

```bash
curl http://localhost:8000/health
```

## Project Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── dependencies.py      # Dependency injection
│   │
│   ├── api/                 # API Layer
│   │   ├── routes/          # REST endpoints
│   │   ├── schemas/         # Request/response models
│   │   └── middleware/      # Custom middleware
│   │
│   ├── services/            # Business Logic Layer
│   ├── agents/              # AI Agent System
│   ├── data/                # Data Access Layer
│   ├── models/              # Domain Models
│   ├── utils/               # Utilities
│   └── core/                # Core (exceptions, constants)
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── prompts/                 # Prompt templates
│   ├── system_prompts/
│   └── templates/
│
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml          # Project configuration
└── pytest.ini              # Test configuration
```

## Development

### Code Quality

```bash
# Format code
black app/
isort app/

# Lint
flake8 app/

# Type check
mypy app/
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test category
pytest -m unit
pytest -m integration
pytest -m e2e
```

### Pre-commit Hooks

Pre-commit hooks are installed during setup. They run automatically on commit:

- trailing whitespace removal
- end-of-file fixer
- YAML validation
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)

To run manually:

```bash
pre-commit run --all-files
```

## Configuration

Configuration is managed via environment variables. See `.env.example` for available options:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | - | Anthropic API key (required) |
| `DEFAULT_MODEL` | `sonnet` | Default Claude model |
| `API_PORT` | `8000` | API server port |
| `LOG_LEVEL` | `INFO` | Logging level |
| `DATA_DIR` | `./data` | Data directory path |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/docs` | Swagger UI |
| GET | `/api/redoc` | ReDoc |

Additional endpoints will be added as the application develops:

- `/api/v1/conversations` - Conversation management
- `/api/v1/messages` - Message operations
- `/api/v1/analysis` - Context analysis
- `/api/v1/settings` - User settings

## Design Decisions

### Pre-commit Tools

We use **flake8** instead of ruff for linting. While ruff offers better performance, flake8's simpler configuration and established ecosystem is sufficient for this small codebase. This is an intentional choice to avoid over-engineering.

### Data Directory

The `data/` directory is **tracked in git** (not gitignored) but encrypted via **git-crypt**. This enables secure storage of sensitive conversation data and research cache while maintaining version control.

### Async Endpoints

Simple endpoints like `/health` and `/` are marked async but don't perform async I/O operations. This is intentional and acceptable for simple operations. Future endpoints that interact with external services (Claude API, external APIs) should properly utilize async I/O patterns.

### Settings Caching

`get_settings()` uses `@lru_cache` to avoid repeated environment variable parsing on every request. This is the recommended Pydantic Settings pattern for performance optimization.

## License

MIT
