import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                            QWidget, QMessageBox, QDialog, QListWidget,
                            QPushButton, QLabel, QStatusBar, QFileDialog, QTextBrowser)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

from tutorial_editor_dialog import TutorialEditorDialog
from tutorial_manager import TutorialManager
from password_dialog import PasswordDialog
from settings_manager import SettingsManager
from tutorial_editor_settings_dialog import TutorialEditorSettingsDialog

class TutorialEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize managers
        self.settings_manager = SettingsManager()
        self.tutorial_manager = TutorialManager()

        # Set up the main window
        self.setWindowTitle("Project Euler Tutorial Editor")
        self.setGeometry(100, 100, 900, 700)



        # Try to set application icon if it exists
        if os.path.exists("fragillidae_icon.png"):
            app_icon = QIcon("fragillidae_icon.png")
            self.setWindowIcon(app_icon)
            QApplication.instance().setWindowIcon(app_icon)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Create menu bar
        self.create_menu_bar()

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Create tutorial list widget
        list_label = QLabel("Available Tutorials:")
        main_layout.addWidget(list_label)

        self.tutorial_list = QListWidget()
        self.tutorial_list.setMinimumHeight(200)
        main_layout.addWidget(self.tutorial_list)

        # Buttons for tutorial management
        button_layout = QHBoxLayout()

        self.new_button = QPushButton("New Tutorial")
        self.new_button.clicked.connect(self.create_new_tutorial)

        self.edit_button = QPushButton("Edit Tutorial")
        self.edit_button.clicked.connect(self.edit_selected_tutorial)

        self.delete_button = QPushButton("Delete Tutorial")
        self.delete_button.clicked.connect(self.delete_selected_tutorial)

        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        main_layout.addLayout(button_layout)

        # Description area
        desc_label = QLabel("Description:")
        main_layout.addWidget(desc_label)

        self.description_label = QLabel("Select a tutorial to see its description")
        self.description_label.setWordWrap(True)
        self.description_label.setMinimumHeight(100)
        main_layout.addWidget(self.description_label)

        # Connect signals
        self.tutorial_list.currentItemChanged.connect(self.show_tutorial_description)

        # Load tutorials
        self.load_tutorials()

        # Apply tutorial editor styling
        self.apply_tutorial_editor_styling()

    def apply_tutorial_editor_styling(self):
        """Apply tutorial editor styling based on current settings."""
        if self.settings_manager:
            settings = self.settings_manager.get_tutorial_editor_settings()

            # Apply styling to the main window
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: {settings['background_color']};
                    color: {settings['text_color']};
                }}
                QLabel {{
                    color: {settings['text_color']};
                    font-weight: bold;
                    font-family: '{settings['font_family']}';
                    font-size: {settings['font_size']}px;
                }}
                QPushButton {{
                    background-color: {settings['background_color']};
                    color: {settings['text_color']};
                    border: 1px solid {settings['text_color']};
                    padding: 5px;
                    min-width: 80px;
                    border-radius: 3px;
                    font-family: '{settings['font_family']}';
                    font-size: {settings['font_size']}px;
                }}
                QPushButton:hover {{
                    background-color: {self.settings_manager._lighten_color(settings['background_color'])};
                }}
                QPushButton:pressed {{
                    background-color: {self.settings_manager._lighten_color(settings['background_color'], 0.4)};
                }}
                QStatusBar {{
                    background-color: {self.settings_manager._lighten_color(settings['background_color'], 0.1)};
                    color: {settings['text_color']};
                    font-family: '{settings['font_family']}';
                    font-size: {settings['font_size']}px;
                }}
                QListWidget {{
                    background-color: {settings['background_color']};
                    color: {settings['text_color']};
                    border: 1px solid {settings['text_color']};
                    padding: 5px;
                    font-family: '{settings['font_family']}';
                    font-size: {settings['font_size']}px;
                }}
                QMenuBar {{
                    background-color: {self.settings_manager._lighten_color(settings['background_color'], 0.1)};
                    color: {settings['text_color']};
                    font-family: '{settings['font_family']}';
                    font-size: {settings['font_size']}px;
                }}
                QMenuBar::item {{
                    background-color: {self.settings_manager._lighten_color(settings['background_color'], 0.1)};
                    color: {settings['text_color']};
                }}
                QMenuBar::item:selected {{
                    background-color: {self.settings_manager._lighten_color(settings['background_color'], 0.3)};
                }}
                QMenu {{
                    background-color: {settings['background_color']};
                    color: {settings['text_color']};
                    border: 1px solid {settings['text_color']};
                    font-family: '{settings['font_family']}';
                    font-size: {settings['font_size']}px;
                }}
                QMenu::item:selected {{
                    background-color: {self.settings_manager._lighten_color(settings['background_color'], 0.3)};
                }}
            """)

            # Update specific widget styles
            if hasattr(self, 'description_label'):
                self.description_label.setStyleSheet(f"""
                    background-color: {self.settings_manager._lighten_color(settings['background_color'], 0.2)};
                    color: {settings['text_color']};
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid {settings['text_color']};
                    font-family: '{settings['font_family']}';
                    font-size: {settings['font_size']}px;
                """)

    def create_menu_bar(self):
        """Create the application menu bar."""
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")

        # New tutorial action
        new_action = QAction("New Tutorial", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.create_new_tutorial)
        file_menu.addAction(new_action)

        # Edit tutorial action
        edit_action = QAction("Edit Tutorial", self)
        edit_action.setShortcut("Ctrl+E")
        edit_action.triggered.connect(self.edit_selected_tutorial)
        file_menu.addAction(edit_action)

        # Delete tutorial action
        delete_action = QAction("Delete Tutorial", self)
        delete_action.setShortcut("Del")
        delete_action.triggered.connect(self.delete_selected_tutorial)
        file_menu.addAction(delete_action)

        file_menu.addSeparator()

        # Import tutorial action
        import_action = QAction("Import Tutorial", self)
        import_action.triggered.connect(self.import_tutorial)
        file_menu.addAction(import_action)

        # Export tutorial action
        export_action = QAction("Export Tutorial", self)
        export_action.triggered.connect(self.export_tutorial)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Settings menu
        settings_menu = menu_bar.addMenu("Settings")

        # Tutorial Editor Settings action
        editor_settings_action = QAction("Tutorial Editor Settings", self)
        editor_settings_action.triggered.connect(self.show_editor_settings)
        settings_menu.addAction(editor_settings_action)

        # Help menu
        help_menu = menu_bar.addMenu("Help")

        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Tutorial guide action
        guide_action = QAction("Tutorial Authoring Guide", self)
        guide_action.triggered.connect(self.show_tutorial_guide)
        help_menu.addAction(guide_action)

    def load_tutorials(self):
        """Load tutorials into the list widget."""
        self.tutorial_list.clear()
        tutorials = self.tutorial_manager.load_tutorials()

        for name, tutorial_data in tutorials.items():
            self.tutorial_list.addItem(f"{name} - {tutorial_data['title']}")

        self.status_bar.showMessage(f"Loaded {len(tutorials)} tutorials")

    def show_tutorial_description(self, current, previous):
        """Show description of the selected tutorial."""
        if current:
            # Extract the tutorial name from the list item text
            tutorial_name = current.text().split(" - ")[0]
            tutorial_data = self.tutorial_manager.get_tutorial(tutorial_name)

            if tutorial_data and 'steps' in tutorial_data and len(tutorial_data['steps']) > 0:
                # Use the first step's content as description or tutorial title if no content
                if 'content' in tutorial_data['steps'][0]:
                    description = tutorial_data['steps'][0]['content']
                    # Truncate if too long
                    if len(description) > 200:
                        description = description[:200] + "..."
                else:
                    description = f"Tutorial: {tutorial_data['title']}"

                steps_count = len(tutorial_data['steps'])
                self.description_label.setText(f"{description}\n\nSteps: {steps_count}")
            else:
                self.description_label.setText("No description available")

    def create_new_tutorial(self):
        """Create a new tutorial using the tutorial editor dialog."""
        dialog = TutorialEditorDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_tutorials()
            self.status_bar.showMessage("New tutorial created")

    def edit_selected_tutorial(self):
        """Edit the selected tutorial."""
        current_item = self.tutorial_list.currentItem()
        if current_item:
            tutorial_name = current_item.text().split(" - ")[0]
            dialog = TutorialEditorDialog(self, tutorial_name=tutorial_name)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_tutorials()
                self.status_bar.showMessage(f"Tutorial '{tutorial_name}' updated")
        else:
            QMessageBox.warning(self, "Warning", "Please select a tutorial to edit")

    def delete_selected_tutorial(self):
        """Delete the selected tutorial."""
        current_item = self.tutorial_list.currentItem()
        if current_item:
            tutorial_name = current_item.text().split(" - ")[0]

            # Confirm deletion
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete the tutorial '{tutorial_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.tutorial_manager.delete_tutorial(tutorial_name):
                    self.load_tutorials()
                    self.status_bar.showMessage(f"Tutorial '{tutorial_name}' deleted")
                else:
                    QMessageBox.warning(self, "Error", f"Failed to delete tutorial '{tutorial_name}'")
        else:
            QMessageBox.warning(self, "Warning", "Please select a tutorial to delete")

    def import_tutorial(self):
        """Import a tutorial from a JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Tutorial",
            "",
            "JSON Files (*.json)"
        )

        if file_path:
            try:
                if self.tutorial_manager.import_tutorial(file_path):
                    self.load_tutorials()
                    self.status_bar.showMessage(f"Tutorial imported successfully")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to import tutorial: Invalid format")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import tutorial: {str(e)}")

    def export_tutorial(self):
        """Export the selected tutorial to a JSON file."""
        current_item = self.tutorial_list.currentItem()
        if current_item:
            tutorial_name = current_item.text().split(" - ")[0]

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Tutorial",
                f"{tutorial_name}.json",
                "JSON Files (*.json)"
            )

            if file_path:
                try:
                    if self.tutorial_manager.export_tutorial(tutorial_name, file_path):
                        self.status_bar.showMessage(f"Tutorial '{tutorial_name}' exported successfully")
                    else:
                        QMessageBox.critical(self, "Error", f"Failed to export tutorial")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to export tutorial: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a tutorial to export")

    def show_editor_settings(self):
        """Show the tutorial editor settings dialog."""
        dialog = TutorialEditorSettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Refresh the styling of the main window
            self.apply_tutorial_editor_styling()
            self.status_bar.showMessage("Settings updated successfully")

    def show_about(self):
        """Show the about dialog."""
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About Tutorial Editor")
        about_dialog.setMinimumWidth(400)
        about_dialog.setMinimumHeight(300)

        # Apply styling to match the main app
        about_dialog.setStyleSheet("""
            QDialog {
                background-color: #000066;
                color: yellow;
            }
            QLabel {
                color: yellow;
            }
            QPushButton {
                background-color: #000088;
                color: yellow;
                border: 1px solid yellow;
                padding: 5px;
                min-width: 80px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0000aa;
            }
        """)

        layout = QVBoxLayout(about_dialog)

        title_label = QLabel("Project Euler Tutorial Editor")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: yellow;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_label = QLabel(
            "A standalone application for creating and editing tutorials\n"
            "for the Project Euler Solutions Editor.\n\n"
            "© 2023 Project Euler Solutions Editor Team"
        )
        content_label.setStyleSheet("color: yellow;")
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_label.setWordWrap(True)

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(about_dialog.accept)

        layout.addWidget(title_label)
        layout.addWidget(content_label)
        layout.addStretch()
        layout.addWidget(btn_close, 0, Qt.AlignmentFlag.AlignCenter)

        about_dialog.exec()

    def show_tutorial_guide(self):
        """Show the tutorial authoring guide."""
        # Check if the guide file exists
        guide_path = os.path.join("tutorials", "tutorial_editor_guide.md")
        if os.path.exists(guide_path):
            try:
                with open(guide_path, 'r') as f:
                    guide_content = f.read()

                # Create a custom dialog to show the guide
                guide_dialog = QDialog(self)
                guide_dialog.setWindowTitle("Tutorial Authoring Guide")
                guide_dialog.setMinimumWidth(700)
                guide_dialog.setMinimumHeight(500)

                # Apply styling
                guide_dialog.setStyleSheet("""
                    QDialog {
                        background-color: #000066;
                        color: yellow;
                    }
                    QTextBrowser {
                        background-color: #000044;
                        color: yellow;
                        border: 1px solid yellow;
                        padding: 5px;
                    }
                    QPushButton {
                        background-color: #000088;
                        color: yellow;
                        border: 1px solid yellow;
                        padding: 5px;
                        min-width: 80px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #0000aa;
                    }
                """)

                layout = QVBoxLayout(guide_dialog)

                # Use QTextBrowser to display the markdown content
                text_browser = QTextBrowser()
                text_browser.setPlainText(guide_content)  # Simple display without markdown formatting
                text_browser.setOpenExternalLinks(True)

                btn_close = QPushButton("Close")
                btn_close.clicked.connect(guide_dialog.accept)

                layout.addWidget(text_browser)
                layout.addWidget(btn_close, 0, Qt.AlignmentFlag.AlignCenter)

                guide_dialog.exec()

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load guide: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "Tutorial authoring guide not found")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Set global stylesheet for message boxes and dialogs
    app.setStyleSheet("""
        QMessageBox, QDialog {
            background-color: #000066;
            color: yellow;
        }
        QMessageBox QLabel, QDialog QLabel {
            color: yellow;
        }
        QMessageBox QPushButton, QDialog QPushButton {
            background-color: #000088;
            color: yellow;
            border: 1px solid yellow;
            padding: 5px;
            min-width: 80px;
            border-radius: 3px;
        }
        QMessageBox QPushButton:hover, QDialog QPushButton:hover {
            background-color: #0000aa;
        }
        QFileDialog {
            background-color: #000066;
            color: yellow;
        }
        QFileDialog QTreeView, QFileDialog QListView {
            background-color: #000044;
            color: yellow;
            border: 1px solid yellow;
        }
        QFileDialog QLineEdit {
            background-color: #000088;
            color: yellow;
            border: 1px solid yellow;
            padding: 5px;
        }
        QFileDialog QPushButton {
            background-color: #000088;
            color: yellow;
            border: 1px solid yellow;
            padding: 5px;
            border-radius: 3px;
        }
    """)

    # Create and show the main window
    window = TutorialEditorApp()
    window.show()

    sys.exit(app.exec())