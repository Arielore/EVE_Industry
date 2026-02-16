#!/usr/bin/env python3
"""Simple database test."""

import sys
sys.path.insert(0, '.')

import os
import shutil

# Remove existing database file
db_path = "data/database/industry.duckdb"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database: {db_path}")

from src.eve_industry.database.schema import recreate_tables, get_schema_version
from src.eve_industry.database.connection import get_db

print('Recreating tables...')
recreate_tables()

# Test insert directly
db = get_db()
print("Testing direct insert...")
try:
    # Insert a test BPO
    db.execute("""
        INSERT INTO bpos (name, me_level, te_level, location, category, materials_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ('Test BPO', 5, 10, 'Test Location', 'test', '{}'))
    print("Direct insert successful!")
except Exception as e:
    print(f"Direct insert failed: {e}")

# Try to query
try:
    cursor = db.execute("SELECT name, me_level, te_level FROM bpos")
    rows = cursor.fetchall()
    print(f"Query returned {len(rows)} rows")
    for row in rows:
        print(f"  - {row}")
except Exception as e:
    print(f"Query failed: {e}")

print(f"Schema version: {get_schema_version()}")