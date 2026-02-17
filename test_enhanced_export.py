#!/usr/bin/env python3
"""
Test enhanced export functionality with SDE blueprint data.
"""
import sys
from pathlib import Path
import shutil
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from eve_industry.database.connection import get_db
from eve_industry.database.schema import initialize_schema
from eve_industry.modules.yaml_handler import export_all_to_yaml

def test_enhanced_export():
    """Test enhanced YAML export with SDE blueprint data."""
    print("Testing enhanced YAML export (with SDE blueprint data)...")
    
    # Initialize schema
    print("Initializing database schema...")
    initialize_schema()
    
    # Check if SDE views exist
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM information_schema.tables 
        WHERE table_name = 'types' AND table_schema = 'main'
    """)
    sde_exists = cursor.fetchone()[0] > 0
    cursor.close()
    
    print(f"SDE views exist: {sde_exists}")
    
    if not sde_exists:
        print("Note: SDE views not found - sde_blueprints.yaml will be empty")
        print("To get SDE data, use the SDE importer from the SDE tab")
    
    # Test export
    test_dir = Path('test_enhanced_export')
    
    print(f"\nExporting data to: {test_dir}")
    start_time = time.time()
    export_counts = export_all_to_yaml(test_dir)
    elapsed_time = time.time() - start_time
    
    print(f"Export completed in {elapsed_time:.2f} seconds")
    print("\nExport counts:", export_counts)
    
    # Check all created files
    print("\nCreated files:")
    total_size = 0
    for f in test_dir.glob('*.yaml'):
        size = f.stat().st_size
        total_size += size
        print(f'  {f.name}: {size:,} bytes')
        
        # Show first few lines of each file
        if size > 0:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                lines = content.split('\n')
                non_empty_lines = [line for line in lines[:5] if line.strip()]
                if non_empty_lines:
                    print(f'    First {len(non_empty_lines)} lines:')
                    for i, line in enumerate(non_empty_lines):
                        if len(line) > 80:
                            print(f'      {line[:77]}...')
                        else:
                            print(f'      {line}')
    
    print(f"\nTotal exported size: {total_size:,} bytes")
    
    # Show SDE blueprint data if exported
    sde_file = test_dir / "sde_blueprints.yaml"
    if sde_file.exists() and sde_file.stat().st_size > 0:
        print("\n=== SDE Blueprint Data ===")
        with open(sde_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            # Count blueprints in file (look for lines starting with '- type_id:')
            bp_count = sum(1 for line in lines if line.strip().startswith('- type_id:'))
            print(f"Number of SDE blueprints exported: {bp_count}")
            
            if bp_count > 0:
                # Show first blueprint details
                print("\nFirst blueprint in export:")
                in_first_bp = False
                bp_lines = []
                for i, line in enumerate(lines):
                    if line.strip().startswith('- type_id:'):
                        if not in_first_bp:
                            in_first_bp = True
                            bp_lines.append(line)
                        else:
                            break
                    elif in_first_bp:
                        if line.strip() and not line.strip().startswith('- '):
                            bp_lines.append(line)
                        elif line.strip().startswith('- '):
                            break
                
                for line in bp_lines[:10]:  # Show first 10 lines of blueprint
                    print(f"  {line}")
    
    # Cleanup
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print(f"\nCleaned up test directory: {test_dir}")
    
    # Summary
    print("\n=== Export Summary ===")
    print(f"Custom BPOs: {export_counts.get('bpos', 0)}")
    print(f"Custom BPCs: {export_counts.get('bpcs', 0)}")
    print(f"Custom Facilities: {export_counts.get('facilities', 0)}")
    print(f"Custom Recipes: {export_counts.get('recipes', 0)}")
    print(f"SDE Blueprints: {export_counts.get('sde_blueprints', 0)}")
    
    return export_counts

if __name__ == "__main__":
    try:
        print("=" * 60)
        print("Testing Enhanced YAML Export with SDE Blueprint Data")
        print("=" * 60)
        test_enhanced_export()
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()