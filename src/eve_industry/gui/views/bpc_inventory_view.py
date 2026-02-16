"""
BPC Inventory View for EVE Industry application.
Displays Blueprint Copies with run counts and color-coding for low runs.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView
)
from PySide6.QtGui import QColor


class BPCInventoryView(QWidget):
    """View for displaying and managing BPCs."""
    
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
        
        add_btn = QPushButton("Add BPC")
        add_btn.clicked.connect(self.add_bpc)
        toolbar.addWidget(add_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Name", "Source BPO", "Runs", "Location", "Category"
        ])
        
        # Configure table
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Name column stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Source BPO
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Runs
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Location
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Category
        
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_bpc)
        
        layout.addWidget(self.table)
    
    def load_data(self):
        """Load BPC data into the table."""
        # TODO: Load actual data from database
        # For now, create sample data
        self.table.setRowCount(3)
        
        sample_data = [
            ("T2 Light Missile Launcher", "Light Missile Launcher", 10, "Keberz", "module_t2"),
            ("T2 Medium Shield Extender", "Medium Shield Extender", 5, "UALX-3", "module_t2"),
            ("T2 Warp Scrambler", "Warp Scrambler", 2, "Keberz", "module_t2")
        ]
        
        for row, (name, source_bpo, runs, location, category) in enumerate(sample_data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(source_bpo))
            
            # Color code runs < 10 yellow
            runs_item = QTableWidgetItem(str(runs))
            if runs < 10:
                runs_item.setBackground(QColor(255, 255, 200))  # Light yellow
            self.table.setItem(row, 2, runs_item)
            
            self.table.setItem(row, 3, QTableWidgetItem(location))
            self.table.setItem(row, 4, QTableWidgetItem(category))
    
    def refresh_data(self):
        """Refresh the table data."""
        self.table.setRowCount(0)
        self.load_data()
    
    def add_bpc(self):
        """Open dialog to add a new BPC."""
        # TODO: Implement BPC add dialog
        print("Add BPC clicked")
    
    def edit_bpc(self, index):
        """Open dialog to edit the selected BPC."""
        row = index.row()
        name = self.table.item(row, 0).text()
        # TODO: Implement BPC edit dialog
        print(f"Edit BPC: {name}")