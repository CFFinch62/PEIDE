"""
Info dialog module for Project Euler Editor.
Shows the README.md contents as plain text.
"""
import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextEdit
from PyQt6.QtCore import Qt

class InfoDialog:
    """
    Shows information from the README file as plain text.
    """

    @staticmethod
    def show(parent=None):
        """Show the info dialog with README.md contents as plain text."""
        readme_path = "README.md"
        dialog_title = "Info"

        try:
            with open(readme_path, "r") as f:
                readme_content = f.read()
                print(f"README.md content length: {len(readme_content)}")
        except FileNotFoundError:
            readme_content = f"README.md file not found at {os.path.abspath(readme_path)}."
            print(f"README.md not found at {os.path.abspath(readme_path)}")

        # Create dialog and layout
        dialog = QDialog(parent)
        dialog.setWindowTitle(dialog_title)
        dialog.setMinimumSize(800, 600)
        dialog.setStyleSheet("background-color: #2D2D2D;")
        layout = QVBoxLayout(dialog)

        # Create text editor in read-only mode for plain text display
        text_editor = QTextEdit()
        text_editor.setReadOnly(True)
        text_editor.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: none;
                font-family: monospace;
                font-size: 12px;
            }
        """)
        text_editor.setPlainText(readme_content)
        layout.addWidget(text_editor)

        # Add close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3D3D3D;
                color: #FFFFFF;
                border: 1px solid #555;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4D4D4D;
            }
        """)
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec()
