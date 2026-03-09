from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QLineEdit, QTextEdit, QListWidget, QMessageBox, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShowEvent
import json
import os

class TutorialEditorDialog(QDialog):
    def __init__(self, parent=None, tutorial_name=None):
        super().__init__(parent)
        self.tutorial_name = tutorial_name
        self.settings_manager = parent.settings_manager if parent else None
        self.setWindowTitle("Create Tutorial" if not tutorial_name else "Edit Tutorial")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        # Create layout
        layout = QVBoxLayout()

        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Tutorial Name:"))
        self.name_input = QLineEdit()
        if tutorial_name:
            self.name_input.setText(tutorial_name)
            self.name_input.setReadOnly(True)  # Don't allow editing the name of existing tutorials
        name_layout.addWidget(self.name_input)

        # Add Load Tutorial button
        self.load_button = QPushButton("Load Tutorial")
        self.load_button.clicked.connect(self.load_tutorial_dialog)
        name_layout.addWidget(self.load_button)

        layout.addLayout(name_layout)

        # Title input
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Tutorial Title:"))
        self.title_input = QLineEdit()
        title_layout.addWidget(self.title_input)
        layout.addLayout(title_layout)

        # Steps list and controls
        steps_layout = QVBoxLayout()
        steps_layout.addWidget(QLabel("Steps:"))

        # Steps list
        self.steps_list = QListWidget()
        self.steps_list.currentItemChanged.connect(self.load_step)
        steps_layout.addWidget(self.steps_list)

        # Step controls
        step_controls = QHBoxLayout()
        self.add_step_button = QPushButton("Add Step")
        self.add_step_button.clicked.connect(self.add_step)
        self.delete_step_button = QPushButton("Delete Step")
        self.delete_step_button.clicked.connect(self.delete_step)
        step_controls.addWidget(self.add_step_button)
        step_controls.addWidget(self.delete_step_button)
        steps_layout.addLayout(step_controls)

        layout.addLayout(steps_layout)

        # Step editor
        step_editor_layout = QVBoxLayout()
        step_editor_layout.addWidget(QLabel("Step Editor:"))

        # Step title
        step_title_layout = QHBoxLayout()
        step_title_layout.addWidget(QLabel("Title:"))
        self.step_title_input = QLineEdit()
        step_title_layout.addWidget(self.step_title_input)
        step_editor_layout.addLayout(step_title_layout)

        # Step content
        step_editor_layout.addWidget(QLabel("Content:"))
        self.step_content_input = QTextEdit()
        step_editor_layout.addWidget(self.step_content_input)

        # Step action
        step_action_layout = QHBoxLayout()
        step_action_layout.addWidget(QLabel("Action:"))
        self.step_action_input = QLineEdit()
        self.step_action_input.setPlaceholderText("none, highlight_areas, highlight_button, select_problem")
        step_action_layout.addWidget(self.step_action_input)
        step_editor_layout.addLayout(step_action_layout)

        # Step params
        step_params_layout = QHBoxLayout()
        step_params_layout.addWidget(QLabel("Params:"))
        self.step_params_input = QLineEdit()
        self.step_params_input.setPlaceholderText("JSON format, e.g., {\"button\": \"run\"}")
        step_params_layout.addWidget(self.step_params_input)
        step_editor_layout.addLayout(step_params_layout)

        # Save step button
        self.save_step_button = QPushButton("Save Step")
        self.save_step_button.clicked.connect(self.save_step)
        step_editor_layout.addWidget(self.save_step_button)

        layout.addLayout(step_editor_layout)

        # Dialog buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Tutorial")
        self.save_button.clicked.connect(self.save_tutorial)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Load tutorial if editing
        if tutorial_name:
            self.load_tutorial()

        # Apply tutorial editor styling
        self.apply_tutorial_editor_styling()

    def apply_tutorial_editor_styling(self):
        """Apply tutorial editor styling based on current settings."""
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
                    font-family: '{settings['font_family']}';
                    font-size: {settings['font_size']}px;
                }}
                QLineEdit, QTextEdit, QListWidget {{
                    background-color: {settings['background_color']};
                    color: {settings['text_color']};
                    border: 1px solid {settings['text_color']};
                    padding: 5px;
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
            """)

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

    def load_tutorial_dialog(self):
        """Show a dialog to select and load an existing tutorial."""
        try:
            # Get the tutorials directory
            tutorials_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tutorials")
            if not os.path.exists(tutorials_dir):
                QMessageBox.warning(self, "Warning", "No tutorials directory found")
                return

            # Get all JSON files in the tutorials directory
            tutorials = []
            for file in os.listdir(tutorials_dir):
                if file.endswith('.json'):
                    # Remove the .json extension to get the tutorial name
                    tutorial_name = file[:-5]
                    tutorials.append(tutorial_name)

            if not tutorials:
                QMessageBox.warning(self, "Warning", "No tutorials found")
                return

            # Create dialog to select tutorial
            dialog = QDialog(self)
            dialog.setWindowTitle("Load Tutorial")
            dialog.setMinimumWidth(400)
            dialog.setMinimumHeight(300)

            # Apply tutorial editor styling to the dialog
            if self.settings_manager:
                settings = self.settings_manager.get_tutorial_editor_settings()
                dialog.setStyleSheet(f"""
                    QDialog {{
                        background-color: {settings['background_color']};
                        color: {settings['text_color']};
                    }}
                    QLabel {{
                        color: {settings['text_color']};
                        font-weight: bold;
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
                """)

            layout = QVBoxLayout()

            # Create list widget for tutorials
            list_widget = QListWidget()
            for tutorial in sorted(tutorials):
                list_widget.addItem(tutorial)
            layout.addWidget(list_widget)

            # Add buttons
            button_layout = QHBoxLayout()
            load_button = QPushButton("Load")
            cancel_button = QPushButton("Cancel")
            button_layout.addWidget(load_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)

            # Connect buttons
            load_button.clicked.connect(dialog.accept)
            cancel_button.clicked.connect(dialog.reject)

            dialog.setLayout(layout)

            # Adjust size to fit content and then center the load dialog on screen
            dialog.adjustSize()

            # Get the primary screen
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            dialog_size = dialog.size()
            x = screen_geometry.x() + (screen_geometry.width() - dialog_size.width()) // 2
            y = screen_geometry.y() + (screen_geometry.height() - dialog_size.height()) // 2
            dialog.setGeometry(x, y, dialog_size.width(), dialog_size.height())

            # Ensure the dialog is raised and activated
            dialog.raise_()
            dialog.activateWindow()

            if dialog.exec() == QDialog.DialogCode.Accepted:
                selected_item = list_widget.currentItem()
                if selected_item:
                    tutorial_name = selected_item.text()
                    self.tutorial_name = tutorial_name
                    self.name_input.setText(tutorial_name)
                    self.name_input.setReadOnly(True)
                    self.setWindowTitle(f"Edit Tutorial: {tutorial_name}")
                    self.load_tutorial()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tutorials: {str(e)}")

    def load_tutorial(self):
        """Load an existing tutorial for editing."""
        try:
            # Get the tutorial manager
            from tutorial_manager import TutorialManager
            tutorial_manager = TutorialManager()

            # Load the tutorial data
            tutorial_data = tutorial_manager.get_tutorial(self.tutorial_name)

            if not tutorial_data:
                QMessageBox.warning(self, "Error", f"Tutorial not found: {self.tutorial_name}")
                return

            # Set the title
            self.title_input.setText(tutorial_data.get("title", ""))

            # Clear and populate the steps list
            self.steps_list.clear()
            self.step_data = tutorial_data.get("steps", [])

            for step in self.step_data:
                self.steps_list.addItem(step.get("title", "Untitled Step"))

            # Select the first step if available
            if self.steps_list.count() > 0:
                self.steps_list.setCurrentRow(0)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tutorial: {str(e)}")

    def add_step(self):
        """Add a new step to the tutorial."""
        self.steps_list.addItem("New Step")
        self.steps_list.setCurrentRow(self.steps_list.count() - 1)
        self.step_title_input.clear()
        self.step_content_input.clear()
        self.step_action_input.clear()
        self.step_params_input.clear()

    def delete_step(self):
        """Delete the selected step."""
        current_row = self.steps_list.currentRow()
        if current_row >= 0:
            self.steps_list.takeItem(current_row)

    def load_step(self, current, previous):
        """Load the selected step for editing."""
        if current is None:
            return

        try:
            # Get the step index
            step_index = self.steps_list.row(current)

            # Make sure we have step data
            if not hasattr(self, 'step_data'):
                self.step_data = []

            # Check if the step data exists
            if step_index < len(self.step_data):
                step = self.step_data[step_index]
                self.step_title_input.setText(step.get("title", ""))
                self.step_content_input.setPlainText(step.get("content", ""))
                self.step_action_input.setText(step.get("action", "none"))

                # Format the params as JSON string if it exists
                params = step.get("params", {})
                if params:
                    params_text = json.dumps(params)
                else:
                    params_text = "{}"

                self.step_params_input.setText(params_text)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load step: {str(e)}")

    def save_step(self):
        """Save the current step."""
        current_row = self.steps_list.currentRow()
        if current_row < 0:
            return

        # Get step data
        title = self.step_title_input.text().strip()
        content = self.step_content_input.toPlainText().strip()
        action = self.step_action_input.text().strip()

        # Parse params if provided
        params = {}
        params_text = self.step_params_input.text().strip()
        if params_text:
            try:
                params = json.loads(params_text)
            except:
                QMessageBox.warning(self, "Warning", "Invalid params format. Use JSON format.")
                return

        # Update the step in the list
        self.steps_list.item(current_row).setText(title)

        # Make sure we have step data
        if not hasattr(self, 'step_data'):
            self.step_data = []

        # Ensure step_data has enough entries
        while len(self.step_data) <= current_row:
            self.step_data.append({})

        # Update the step data
        self.step_data[current_row] = {
            "title": title,
            "content": content,
            "action": action,
            "params": params
        }

    def save_tutorial(self):
        """Save the tutorial and close the dialog."""
        name = self.name_input.text().strip()
        title = self.title_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a tutorial name")
            return

        if not title:
            QMessageBox.warning(self, "Warning", "Please enter a tutorial title")
            return

        # Collect all steps
        steps = []
        for i in range(self.steps_list.count()):
            # Get the current step item
            item = self.steps_list.item(i)
            title = item.text()

            # Get the step details from our saved data if available
            if i < len(self.step_data):
                step_data = self.step_data[i]
            else:
                # Create empty step data if none exists
                step_data = {
                    "title": title,
                    "content": "",
                    "action": "none",
                    "params": {}
                }

            steps.append(step_data)

        # Create tutorial data
        tutorial_data = {
            "title": title,
            "steps": steps
        }

        # Save using the tutorial manager
        try:
            # Get the tutorial manager
            from tutorial_manager import TutorialManager
            tutorial_manager = TutorialManager()

            # Save the tutorial
            tutorial_manager.save_tutorial(name, tutorial_data)

            # Close the dialog
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save tutorial: {str(e)}")