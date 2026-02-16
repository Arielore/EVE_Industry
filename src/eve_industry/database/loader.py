"""
Data loader for EVE Industry application.
Loads YAML data into DuckDB database.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any

from eve_industry.database.connection import get_db


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """Load and parse YAML file."""
    if not file_path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_bpos_from_yaml(file_path: Path) -> List[Dict[str, Any]]:
    """Load BPOs from YAML file."""
    data = load_yaml_file(file_path)
    return data.get('bpos', [])


def load_bpcs_from_yaml(file_path: Path) -> List[Dict[str, Any]]:
    """Load BPCs from YAML file."""
    data = load_yaml_file(file_path)
    return data.get('bpcs', [])


def load_recipes_from_yaml(file_path: Path) -> List[Dict[str, Any]]:
    """Load recipes from YAML file."""
    data = load_yaml_file(file_path)
    return data.get('recipes', [])


def load_facilities_from_yaml(file_path: Path) -> List[Dict[str, Any]]:
    """Load facilities from YAML file."""
    data = load_yaml_file(file_path)
    return data.get('facilities', [])


def insert_bpos(bpos_data: List[Dict[str, Any]]) -> int:
    """Insert BPOs into database."""
    db = get_db()
    inserted = 0
    
    for bpo in bpos_data:
        try:
            # First, try to delete any existing BPO with the same name
            db.execute("DELETE FROM bpos WHERE name = ?", (bpo.get('name'),))
            
            # Then insert the new BPO
            db.execute(
                """
                INSERT INTO bpos 
                (name, me_level, te_level, location, category, materials_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    bpo.get('name'),
                    bpo.get('me_level', 0),
                    bpo.get('te_level', 0),
                    bpo.get('location', ''),
                    bpo.get('category', ''),
                    json.dumps(bpo.get('materials', {}))
                )
            )
            inserted += 1
        except Exception as e:
            print(f"Error inserting BPO {bpo.get('name')}: {e}")
    
    return inserted


def insert_bpcs(bpcs_data: List[Dict[str, Any]]) -> int:
    """Insert BPCs into database."""
    db = get_db()
    inserted = 0
    
    for bpc in bpcs_data:
        try:
            # First, try to delete any existing BPC with the same name
            db.execute("DELETE FROM bpcs WHERE name = ?", (bpc.get('name'),))
            
            # Then insert the new BPC
            db.execute(
                """
                INSERT INTO bpcs 
                (name, source_bpo, runs_remaining, location, category, materials_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    bpc.get('name'),
                    bpc.get('source_bpo', ''),
                    bpc.get('runs_remaining', 0),
                    bpc.get('location', ''),
                    bpc.get('category', ''),
                    json.dumps(bpc.get('materials', {}))
                )
            )
            inserted += 1
        except Exception as e:
            print(f"Error inserting BPC {bpc.get('name')}: {e}")
    
    return inserted


def insert_recipes(recipes_data: List[Dict[str, Any]]) -> int:
    """Insert recipes into database."""
    db = get_db()
    inserted = 0
    
    for recipe in recipes_data:
        try:
            # First, try to delete any existing recipe with the same name
            db.execute("DELETE FROM recipes WHERE name = ?", (recipe.get('name'),))
            
            # Then insert the new recipe
            db.execute(
                """
                INSERT INTO recipes 
                (name, recipe_type, base_item, me_level, te_level, materials_json, upgrade_paths_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    recipe.get('name'),
                    recipe.get('recipe_type', ''),
                    recipe.get('base_item', ''),
                    recipe.get('me_level', 0),
                    recipe.get('te_level', 0),
                    json.dumps(recipe.get('materials', {})),
                    json.dumps(recipe.get('upgrade_paths', []))
                )
            )
            inserted += 1
        except Exception as e:
            print(f"Error inserting recipe {recipe.get('name')}: {e}")
    
    return inserted


def insert_facilities(facilities_data: List[Dict[str, Any]]) -> int:
    """Insert facilities into database."""
    db = get_db()
    inserted = 0
    
    for facility in facilities_data:
        try:
            # First, try to delete any existing facility with the same name
            db.execute("DELETE FROM facilities WHERE name = ?", (facility.get('name'),))
            
            # Then insert the new facility
            db.execute(
                """
                INSERT INTO facilities 
                (name, system, region, facility_type, owner, services_json, 
                 manufacturing_slots, research_slots, cost_index, rigs_json, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    facility.get('name'),
                    facility.get('system', ''),
                    facility.get('region', ''),
                    facility.get('facility_type', ''),
                    facility.get('owner', ''),
                    json.dumps(facility.get('services', {})),
                    facility.get('manufacturing_slots', 0),
                    facility.get('research_slots', 0),
                    facility.get('cost_index', 0.0),
                    json.dumps(facility.get('rigs', {})),
                    facility.get('notes', '')
                )
            )
            inserted += 1
        except Exception as e:
            print(f"Error inserting facility {facility.get('name')}: {e}")
    
    return inserted


def load_all_initial_data():
    """Load all initial data from YAML files into database."""
    data_dir = Path(__file__).parent.parent.parent.parent / "data" / "initial"
    
    print("Loading initial data from YAML files...")
    
    total_inserted = 0
    
    # Load BPOs
    bpos_file = data_dir / "bpos.yaml"
    if bpos_file.exists():
        bpos_data = load_bpos_from_yaml(bpos_file)
        inserted = insert_bpos(bpos_data)
        print(f"  Loaded {inserted} BPOs from {bpos_file.name}")
        total_inserted += inserted
    
    # Load BPCs
    bpcs_file = data_dir / "bpcs.yaml"
    if bpcs_file.exists():
        bpcs_data = load_bpcs_from_yaml(bpcs_file)
        inserted = insert_bpcs(bpcs_data)
        print(f"  Loaded {inserted} BPCs from {bpcs_file.name}")
        total_inserted += inserted
    
    # Load recipes
    recipes_file = data_dir / "recipes.yaml"
    if recipes_file.exists():
        recipes_data = load_recipes_from_yaml(recipes_file)
        inserted = insert_recipes(recipes_data)
        print(f"  Loaded {inserted} recipes from {recipes_file.name}")
        total_inserted += inserted
    
    # Load facilities
    facilities_file = data_dir / "facilities.yaml"
    if facilities_file.exists():
        facilities_data = load_facilities_from_yaml(facilities_file)
        inserted = insert_facilities(facilities_data)
        print(f"  Loaded {inserted} facilities from {facilities_file.name}")
        total_inserted += inserted
    
    print(f"Total records loaded: {total_inserted}")
    return total_inserted


def get_bpos_from_db() -> List[Dict[str, Any]]:
    """Get all BPOs from database."""
    db = get_db()
    
    try:
        # Use connection directly to avoid cursor closure issues
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, me_level, te_level, location, category 
            FROM bpos 
            ORDER BY name
        """)
        
        bpos = []
        rows = cursor.fetchall()
        cursor.close()
        
        for row in rows:
            bpos.append({
                'name': row[0],
                'me_level': row[1],
                'te_level': row[2],
                'location': row[3],
                'category': row[4]
            })
        return bpos
    except Exception as e:
        print(f"Error getting BPOs from database: {e}")
        return []


def clear_all_data():
    """Clear all data from tables (for testing)."""
    db = get_db()
    tables = ['bpos', 'bpcs', 'recipes', 'facilities']
    
    for table in tables:
        try:
            db.execute(f"DELETE FROM {table}")
            print(f"Cleared {table} table")
        except Exception as e:
            print(f"Error clearing {table}: {e}")


if __name__ == "__main__":
    # When run directly, load initial data
    from eve_industry.database.schema import initialize_schema
    
    print("Initializing database schema...")
    initialize_schema()
    
    print("Loading initial data...")
    load_all_initial_data()