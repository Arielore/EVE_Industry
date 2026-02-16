"""
Settings View for EVE Industry application.
Configuration for database, import/export, and application settings.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QComboBox, QSpinBox, QGroupBox
)


class SettingsView(QWidget):
    """View for application settings and configuration."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Database configuration group
        db_group = QGroupBox("Database Configuration")
        db_layout = QFormLayout()
        
        self.db_path_edit = QLineEdit()
        self.db_path_edit.setPlaceholderText("Path to database file")
        db_layout.addRow("Database Path:", self.db_path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_database)
        db_layout.addRow("", browse_btn)
        
        db_group.setLayout(db_layout)
        layout.addWidget(db_group)
        
        # Trade hub configuration group
        trade_group = QGroupBox("Trade Hub Configuration")
        trade_layout = QFormLayout()
        
        self.trade_hub_combo = QComboBox()
        self.trade_hub_combo.addItems(["Jita", "Amarr", "Dodixie", "Rens", "Hek"])
        trade_layout.addRow("Default Trade Hub:", self.trade_hub_combo)
        
        trade_group.setLayout(trade_layout)
        layout.addWidget(trade_group)
        
        # Price fetcher configuration group
        price_group = QGroupBox("Price Fetcher Configuration")
        price_layout = QFormLayout()
        
        self.cache_duration_spin = QSpinBox()
        self.cache_duration_spin.setRange(1, 24)
        self.cache_duration_spin.setSuffix(" hours")
        self.cache_duration_spin.setValue(6)
        price_layout.addRow("Cache Duration:", self.cache_duration_spin)
        
        price_group.setLayout(price_layout)
        layout.addWidget(price_group)
        
        # Import/Export buttons
        import_export_layout = QHBoxLayout()
        
        import_all_btn = QPushButton("Import All YAML")
        import_all_btn.clicked.connect(self.import_all_yaml)
        import_export_layout.addWidget(import_all_btn)
        
        export_all_btn = QPushButton("Export All YAML")
        export_all_btn.clicked.connect(self.export_all_yaml)
        import_export_layout.addWidget(export_all_btn)
        
        layout.addLayout(import_export_layout)
        
        # Save/Cancel buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.cancel_changes)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Add stretch at bottom
        layout.addStretch()
    
    def browse_database(self):
        """Open file dialog to browse for database file."""
        # TODO: Implement file dialog
        print("Browse database clicked")
    
    def import_all_yaml(self):
        """Import all data from YAML files."""
        # TODO: Implement YAML import for all tables
        print("Import all YAML clicked")
    
    def export_all_yaml(self):
        """Export all data to YAML files."""
        # TODO: Implement YAML export for all tables
        print("Export all YAML clicked")
    
    def save_settings(self):
        """Save application settings."""
        # TODO: Save settings to database/config file
        print("Save settings clicked")
    
    def cancel_changes(self):
        """Cancel changes to settings."""
        # TODO: Reset form fields to current values
        print("Cancel clicked")