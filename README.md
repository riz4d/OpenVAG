# OpenVAG

OpenVAG (Open-source REST API for VAG (Volkswagen/Audi Group) DTC) provides fast lookup, full-text search, and cross-reference capabilities across DTC codes, fault variants, and VAG component identifiers. Built for mechanics, enthusiasts, and developers building diagnostic tools for VW, Audi, Škoda, SEAT, and other VAG-platform vehicles.

## Features

- DTC code lookup with full fault variant details (symptoms, causes, solutions)
- Full-text search with porter-stemmed tokenization across all fields
- Component identifier resolution (G-sensors, N-valves, J-modules, etc.)
- Cross-reference between related DTC codes
- Paginated list endpoints for browsing the full database
- Interactive Swagger UI documentation at `/`

## Quick Start

```bash
git clone https://github.com/riz4d/OpenVAG.git
cd OpenVAG

python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

uvicorn app.main:app --reload
```

Open http://localhost:8000 for the interactive API documentation.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/dtc` | List all DTC codes (paginated) |
| GET | `/api/v1/dtc/search?q=` | Full-text search |
| GET | `/api/v1/dtc/{code}` | Get DTC detail with variants |
| GET | `/api/v1/components` | List components (paginated) |
| GET | `/api/v1/components/{identifier}` | Component detail with related DTCs |
| GET | `/api/v1/stats` | Database statistics |

## Database

SQLite database with 995 DTC codes, 1,103 fault variants, 341 component identifiers, and full-text search powered by FTS5. See [db/README.md](db/README.md) for schema documentation.

## Documentation

- [API Reference](docs/API.md) — full endpoint documentation with examples
- [Development Guide](docs/DEVELOPMENT.md) — setup, configuration, testing

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.
