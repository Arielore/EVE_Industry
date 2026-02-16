"""
Main window for EVE Industry application.
Provides navigation and hosts different views.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QStackedWidget, QSplitter
)
from PySide6.QtCore import Qt

from eve_industry.gui.views.bpo_list_view import BPOListView
from eve_industry.gui.views.bpc_inventory_view import BPCInventoryView
from eve_industry.gui.views.recipes_view import RecipesView
from eve_industry.gui.views.facilities_view import FacilitiesView
from eve_industry.gui.views.settings_view import SettingsView


class MainWindow(QMainWindow):
    """Main application window with navigation and stacked views."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EVE Industry Management")
        self.resize(1200, 800)
        
        # Initialize views dictionary
        self.views = {}
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for sidebar and content
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Create sidebar with navigation buttons
        sidebar = self._create_sidebar()
        splitter.addWidget(sidebar)
        
        # Create stacked widget for views
        self.stacked_widget = QStackedWidget()
        splitter.addWidget(self.stacked_widget)
        
        # Initialize views (they will be created lazily on first access)
        self._view_classes = {
            'bpos': BPOListView,
            'bpcs': BPCInventoryView,
            'recipes': RecipesView,
            'facilities': FacilitiesView,
            'settings': SettingsView
        }
        
        # Set splitter sizes
        splitter.setSizes([200, 1000])
        
        # Show BPO list by default
        self.show_view('bpos')
    
    def _create_sidebar(self) -> QWidget:
        """Create sidebar with navigation buttons."""
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(5)
        
        # Navigation buttons
        buttons = [
            ("BPO List", "bpos"),
            ("BPC Inventory", "bpcs"),
            ("Recipes", "recipes"),
            ("Facilities", "facilities"),
            ("Settings", "settings")
        ]
        
        for text, view_name in buttons:
            button = QPushButton(text)
            button.setFixedHeight(40)
            button.clicked.connect(lambda checked, vn=view_name: self.show_view(vn))
            sidebar_layout.addWidget(button)
        
        # Add stretch at the bottom
        sidebar_layout.addStretch()
        
        return sidebar
    
    def get_view(self, view_name: str) -> QWidget:
        """Get view instance, creating it if it doesn't exist."""
        if view_name not in self.views:
            view_class = self._view_classes.get(view_name)
            if view_class:
                self.views[view_name] = view_class()
                self.stacked_widget.addWidget(self.views[view_name])
            else:
                # Fallback to empty widget
                self.views[view_name] = QWidget()
                self.stacked_widget.addWidget(self.views[view_name])
        
        return self.views[view_name]
    
    def show_view(self, view_name: str):
        """Show the specified view."""
        view = self.get_view(view_name)
        self.stacked_widget.setCurrentWidget(view)
        
        # Update window title
        titles = {
            'bpos': 'BPO List',
            'bpcs': 'BPC Inventory',
            'recipes': 'Recipes',
            'facilities': 'Facilities',
            'settings': 'Settings'
        }
        title = titles.get(view_name, 'EVE Industry')
        self.setWindowTitle(f"EVE Industry Management - {title}")


if __name__ == "__main__":
    # Simple test
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())