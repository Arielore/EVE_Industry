"""
Recipes View for EVE Industry application.
Displays manufacturing recipes with categories tree and details view.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QTextEdit, QPushButton
)
from PySide6.QtCore import Qt


class RecipesView(QWidget):
    """View for displaying and managing recipes."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Toolbar with buttons
        toolbar = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        toolbar.addWidget(refresh_btn)
        
        add_btn = QPushButton("Add Recipe")
        add_btn.clicked.connect(self.add_recipe)
        toolbar.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Recipe")
        edit_btn.clicked.connect(self.edit_recipe)
        toolbar.addWidget(edit_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Create split view
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Left side: Recipe categories tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Recipe Categories"])
        self.tree.itemClicked.connect(self.on_recipe_selected)
        splitter.addWidget(self.tree)
        
        # Right side: Recipe details
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        splitter.addWidget(self.details)
        
        # Set splitter sizes
        splitter.setSizes([300, 700])
    
    def load_data(self):
        """Load recipe categories into the tree."""
        self.tree.clear()
        
        # BPO Recipes category
        bpo_root = QTreeWidgetItem(self.tree, ["BPO Recipes"])
        categories = ["Capital Components", "Fuel", "Modules T1", "Rigs", "Drones", "Ammunition"]
        for category in categories:
            QTreeWidgetItem(bpo_root, [category])
        
        # BPC Recipes category
        bpc_root = QTreeWidgetItem(self.tree, ["BPC Recipes"])
        sources = ["Light Missile Launcher", "Medium Shield Extender", "Warp Scrambler"]
        for source in sources:
            QTreeWidgetItem(bpc_root, [f"From: {source}"])
        
        # PI Components category
        pi_root = QTreeWidgetItem(self.tree, ["PI Components"])
        tiers = ["Tier 1", "Tier 2", "Tier 3", "Tier 4"]
        for tier in tiers:
            QTreeWidgetItem(pi_root, [tier])
        
        # Expand all top-level items
        for i in range(self.tree.topLevelItemCount()):
            self.tree.topLevelItem(i).setExpanded(True)
    
    def on_recipe_selected(self, item, column):
        """Handle recipe selection in tree."""
        if item.parent() is None:
            # Top-level category selected
            self.details.setText(f"Category: {item.text(0)}\n\nSelect a sub-category to see recipes.")
        else:
            # Sub-category selected
            category = item.parent().text(0)
            subcat = item.text(0)
            self.details.setText(
                f"Category: {category}\n"
                f"Sub-category: {subcat}\n\n"
                f"Sample recipes would be displayed here.\n"
                f"This would show name, type, material requirements,\n"
                f"and upgrade paths for recipes in this category."
            )
    
    def refresh_data(self):
        """Refresh the recipe data."""
        self.load_data()
        self.details.clear()
    
    def add_recipe(self):
        """Open dialog to add a new recipe."""
        # TODO: Implement recipe add dialog
        print("Add Recipe clicked")
    
    def edit_recipe(self):
        """Open dialog to edit the selected recipe."""
        # TODO: Implement recipe edit dialog
        print("Edit Recipe clicked")