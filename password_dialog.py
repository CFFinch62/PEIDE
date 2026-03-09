"""
Custom password dialog with show/hide toggle button.
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QDialogButtonBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class PasswordDialog(QDialog):
    """
    A custom dialog for password input with a show/hide toggle button.
    """
    
    def __init__(self, parent=None, title="Password", prompt="Enter password:"):
        """
        Initialize the password dialog.
        
        Args:
            parent: Parent widget
            title: Dialog title
            prompt: Text prompt for the password
        """
        super().__init__(parent)
        
        self.setWindowTitle(title)
        self.setMinimumWidth(350)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Add prompt label
        self.prompt_label = QLabel(prompt)
        layout.addWidget(self.prompt_label)
        
        # Create password input with toggle button
        password_layout = QHBoxLayout()
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input)
        
        # Toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setFixedWidth(30)
        self.toggle_button.setToolTip("Show/Hide Password")
        
        # Set eye icon (using text as fallback)
        self.toggle_button.setText("👁️")
        
        # Connect toggle button
        self.toggle_button.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.toggle_button)
        
        layout.addLayout(password_layout)
        
        # Add standard buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                     QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Apply styling to match the application theme
        self.apply_styling()
        
        # Set focus to password field
        self.password_input.setFocus()
    
    def toggle_password_visibility(self):
        """Toggle between showing and hiding the password."""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_button.setText("🔒")
            self.toggle_button.setToolTip("Hide Password")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_button.setText("👁️")
            self.toggle_button.setToolTip("Show Password")
    
    def apply_styling(self):
        """Apply styling to match the application theme."""
        # Dark blue background with yellow text (matching the app's style)
        self.setStyleSheet("""
            QDialog {
                background-color: #000000;
                color: yellow;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #909090;
                color: black;
                border: none;
                padding: 5px;
            }
            QPushButton {
                background-color: #202020;
                color: 000000;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #909090;
            }
        """)
    
    def get_password(self):
        """Get the entered password."""
        return self.password_input.text()
    
    @staticmethod
    def get_password_input(parent=None, title="Password", prompt="Enter password:"):
        """
        Static method to create and show a password dialog.
        
        Args:
            parent: Parent widget
            title: Dialog title
            prompt: Text prompt for the password
            
        Returns:
            tuple: (password, ok) where ok is True if user clicked OK
        """
        dialog = PasswordDialog(parent, title, prompt)
        result = dialog.exec()
        
        return dialog.get_password(), result == QDialog.DialogCode.Accepted
