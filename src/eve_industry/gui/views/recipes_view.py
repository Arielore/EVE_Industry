"""
Recipes View for EVE Industry application.
Displays manufacturing recipes from SDE data with categories tree and details view.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel
)
from PySide6.QtCore import Qt

from eve_industry.database.connection import get_db


class RecipesView(QWidget):
    """View for displaying and managing recipes from SDE data."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sde_data()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Toolbar with buttons
        toolbar = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        toolbar.addWidget(refresh_btn)
        
        add_btn = QPushButton("Add Custom Recipe")
        add_btn.clicked.connect(self.add_recipe)
        toolbar.addWidget(add_btn)
        
        toolbar.addStretch()
        
        # SDE status label
        self.status_label = QLabel("Loading SDE data...")
        toolbar.addWidget(self.status_label)
        
        layout.addLayout(toolbar)
        
        # Create split view
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Left side: Recipe categories tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Blueprint Categories"])
        self.tree.itemClicked.connect(self.on_recipe_selected)
        splitter.addWidget(self.tree)
        
        # Right side: Recipe details panel
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        
        # Recipe header
        self.recipe_header = QLabel("Select a blueprint to view details")
        self.recipe_header.setStyleSheet("font-weight: bold; font-size: 14px;")
        details_layout.addWidget(self.recipe_header)
        
        # Basic info table
        self.info_table = QTableWidget()
        self.info_table.setColumnCount(2)
        self.info_table.setHorizontalHeaderLabels(["Property", "Value"])
        self.info_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.info_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.info_table.setMaximumHeight(150)
        details_layout.addWidget(self.info_table)
        
        # Materials table
        materials_label = QLabel("Material Requirements")
        materials_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        details_layout.addWidget(materials_label)
        
        self.materials_table = QTableWidget()
        self.materials_table.setColumnCount(3)
        self.materials_table.setHorizontalHeaderLabels(["Material", "Quantity", "TypeID"])
        self.materials_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.materials_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.materials_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        details_layout.addWidget(self.materials_table)
        
        # Products table
        products_label = QLabel("Products")
        products_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        details_layout.addWidget(products_label)
        
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(3)
        self.products_table.setHorizontalHeaderLabels(["Product", "Quantity", "Probability"])
        self.products_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.products_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.products_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        details_layout.addWidget(self.products_table)
        
        splitter.addWidget(details_widget)
        
        # Set splitter sizes
        splitter.setSizes([300, 700])
    
    def set_tree_item_data(self, item: QTreeWidgetItem, **kwargs):
        """Set data on tree item using Qt roles."""
        for key, value in kwargs.items():
            if key == "type_id":
                item.setData(0, Qt.UserRole + 1, value)
            elif key == "group_id":
                item.setData(0, Qt.UserRole + 2, value)
            elif key == "category_id":
                item.setData(0, Qt.UserRole + 3, value)
            elif key == "time":
                item.setData(0, Qt.UserRole + 4, value)
    
    def get_tree_item_data(self, item: QTreeWidgetItem, key: str):
        """Get data from tree item."""
        if key == "type_id":
            return item.data(0, Qt.UserRole + 1)
        elif key == "group_id":
            return item.data(0, Qt.UserRole + 2)
        elif key == "category_id":
            return item.data(0, Qt.UserRole + 3)
        elif key == "time":
            return item.data(0, Qt.UserRole + 4)
        return None
    
    def load_sde_data(self):
        """Load SDE blueprint data into the tree."""
        try:
            db = get_db()
            
            # Check if SDE views exist
            result = db.execute_df("""
                SELECT COUNT(*) as count 
                FROM information_schema.tables 
                WHERE table_name = 'types' AND table_schema = 'main'
            """)
            
            if len(result) == 0 or result['count'].iloc[0] == 0:
                self.status_label.setText("SDE data not loaded - use SDE tab to import")
                self.load_fallback_data()
                return
            
            # Get blueprint groups with manufacturing activities
            query = """
            SELECT DISTINCT 
                g.groupID,
                g.name_en as group_name,
                COUNT(DISTINCT t.typeID) as blueprint_count
            FROM groups g
            JOIN types t ON g.groupID = t.groupID
            JOIN industryActivity a ON t.typeID = a.typeID AND a.activityID = 1
            WHERE g.published = true
            AND t.published = true
            AND a.activityID = 1
            AND g.name_en LIKE '%Blueprint%'
            GROUP BY g.groupID, g.name_en
            HAVING COUNT(DISTINCT t.typeID) > 0
            ORDER BY g.name_en
            """
            
            groups = db.execute_df(query)
            
            self.tree.clear()
            
            if len(groups) == 0:
                self.status_label.setText("No blueprint data found")
                self.load_fallback_data()
                return
            
            # Create tree items for each blueprint group
            for _, group in groups.iterrows():
                group_item = QTreeWidgetItem(self.tree, [f"{group['group_name']} ({group['blueprint_count']})"])
                self.set_tree_item_data(group_item, group_id=group['groupID'])
                
                # Get blueprints in this group
                blueprints_query = """
                SELECT 
                    t.typeID,
                    t.name_en as blueprint_name,
                    a.time
                FROM types t
                JOIN industryActivity a ON t.typeID = a.typeID
                WHERE t.groupID = ?
                AND a.activityID = 1
                AND t.published = true
                ORDER BY t.name_en
                LIMIT 100  -- Limit per group for performance
                """
                
                blueprints = db.execute_df(blueprints_query, (group['groupID'],))
                
                for _, bp in blueprints.iterrows():
                    bp_item = QTreeWidgetItem(group_item, [bp['blueprint_name']])
                    self.set_tree_item_data(bp_item, type_id=bp['typeID'], time=bp['time'])
            
            # Expand all top-level items
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                if item:
                    item.setExpanded(True)
            
            self.status_label.setText(f"Loaded {len(groups)} blueprint groups")
            
        except Exception as e:
            print(f"Error loading SDE data: {e}")
            self.status_label.setText(f"Error: {str(e)[:50]}...")
            self.load_fallback_data()
    
    def load_fallback_data(self):
        """Load fallback data if SDE is not available."""
        self.tree.clear()
        
        # Fallback categories
        categories = [
            "Capital Components",
            "Fuel Blocks", 
            "Modules",
            "Rigs",
            "Drones",
            "Ammunition",
            "Ships"
        ]
        
        for category in categories:
            item = QTreeWidgetItem(self.tree, [category])
            # Add some sample blueprints
            if category == "Ships":
                bp_item = QTreeWidgetItem(item, ["Rifter Blueprint"])
                self.set_tree_item_data(bp_item, type_id=691, time=6000)
                bp_item = QTreeWidgetItem(item, ["Merlin Blueprint"])
                self.set_tree_item_data(bp_item, type_id=603, time=6000)
            elif category == "Modules":
                bp_item = QTreeWidgetItem(item, ["Medium Shield Extender Blueprint"])
                self.set_tree_item_data(bp_item, type_id=309, time=3000)
                bp_item = QTreeWidgetItem(item, ["Warp Scrambler Blueprint"])
                self.set_tree_item_data(bp_item, type_id=324, time=3000)
        
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item:
                item.setExpanded(True)
    
    def on_recipe_selected(self, item, column):
        """Handle recipe selection in tree."""
        type_id = self.get_tree_item_data(item, "type_id")
        group_id = self.get_tree_item_data(item, "group_id")
        category_id = self.get_tree_item_data(item, "category_id")
        
        if type_id is not None:
            # Blueprint selected - load detailed info
            self.load_blueprint_details(type_id)
        elif group_id is not None:
            # Group selected - show summary
            self.show_group_summary(group_id)
        elif category_id is not None:
            # Category selected - show summary
            self.show_category_summary(category_id)
        else:
            # Fallback item selected
            self.show_fallback_details(item.text(0))
    
    def load_blueprint_details(self, type_id: int):
        """Load detailed blueprint information."""
        try:
            db = get_db()
            
            # Get blueprint basic info
            info_query = """
            SELECT 
                t.typeID,
                t.name_en as blueprint_name,
                g.name_en as group_name,
                c.name_en as category_name,
                a.time,
                t.volume,
                t.mass,
                t.description_en
            FROM types t
            LEFT JOIN groups g ON t.groupID = g.groupID
            LEFT JOIN categories c ON g.categoryID = c.categoryID
            LEFT JOIN industryActivity a ON t.typeID = a.typeID AND a.activityID = 1
            WHERE t.typeID = ?
            """
            
            info_result = db.execute_df(info_query, (type_id,))
            
            if len(info_result) == 0:
                self.show_error("Blueprint not found")
                return
            
            info = info_result.iloc[0]
            
            # Update header
            self.recipe_header.setText(f"Blueprint: {info['blueprint_name']}")
            
            # Update info table
            self.info_table.setRowCount(6)
            properties = [
                ("TypeID", str(info['typeID'])),
                ("Category", str(info['category_name'])),
                ("Group", str(info['group_name'])),
                ("Manufacturing Time", f"{info['time']} seconds"),
                ("Volume", f"{info.get('volume', 'N/A')} m³"),
                ("Mass", f"{info.get('mass', 'N/A')} kg")
            ]
            
            for row, (prop, value) in enumerate(properties):
                self.info_table.setItem(row, 0, QTableWidgetItem(prop))
                self.info_table.setItem(row, 1, QTableWidgetItem(value))
            
            # Load materials
            materials_query = """
            SELECT 
                m.materialTypeID,
                m.quantity,
                mt.name_en as material_name
            FROM industryActivityMaterials m
            LEFT JOIN types mt ON m.materialTypeID = mt.typeID
            WHERE m.typeID = ? AND m.activityID = 1
            ORDER BY m.quantity DESC
            """
            
            materials = db.execute_df(materials_query, (type_id,))
            self.materials_table.setRowCount(len(materials))
            
            for row, (_, material) in enumerate(materials.iterrows()):
                self.materials_table.setItem(row, 0, QTableWidgetItem(str(material['material_name'])))
                self.materials_table.setItem(row, 1, QTableWidgetItem(str(material['quantity'])))
                self.materials_table.setItem(row, 2, QTableWidgetItem(str(material['materialTypeID'])))
            
            # Load products
            products_query = """
            SELECT 
                p.productTypeID,
                p.quantity,
                p.probability,
                pt.name_en as product_name
            FROM industryActivityProducts p
            LEFT JOIN types pt ON p.productTypeID = pt.typeID
            WHERE p.typeID = ? AND p.activityID = 1
            """
            
            products = db.execute_df(products_query, (type_id,))
            self.products_table.setRowCount(len(products))
            
            for row, (_, product) in enumerate(products.iterrows()):
                self.products_table.setItem(row, 0, QTableWidgetItem(str(product['product_name'])))
                self.products_table.setItem(row, 1, QTableWidgetItem(str(product['quantity'])))
                self.products_table.setItem(row, 2, QTableWidgetItem(str(product['probability'])))
            
        except Exception as e:
            print(f"Error loading blueprint details: {e}")
            self.show_error(f"Error loading details: {str(e)[:50]}")
    
    def show_group_summary(self, group_id: int):
        """Show summary for a blueprint group."""
        try:
            db = get_db()
            
            query = """
            SELECT 
                g.name_en as group_name,
                COUNT(DISTINCT t.typeID) as blueprint_count,
                AVG(a.time) as avg_time
            FROM groups g
            LEFT JOIN types t ON g.groupID = t.groupID
            LEFT JOIN industryActivity a ON t.typeID = a.typeID AND a.activityID = 1
            WHERE g.groupID = ?
            GROUP BY g.name_en
            """
            
            result = db.execute_df(query, (group_id,))
            
            if len(result) > 0:
                group = result.iloc[0]
                self.recipe_header.setText(f"Group: {group['group_name']}")
                
                # Update info table
                self.info_table.setRowCount(3)
                self.info_table.setItem(0, 0, QTableWidgetItem("Group Name"))
                self.info_table.setItem(0, 1, QTableWidgetItem(str(group['group_name'])))
                self.info_table.setItem(1, 0, QTableWidgetItem("Blueprint Count"))
                self.info_table.setItem(1, 1, QTableWidgetItem(str(group['blueprint_count'])))
                self.info_table.setItem(2, 0, QTableWidgetItem("Average Time"))
                self.info_table.setItem(2, 1, QTableWidgetItem(f"{group['avg_time']:.0f} seconds"))
            
            # Clear materials and products
            self.materials_table.setRowCount(0)
            self.products_table.setRowCount(0)
            
        except Exception as e:
            print(f"Error showing group summary: {e}")
            self.show_error(f"Error: {str(e)[:50]}")
    
    def show_category_summary(self, category_id: int):
        """Show summary for a category."""
        try:
            db = get_db()
            
            query = """
            SELECT 
                c.name_en as category_name,
                COUNT(DISTINCT g.groupID) as group_count,
                COUNT(DISTINCT t.typeID) as blueprint_count
            FROM categories c
            LEFT JOIN groups g ON c.categoryID = g.categoryID
            LEFT JOIN types t ON g.groupID = t.groupID
            LEFT JOIN industryActivity a ON t.typeID = a.typeID AND a.activityID = 1
            WHERE c.categoryID = ?
            GROUP BY c.name_en
            """
            
            result = db.execute_df(query, (category_id,))
            
            if len(result) > 0:
                category = result.iloc[0]
                self.recipe_header.setText(f"Category: {category['category_name']}")
                
                # Update info table
                self.info_table.setRowCount(3)
                self.info_table.setItem(0, 0, QTableWidgetItem("Category Name"))
                self.info_table.setItem(0, 1, QTableWidgetItem(str(category['category_name'])))
                self.info_table.setItem(1, 0, QTableWidgetItem("Group Count"))
                self.info_table.setItem(1, 1, QTableWidgetItem(str(category['group_count'])))
                self.info_table.setItem(2, 0, QTableWidgetItem("Blueprint Count"))
                self.info_table.setItem(2, 1, QTableWidgetItem(str(category['blueprint_count'])))
            
            # Clear materials and products
            self.materials_table.setRowCount(0)
            self.products_table.setRowCount(0)
            
        except Exception as e:
            print(f"Error showing category summary: {e}")
            self.show_error(f"Error: {str(e)[:50]}")
    
    def show_fallback_details(self, item_text: str):
        """Show details for fallback items."""
        self.recipe_header.setText(f"Item: {item_text}")
        
        # Update info table with sample data
        self.info_table.setRowCount(3)
        self.info_table.setItem(0, 0, QTableWidgetItem("Item Name"))
        self.info_table.setItem(0, 1, QTableWidgetItem(item_text))
        self.info_table.setItem(1, 0, QTableWidgetItem("Status"))
        self.info_table.setItem(1, 1, QTableWidgetItem("Sample Data - SDE not loaded"))
        self.info_table.setItem(2, 0, QTableWidgetItem("Action"))
        self.info_table.setItem(2, 1, QTableWidgetItem("Use SDE tab to import data"))
        
        # Clear materials and products
        self.materials_table.setRowCount(0)
        self.products_table.setRowCount(0)
    
    def show_error(self, message: str):
        """Show error message."""
        self.recipe_header.setText("Error")
        self.info_table.setRowCount(1)
        self.info_table.setItem(0, 0, QTableWidgetItem("Error"))
        self.info_table.setItem(0, 1, QTableWidgetItem(message))
        self.materials_table.setRowCount(0)
        self.products_table.setRowCount(0)
    
    def refresh_data(self):
        """Refresh the recipe data."""
        self.load_sde_data()
        self.clear_details()
    
    def clear_details(self):
        """Clear the details panels."""
        self.recipe_header.setText("Select a blueprint to view details")
        self.info_table.setRowCount(0)
        self.materials_table.setRowCount(0)
        self.products_table.setRowCount(0)
    
    def add_recipe(self):
        """Open dialog to add a new custom recipe."""
        # TODO: Implement custom recipe add dialog
        print("Add Custom Recipe clicked")
    
    def edit_recipe(self):
        """Open dialog to edit the selected recipe."""
        # TODO: Implement recipe edit dialog
        print("Edit Recipe clicked")