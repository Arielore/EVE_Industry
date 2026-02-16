"""
BPO List View for EVE Industry application.
Displays Blueprint Originals in a table with filtering and editing capabilities.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView
)
from PySide6.QtCore import Qt

from eve_industry.database.loader import get_bpos_from_db


class BPOListView(QWidget):
    """View for displaying and managing BPOs."""
    
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
        
        add_btn = QPushButton("Add BPO")
        add_btn.clicked.connect(self.add_bpo)
        toolbar.addWidget(add_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Name", "ME", "TE", "Location", "Category"
        ])
        
        # Configure table
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Name column stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # ME
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # TE
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Location
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Category
        
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_bpo)
        
        layout.addWidget(self.table)
    
    def load_data(self):
        """Load BPO data into the table."""
        try:
            # Get BPOs from database
            bpos = get_bpos_from_db()
            
            # Set table row count
            self.table.setRowCount(len(bpos))
            
            # Populate table with data
            for row, bpo in enumerate(bpos):
                self.table.setItem(row, 0, QTableWidgetItem(bpo['name']))
                self.table.setItem(row, 1, QTableWidgetItem(str(bpo['me_level'])))
                self.table.setItem(row, 2, QTableWidgetItem(str(bpo['te_level'])))
                self.table.setItem(row, 3, QTableWidgetItem(bpo['location']))
                self.table.setItem(row, 4, QTableWidgetItem(bpo['category']))
                
            print(f"Loaded {len(bpos)} BPOs into table")
            
        except Exception as e:
            print(f"Error loading BPO data: {e}")
            # Fall back to sample data if database is empty
            self.table.setRowCount(3)
            sample_data = [
                ("Capital Capacitor Battery", 9, 18, "Keberz", "capital_components"),
                ("Oxygen Fuel Block", 10, 10, "UALX-3", "fuel"),
                ("XL Cruise Missile Launcher", 8, 0, "Keberz", "capital_components")
            ]
            
            for row, (name, me, te, location, category) in enumerate(sample_data):
                self.table.setItem(row, 0, QTableWidgetItem(name))
                self.table.setItem(row, 1, QTableWidgetItem(str(me)))
                self.table.setItem(row, 2, QTableWidgetItem(str(te)))
                self.table.setItem(row, 3, QTableWidgetItem(location))
                self.table.setItem(row, 4, QTableWidgetItem(category))
            print("Using sample data (database may be empty)")
    
    def refresh_data(self):
        """Refresh the table data."""
        self.table.setRowCount(0)
        self.load_data()
    
    def add_bpo(self):
        """Open dialog to add a new BPO."""
        # TODO: Implement BPO add dialog
        print("Add BPO clicked")
    
    def edit_bpo(self, index):
        """Open dialog to edit the selected BPO."""
        row = index.row()
        item = self.table.item(row, 0)
        if item:
            name = item.text()
            # TODO: Implement BPO edit dialog
            print(f"Edit BPO: {name}")
        else:
            print("No BPO selected or item is empty")
