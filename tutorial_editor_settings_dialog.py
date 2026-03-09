from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QComboBox, QSpinBox, QPushButton, QColorDialog,
                            QGroupBox, QFormLayout, QMessageBox, QApplication)
from PyQt6.QtGui import QFont, QFontDatabase, QColor, QShowEvent
from PyQt6.QtCore import Qt, QTimer

class TutorialEditorSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tutorial Editor Settings")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        # Get the settings manager from parent
        self.settings_manager = parent.settings_manager if parent and hasattr(parent, 'settings_manager') else None

        # Create main layout
        layout = QVBoxLayout(self)

        # Get system fonts
        system_fonts = QFontDatabase.families()

        # Tutorial Editor Settings Group
        editor_group = QGroupBox("Tutorial Editor Appearance")
        editor_layout = QFormLayout()

        # Font family
        self.font_family = QComboBox()
        self.font_family.addItems(system_fonts)
        editor_layout.addRow("Font:", self.font_family)

        # Font size
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 72)
        self.font_size.setValue(12)
        editor_layout.addRow("Font Size:", self.font_size)

        # Text color
        self.text_color_button = QPushButton("Choose Text Color")
        self.text_color_button.clicked.connect(lambda: self.choose_color("text"))
        editor_layout.addRow("Text Color:", self.text_color_button)

        # Background color
        self.bg_color_button = QPushButton("Choose Background Color")
        self.bg_color_button.clicked.connect(lambda: self.choose_color("background"))
        editor_layout.addRow("Background Color:", self.bg_color_button)

        editor_group.setLayout(editor_layout)
        layout.addWidget(editor_group)

        # Buttons
        button_layout = QHBoxLayout()

        # Reset to defaults button
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_button)

        # Add spacer
        button_layout.addStretch()

        # OK and Cancel buttons
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Store current colors
        self.current_colors = {
            "text": "#FFFF00",
            "background": "#000066"
        }

        # Load current settings
        self.load_current_settings()

        # Apply tutorial editor styling to this dialog
        self.apply_tutorial_editor_styling()

    def load_current_settings(self):
        """Load current settings from the settings manager."""
        if self.settings_manager:
            settings = self.settings_manager.get_tutorial_editor_settings()

            # Set font family
            font_family = settings.get("font_family", "Courier New")
            index = self.font_family.findText(font_family)
            if index >= 0:
                self.font_family.setCurrentIndex(index)

            # Set font size
            self.font_size.setValue(settings.get("font_size", 12))

            # Set colors
            text_color = settings.get("text_color", "#FFFF00")
            bg_color = settings.get("background_color", "#000066")

            self.current_colors["text"] = text_color
            self.current_colors["background"] = bg_color

            # Update button colors
            self.text_color_button.setStyleSheet(f"background-color: {text_color}")
            self.bg_color_button.setStyleSheet(f"background-color: {bg_color}")

    def choose_color(self, color_type):
        """Open color dialog and update button background."""
        current_color = QColor(self.current_colors[color_type])
        color = QColorDialog.getColor(current_color, self)

        if color.isValid():
            color_hex = color.name(QColor.NameFormat.HexRgb)
            self.current_colors[color_type] = color_hex

            # Update button appearance
            if color_type == "text":
                self.text_color_button.setStyleSheet(f"background-color: {color_hex}")
            elif color_type == "background":
                self.bg_color_button.setStyleSheet(f"background-color: {color_hex}")

    def showEvent(self, event):
        """Override showEvent to center the dialog when it's shown."""
        super().showEvent(event)
        # Use a timer to delay centering until after the dialog is fully rendered
        QTimer.singleShot(0, self.center_on_screen)

    def center_on_screen(self):
        """Center the dialog on the screen."""
        # Get the primary screen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Get the dialog size
        dialog_size = self.size()

        # Calculate the center position relative to screen
        x = screen_geometry.x() + (screen_geometry.width() - dialog_size.width()) // 2
        y = screen_geometry.y() + (screen_geometry.height() - dialog_size.height()) // 2

        # Move the dialog to the center using absolute screen coordinates
        # Use setGeometry to ensure the dialog is positioned correctly and override parent positioning
        self.setGeometry(x, y, dialog_size.width(), dialog_size.height())

        # Ensure the dialog is raised and activated
        self.raise_()
        self.activateWindow()

    def reset_to_defaults(self):
        """Reset all settings to default values."""
        # Set default values
        self.font_family.setCurrentText("Courier New")
        self.font_size.setValue(12)
        self.current_colors["text"] = "#FFFF00"
        self.current_colors["background"] = "#000066"

        # Update button colors
        self.text_color_button.setStyleSheet("background-color: #FFFF00")
        self.bg_color_button.setStyleSheet("background-color: #000066")

        QMessageBox.information(self, "Reset", "Settings have been reset to defaults.")

    def get_settings(self):
        """Get the current settings from the dialog."""
        return {
            "font_family": self.font_family.currentText(),
            "font_size": self.font_size.value(),
            "text_color": self.current_colors["text"],
            "background_color": self.current_colors["background"]
        }

    def apply_tutorial_editor_styling(self):
        """Apply tutorial editor styling to this dialog."""
        if self.settings_manager:
            settings = self.settings_manager.get_tutorial_editor_settings()

            self.setStyleSheet(f"""
                QDialog {{
                    background-color: {settings['background_color']};
                    color: {settings['text_color']};
                }}
                QLabel {{
                    color: {settings['text_color']};
                    font-weight: bold;
                }}
                QComboBox, QSpinBox {{
                    background-color: {settings['background_color']};
                    color: {settings['text_color']};
                    border: 1px solid {settings['text_color']};
                    padding: 5px;
                }}
                QPushButton {{
                    background-color: {settings['background_color']};
                    color: {settings['text_color']};
                    border: 1px solid {settings['text_color']};
                    padding: 5px;
                    min-width: 80px;
                    border-radius: 3px;
                }}
                QPushButton:hover {{
                    background-color: #0000aa;
                }}
                QPushButton:pressed {{
                    background-color: #0000cc;
                }}
                QGroupBox {{
                    color: {settings['text_color']};
                    font-weight: bold;
                    border: 2px solid {settings['text_color']};
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """)

    def accept(self):
        """Save settings and close dialog."""
        if self.settings_manager:
            settings = self.get_settings()
            self.settings_manager.update_tutorial_editor_settings(
                settings["font_family"],
                settings["font_size"],
                settings["text_color"],
                settings["background_color"]
            )
            QMessageBox.information(self, "Settings Saved",
                                  "Tutorial editor settings have been saved successfully!")
        super().accept()
