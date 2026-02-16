"""
Facilities View for EVE Industry application.
Displays manufacturing facilities with services, slots, and cost indices.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView
)
from PySide6.QtCore import Qt


class FacilitiesView(QWidget):
    """View for displaying and managing facilities."""
    
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
        
        add_btn = QPushButton("Add Facility")
        add_btn.clicked.connect(self.add_facility)
        toolbar.addWidget(add_btn)
        
        import_btn = QPushButton("Import YAML")
        import_btn.clicked.connect(self.import_yaml)
        toolbar.addWidget(import_btn)
        
        export_btn = QPushButton("Export YAML")
        export_btn.clicked.connect(self.export_yaml)
        toolbar.addWidget(export_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Name", "System", "Type", "Owner", "Mfg Slots", "Research Slots", "Cost Index"
        ])
        
        # Configure table
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Name column stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # System
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Type
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Owner
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Mfg Slots
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Research Slots
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Cost Index
        
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_facility)
        
        layout.addWidget(self.table)
    
    def load_data(self):
        """Load facility data into the table."""
        # TODO: Load actual data from database
        # For now, create sample data
        self.table.setRowCount(3)
        
        sample_data = [
            ("Empire Reforged", "Keberz", "Azbel", "Brave Empire", 10, 8, 0.035),
            ("Starforge of Bravery", "UALX-3", "Sotiyo", "Brave Collective", 15, 10, 0.0659),
            ("The Science Lounge", "UALX-3", "Sotiyo", "Brave Collective", 0, 20, 0.0659)
        ]
        
        for row, (name, system, ftype, owner, mfg_slots, research_slots, cost_index) in enumerate(sample_data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(system))
            self.table.setItem(row, 2, QTableWidgetItem(ftype))
            self.table.setItem(row, 3, QTableWidgetItem(owner))
            self.table.setItem(row, 4, QTableWidgetItem(str(mfg_slots)))
            self.table.setItem(row, 5, QTableWidgetItem(str(research_slots)))
            self.table.setItem(row, 6, QTableWidgetItem(f"{cost_index:.4f}"))
    
    def refresh_data(self):
        """Refresh the table data."""
        self.table.setRowCount(0)
        self.load_data()
    
    def add_facility(self):
        """Open dialog to add a new facility."""
        # TODO: Implement facility add dialog
        print("Add Facility clicked")
    
    def import_yaml(self):
        """Import facilities from YAML file."""
        # TODO: Implement YAML import
        print("Import YAML clicked")
    
    def export_yaml(self):
        """Export facilities to YAML file."""
        # TODO: Implement YAML export
        print("Export YAML clicked")
    
    def edit_facility(self, index):
        """Open dialog to edit the selected facility."""
        row = index.row()
        name = self.table.item(row, 0).text()
        # TODO: Implement facility edit dialog
        print(f"Edit Facility: {name}")