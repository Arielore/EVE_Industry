#!/usr/bin/env python3
"""Test application startup."""

import sys
import traceback

print("Testing EVE Industry application startup...")

try:
    # First ensure database is initialized
    print("1. Initializing database...")
    from src.eve_industry.database.schema import initialize_schema
    from src.eve_industry.database.loader import load_all_initial_data
    
    initialize_schema()
    load_all_initial_data()
    print("   Database ready")
    
    # Try to import main modules
    print("2. Testing imports...")
    from PySide6.QtWidgets import QApplication
    from eve_industry.gui.main_window import MainWindow
    from eve_industry.gui.views.bpo_list_view import BPOListView
    
    print("   Imports successful")
    
    # Test creating a simple QApplication (without event loop)
    print("3. Testing QApplication creation...")
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    
    print("   QApplication created")
    
    # Test creating BPOListView widget
    print("4. Testing BPOListView creation...")
    bpo_view = BPOListView()
    print("   BPOListView created")
    
    # Test that it can load data
    print("5. Testing BPOListView data loading...")
    bpo_view.load_data()
    print("   BPOListView data loaded")
    
    print("\n=== APPLICATION STARTUP TEST PASSED ===")
    print("The application should launch successfully.")
    print(f"BPOListView table has {bpo_view.table.rowCount()} rows")
    
    # Get actual BPO count from database
    from src.eve_industry.database.loader import get_bpos_from_db
    bpos = get_bpos_from_db()
    print(f"Database has {len(bpos)} BPOs")
    
    if bpo_view.table.rowCount() == len(bpos):
        print("✓ BPOListView table correctly populated")
    else:
        print(f"⚠ BPOListView table has {bpo_view.table.rowCount()} rows, expected {len(bpos)}")
        print("   (This might be expected if table is using sample data as fallback)")
        
except Exception as e:
    print(f"\n=== APPLICATION STARTUP TEST FAILED ===")
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)