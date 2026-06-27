# OpenVAG API Reference

Base URL: `http://localhost:8000`

Interactive documentation is available at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI JSON**: `/openapi.json`

---

## Health Check

### `GET /health`

Returns application health status including database connectivity and uptime.

**Response 200:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "uptime": 5432,
  "dtc_count": 995
}
```

**Response 503** (database unreachable):
```json
{
  "status": "unhealthy",
  "version": "1.0.0",
  "database": "disconnected",
  "uptime": 5432,
  "dtc_count": 0
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"healthy"` or `"unhealthy"` |
| `version` | string | API version |
| `database` | string | `"connected"` or `"disconnected"` |
| `uptime` | int | Seconds since app startup |
| `dtc_count` | int | Total DTC codes in database |

---

## DTC Codes

### `GET /api/v1/dtc`

List all DTC codes (paginated).

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number (1-indexed) |
| `per_page` | int | 25 | Items per page (1–100) |

**Response 200:**
```json
{
  "items": [
    {
      "code": "00003",
      "title": "Control Module"
    },
    {
      "code": "00059",
      "title": "Terminal 30 for Interior Lighting"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total": 995,
    "pages": 40,
    "has_next": true,
    "has_previous": false
  }
}
```

---

### `GET /api/v1/dtc/search`

Full-text search across all DTC fields (code, title, subtitle, symptoms, causes, solutions, special notes). Uses porter-stemmed tokenization.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `q` | string | *required* | Search query |
| `page` | int | 1 | Page number |
| `per_page` | int | 25 | Items per page (1–100) |

**Response 200:**
```json
{
  "items": [
    {
      "code": "00561",
      "title": "Mixture Adaptation",
      "subtitle": "Mixture Adaptation: Adaptation Limit (Add) Exceeded"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total": 12,
    "pages": 1,
    "has_next": false,
    "has_previous": false
  }
}
```

**Response 422** (missing `q` parameter):
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "q"],
      "msg": "Field required"
    }
  ]
}
```

---

### `GET /api/v1/dtc/{code}`

Get full detail for a specific DTC code.

**Path Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `code` | string | DTC code (e.g., `00283`, `16684/P0300/000768`, `P0016`) |

**Response 200:**
```json
{
  "code": "00283",
  "title": "ABS Wheel Speed Sensor Front Left (G47)",
  "variants": [
    {
      "subtitle": "Signal Outside Specifications",
      "symptoms": [
        "ABS warning light on",
        "Traction control disabled"
      ],
      "causes": [
        "Sensor faulty",
        "Wiring damage",
        "Tone wheel contaminated"
      ],
      "solutions": [
        "Check sensor air gap",
        "Inspect wiring for damage",
        "Replace sensor G47"
      ],
      "special_notes": "Check related codes 00285, 00287 for other wheel speed sensors"
    }
  ],
  "components": ["G47", "J104"],
  "related_codes": ["00285", "00287"]
}
```

**Response 404:**
```json
{
  "detail": "DTC code '99999' not found"
}
```

#### Variant Fields

| Field | Type | Description |
|-------|------|-------------|
| `subtitle` | string \| null | Fault subtype (e.g., "Short to Ground") |
| `symptoms` | string[] | Observable symptoms |
| `causes` | string[] | Possible causes |
| `solutions` | string[] | Repair steps |
| `special_notes` | string \| null | Vehicle-specific notes, TSB references |

---

## Components

### `GET /api/v1/components`

List all known VAG component identifiers (paginated).

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `per_page` | int | 25 | Items per page (1–100) |

**Response 200:**
```json
{
  "items": [
    {
      "identifier": "G47",
      "description": null
    },
    {
      "identifier": "N75",
      "description": null
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total": 341,
    "pages": 14,
    "has_next": true,
    "has_previous": false
  }
}
```

---

### `GET /api/v1/components/{identifier}`

Get component detail with all related DTC codes. Identifier lookup is case-insensitive.

**Path Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `identifier` | string | Component ID (e.g., `G47`, `N75`, `J104`) |

**Response 200:**
```json
{
  "identifier": "N75",
  "description": null,
  "dtc_codes": [
    {
      "code": "00575",
      "title": "Boost Pressure Control Valve (N75)"
    },
    {
      "code": "16826",
      "title": "Boost Pressure Regulation Valve (N75): Short to Ground"
    }
  ]
}
```

**Response 404:**
```json
{
  "detail": "Component 'X99' not found"
}
```

---

## Statistics

### `GET /api/v1/stats`

Returns row counts for all major tables.

**Response 200:**
```json
{
  "dtc_codes": 995,
  "dtc_variants": 1103,
  "components": 341,
  "dtc_components": 712,
  "related_codes": 276
}
```

---

## Common Response Patterns

### Pagination

All list endpoints return paginated responses:

```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total": 995,
    "pages": 40,
    "has_next": true,
    "has_previous": false
  }
}
```

### Error Responses

| Status | Description |
|--------|-------------|
| 200 | Success |
| 404 | Resource not found |
| 422 | Validation error (invalid query parameters) |
| 503 | Service unhealthy (database unreachable) |

---

## VAG Component Prefix Reference

| Prefix | Type | Example |
|--------|------|---------|
| G | Sensor | G47 = ABS Wheel Speed Sensor Front Left |
| N | Solenoid/Valve | N75 = Boost Pressure Control Valve |
| V | Motor/Actuator | V60 = Throttle Position Actuator |
| J | Control Module | J104 = Brake Electronics Control Module |
| F | Switch | F125 = Multi-Function Switch |
| E | Control Element | E45 = Cruise Control Switch |
| Z | Heating Element | Z35 = Heater Element |
| R | Antenna/Radio | R134 = Access/Start Authorization Antenna |
| Q | Glow Plug | Q10 = Cylinder 1 Glow Plug |
