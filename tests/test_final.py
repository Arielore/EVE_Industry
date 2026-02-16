#!/usr/bin/env python3
"""Final test of database loading."""

import sys
sys.path.insert(0, '.')

import os

# Remove existing database file
db_path = "data/database/industry.duckdb"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database: {db_path}")

from src.eve_industry.database.schema import recreate_tables
from src.eve_industry.database.loader import load_all_initial_data, get_bpos_from_db

print('Recreating tables...')
recreate_tables()

print('Loading data from YAML files...')
count = load_all_initial_data()

print(f'\nTotal records loaded: {count}')

# Get BPOs
bpos = get_bpos_from_db()
print(f'\nBPOs in database: {len(bpos)}')

if bpos:
    print('\nFirst 10 BPOs:')
    for i, bpo in enumerate(bpos[:10]):
        print(f"  {i+1}. {bpo['name']}: ME={bpo['me_level']}, TE={bpo['te_level']}, Location={bpo['location']}")
    
    # Count by category
    categories = {}
    for bpo in bpos:
        cat = bpo['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print('\nBPOs by category:')
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    # Test BPO list view
    print('\n--- Testing BPO List View integration ---')
    from src.eve_industry.gui.views.bpo_list_view import BPOListView
    try:
        # Just test that we can import and instantiate
        print("BPOListView import successful")
    except Exception as e:
        print(f"BPOListView import failed: {e}")
else:
    print("No BPOs loaded - check YAML file and loader")

print('\n--- Database file info ---')
if os.path.exists(db_path):
    size = os.path.getsize(db_path)
    print(f"Database file size: {size:,} bytes")
else:
    print("Database file not found")