"""
Data File Panel module for Project Euler Editor.
Handles UI components and user interactions for data file management.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTextEdit, QPushButton, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal


class DataFilePanel(QWidget):
    """
    Panel for displaying and managing data files.
    Handles UI components and user interactions only.
    """
    
    # Signal emitted when user wants to insert data loading code
    insert_code_requested = pyqtSignal()
    # Signal emitted when user wants to add a data file for the current problem
    add_file_requested = pyqtSignal()
    
    def __init__(self, settings_manager):
        """
        Initialize the Data File Panel.
        
        Args:
            settings_manager: The settings manager instance for styling
        """
        super().__init__()
        self.settings_manager = settings_manager
        self.current_data_info = None
        
        # Create UI components
        self._create_ui()
        
        # Apply initial settings
        self._apply_settings()
        
        # Nothing to insert until a problem with a data file is loaded
        self.insert_data_code_button.setEnabled(False)
    
    def _create_ui(self):
        """Create and set up UI components."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing
        
        # Create splitter for info and preview sections
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Info section
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(5, 5, 5, 5)  # Add small margins
        
        # Data files text
        self.data_files_text = QTextEdit()
        self.data_files_text.setReadOnly(True)
        self.data_files_text.setFixedHeight(100)
        info_layout.addWidget(self.data_files_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.insert_data_code_button = QPushButton("Insert Data Loading Code")
        self.insert_data_code_button.clicked.connect(self._handle_insert_code)
        button_layout.addWidget(self.insert_data_code_button)
        
        self.add_data_file_button = QPushButton("Add Data File...")
        self.add_data_file_button.setToolTip(
            "Copy a data file downloaded from Project Euler into the data folder for this problem")
        self.add_data_file_button.clicked.connect(self.add_file_requested.emit)
        button_layout.addWidget(self.add_data_file_button)
        info_layout.addLayout(button_layout)
        
        # Preview section
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(5, 5, 5, 5)  # Add small margins
        
        # Preview label
        self.data_preview_label = QLabel("Data Preview:")
        preview_layout.addWidget(self.data_preview_label)
        
        # Preview text
        self.data_preview_text = QTextEdit()
        self.data_preview_text.setReadOnly(True)
        preview_layout.addWidget(self.data_preview_text)
        
        # Add widgets to splitter
        splitter.addWidget(info_widget)
        splitter.addWidget(preview_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([150, 450])
        
        # Add splitter to main layout
        layout.addWidget(splitter)
        
        # Set minimum size for the panel
        self.setMinimumSize(400, 300)
    
    def _apply_settings(self):
        """Apply current settings to UI components."""
        settings = self.settings_manager.settings
        
        # Apply data files settings
        self.settings_manager.apply_data_files_settings(self.data_files_text)
        self.settings_manager.apply_data_files_settings(self.data_preview_text)
        self.data_preview_label.setStyleSheet(f"color: {settings['data_files']['text_color']};")
    
    def _handle_insert_code(self):
        """Handle insert code button click."""
        if self.current_data_info and self.current_data_info.get('has_data', False):
            self.insert_code_requested.emit()
    
    def update_data_info(self, data_info):
        """
        Update the panel with new data file information.
        
        Args:
            data_info: Dictionary containing data file information
        """
        self.current_data_info = data_info
        
        if data_info and data_info.get('has_data', False):
            # Update data files text
            self.data_files_text.setPlainText(
                f"Data File: {data_info['file']}\n"
                f"Description: {data_info['description']}\n\n"
                f"Example Code:\n{data_info['example']}"
            )
            
            # Enable the insert button
            self.insert_data_code_button.setEnabled(True)
            self.add_data_file_button.setText("Replace Data File...")
            
            # Make sure the panel is visible
            self.show()
        else:
            # No data file: leave the panel usable so one can be added
            self.data_files_text.setPlainText(
                "No data file found for this problem.\n\n"
                "If the problem needs one, download it from Project Euler and click "
                "'Add Data File...'. Files saved directly into the data folder are "
                "also recognised if their name starts with the problem number "
                "(e.g. 0102_triangles.txt).")
            self.data_preview_text.setPlainText("No data file for this problem.")
            self.insert_data_code_button.setEnabled(False)
            self.add_data_file_button.setText("Add Data File...")
    
    def update_data_preview(self, content):
        """
        Update the data preview with new content.
        
        Args:
            content: The content to display in the preview
        """
        self.data_preview_text.setPlainText(content)
        # Make sure the preview is visible
        self.data_preview_text.show()
    
    def clear(self):
        """Clear all panel content."""
        self.data_files_text.clear()
        self.data_preview_text.clear()
        self.current_data_info = None
        self.insert_data_code_button.setEnabled(False)
    
    def showEvent(self, event):
        """Handle show events to ensure proper visibility."""
        super().showEvent(event)
        # Make sure all widgets are visible
        self.data_files_text.show()
        self.data_preview_text.show()
        self.insert_data_code_button.show() 