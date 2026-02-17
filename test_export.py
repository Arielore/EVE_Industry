#!/usr/bin/env python3
"""
Test script to verify YAML export functionality.
"""
import sys
from pathlib import Path
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from eve_industry.database.connection import get_db
from eve_industry.database.schema import initialize_schema
from eve_industry.modules.yaml_handler import export_all_to_yaml

def test_export():
    """Test YAML export functionality."""
    print("Testing YAML export functionality...")
    
    # Initialize schema
    print("Initializing database schema...")
    initialize_schema()
    
    # Test export
    test_dir = Path('test_export_output')
    
    print(f"Exporting data to: {test_dir}")
    export_counts = export_all_to_yaml(test_dir)
    
    print("Export counts:", export_counts)
    
    # Check if files were created
    print("\nCreated files:")
    for f in test_dir.glob('*.yaml'):
        print(f'  {f.name}: {f.stat().st_size} bytes')
        
        # Read and show first few lines
        with open(f, 'r') as file:
            content = file.read()
            lines = content.split('\n')
            print(f'    First 3 lines:')
            for i, line in enumerate(lines[:3]):
                if line.strip():
                    print(f'      {line[:80]}{"..." if len(line) > 80 else ""}')
    
    # Cleanup
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print(f"\nCleaned up test directory: {test_dir}")
    
    # Check database tables
    print("\nDatabase table counts:")
    db = get_db()
    conn = db.get_connection()
    
    for table in ['bpos', 'bpcs', 'recipes', 'facilities']:
        cursor = conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        cursor.close()
        print(f'  {table}: {count}')
    
    return export_counts

if __name__ == "__main__":
    try:
        test_export()
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()