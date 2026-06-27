# OpenVAG Database

SQLite database containing VAG (Volkswagen/Audi Group) Diagnostic Trouble Codes (DTCs).

## Stats

| Table | Rows | Description |
|-------|------|-------------|
| `dtc_codes` | 995 | Unique DTC code + title combinations |
| `dtc_variants` | 1,103 | Fault subtypes (one code can have many) |
| `components` | 341 | Extracted VAG component identifiers |
| `dtc_components` | 712 | Code ↔ Component links |
| `related_codes` | 276 | Cross-references between DTCs |
| `dtc_fts` | 1,103 | Full-text search index |

Database file size: ~2.1 MB

---

## Schema Overview

```
dtc_codes (1)──────<(many) dtc_variants
     │
     ├──────<(many) dtc_components >(many)──── components
     │
     └──────<(many) related_codes
```

### `dtc_codes`

The primary table. Each row represents a unique DTC identified by its code and title.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `code` | TEXT | DTC code (e.g., `00283`, `16684/P0300/000768`, `P0016`) |
| `title` | TEXT | Component/system name (e.g., `ABS Wheel Speed Sensor Front Left (G47)`) |

Code formats:
- **5-digit VAG codes**: `00283`, `01262`
- **Combined format**: `16684/P0300/000768` (VAG/OBD-II/internal)
- **OBD-II P-codes**: `P0016`, `P2293`
- **Body codes**: `B1015`, `B2000`
- **Chassis codes**: `C1011`, `C10AC`
- **Network codes**: `U0103`, `U1122`

### `dtc_variants`

One DTC code can have multiple fault subtypes. For example, code `00283` (ABS Wheel Speed Sensor Front Left) has:
- "Signal Outside Specifications"
- "Mechanical Malfunction"

Each variant has its own symptoms, causes, solutions, and notes.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `dtc_code_id` | INTEGER FK | References `dtc_codes.id` |
| `subtitle` | TEXT | Fault subtype (e.g., `Short to Ground`, `Implausible Signal`) |
| `symptoms` | TEXT | Observable symptoms (semicolon-separated) |
| `causes` | TEXT | Possible causes (semicolon-separated) |
| `solutions` | TEXT | Repair steps (semicolon-separated) |
| `special_notes` | TEXT | Vehicle-specific info, TSB references, tips |

**Semicolon convention**: Multi-value fields use `;` as a delimiter.
```
"Fuse(s) faulty; Wiring faulty; Sensor faulty"
```

### `components`

VAG uses a letter + number system for component identification:

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

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `identifier` | TEXT UNIQUE | Component ID (e.g., `G47`, `N75`) |
| `description` | TEXT | Human-readable name (nullable, for future use) |

### `dtc_components`

Junction table linking DTC codes to the components they reference.

| Column | Type | Description |
|--------|------|-------------|
| `dtc_code_id` | INTEGER FK | References `dtc_codes.id` |
| `component_id` | INTEGER FK | References `components.id` |

### `related_codes`

Cross-references between DTC codes, parsed from `special_notes` fields.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `dtc_code_id` | INTEGER FK | The code that references another |
| `related_code` | TEXT | The referenced code string |

### `dtc_fts` / `dtc_fts_content`

FTS5 full-text search index. Supports porter-stemmed, case-insensitive search across all text fields.

---

## Example Queries

### Lookup a DTC by code

```sql
SELECT c.code, c.title, v.subtitle, v.symptoms, v.causes, v.solutions, v.special_notes
FROM dtc_codes c
JOIN dtc_variants v ON v.dtc_code_id = c.id
WHERE c.code = '00283';
```

### Find all DTCs for a component

```sql
SELECT c.code, c.title
FROM dtc_codes c
JOIN dtc_components dc ON dc.dtc_code_id = c.id
JOIN components comp ON comp.id = dc.component_id
WHERE comp.identifier = 'N75';
```

### Full-text search

```sql
SELECT fc.code, fc.title, fc.subtitle
FROM dtc_fts f
JOIN dtc_fts_content fc ON fc.id = f.rowid
WHERE dtc_fts MATCH 'boost pressure leak'
LIMIT 10;
```

### Get related codes

```sql
SELECT rc.related_code
FROM related_codes rc
JOIN dtc_codes c ON c.id = rc.dtc_code_id
WHERE c.code = '00096';
```

### Search by symptom

```sql
SELECT DISTINCT c.code, c.title
FROM dtc_codes c
JOIN dtc_variants v ON v.dtc_code_id = c.id
WHERE v.symptoms LIKE '%MIL%'
LIMIT 20;
```

### Count codes per component prefix (system category)

```sql
SELECT 
    SUBSTR(comp.identifier, 1, 1) AS prefix,
    COUNT(DISTINCT dc.dtc_code_id) AS code_count
FROM components comp
JOIN dtc_components dc ON dc.component_id = comp.id
GROUP BY prefix
ORDER BY code_count DESC;
```
