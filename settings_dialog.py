from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QComboBox, QSpinBox, QPushButton, QColorDialog,
                            QGroupBox, QFormLayout, QScrollArea, QWidget,
                            QGridLayout, QFileDialog, QMessageBox, QLineEdit,
                            QCheckBox)
from PyQt6.QtGui import QFont, QFontDatabase, QColor
from PyQt6.QtCore import Qt
import json
import os

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        # Reduce the minimum width since we're making a more compact layout
        self.setMinimumWidth(1100)
        self.setMinimumHeight(700)

        # Create main layout
        layout = QVBoxLayout(self)

        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Get system fonts
        system_fonts = QFontDatabase.families()

        # Create grid layout for settings groups
        settings_grid = QGridLayout()
        settings_grid.setSpacing(20)  # Add spacing between groups

        # First Column
        first_column = QVBoxLayout()

        # Template Editor Settings
        template_group = QGroupBox("Template Editor")
        template_layout = QFormLayout()
        template_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.template_font_family = QComboBox()
        self.template_font_family.addItems(system_fonts)
        template_layout.addRow("Font:", self.template_font_family)
        self.template_font_size = QSpinBox()
        self.template_font_size.setRange(8, 72)
        self.template_font_size.setValue(12)
        template_layout.addRow("Size:", self.template_font_size)
        self.template_text_color = QPushButton("Choose Color")
        self.template_text_color.clicked.connect(lambda: self.choose_color("template_text"))
        template_layout.addRow("Text:", self.template_text_color)
        self.template_bg_color = QPushButton("Choose Color")
        self.template_bg_color.clicked.connect(lambda: self.choose_color("template_bg"))
        template_layout.addRow("Background:", self.template_bg_color)
        template_group.setLayout(template_layout)
        first_column.addWidget(template_group)

        # Code Editor Settings
        code_group = QGroupBox("Code Editor")
        code_layout = QFormLayout()
        code_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.code_font_family = QComboBox()
        self.code_font_family.addItems(system_fonts)
        code_layout.addRow("Font:", self.code_font_family)
        self.code_font_size = QSpinBox()
        self.code_font_size.setRange(8, 72)
        self.code_font_size.setValue(12)
        code_layout.addRow("Size:", self.code_font_size)
        self.code_text_color = QPushButton("Choose Color")
        self.code_text_color.clicked.connect(lambda: self.choose_color("code_text"))
        code_layout.addRow("Text:", self.code_text_color)
        self.code_bg_color = QPushButton("Choose Color")
        self.code_bg_color.clicked.connect(lambda: self.choose_color("code_bg"))
        code_layout.addRow("Background:", self.code_bg_color)
        code_group.setLayout(code_layout)
        first_column.addWidget(code_group)

        # Second Column
        second_column = QVBoxLayout()

        # Helper Editor Settings
        helper_group = QGroupBox("Helper Editor")
        helper_layout = QFormLayout()
        helper_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.helper_font_family = QComboBox()
        self.helper_font_family.addItems(system_fonts)
        helper_layout.addRow("Font:", self.helper_font_family)
        self.helper_font_size = QSpinBox()
        self.helper_font_size.setRange(8, 72)
        self.helper_font_size.setValue(12)
        helper_layout.addRow("Size:", self.helper_font_size)
        self.helper_text_color = QPushButton("Choose Color")
        self.helper_text_color.clicked.connect(lambda: self.choose_color("helper_text"))
        helper_layout.addRow("Text:", self.helper_text_color)
        self.helper_bg_color = QPushButton("Choose Color")
        self.helper_bg_color.clicked.connect(lambda: self.choose_color("helper_bg"))
        helper_layout.addRow("Background:", self.helper_bg_color)
        helper_group.setLayout(helper_layout)
        # Reduce the size of the helper editor group
        helper_group.setMaximumWidth(300)
        second_column.addWidget(helper_group)

        # Data Files Settings
        data_files_group = QGroupBox("Data Files")
        data_files_layout = QFormLayout()
        data_files_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.data_files_font_family = QComboBox()
        self.data_files_font_family.addItems(system_fonts)
        data_files_layout.addRow("Font:", self.data_files_font_family)
        self.data_files_font_size = QSpinBox()
        self.data_files_font_size.setRange(8, 72)
        self.data_files_font_size.setValue(12)
        data_files_layout.addRow("Size:", self.data_files_font_size)
        self.data_files_text_color = QPushButton("Choose Color")
        self.data_files_text_color.clicked.connect(lambda: self.choose_color("data_files_text"))
        data_files_layout.addRow("Text:", self.data_files_text_color)
        self.data_files_bg_color = QPushButton("Choose Color")
        self.data_files_bg_color.clicked.connect(lambda: self.choose_color("data_files_bg"))
        data_files_layout.addRow("Background:", self.data_files_bg_color)
        data_files_group.setLayout(data_files_layout)
        # Reduce the size of the data files group
        data_files_group.setMaximumWidth(300)
        second_column.addWidget(data_files_group)
        
        # Code Formatting Settings - Moved to the second column
        formatting_group = QGroupBox("Code Formatting (Black)")
        formatting_layout = QFormLayout()
        formatting_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        # Auto-format on save option
        self.auto_format_on_save = QCheckBox("Auto-format on save")
        formatting_layout.addRow("", self.auto_format_on_save)
        
        # Line length option
        self.line_length = QSpinBox()
        self.line_length.setRange(80, 200)
        self.line_length.setValue(88)  # Black's default
        formatting_layout.addRow("Line Length:", self.line_length)
        
        # Skip string normalization option
        self.skip_string_normalization = QCheckBox("Skip string normalization")
        formatting_layout.addRow("", self.skip_string_normalization)
        
        formatting_group.setLayout(formatting_layout)
        # Set maximum width to make it more compact
        formatting_group.setMaximumWidth(300)
        second_column.addWidget(formatting_group)
        
        # Linting Settings - Moved to the second column
        linting_group = QGroupBox("Code Linting (Pylint)")
        linting_layout = QFormLayout()
        linting_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        # Auto-lint on save option
        self.auto_lint_on_save = QCheckBox("Auto-lint on save")
        linting_layout.addRow("", self.auto_lint_on_save)
        
        # Disable specific checks
        self.disabled_checks = QLineEdit()
        self.disabled_checks.setPlaceholderText("C0111,C0303,W0613")
        linting_layout.addRow("Disabled Checks:", self.disabled_checks)
        
        # Linting threshold
        self.linting_threshold = QSpinBox()
        self.linting_threshold.setRange(1, 10)
        self.linting_threshold.setValue(7)
        linting_layout.addRow("Min. Score:", self.linting_threshold)
        
        linting_group.setLayout(linting_layout)
        # Set maximum width to make it more compact
        linting_group.setMaximumWidth(300)
        second_column.addWidget(linting_group)

        # Third Column - Syntax Highlighting and Editor Themes
        third_column = QVBoxLayout()

        # Syntax Highlighting Settings
        syntax_group = QGroupBox("Syntax Highlighting")
        syntax_layout = QFormLayout()
        syntax_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        syntax_group.setMaximumHeight(350)  # Reduce height to make room for editor themes

        self.keywords_color = QPushButton("Choose Color")
        self.keywords_color.clicked.connect(lambda: self.choose_color("keywords"))
        syntax_layout.addRow("Keywords:", self.keywords_color)

        self.strings_color = QPushButton("Choose Color")
        self.strings_color.clicked.connect(lambda: self.choose_color("strings"))
        syntax_layout.addRow("Strings:", self.strings_color)

        self.numbers_color = QPushButton("Choose Color")
        self.numbers_color.clicked.connect(lambda: self.choose_color("numbers"))
        syntax_layout.addRow("Numbers:", self.numbers_color)

        self.comments_color = QPushButton("Choose Color")
        self.comments_color.clicked.connect(lambda: self.choose_color("comments"))
        syntax_layout.addRow("Comments:", self.comments_color)

        self.operators_color = QPushButton("Choose Color")
        self.operators_color.clicked.connect(lambda: self.choose_color("operators"))
        syntax_layout.addRow("Operators:", self.operators_color)

        self.functions_color = QPushButton("Choose Color")
        self.functions_color.clicked.connect(lambda: self.choose_color("functions"))
        syntax_layout.addRow("Functions:", self.functions_color)

        self.punctuation_color = QPushButton("Choose Color")
        self.punctuation_color.clicked.connect(lambda: self.choose_color("punctuation"))
        syntax_layout.addRow("Punctuation:", self.punctuation_color)

        # Add spacing before theme controls
        syntax_layout.addRow("", QLabel(""))  # Empty row for spacing

        # Theme name input
        theme_name_layout = QHBoxLayout()
        self.syntax_theme_name_input = QLineEdit()
        self.syntax_theme_name_input.setPlaceholderText("Enter syntax theme name")
        theme_name_layout.addWidget(self.syntax_theme_name_input)
        syntax_layout.addRow("Theme:", theme_name_layout)

        # Theme buttons on a new line
        theme_buttons_layout = QHBoxLayout()
        self.save_syntax_theme_button = QPushButton("Save Theme")
        self.save_syntax_theme_button.clicked.connect(self.save_syntax_theme)
        self.load_syntax_theme_button = QPushButton("Load Theme")
        self.load_syntax_theme_button.clicked.connect(self.load_syntax_theme)
        theme_buttons_layout.addWidget(self.save_syntax_theme_button)
        theme_buttons_layout.addWidget(self.load_syntax_theme_button)
        syntax_layout.addRow("", theme_buttons_layout)  # Empty label for the buttons row

        syntax_group.setLayout(syntax_layout)
        third_column.addWidget(syntax_group)

        # Editor Themes Settings
        editor_themes_group = QGroupBox("Editor Themes")
        editor_themes_layout = QFormLayout()
        editor_themes_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        # Add spacing before theme controls
        editor_themes_layout.addRow("", QLabel("Save/load font and color settings for all editors"))

        # Theme name input
        editor_theme_name_layout = QHBoxLayout()
        self.editor_theme_name_input = QLineEdit()
        self.editor_theme_name_input.setPlaceholderText("Enter editor theme name")
        editor_theme_name_layout.addWidget(self.editor_theme_name_input)
        editor_themes_layout.addRow("Theme:", editor_theme_name_layout)

        # Theme buttons on a new line
        editor_theme_buttons_layout = QHBoxLayout()
        self.save_editor_theme_button = QPushButton("Save Theme")
        self.save_editor_theme_button.clicked.connect(self.save_editor_theme)
        self.load_editor_theme_button = QPushButton("Load Theme")
        self.load_editor_theme_button.clicked.connect(self.load_editor_theme)
        editor_theme_buttons_layout.addWidget(self.save_editor_theme_button)
        editor_theme_buttons_layout.addWidget(self.load_editor_theme_button)
        editor_themes_layout.addRow("", editor_theme_buttons_layout)

        editor_themes_group.setLayout(editor_themes_layout)
        third_column.addWidget(editor_themes_group)

        # Add columns to the grid
        settings_grid.addLayout(first_column, 0, 0)
        settings_grid.addLayout(second_column, 0, 1)
        settings_grid.addLayout(third_column, 0, 2)

        scroll_layout.addLayout(settings_grid)

        # Add buttons at the bottom
        button_layout = QHBoxLayout()

        # Add Reset to Defaults button on the left
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.setToolTip("Reset all settings to default values")
        self.reset_button.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_button)

        # Add spacer to push OK/Cancel to the right
        button_layout.addStretch()

        # Add OK/Cancel buttons
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        layout.addLayout(button_layout)

        # Store current colors
        self.current_colors = {}

    def choose_color(self, color_type):
        """Open color dialog and update button background."""
        color = QColorDialog.getColor()
        if color.isValid():
            # Get the color in a consistent format
            color_hex = color.name(QColor.NameFormat.HexRgb)
            button = getattr(self, f"{color_type}_color")
            button.setStyleSheet(f"background-color: {color_hex}")
            self.current_colors[color_type] = color_hex

            # If this is a syntax highlighting color, update the settings and highlighter
            if color_type in ["keywords", "strings", "numbers", "comments",
                            "operators", "functions", "punctuation"]:
                # Get the parent window to access the code editor
                parent = self.parent()
                if parent and hasattr(parent, 'code_editor'):
                    # Update the settings manager with the new color
                    if hasattr(parent, 'settings_manager'):
                        settings = parent.settings_manager.get_settings()
                        if 'syntax_highlighting' not in settings:
                            settings['syntax_highlighting'] = {}
                        settings['syntax_highlighting'][color_type] = color_hex
                        parent.settings_manager.set_settings(settings)
                        parent.settings_manager.save_settings()
                        print(f"Updated settings manager with new {color_type} color: {color_hex}")  # Debug print

                    # Update the highlighter
                    if hasattr(parent, 'highlighter'):
                        parent.highlighter.update_highlighting_rules()
                        parent.highlighter.rehighlight()
                        print(f"Updated main editor highlighter with new {color_type} color")  # Debug print

                    # Also update the helper editor highlighter
                    if hasattr(parent, 'helpers_highlighter'):
                        parent.helpers_highlighter.update_highlighting_rules()
                        parent.helpers_highlighter.rehighlight()
                        print(f"Updated helper editor highlighter with new {color_type} color")  # Debug print

    def get_settings(self):
        """Get all settings from the dialog."""
        settings = {
            "template_editor": {
                "font_family": self.template_font_family.currentText(),
                "font_size": self.template_font_size.value(),
                "text_color": self.current_colors.get("template_text", "#FFFFFF"),
                "background_color": self.current_colors.get("template_bg", "#000000")
            },
            "code_editor": {
                "font_family": self.code_font_family.currentText(),
                "font_size": self.code_font_size.value(),
                "text_color": self.current_colors.get("code_text", "#FFFFFF"),
                "background_color": self.current_colors.get("code_bg", "#000000")
            },
            "helper_editor": {
                "font_family": self.helper_font_family.currentText(),
                "font_size": self.helper_font_size.value(),
                "text_color": self.current_colors.get("helper_text", "#FFFFFF"),
                "background_color": self.current_colors.get("helper_bg", "#000000   ")
            },
            "data_files": {
                "font_family": self.data_files_font_family.currentText(),
                "font_size": self.data_files_font_size.value(),
                "text_color": self.current_colors.get("data_files_text", "#FFFFFF"),
                "background_color": self.current_colors.get("data_files_bg", "#000000")
            },
            "syntax_highlighting": {
                "keywords": self.current_colors.get("keywords", "#569CD6"),
                "strings": self.current_colors.get("strings", "#CE9178"),
                "numbers": self.current_colors.get("numbers", "#E07912"),
                "comments": self.current_colors.get("comments", "#6A9955"),
                "operators": self.current_colors.get("operators", "#DCDCAA"),
                "functions": self.current_colors.get("functions", "#DCDCAA"),
                "punctuation": self.current_colors.get("punctuation", "#D4D4D4")
            },
            "code_formatting": {
                "auto_format_on_save": self.auto_format_on_save.isChecked(),
                "line_length": self.line_length.value(),
                "skip_string_normalization": self.skip_string_normalization.isChecked()
            },
            "code_linting": {
                "auto_lint_on_save": self.auto_lint_on_save.isChecked(),
                "disabled_checks": self.disabled_checks.text(),
                "threshold": self.linting_threshold.value()
            }
        }
        return settings

    def set_settings(self, settings):
        """Set all settings in the dialog."""
        # Set template editor settings
        if "template_editor" in settings:
            template = settings["template_editor"]
            self.template_font_family.setCurrentText(template.get("font_family", "Arial"))
            self.template_font_size.setValue(template.get("font_size", 12))
            self.template_text_color.setStyleSheet(f"background-color: {template.get('text_color', '#FFFFFF')}")
            self.template_bg_color.setStyleSheet(f"background-color: {template.get('background_color', '#000000')}")
            self.current_colors["template_text"] = template.get("text_color", "#FFFFFF")
            self.current_colors["template_bg"] = template.get("background_color", "#000000")

        # Set code editor settings
        if "code_editor" in settings:
            code = settings["code_editor"]
            self.code_font_family.setCurrentText(code.get("font_family", "Courier New"))
            self.code_font_size.setValue(code.get("font_size", 12))
            self.code_text_color.setStyleSheet(f"background-color: {code.get('text_color', '#FFFFFF')}")
            self.code_bg_color.setStyleSheet(f"background-color: {code.get('background_color', '#000000')}")
            self.current_colors["code_text"] = code.get("text_color", "#FFFFFF")
            self.current_colors["code_bg"] = code.get("background_color", "#000000")

        # Set helper editor settings
        if "helper_editor" in settings:
            helper = settings["helper_editor"]
            self.helper_font_family.setCurrentText(helper.get("font_family", "Courier New"))
            self.helper_font_size.setValue(helper.get("font_size", 12))
            self.helper_text_color.setStyleSheet(f"background-color: {helper.get('text_color', '#FFFFFF')}")
            self.helper_bg_color.setStyleSheet(f"background-color: {helper.get('background_color', '#000000')}")
            self.current_colors["helper_text"] = helper.get("text_color", "#FFFFFF")
            self.current_colors["helper_bg"] = helper.get("background_color", "#000000")

        # Set data files settings
        if "data_files" in settings:
            data_files = settings["data_files"]
            self.data_files_font_family.setCurrentText(data_files.get("font_family", "Courier New"))
            self.data_files_font_size.setValue(data_files.get("font_size", 12))
            self.data_files_text_color.setStyleSheet(f"background-color: {data_files.get('text_color', '#FFFFFF')}")
            self.data_files_bg_color.setStyleSheet(f"background-color: {data_files.get('background_color', '#000000')}")
            self.current_colors["data_files_text"] = data_files.get("text_color", "#FFFFFF")
            self.current_colors["data_files_bg"] = data_files.get("background_color", "#000000")

        # Set syntax highlighting settings
        if "syntax_highlighting" in settings:
            syntax = settings["syntax_highlighting"]
            for element in ["keywords", "strings", "numbers", "comments",
                          "operators", "functions", "punctuation"]:
                if element in syntax:  # Only process elements that exist in the settings
                    color = syntax.get(element, "#000000")
                    button = getattr(self, f"{element}_color")
                    button.setStyleSheet(f"background-color: {color}")
                    self.current_colors[element] = color

        # Set code formatting settings
        if "code_formatting" in settings:
            formatting = settings["code_formatting"]
            self.auto_format_on_save.setChecked(formatting.get("auto_format_on_save", False))
            self.line_length.setValue(formatting.get("line_length", 88))
            self.skip_string_normalization.setChecked(formatting.get("skip_string_normalization", False))

        # Set linting settings
        if "code_linting" in settings:
            linting = settings["code_linting"]
            self.auto_lint_on_save.setChecked(linting.get("auto_lint_on_save", False))
            self.disabled_checks.setText(linting.get("disabled_checks", ""))
            self.linting_threshold.setValue(linting.get("threshold", 7))

    def save_syntax_theme(self):
        """Save the current syntax highlighting colors to a theme file."""
        theme_name = self.syntax_theme_name_input.text().strip()
        if not theme_name:
            QMessageBox.warning(self, "Warning", "Please enter a syntax theme name")
            return

        theme = {
            "name": theme_name,
            "type": "syntax",
            "colors": {
                "keywords": self.current_colors.get("keywords", "#569CD6"),
                "strings": self.current_colors.get("strings", "#CE9178"),
                "numbers": self.current_colors.get("numbers", "#E07912"),
                "comments": self.current_colors.get("comments", "#6A9955"),
                "operators": self.current_colors.get("operators", "#DCDCAA"),
                "functions": self.current_colors.get("functions", "#DCDCAA"),
                "punctuation": self.current_colors.get("punctuation", "#D4D4D4")
            }
        }

        # Get the themes directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        themes_dir = os.path.join(current_dir, "themes")
        print(f"Creating themes directory at: {themes_dir}")  # Debug print

        try:
            os.makedirs(themes_dir, exist_ok=True)
            # Create filename from theme name
            filename = f"syntax_{theme_name.lower().replace(' ', '_')}.json"
            file_path = os.path.join(themes_dir, filename)
            print(f"Saving syntax theme to: {file_path}")  # Debug print

            with open(file_path, 'w') as f:
                json.dump(theme, f, indent=4)
            QMessageBox.information(self, "Success", f"Syntax theme '{theme_name}' saved successfully!\nLocation: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save syntax theme: {str(e)}")

    def save_editor_theme(self):
        """Save the current editor font and color settings to a theme file."""
        theme_name = self.editor_theme_name_input.text().strip()
        if not theme_name:
            QMessageBox.warning(self, "Warning", "Please enter an editor theme name")
            return

        # Collect all editor settings
        theme = {
            "name": theme_name,
            "type": "editor",
            "settings": {
                "template_editor": {
                    "font_family": self.template_font_family.currentText(),
                    "font_size": self.template_font_size.value(),
                    "text_color": self.current_colors.get("template_text", "#FFFFFF"),
                    "background_color": self.current_colors.get("template_bg", "#000000")
                },
                "code_editor": {
                    "font_family": self.code_font_family.currentText(),
                    "font_size": self.code_font_size.value(),
                    "text_color": self.current_colors.get("code_text", "#FFFFFF"),
                    "background_color": self.current_colors.get("code_bg", "#000000")
                },
                "helper_editor": {
                    "font_family": self.helper_font_family.currentText(),
                    "font_size": self.helper_font_size.value(),
                    "text_color": self.current_colors.get("helper_text", "#FFFFFF"),
                    "background_color": self.current_colors.get("helper_bg", "#000000")
                },
                "data_files": {
                    "font_family": self.data_files_font_family.currentText(),
                    "font_size": self.data_files_font_size.value(),
                    "text_color": self.current_colors.get("data_files_text", "#FFFFFF"),
                    "background_color": self.current_colors.get("data_files_bg", "#000000")
                }
            }
        }

        # Get the themes directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        themes_dir = os.path.join(current_dir, "themes")
        print(f"Creating themes directory at: {themes_dir}")  # Debug print

        try:
            os.makedirs(themes_dir, exist_ok=True)
            # Create filename from theme name
            filename = f"editor_{theme_name.lower().replace(' ', '_')}.json"
            file_path = os.path.join(themes_dir, filename)
            print(f"Saving editor theme to: {file_path}")  # Debug print

            with open(file_path, 'w') as f:
                json.dump(theme, f, indent=4)
            QMessageBox.information(self, "Success", f"Editor theme '{theme_name}' saved successfully!\nLocation: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save editor theme: {str(e)}")

    def load_syntax_theme(self):
        """Load a syntax highlighting theme from a file."""
        # Get the themes directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        themes_dir = os.path.join(current_dir, "themes")
        print(f"Looking for syntax themes in: {themes_dir}")  # Debug print

        try:
            # Create themes directory if it doesn't exist
            os.makedirs(themes_dir, exist_ok=True)

            # Get list of theme files (filter for syntax themes)
            theme_files = [f for f in os.listdir(themes_dir) if f.endswith('.json')]
            syntax_theme_files = []

            # Check each file to see if it's a syntax theme
            for theme_file in theme_files:
                try:
                    with open(os.path.join(themes_dir, theme_file), 'r') as f:
                        theme_data = json.load(f)
                        if theme_data.get('type') == 'syntax' or 'colors' in theme_data:
                            syntax_theme_files.append(theme_file)
                except:
                    # If we can't read the file, skip it
                    pass

            print(f"Found syntax theme files: {syntax_theme_files}")  # Debug print

            if not syntax_theme_files:
                QMessageBox.information(
                    self,
                    "No Syntax Themes Found",
                    f"No syntax theme files found in {themes_dir}\n\n"
                    "To create a syntax theme:\n"
                    "1. Adjust the syntax highlighting colors\n"
                    "2. Enter a syntax theme name\n"
                    "3. Click 'Save Theme'"
                )
                return

            # Create dialog to select theme
            theme_dialog = QDialog(self)
            theme_dialog.setWindowTitle("Select Syntax Theme")
            theme_dialog.setModal(True)

            layout = QVBoxLayout(theme_dialog)

            # Create theme list
            theme_list = QComboBox()
            theme_names = []
            theme_data = {}  # Store theme data for each file

            for theme_file in syntax_theme_files:
                try:
                    with open(os.path.join(themes_dir, theme_file), 'r') as f:
                        theme = json.load(f)
                        theme_name = theme.get('name', theme_file[:-5])
                        theme_names.append(theme_name)
                        theme_data[theme_name] = theme
                        print(f"Loaded syntax theme '{theme_name}' from {theme_file}")  # Debug print
                except Exception as e:
                    print(f"Error loading syntax theme {theme_file}: {str(e)}")  # Debug print
                    theme_names.append(theme_file[:-5])

            theme_list.addItems(theme_names)
            layout.addWidget(theme_list)

            # Add buttons
            button_layout = QHBoxLayout()
            load_button = QPushButton("Load")
            cancel_button = QPushButton("Cancel")
            button_layout.addWidget(load_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)

            # Connect buttons
            load_button.clicked.connect(theme_dialog.accept)
            cancel_button.clicked.connect(theme_dialog.reject)

            if theme_dialog.exec() == QDialog.DialogCode.Accepted:
                selected_theme_name = theme_list.currentText()
                print(f"Selected syntax theme: {selected_theme_name}")  # Debug print

                if selected_theme_name in theme_data:
                    theme = theme_data[selected_theme_name]
                    colors = theme.get('colors', {})
                    print(f"Applying syntax theme colors: {colors}")  # Debug print

                    # Update colors in the dialog
                    for element, color in colors.items():
                        if element in ["keywords", "strings", "numbers", "comments",
                                     "operators", "functions", "punctuation"]:
                            button = getattr(self, f"{element}_color")
                            button.setStyleSheet(f"background-color: {color}")
                            self.current_colors[element] = color
                            print(f"Set {element} color to {color}")  # Debug print

                    # Get the parent window to access the code editor
                    parent = self.parent()
                    if parent and hasattr(parent, 'code_editor'):
                        # Update the settings manager with the new colors
                        if hasattr(parent, 'settings_manager'):
                            settings = parent.settings_manager.get_settings()
                            if 'syntax_highlighting' not in settings:
                                settings['syntax_highlighting'] = {}
                            settings['syntax_highlighting'].update(colors)
                            parent.settings_manager.set_settings(settings)
                            parent.settings_manager.save_settings()
                            print("Updated settings manager with new colors")  # Debug print

                        # Update the highlighter
                        if hasattr(parent, 'highlighter'):
                            parent.highlighter.update_highlighting_rules()
                            parent.highlighter.rehighlight()
                            print("Updated main editor highlighter")  # Debug print

                        # Also update the helper editor highlighter
                        if hasattr(parent, 'helpers_highlighter'):
                            parent.helpers_highlighter.update_highlighting_rules()
                            parent.helpers_highlighter.rehighlight()
                            print("Updated helper editor highlighter")  # Debug print

                    QMessageBox.information(self, "Success", f"Syntax theme '{theme['name']}' loaded successfully!")
                else:
                    QMessageBox.critical(self, "Error", f"Could not find theme data for '{selected_theme_name}'")
        except Exception as e:
            print(f"Error in load_syntax_theme: {str(e)}")  # Debug print
            QMessageBox.critical(self, "Error", f"Failed to access themes directory: {str(e)}")

    def load_editor_theme(self):
        """Load an editor theme from a file."""
        # Get the themes directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        themes_dir = os.path.join(current_dir, "themes")
        print(f"Looking for editor themes in: {themes_dir}")  # Debug print

        try:
            # Create themes directory if it doesn't exist
            os.makedirs(themes_dir, exist_ok=True)

            # Get list of theme files (filter for editor themes)
            theme_files = [f for f in os.listdir(themes_dir) if f.endswith('.json')]
            editor_theme_files = []

            # Check each file to see if it's an editor theme
            for theme_file in theme_files:
                try:
                    with open(os.path.join(themes_dir, theme_file), 'r') as f:
                        theme_data = json.load(f)
                        if theme_data.get('type') == 'editor' or 'settings' in theme_data:
                            editor_theme_files.append(theme_file)
                except:
                    # If we can't read the file, skip it
                    pass

            print(f"Found editor theme files: {editor_theme_files}")  # Debug print

            if not editor_theme_files:
                QMessageBox.information(
                    self,
                    "No Editor Themes Found",
                    f"No editor theme files found in {themes_dir}\n\n"
                    "To create an editor theme:\n"
                    "1. Adjust the editor font and color settings\n"
                    "2. Enter an editor theme name\n"
                    "3. Click 'Save Theme'"
                )
                return

            # Create dialog to select theme
            theme_dialog = QDialog(self)
            theme_dialog.setWindowTitle("Select Editor Theme")
            theme_dialog.setModal(True)

            layout = QVBoxLayout(theme_dialog)

            # Create theme list
            theme_list = QComboBox()
            theme_names = []
            theme_data = {}  # Store theme data for each file

            for theme_file in editor_theme_files:
                try:
                    with open(os.path.join(themes_dir, theme_file), 'r') as f:
                        theme = json.load(f)
                        theme_name = theme.get('name', theme_file[:-5])
                        theme_names.append(theme_name)
                        theme_data[theme_name] = theme
                        print(f"Loaded editor theme '{theme_name}' from {theme_file}")  # Debug print
                except Exception as e:
                    print(f"Error loading editor theme {theme_file}: {str(e)}")  # Debug print
                    theme_names.append(theme_file[:-5])

            theme_list.addItems(theme_names)
            layout.addWidget(theme_list)

            # Add buttons
            button_layout = QHBoxLayout()
            load_button = QPushButton("Load")
            cancel_button = QPushButton("Cancel")
            button_layout.addWidget(load_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)

            # Connect buttons
            load_button.clicked.connect(theme_dialog.accept)
            cancel_button.clicked.connect(theme_dialog.reject)

            if theme_dialog.exec() == QDialog.DialogCode.Accepted:
                selected_theme_name = theme_list.currentText()
                print(f"Selected editor theme: {selected_theme_name}")  # Debug print

                if selected_theme_name in theme_data:
                    theme = theme_data[selected_theme_name]
                    settings = theme.get('settings', {})
                    print(f"Applying editor theme settings: {settings}")  # Debug print

                    # Apply the settings to the dialog
                    self.set_settings(settings)

                    # Get the parent window to access the settings manager
                    parent = self.parent()
                    if parent and hasattr(parent, 'settings_manager'):
                        # Update the settings manager with the new settings
                        parent_settings = parent.settings_manager.get_settings()

                        # Update each editor section
                        for section in ["template_editor", "code_editor", "helper_editor", "data_files"]:
                            if section in settings:
                                parent_settings[section] = settings[section]

                        parent.settings_manager.set_settings(parent_settings)
                        parent.settings_manager.save_settings()
                        print("Updated settings manager with new editor settings")  # Debug print

                    QMessageBox.information(self, "Success", f"Editor theme '{theme['name']}' loaded successfully!")
                else:
                    QMessageBox.critical(self, "Error", f"Could not find theme data for '{selected_theme_name}'")
        except Exception as e:
            print(f"Error in load_editor_theme: {str(e)}")  # Debug print
            QMessageBox.critical(self, "Error", f"Failed to access themes directory: {str(e)}")

    def reset_to_defaults(self):
        """Reset all settings to default values in the dialog and delete the settings file."""
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Reset to Defaults",
            "Are you sure you want to reset all settings to their default values?\n\n"
            "This will reset all settings to their defaults and cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Get the settings file path
                current_dir = os.path.dirname(os.path.abspath(__file__))
                settings_dir = os.path.join(current_dir, 'settings')
                settings_file = os.path.join(settings_dir, 'settings.json')

                # Delete the settings file if it exists
                if os.path.exists(settings_file):
                    os.remove(settings_file)

                # Load default settings
                default_settings = self.get_default_settings()

                # Apply default settings to the dialog
                self.set_settings(default_settings)

                QMessageBox.information(
                    self,
                    "Settings Reset",
                    "Settings have been reset to defaults.\n\n"
                    "Click OK to apply these default settings to the application."
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to reset settings: {str(e)}"
                )

    def get_default_settings(self):
        """Return the default settings."""
        return {
            "problem_text": {
                "font_family": "Courier New",
                "font_size": 12,
                "text_color": "#FFFFFF",
                "background_color": "#000000"
            },
            "code_editor": {
                "font_family": "Courier New",
                "font_size": 12,
                "text_color": "#FFFFFF",
                "background_color": "#000000"
            },
            "helper_editor": {
                "font_family": "Courier New",
                "font_size": 12,
                "text_color": "#FFFFFF",
                "background_color": "#000000"
            },
            "template_editor": {
                "font_family": "Courier New",
                "font_size": 12,
                "text_color": "#FFFFFF",
                "background_color": "#000000"
            },
            "data_files": {
                "font_family": "Courier New",
                "font_size": 12,
                "text_color": "#FFFFFF",
                "background_color": "#000000"
            },
            "syntax_highlighting": {
                "keywords": "#569CD6",
                "strings": "#CE9178",
                "numbers": "#E07912",
                "comments": "#6A9955",
                "operators": "#DCDCAA",
                "functions": "#DCDCAA",
                "punctuation": "#D4D4D4"
            },
            "theme": "dark",
            "debug": {
                "enabled": True,
                "levels": {
                    "debug": True,
                    "important": True,
                    "info": True,
                    "error": True,
                    "detail": True,
                    "trace": True
                },
                "show_timestamps": False
            },
            "code_formatting": {
                "auto_format_on_save": False,
                "line_length": 88,
                "skip_string_normalization": False
            },
            "code_linting": {
                "auto_lint_on_save": False,
                "disabled_checks": "",
                "threshold": 7
            }
        }