from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QListWidget, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from template_editor_dialog import TemplateEditorDialog
from ui.code_editor import CodeEditor

class TemplatesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = parent.settings_manager if parent else None
        self.setWindowTitle("Code Templates")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create list widget for templates
        self.templates_list = QListWidget()
        self.templates_list.currentItemChanged.connect(self.show_template_details)
        self.templates_list.setStyleSheet("""
            QListWidget {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        layout.addWidget(QLabel("Available Templates:"))
        layout.addWidget(self.templates_list)
        
        # Create details area
        self.description_label = QLabel()
        self.description_label.setStyleSheet("color: yellow;")
        self.code_preview = CodeEditor(settings_manager=self.settings_manager)
        self.code_preview.setReadOnly(True)
        
        # Apply settings using SettingsManager
        if self.settings_manager:
            # Temporarily update settings for the code preview
            self.settings_manager.update_code_editor_settings(
                font_family="Consolas",
                font_size=12,
                text_color="#FFFF00",  # Yellow
                background_color="#000066"  # Dark blue
            )
            self.settings_manager.apply_code_editor_settings(self.code_preview)
        
        layout.addWidget(QLabel("Template Details:"))
        layout.addWidget(self.description_label)
        layout.addWidget(QLabel("Code Preview:"))
        layout.addWidget(self.code_preview)
        
        # Create buttons
        button_layout = QHBoxLayout()
        self.new_button = QPushButton("New Template")
        self.new_button.clicked.connect(self.create_new_template)
        self.insert_button = QPushButton("Insert Template")
        self.insert_button.clicked.connect(self.insert_template)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.insert_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Load templates
        self.load_templates()

    def load_templates(self):
        """Load templates into the list widget."""
        from templates_manager import TemplatesManager
        self.templates_manager = TemplatesManager()
        templates = self.templates_manager.load_templates()
        
        self.templates_list.clear()
        for name, template in templates.items():
            self.templates_list.addItem(template["name"])

    def show_template_details(self, current, previous):
        """Show details of the selected template."""
        if current is None:
            return
            
        # Get the template name from the list item
        template_name = current.text()
        
        # Find the template key that matches this name
        templates = self.templates_manager.load_templates()
        template_key = None
        for key, template in templates.items():
            if template["name"] == template_name:
                template_key = key
                break
                
        if template_key:
            template = templates[template_key]
            self.description_label.setText(template["description"])
            self.code_preview.setPlainText(template["code"])

    def create_new_template(self):
        """Open the template editor dialog to create a new template."""
        dialog = TemplateEditorDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Reload templates to show the new one
            self.load_templates()

    def insert_template(self):
        """Insert the selected template into the editor."""
        current_item = self.templates_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "Please select a template first")
            return
            
        # Get the template name from the list item
        template_name = current_item.text()
        
        # Find the template key that matches this name
        templates = self.templates_manager.load_templates()
        template_key = None
        for key, template in templates.items():
            if template["name"] == template_name:
                template_key = key
                break
                
        if template_key:
            template = templates[template_key]
            self.parent().code_editor.insertPlainText(template["code"])
            self.close()
        else:
            QMessageBox.warning(self, "Warning", "Could not find the selected template") 