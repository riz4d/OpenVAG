# OpenVAG

REST API for VAG (Volkswagen/Audi Group) Diagnostic Trouble Codes.

Provides lookup, full-text search, and cross-reference capabilities for DTC codes, component identifiers, and fault variants.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for interactive API documentation.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/dtc` | List all DTC codes (paginated) |
| GET | `/api/v1/dtc/search?q=` | Full-text search |
| GET | `/api/v1/dtc/{code}` | Get DTC detail |
| GET | `/api/v1/components` | List components (paginated) |
| GET | `/api/v1/components/{identifier}` | Component detail with related DTCs |
| GET | `/api/v1/stats` | Database statistics |

## Database

SQLite database with 995 DTC codes, 1,103 variants, and 341 component identifiers. See [db/README.md](db/README.md) for schema documentation.

## Documentation

- [API Reference](docs/API.md) — full endpoint documentation with examples
- [Development Guide](docs/DEVELOPMENT.md) — setup, running, testing

