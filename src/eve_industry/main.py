#!/usr/bin/env python3
"""
Main entry point for the EVE Industry application.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon

from eve_industry.gui.main_window import MainWindow


def load_styles(app: QApplication) -> bool:
    """Load application styles from QSS file."""
    styles_path = Path(__file__).parent / "styles" / "dark_theme.qss"
    if styles_path.exists():
        file = QFile(str(styles_path))
        if file.open(QFile.ReadOnly | QFile.Text):
            style = str(file.readAll(), encoding="utf-8")
            app.setStyleSheet(style)
            file.close()
            return True
    return False


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("EVE Industry")
    app.setOrganizationName("EVE Industry")
    
    # Try to load application icon
    icon_path = Path(__file__).parent / "resources" / "app_icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Load styles
    load_styles(app)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()