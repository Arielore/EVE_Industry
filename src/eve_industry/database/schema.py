"""
Database schema definition for EVE Industry application.
Contains table creation statements and schema version tracking.
"""

from eve_industry.database.connection import get_db


def create_tables():
    """Create all database tables if they don't exist."""
    db = get_db()
    
    # Table: bpos (Blueprint Originals)
    db.execute("""
        CREATE TABLE IF NOT EXISTS bpos (
            name TEXT PRIMARY KEY,
            me_level INTEGER,
            te_level INTEGER,
            location TEXT,
            category TEXT,
            materials_json TEXT
        )
    """)
    
    # Table: bpcs (Blueprint Copies)
    db.execute("""
        CREATE TABLE IF NOT EXISTS bpcs (
            name TEXT PRIMARY KEY,
            source_bpo TEXT,
            me_level INTEGER,
            te_level INTEGER,
            runs_remaining INTEGER,
            location TEXT,
            category TEXT,
            materials_json TEXT
        )
    """)
    
    # Table: recipes
    db.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            name TEXT PRIMARY KEY,
            recipe_type TEXT,
            base_item TEXT,
            me_level INTEGER,
            te_level INTEGER,
            materials_json TEXT,
            upgrade_paths_json TEXT
        )
    """)
    
    # Table: facilities
    db.execute("""
        CREATE TABLE IF NOT EXISTS facilities (
            name TEXT PRIMARY KEY,
            system TEXT,
            region TEXT,
            facility_type TEXT,
            owner TEXT,
            services_json TEXT,
            manufacturing_slots INTEGER,
            research_slots INTEGER,
            cost_index DECIMAL,
            rigs_json TEXT,
            notes TEXT
        )
    """)
    
    # Table: metadata
    db.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes
    db.execute("CREATE INDEX IF NOT EXISTS idx_bpos_category ON bpos(category)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_bpos_location ON bpos(location)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_bpcs_source ON bpcs(source_bpo)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_recipes_type ON recipes(recipe_type)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_facilities_system ON facilities(system)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_facilities_region ON facilities(region)")


def get_schema_version() -> int:
    """Get current schema version from metadata table."""
    db = get_db()
    
    try:
        cursor = db.execute("SELECT value FROM metadata WHERE key = 'schema_version'")
        result = cursor.fetchone()
        if result:
            return int(result[0])
    except Exception:
        pass
    
    return 0


def set_schema_version(version: int):
    """Set schema version in metadata table."""
    db = get_db()
    db.execute(
        "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
        ('schema_version', str(version))
    )


def initialize_schema():
    """Initialize database schema to latest version."""
    current_version = get_schema_version()
    
    if current_version == 0:
        # Create all tables for version 1
        create_tables()
        set_schema_version(1)
        print("Database schema initialized to version 1")
    elif current_version < 1:
        # Future migration logic would go here
        pass


def recreate_tables():
    """Drop and recreate all tables (for schema updates)."""
    db = get_db()
    
    # Drop all tables
    drop_all_tables()
    
    # Recreate all tables with latest schema
    create_tables()
    
    # Reset schema version
    set_schema_version(1)
    print("Tables recreated with latest schema")


def drop_all_tables():
    """Drop all tables (for testing/reset)."""
    db = get_db()
    tables = ['bpos', 'bpcs', 'recipes', 'facilities', 'metadata']
    
    for table in tables:
        try:
            db.execute(f"DROP TABLE IF EXISTS {table}")
        except Exception:
            pass


if __name__ == "__main__":
    # When run directly, initialize schema
    initialize_schema()
