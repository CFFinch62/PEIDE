"""
About dialog module for Project Euler Editor.
"""
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class AboutDialog:
    """
    Shows information about the application, including version and copyright.
    """
    
    @staticmethod
    def show(parent=None):
        """Show the about dialog with application information."""
        about_text = """
        <h2>Project Euler Solutions Editor</h2>
        <p>Version 1.6</p>
        <p>A specialized editor for solving Project Euler problems with Python.</p>
        <p>© 2025  Chuck Finch - Fragillidae Software</p>
        """
        
        msg = QMessageBox(parent)
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(about_text)
        
        # Add icon to the About dialog
        icon = QIcon("PEIDE.png")
        msg.setIconPixmap(icon.pixmap(64, 64))
        
        msg.exec() 