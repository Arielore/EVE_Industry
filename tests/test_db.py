#!/usr/bin/env python3
"""Test database recreation and data loading."""

import sys
sys.path.insert(0, '.')

from src.eve_industry.database.schema import recreate_tables
from src.eve_industry.database.loader import load_all_initial_data, get_bpos_from_db

print('Recreating tables...')
recreate_tables()

print('Loading data...')
count = load_all_initial_data()

bpos = get_bpos_from_db()
print(f'Loaded {count} total records')
print(f'BPOs in database: {len(bpos)}')
print(f'First 5 BPOs: {[b["name"] for b in bpos[:5]]}')

if len(bpos) > 0:
    print('\nSample BPO details:')
    for i, bpo in enumerate(bpos[:3]):
        print(f"  {i+1}. {bpo['name']}: ME={bpo['me_level']}, TE={bpo['te_level']}, Location={bpo['location']}, Category={bpo['category']}")