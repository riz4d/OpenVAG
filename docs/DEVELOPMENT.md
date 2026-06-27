# Development Guide

## Prerequisites

- Python 3.11+
- `uv` or `pip` for package management

## Setup

```bash
# Clone the repository
git clone https://github.com/your-org/OpenVAG.git
cd OpenVAG

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies (including dev tools)
pip install -e ".[dev]"

# Copy environment template
cp .env.example .env
```

## Running the API

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── main.py              # App factory, lifespan, middleware
├── api/                 # Route handlers
│   ├── router.py        # Top-level router (includes sub-routers)
│   ├── health.py        # GET /health
│   ├── dtc.py           # DTC endpoints
│   ├── components.py    # Component endpoints
│   └── stats.py         # Stats endpoint
├── schemas/             # Pydantic response models
│   ├── dtc.py
│   ├── component.py
│   ├── health.py
│   └── stats.py
├── core/                # Application infrastructure
│   ├── config.py        # Settings (pydantic-settings)
│   ├── exceptions.py    # Custom exceptions
│   └── pagination.py    # Shared pagination logic
├── db/                  # Database layer
│   ├── base.py          # Connection setup
│   ├── session.py       # get_db dependency
│   └── models.py        # Row type definitions
└── services/            # Business logic
    ├── dtc_service.py
    └── component_service.py
```

## Configuration

Environment variables (via `.env` file or system environment):

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `db/openvag.db` | Path to SQLite database |
| `API_TITLE` | `OpenVAG API` | Title shown in docs |
| `API_VERSION` | `1.0.0` | API version |
| `DEBUG` | `false` | Enable debug mode |
| `ALLOWED_ORIGINS` | `*` | CORS origins (comma-separated) |

## Database

The SQLite database (`db/openvag.db`) contains VAG diagnostic trouble codes. See `db/README.md` for schema details.

The API accesses the database in read-only mode. No writes are performed through the API layer.

## Linting & Formatting

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

## Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_dtc.py
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/dtc` | List DTCs (paginated) |
| GET | `/api/v1/dtc/search?q=` | Full-text search |
| GET | `/api/v1/dtc/{code}` | DTC detail |
| GET | `/api/v1/components` | List components (paginated) |
| GET | `/api/v1/components/{id}` | Component detail |
| GET | `/api/v1/stats` | Database stats |

See `docs/API.md` for complete API reference.
