-- OpenVAG Database Schema
-- SQLite 3.x

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- =============================================================================
-- CORE TABLES
-- =============================================================================

-- Main DTC codes table (one row per unique code + title combination)
CREATE TABLE IF NOT EXISTS dtc_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,              -- e.g., "00283", "16684/P0300/000768", "P0016"
    title TEXT NOT NULL,             -- e.g., "ABS Wheel Speed Sensor Front Left (G47)"
    UNIQUE(code, title)
);

-- Variants table (one code can have multiple fault subtypes)
-- e.g., code 00283 has "Signal Outside Specifications" and "Mechanical Malfunction"
CREATE TABLE IF NOT EXISTS dtc_variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dtc_code_id INTEGER NOT NULL,
    subtitle TEXT,                   -- Fault subtype description
    symptoms TEXT,                   -- Semicolon-separated list of symptoms
    causes TEXT,                     -- Semicolon-separated list of possible causes
    solutions TEXT,                  -- Semicolon-separated list of repair steps
    special_notes TEXT,              -- Vehicle-specific notes, TSB references, tips
    FOREIGN KEY (dtc_code_id) REFERENCES dtc_codes(id) ON DELETE CASCADE
);

-- =============================================================================
-- COMPONENT REFERENCE
-- =============================================================================

-- VAG component identifiers extracted from DTC descriptions
-- Prefix convention:
--   G = Sensor          (e.g., G47 = ABS Wheel Speed Sensor Front Left)
--   N = Solenoid/Valve  (e.g., N75 = Boost Pressure Control Valve)
--   V = Motor/Actuator  (e.g., V60 = Throttle Position Actuator)
--   J = Control Module  (e.g., J104 = Brake Electronics Control Module)
--   F = Switch          (e.g., F125 = Multi-Function Switch)
--   E = Control Element (e.g., E45 = Cruise Control Switch)
--   Z = Heating Element (e.g., Z35 = Heater Element for Auxiliary Heater)
--   R = Antenna/Radio   (e.g., R134 = Access/Start Authorization Antenna)
--   Q = Glow Plug       (e.g., Q10 = Cylinder 1 Glow Plug)
CREATE TABLE IF NOT EXISTS components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identifier TEXT NOT NULL UNIQUE, -- e.g., "G47", "N75", "J104"
    description TEXT                 -- Optional human-readable name
);

-- Many-to-many relationship: DTC codes <-> Components
CREATE TABLE IF NOT EXISTS dtc_components (
    dtc_code_id INTEGER NOT NULL,
    component_id INTEGER NOT NULL,
    PRIMARY KEY (dtc_code_id, component_id),
    FOREIGN KEY (dtc_code_id) REFERENCES dtc_codes(id) ON DELETE CASCADE,
    FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
);

-- =============================================================================
-- CROSS-REFERENCES
-- =============================================================================

-- Related codes parsed from special_notes
-- e.g., code 00096 references code 00928 in its notes
CREATE TABLE IF NOT EXISTS related_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dtc_code_id INTEGER NOT NULL,
    related_code TEXT NOT NULL,      -- The referenced code (e.g., "00928", "P0798")
    FOREIGN KEY (dtc_code_id) REFERENCES dtc_codes(id) ON DELETE CASCADE
);

-- =============================================================================
-- FULL-TEXT SEARCH
-- =============================================================================

-- Backing content table for FTS5 (stores actual text for retrieval)
CREATE TABLE IF NOT EXISTS dtc_fts_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    title TEXT,
    subtitle TEXT,
    symptoms TEXT,
    causes TEXT,
    solutions TEXT,
    special_notes TEXT,
    dtc_code_id INTEGER,
    variant_id INTEGER
);

-- FTS5 virtual table for full-text search across all fields
CREATE VIRTUAL TABLE IF NOT EXISTS dtc_fts USING fts5(
    code,
    title,
    subtitle,
    symptoms,
    causes,
    solutions,
    special_notes,
    content='dtc_fts_content',
    tokenize='porter unicode61'
);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_dtc_codes_code ON dtc_codes(code);
CREATE INDEX IF NOT EXISTS idx_dtc_variants_dtc_code_id ON dtc_variants(dtc_code_id);
CREATE INDEX IF NOT EXISTS idx_related_codes_dtc_code_id ON related_codes(dtc_code_id);
CREATE INDEX IF NOT EXISTS idx_related_codes_related_code ON related_codes(related_code);
CREATE INDEX IF NOT EXISTS idx_components_identifier ON components(identifier);
