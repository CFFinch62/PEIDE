"""
Welcome dialog module for Project Euler Editor.
"""
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

class WelcomeDialog:
    """
    Shows a welcome message for first-time users with information about the application.
    """
    
    @staticmethod
    def show(parent=None):
        """Show the welcome dialog with basic application information."""
        welcome_text = """
        <h2>Welcome to Project Euler Editor!</h2>
        <p>This application helps you solve Project Euler problems and build your coding portfolio.</p>
        
        <h3>Getting Started:</h3>
        <ol>
            <li>Click on any problem number in the grid to load it</li>
            <li>Read the problem description carefully</li>
            <li>Write your solution in the code editor</li>
            <li>Click "Run Code" to test your solution</li>
            <li>Save your solution to build your portfolio</li>
        </ol>
        
        <h3>Features:</h3>
        <ul>
            <li>Syntax highlighting for better code readability</li>
            <li>Helper files to organize your code</li>
            <li>Progress tracking to see your improvement</li>
            <li>Hints when you get stuck</li>
            <li>Data file management for problems that need external data</li>
        </ul>
        
        <p>Click "OK" to start your coding journey!</p>
        """
        
        msg = QMessageBox(parent)
        msg.setWindowTitle("Welcome")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(welcome_text)
        msg.exec() 