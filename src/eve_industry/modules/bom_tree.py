"""
Bill of Materials (BOM) Tree Analysis Module for EVE Industry.

This module provides functions to build and analyze manufacturing trees
from final products back to raw materials, supporting both custom recipes
and SDE manufacturing data.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from eve_industry.database.connection import get_db


class RecipeSource(Enum):
    """Source of a recipe."""
    CUSTOM = "custom"  # From recipes table
    SDE = "sde"  # From SDE manufacturing data
    RAW = "raw"  # No recipe (raw material)


@dataclass
class MaterialNode:
    """Node in the BOM tree representing a material."""
    name: str
    quantity: float
    is_raw: bool = False
    recipe_source: Optional[RecipeSource] = None
    activity_time: Optional[float] = None  # Manufacturing time in seconds
    materials: List['MaterialNode'] = field(default_factory=list)
    
    def __repr__(self):
        return f"MaterialNode(name={self.name}, quantity={self.quantity}, is_raw={self.is_raw}, materials={len(self.materials)})"


@dataclass
class BOMAnalysis:
    """Complete BOM analysis result."""
    root: MaterialNode
    raw_materials: Dict[str, float]  # Material name -> total quantity
    total_operations: int
    total_time: float  # Total manufacturing time in seconds
    operations_sequence: List[Dict[str, Any]]  # Ordered operations for scheduling
    
    def __repr__(self):
        return f"BOMAnalysis(root={self.root.name}, raw_materials={len(self.raw_materials)}, ops={self.total_operations}, time={self.total_time}s)"


class BOMTreeBuilder:
    """Builds BOM trees from product names."""
    
    def __init__(self):
        self.db = get_db()
        self._cache = {}  # Cache for recipe lookups
        
    def find_custom_recipe(self, item_name: str) -> Optional[Dict[str, Any]]:
        """Find custom recipe by item name."""
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                "SELECT name, recipe_type, base_item, me_level, te_level, materials_json FROM recipes WHERE name = ?",
                (item_name,)
            )
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                materials = json.loads(row[5]) if row[5] else {}
                return {
                    'name': row[0],
                    'recipe_type': row[1],
                    'base_item': row[2],
                    'me_level': row[3],
                    'te_level': row[4],
                    'materials': materials,
                    'source': RecipeSource.CUSTOM
                }
        except Exception as e:
            print(f"Error finding custom recipe for {item_name}: {e}")
        return None
    
    def find_sde_recipe(self, item_name: str) -> Optional[Dict[str, Any]]:
        """Find SDE manufacturing recipe by product name."""
        try:
            cursor = self.db.get_connection().cursor()
            # Look for manufacturing recipe (activityID = 1)
            cursor.execute("""
                SELECT DISTINCT
                    t.typeID,
                    t.name_en as blueprint_name,
                    a.time as activity_time,
                    GROUP_CONCAT(
                        CASE 
                            WHEN mt.name_en IS NOT NULL AND mt.name_en != '' AND mt.name_en != 'nan' 
                            THEN mt.name_en || ':' || m.quantity 
                            ELSE NULL 
                        END
                    ) as materials_str
                FROM types t
                LEFT JOIN industryActivityProducts p ON t.typeID = p.typeID AND p.activityID = 1
                LEFT JOIN types pt ON p.productTypeID = pt.typeID
                LEFT JOIN industryActivity a ON t.typeID = a.typeID AND a.activityID = 1
                LEFT JOIN industryActivityMaterials m ON t.typeID = m.typeID AND m.activityID = 1
                LEFT JOIN types mt ON m.materialTypeID = mt.typeID
                WHERE pt.name_en = ? AND a.time IS NOT NULL
                    AND pt.name_en IS NOT NULL AND pt.name_en != '' AND pt.name_en != 'nan'
                GROUP BY t.typeID, t.name_en, a.time
                LIMIT 1
            """, (item_name,))
            
            row = cursor.fetchone()
            cursor.close()
            
            if row and row[3]:  # Has materials string
                materials = {}
                for mat_str in row[3].split(','):
                    if mat_str and ':' in mat_str:
                        name, qty = mat_str.split(':', 1)
                        name = name.strip()
                        if name and name != 'nan':
                            try:
                                materials[name] = float(qty)
                            except ValueError:
                                print(f"Warning: Could not convert quantity '{qty}' to float for material '{name}'")
                
                if materials:  # Only return if we have valid materials
                    return {
                        'blueprint_id': row[0],
                        'blueprint_name': row[1],
                        'activity_time': row[2],
                        'materials': materials,
                        'source': RecipeSource.SDE
                    }
        except Exception as e:
            print(f"Error finding SDE recipe for {item_name}: {e}")
        return None
    
    def is_raw_material(self, item_name: str) -> bool:
        """Check if an item is a raw material (no manufacturing recipe)."""
        # First check if it's a known raw material from our list
        known_raw_materials = {
            'Tritanium', 'Pyerite', 'Mexallon', 'Isogen', 'Nocxium', 'Zydrine', 'Megacyte',
            'Morphite', 'Crystalline Carbonide', 'Titanium Carbide', 'Tungsten Carbide',
            'Fernite Carbide', 'Sylramic Fibers', 'Fullerides', 'Phenolic Composites',
            'Plasmoids', 'Oxides', 'Oxygen', 'Hydrogen', 'Helium', 'Water'
        }
        
        if item_name in known_raw_materials:
            return True
        
        # Check SDE for manufacturing blueprint
        recipe = self.find_sde_recipe(item_name)
        return recipe is None
    
    def build_tree(self, item_name: str, quantity: float = 1.0, depth: int = 0, max_depth: int = 10) -> Optional[MaterialNode]:
        """
        Build BOM tree recursively for an item.
        
        Args:
            item_name: Name of the item to build tree for
            quantity: Required quantity of the item
            depth: Current recursion depth
            max_depth: Maximum recursion depth to prevent infinite loops
            
        Returns:
            MaterialNode representing the tree, or None if item not found
        """
        if depth >= max_depth:
            print(f"Max depth reached for {item_name}")
            return None
            
        # Check cache first
        cache_key = f"{item_name}:{quantity}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Check if it's a raw material
        if self.is_raw_material(item_name):
            node = MaterialNode(
                name=item_name,
                quantity=quantity,
                is_raw=True,
                recipe_source=RecipeSource.RAW
            )
            self._cache[cache_key] = node
            return node
        
        # Try to find recipe
        recipe = self.find_custom_recipe(item_name)
        if not recipe:
            recipe = self.find_sde_recipe(item_name)
        
        if not recipe:
            # No recipe found, treat as raw material
            node = MaterialNode(
                name=item_name,
                quantity=quantity,
                is_raw=True,
                recipe_source=RecipeSource.RAW
            )
            self._cache[cache_key] = node
            return node
        
        # Build node with recipe
        node = MaterialNode(
            name=item_name,
            quantity=quantity,
            is_raw=False,
            recipe_source=recipe['source'],
            activity_time=recipe.get('activity_time')
        )
        
        # Recursively build tree for each material
        for material_name, material_qty in recipe['materials'].items():
            # Calculate required quantity considering parent quantity
            required_qty = material_qty * quantity
            child_node = self.build_tree(material_name, required_qty, depth + 1, max_depth)
            if child_node:
                node.materials.append(child_node)
        
        self._cache[cache_key] = node
        return node
    
    def analyze_bom(self, item_name: str, quantity: float = 1.0) -> Optional[BOMAnalysis]:
        """
        Analyze BOM for an item, returning raw materials, operations, and timing.
        
        Args:
            item_name: Name of the item to analyze
            quantity: Required quantity of the item
            
        Returns:
            BOMAnalysis object with complete analysis, or None if item not found
        """
        root = self.build_tree(item_name, quantity)
        if not root:
            return None
        
        # Collect raw materials
        raw_materials = {}
        total_operations = 0
        total_time = 0.0
        operations_sequence = []
        
        def traverse(node: MaterialNode, parent_quantity: float = 1.0):
            nonlocal total_operations, total_time
            
            if node.is_raw:
                # Add to raw materials
                if node.name in raw_materials:
                    raw_materials[node.name] += node.quantity
                else:
                    raw_materials[node.name] = node.quantity
            else:
                # This is a manufacturing operation
                total_operations += 1
                if node.activity_time:
                    total_time += node.activity_time * (node.quantity / parent_quantity)
                
                # Add to operations sequence
                ops_data = {
                    'operation': f"Manufacture {node.name}",
                    'item': node.name,
                    'quantity': node.quantity,
                    'time': node.activity_time,
                    'source': node.recipe_source.value if node.recipe_source else 'unknown',
                    'materials': [(m.name, m.quantity) for m in node.materials]
                }
                operations_sequence.append(ops_data)
            
            # Recurse for child materials
            for child in node.materials:
                traverse(child, node.quantity)
        
        traverse(root)
        
        # Sort operations by dependencies (simplified topological sort)
        # For now, just keep as-is (depth-first)
        
        return BOMAnalysis(
            root=root,
            raw_materials=raw_materials,
            total_operations=total_operations,
            total_time=total_time,
            operations_sequence=operations_sequence
        )
    
    def print_tree(self, node: MaterialNode, indent: int = 0):
        """Print tree structure for debugging."""
        prefix = "  " * indent
        if node.is_raw:
            print(f"{prefix}└── {node.name} x{node.quantity} (RAW)")
        else:
            source_str = node.recipe_source.value if node.recipe_source else "unknown"
            time_str = f" ({node.activity_time}s)" if node.activity_time else ""
            print(f"{prefix}└── {node.name} x{node.quantity} [{source_str}]{time_str}")
            for child in node.materials:
                self.print_tree(child, indent + 1)
    
    def get_flat_bom(self, item_name: str, quantity: float = 1.0) -> Dict[str, float]:
        """Get flat BOM (raw materials only) for an item."""
        analysis = self.analyze_bom(item_name, quantity)
        if not analysis:
            return {}
        return analysis.raw_materials


# Convenience functions
def build_bom_tree(item_name: str, quantity: float = 1.0) -> Optional[MaterialNode]:
    """Convenience function to build BOM tree."""
    builder = BOMTreeBuilder()
    return builder.build_tree(item_name, quantity)


def analyze_bom(item_name: str, quantity: float = 1.0) -> Optional[BOMAnalysis]:
    """Convenience function to analyze BOM."""
    builder = BOMTreeBuilder()
    return builder.analyze_bom(item_name, quantity)


def get_flat_bom(item_name: str, quantity: float = 1.0) -> Dict[str, float]:
    """Convenience function to get flat BOM."""
    builder = BOMTreeBuilder()
    return builder.get_flat_bom(item_name, quantity)


if __name__ == "__main__":
    # Test the module
    print("Testing BOM Tree Analysis Module")
    print("=" * 60)
    
    builder = BOMTreeBuilder()
    
    # Test with Light Missile Launcher I
    test_item = "Light Missile Launcher I"
    print(f"\nBuilding BOM tree for {test_item}:")
    tree = builder.build_tree(test_item)
    if tree:
        builder.print_tree(tree)
        
        print(f"\nAnalyzing BOM for {test_item}:")
        analysis = builder.analyze_bom(test_item)
        if analysis:
            print(f"Total raw materials: {len(analysis.raw_materials)}")
            for material, qty in analysis.raw_materials.items():
                print(f"  {material}: {qty:.1f}")
            print(f"Total operations: {analysis.total_operations}")
            print(f"Total manufacturing time: {analysis.total_time:.1f} seconds")
            print(f"Operations sequence ({len(analysis.operations_sequence)} operations):")
            for i, op in enumerate(analysis.operations_sequence, 1):
                print(f"  {i}. {op['operation']} - {op['time']}s")
    else:
        print(f"Could not build tree for {test_item}")