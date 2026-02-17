"""
YAML handler for EVE Industry application.
Provides import and export functionality for all data tables.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import datetime

from eve_industry.database.connection import get_db


def import_all_from_yaml(data_dir: Path) -> Dict[str, int]:
    """
    Import all data from YAML files in the specified directory.
    
    Args:
        data_dir: Path to directory containing YAML files
    
    Returns:
        Dictionary with counts of imported records by table
    """
    import_counts = {}
    
    # Import BPOs
    bpos_file = data_dir / "bpos.yaml"
    if bpos_file.exists():
        import_counts['bpos'] = _import_bpos_from_yaml(bpos_file)
    
    # Import BPCs
    bpcs_file = data_dir / "bpcs.yaml"
    if bpcs_file.exists():
        import_counts['bpcs'] = _import_bpc_from_yaml(bpcs_file)
    
    # Import facilities
    facilities_file = data_dir / "facilities.yaml"
    if facilities_file.exists():
        import_counts['facilities'] = _import_facilities_from_yaml(facilities_file)
    
    # Import recipes (if file exists)
    recipes_file = data_dir / "recipes.yaml"
    if recipes_file.exists():
        import_counts['recipes'] = _import_recipes_from_yaml(recipes_file)
    
    return import_counts


def export_all_to_yaml(output_dir: Path) -> Dict[str, int]:
    """
    Export all data from database to YAML files in the specified directory.
    Includes custom data (BPOs, BPCs, facilities) AND SDE blueprint data.
    Recipes are not exported as they currently contain only sample data.
    
    Args:
        output_dir: Path to directory where YAML files will be saved
    
    Returns:
        Dictionary with counts of exported records by table
    """
    export_counts = {}
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Export BPOs
    export_counts['bpos'] = _export_bpos_to_yaml(output_dir / "bpos.yaml")
    
    # Export BPCs
    export_counts['bpcs'] = _export_bpcs_to_yaml(output_dir / "bpcs.yaml")
    
    # Export facilities
    export_counts['facilities'] = _export_facilities_to_yaml(output_dir / "facilities.yaml")
    
    # Export SDE blueprints (if SDE is loaded)
    export_counts['sde_blueprints'] = _export_sde_blueprints_to_yaml(output_dir / "sde_blueprints.yaml")
    
    # Note: Recipes are not exported as they currently contain only sample data
    export_counts['recipes'] = 0
    
    return export_counts


def _load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """Load and parse YAML file."""
    if not file_path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def _import_bpos_from_yaml(file_path: Path) -> int:
    """Import BPOs from YAML file."""
    data = _load_yaml_file(file_path)
    bpos_data = data.get('bpos', [])
    
    db = get_db()
    inserted = 0
    
    for bpo in bpos_data:
        try:
            # Delete existing BPO with same name
            db.execute("DELETE FROM bpos WHERE name = ?", (bpo.get('name'),))
            
            # Insert new BPO
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
            print(f"Error importing BPO {bpo.get('name')}: {e}")
    
    return inserted


def _import_bpc_from_yaml(file_path: Path) -> int:
    """Import BPCs from YAML file."""
    data = _load_yaml_file(file_path)
    bpcs_data = data.get('bpcs', [])
    
    db = get_db()
    inserted = 0
    
    for bpc in bpcs_data:
        try:
            # Delete existing BPC with same name
            db.execute("DELETE FROM bpcs WHERE name = ?", (bpc.get('name'),))
            
            # Insert new BPC
            db.execute(
                """
                INSERT INTO bpcs 
                (name, source_bpo, me_level, te_level, runs_remaining, location, category, materials_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    bpc.get('name'),
                    bpc.get('source_bpo', ''),
                    bpc.get('me_level', 0),
                    bpc.get('te_level', 0),
                    bpc.get('runs_remaining', 0),
                    bpc.get('location', ''),
                    bpc.get('category', ''),
                    json.dumps(bpc.get('materials', {}))
                )
            )
            inserted += 1
        except Exception as e:
            print(f"Error importing BPC {bpc.get('name')}: {e}")
    
    return inserted


def _import_facilities_from_yaml(file_path: Path) -> int:
    """Import facilities from YAML file."""
    data = _load_yaml_file(file_path)
    facilities_data = data.get('facilities', [])
    
    db = get_db()
    inserted = 0
    
    for facility in facilities_data:
        try:
            # Delete existing facility with same name
            db.execute("DELETE FROM facilities WHERE name = ?", (facility.get('name'),))
            
            # Insert new facility
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
                    json.dumps(facility.get('services', [])),
                    facility.get('manufacturing_slots', 0),
                    facility.get('research_slots', 0),
                    facility.get('cost_index', 0.0),
                    json.dumps(facility.get('rigs', [])),
                    facility.get('notes', '')
                )
            )
            inserted += 1
        except Exception as e:
            print(f"Error importing facility {facility.get('name')}: {e}")
    
    return inserted


def _import_recipes_from_yaml(file_path: Path) -> int:
    """Import recipes from YAML file."""
    data = _load_yaml_file(file_path)
    recipes_data = data.get('recipes', [])
    
    db = get_db()
    inserted = 0
    
    for recipe in recipes_data:
        try:
            # Delete existing recipe with same name
            db.execute("DELETE FROM recipes WHERE name = ?", (recipe.get('name'),))
            
            # Insert new recipe
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
            print(f"Error importing recipe {recipe.get('name')}: {e}")
    
    return inserted


def _export_bpos_to_yaml(output_file: Path) -> int:
    """Export all BPOs to YAML file."""
    db = get_db()
    
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT name, me_level, te_level, location, category, materials_json
                FROM bpos 
                ORDER BY name
            """)
            
            bpos = []
            rows = cursor.fetchall()
            
            for row in rows:
                bpo = {
                    'name': row[0],
                    'me_level': row[1],
                    'te_level': row[2],
                    'location': row[3],
                    'category': row[4]
                }
                
                # Parse materials JSON if present
                materials_json = row[5]
                if materials_json and materials_json != 'null':
                    try:
                        bpo['materials'] = json.loads(materials_json)
                    except:
                        bpo['materials'] = {}
                else:
                    bpo['materials'] = {}
                
                bpos.append(bpo)
        
        # Write to YAML
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump({'bpos': bpos}, f, default_flow_style=False, sort_keys=False)
        
        return len(bpos)
    except Exception as e:
        print(f"Error exporting BPOs: {e}")
        return 0


def _export_bpcs_to_yaml(output_file: Path) -> int:
    """Export all BPCs to YAML file."""
    db = get_db()
    
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT name, source_bpo, me_level, te_level, runs_remaining, location, category, materials_json
                FROM bpcs 
                ORDER BY name
            """)
            
            bpcs = []
            rows = cursor.fetchall()
            
            for row in rows:
                bpc = {
                    'name': row[0],
                    'source_bpo': row[1],
                    'me_level': row[2],
                    'te_level': row[3],
                    'runs_remaining': row[4],
                    'location': row[5],
                    'category': row[6]
                }
                
                # Parse materials JSON if present
                materials_json = row[7]
                if materials_json and materials_json != 'null':
                    try:
                        bpc['materials'] = json.loads(materials_json)
                    except:
                        bpc['materials'] = {}
                else:
                    bpc['materials'] = {}
                
                bpcs.append(bpc)
        
        # Write to YAML
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump({'bpcs': bpcs}, f, default_flow_style=False, sort_keys=False)
        
        return len(bpcs)
    except Exception as e:
        print(f"Error exporting BPCs: {e}")
        return 0


def _export_facilities_to_yaml(output_file: Path) -> int:
    """Export all facilities to YAML file."""
    db = get_db()
    
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT name, system, region, facility_type, owner, services_json,
                       manufacturing_slots, research_slots, cost_index, rigs_json, notes
                FROM facilities 
                ORDER BY name
            """)
            
            facilities = []
            rows = cursor.fetchall()
            
            for row in rows:
                facility = {
                    'name': row[0],
                    'system': row[1],
                    'region': row[2],
                    'facility_type': row[3],
                    'owner': row[4],
                    'manufacturing_slots': row[6],
                    'research_slots': row[7],
                    'cost_index': float(row[8]) if row[8] else 0.0,
                    'notes': row[10]
                }
                
                # Parse services JSON if present
                services_json = row[5]
                if services_json and services_json != 'null':
                    try:
                        facility['services'] = json.loads(services_json)
                    except:
                        facility['services'] = []
                else:
                    facility['services'] = []
                
                # Parse rigs JSON if present
                rigs_json = row[9]
                if rigs_json and rigs_json != 'null':
                    try:
                        facility['rigs'] = json.loads(rigs_json)
                    except:
                        facility['rigs'] = []
                else:
                    facility['rigs'] = []
                
                facilities.append(facility)
        
        # Write to YAML
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump({'facilities': facilities}, f, default_flow_style=False, sort_keys=False)
        
        return len(facilities)
    except Exception as e:
        print(f"Error exporting facilities: {e}")
        return 0


def _export_recipes_to_yaml(output_file: Path) -> int:
    """Export all recipes to YAML file."""
    db = get_db()
    
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT name, recipe_type, base_item, me_level, te_level, materials_json, upgrade_paths_json
                FROM recipes 
                ORDER BY name
            """)
            
            recipes = []
            rows = cursor.fetchall()
            
            for row in rows:
                recipe = {
                    'name': row[0],
                    'recipe_type': row[1],
                    'base_item': row[2],
                    'me_level': row[3],
                    'te_level': row[4]
                }
                
                # Parse materials JSON if present
                materials_json = row[5]
                if materials_json and materials_json != 'null':
                    try:
                        recipe['materials'] = json.loads(materials_json)
                    except:
                        recipe['materials'] = {}
                else:
                    recipe['materials'] = {}
                
                # Parse upgrade paths JSON if present
                upgrade_paths_json = row[6]
                if upgrade_paths_json and upgrade_paths_json != 'null':
                    try:
                        recipe['upgrade_paths'] = json.loads(upgrade_paths_json)
                    except:
                        recipe['upgrade_paths'] = []
                else:
                    recipe['upgrade_paths'] = []
                
                recipes.append(recipe)
        
        # Write to YAML
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump({'recipes': recipes}, f, default_flow_style=False, sort_keys=False)
        
        return len(recipes)
    except Exception as e:
        print(f"Error exporting recipes: {e}")
        return 0


def _export_sde_blueprints_to_yaml(output_file: Path) -> int:
    """Export SDE blueprint data to YAML file."""
    db = get_db()
    
    try:
        conn = db.get_connection()
        
        # First check if SDE views exist
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM information_schema.tables 
            WHERE table_name = 'types' AND table_schema = 'main'
        """)
        result = cursor.fetchone()
        cursor.close()
        
        if not result or result[0] == 0:
            # SDE views don't exist
            print("SDE views not found - skipping SDE blueprint export")
            return 0
        
        # Get blueprint data with manufacturing activities
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT 
                t.typeID,
                t.name_en as blueprint_name,
                t.published,
                t.volume,
                t.mass,
                g.name_en as group_name,
                c.name_en as category_name,
                a.time as manufacturing_time
            FROM types t
            LEFT JOIN groups g ON t.groupID = g.groupID
            LEFT JOIN categories c ON g.categoryID = c.categoryID
            LEFT JOIN industryActivity a ON t.typeID = a.typeID AND a.activityID = 1
            WHERE a.activityID = 1  -- Manufacturing only
            AND t.published = true
            ORDER BY t.name_en
            LIMIT 1000  -- Limit for performance
        """)
        
        blueprints = []
        rows = cursor.fetchall()
        cursor.close()
        
        for row in rows:
            bp = {
                'type_id': row[0],
                'name': row[1],
                'published': bool(row[2]),
                'volume': row[3],
                'mass': row[4],
                'group': row[5],
                'category': row[6],
                'manufacturing_time': row[7]
            }
            
            # Get materials for this blueprint
            cursor2 = conn.cursor()
            cursor2.execute("""
                SELECT 
                    m.materialTypeID,
                    m.quantity,
                    mt.name_en as material_name
                FROM industryActivityMaterials m
                LEFT JOIN types mt ON m.materialTypeID = mt.typeID
                WHERE m.typeID = ? AND m.activityID = 1
                ORDER BY m.quantity DESC
            """, (row[0],))
            
            materials = []
            material_rows = cursor2.fetchall()
            cursor2.close()
            
            for mat_row in material_rows:
                materials.append({
                    'type_id': mat_row[0],
                    'quantity': mat_row[1],
                    'name': mat_row[2] or f"TypeID {mat_row[0]}"
                })
            
            if materials:
                bp['materials'] = materials
            
            # Get products for this blueprint
            cursor2 = conn.cursor()
            cursor2.execute("""
                SELECT 
                    p.productTypeID,
                    p.quantity,
                    p.probability,
                    pt.name_en as product_name
                FROM industryActivityProducts p
                LEFT JOIN types pt ON p.productTypeID = pt.typeID
                WHERE p.typeID = ? AND p.activityID = 1
            """, (row[0],))
            
            products = []
            product_rows = cursor2.fetchall()
            cursor2.close()
            
            for prod_row in product_rows:
                products.append({
                    'type_id': prod_row[0],
                    'quantity': prod_row[1],
                    'probability': prod_row[2],
                    'name': prod_row[3] or f"TypeID {prod_row[0]}"
                })
            
            if products:
                bp['products'] = products
            
            blueprints.append(bp)
        
        # Write to YAML
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump({'sde_blueprints': blueprints}, f, default_flow_style=False, sort_keys=False)
        
        print(f"Exported {len(blueprints)} SDE blueprints to {output_file}")
        return len(blueprints)
        
    except Exception as e:
        print(f"Error exporting SDE blueprints: {e}")
        # Don't fail the whole export if SDE export fails
        return 0


def get_import_export_stats() -> Dict[str, Any]:
    """
    Get statistics about current data in database.
    
    Returns:
        Dictionary with table counts and last export info
    """
    db = get_db()
    stats = {}
    
    tables = ['bpos', 'bpcs', 'recipes', 'facilities']
    
    for table in tables:
        try:
            with db.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                result = cursor.fetchone()
                if result and result[0] is not None:
                    stats[f"{table}_count"] = result[0]
                else:
                    stats[f"{table}_count"] = 0
        except Exception:
            stats[f"{table}_count"] = 0
    
    return stats
