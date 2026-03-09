import json
import os
from PyQt6.QtGui import QFont

class SettingsManager:
    def __init__(self):
        self.settings_file = self._get_settings_path()
        self.settings = self._load_settings()

    def _get_settings_path(self):
        """Get the path to the settings file in the application directory."""
        # Use the current directory where the application is running
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Create a settings directory if it doesn't exist
        settings_dir = os.path.join(base_dir, 'settings')
        os.makedirs(settings_dir, exist_ok=True)

        return os.path.join(settings_dir, 'settings.json')

    def _load_settings(self):
        """Load settings from file or return defaults if file doesn't exist."""
        default_settings = {
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
            "tutorial_editor": {
                "password": "euler123",  # Default password
                "font_family": "Courier New",
                "font_size": 12,
                "text_color": "#FFFF00",  # Yellow text
                "background_color": "#000066"  # Dark blue background
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

        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Ensure all default settings are present
                    for category, defaults in default_settings.items():
                        if category not in loaded_settings:
                            loaded_settings[category] = defaults
                        elif category == "syntax_highlighting":
                            # Ensure all syntax highlighting elements are present
                            for element, default_color in defaults.items():
                                if element not in loaded_settings[category]:
                                    loaded_settings[category][element] = default_color
                    return loaded_settings
        except Exception as e:
            print(f"Error loading settings: {e}")

        return default_settings

    def save_settings(self):
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError:
            pass

    def get_problem_text_settings(self):
        """Get settings for problem text area."""
        return self.settings["problem_text"]

    def get_code_editor_settings(self):
        """Get settings for code editor area."""
        return self.settings["code_editor"]

    def get_helper_editor_settings(self):
        """Get helper editor settings."""
        return self.settings.get("helper_editor", {
            "font_family": "Courier New",
            "font_size": 12,
            "text_color": "#000000",
            "background_color": "#FFFFFF"
        })

    def get_data_files_settings(self):
        """Get the current data files settings."""
        return self.settings.get("data_files", {
            "font_family": "Courier New",
            "font_size": 12,
            "text_color": "#FFFFFF",
            "background_color": "#000000"
        })

    def get_highlighting_color(self, element):
        """Get the color for a specific syntax highlighting element."""
        if not hasattr(self, 'settings'):
            self.settings = self._load_settings()
        return self.settings.get("syntax_highlighting", {}).get(element, "#000000")

    def update_problem_text_settings(self, font_family, font_size, text_color, background_color):
        """Update problem text settings."""
        self.settings["problem_text"] = {
            "font_family": font_family,
            "font_size": font_size,
            "text_color": text_color,
            "background_color": background_color
        }
        self.save_settings()

    def update_code_editor_settings(self, font_family, font_size, text_color, background_color):
        """Update code editor settings."""
        self.settings["code_editor"] = {
            "font_family": font_family,
            "font_size": font_size,
            "text_color": text_color,
            "background_color": background_color
        }
        self.save_settings()

    def update_helper_editor_settings(self, font_family, font_size, text_color, background_color):
        """Update helper editor settings."""
        if "helper_editor" not in self.settings:
            self.settings["helper_editor"] = {}
        self.settings["helper_editor"].update({
            "font_family": font_family,
            "font_size": font_size,
            "text_color": text_color,
            "background_color": background_color
        })
        self.save_settings()

    def update_data_files_settings(self, settings):
        """Update the data files settings."""
        if "data_files" not in self.settings:
            self.settings["data_files"] = {}
        self.settings["data_files"].update(settings)
        self.save_settings()

    def update_highlighting_colors(self, colors):
        """Update syntax highlighting colors."""
        if "syntax_highlighting" not in self.settings:
            self.settings["syntax_highlighting"] = {}
        self.settings["syntax_highlighting"].update(colors)
        self.save_settings()

    def apply_problem_text_settings(self, text_edit):
        """Apply saved settings to a problem text QTextEdit."""
        settings = self.get_problem_text_settings()
        font = QFont(settings["font_family"], settings["font_size"])
        text_edit.setFont(font)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                color: {settings["text_color"]};
                background-color: {settings["background_color"]};
                border: none;
                padding: 10px;
            }}
        """)

    def apply_code_editor_settings(self, text_edit):
        """Apply saved settings to a code editor QTextEdit or QPlainTextEdit."""
        settings = self.get_code_editor_settings()
        font = QFont(settings["font_family"], settings["font_size"])
        text_edit.setFont(font)

        # Determine the widget type for the stylesheet
        widget_type = "QPlainTextEdit" if hasattr(text_edit, "setLineWrapMode") and hasattr(text_edit, "setTabStopDistance") else "QTextEdit"

        text_edit.setStyleSheet(f"""
            {widget_type} {{
                background-color: {settings["background_color"]};
                color: {settings["text_color"]};
                border: none;
                padding: 10px;
                font-family: '{settings["font_family"]}';
            }}
        """)

    def apply_helper_editor_settings(self, text_edit):
        """Apply saved settings to a helper editor QTextEdit."""
        settings = self.get_helper_editor_settings()

        # Set font
        font = QFont(settings["font_family"], settings["font_size"])
        text_edit.setFont(font)

        # Determine the widget type for the stylesheet
        widget_type = "QPlainTextEdit" if hasattr(text_edit, "setLineWrapMode") and hasattr(text_edit, "setTabStopDistance") else "QTextEdit"

        # Set colors with full styling
        text_edit.setStyleSheet(f"""
            {widget_type} {{
                background-color: {settings['background_color']};
                color: {settings['text_color']};
                border: none;
                padding: 10px;
                font-family: '{settings['font_family']}';
            }}
        """)

    def apply_data_files_settings(self, widget):
        """Apply data files settings to a widget."""
        settings = self.get_data_files_settings()
        font = QFont(settings["font_family"], settings["font_size"])
        widget.setFont(font)
        widget.setStyleSheet(f"""
            QTextEdit {{
                color: {settings["text_color"]};
                background-color: {settings["background_color"]};
                border: none;
                padding: 5px;
            }}
        """)

    def get_settings(self):
        """Get the current settings."""
        return self.settings

    def set_settings(self, settings):
        """Set new settings."""
        self.settings = settings
        self.save_settings()

    def get_template_editor_settings(self):
        """Get template editor settings."""
        return self.settings.get("template_editor", {
            "font_family": "Consolas",
            "font_size": 12,
            "text_color": "#FFFFFF",
            "background_color": "#000000"
        })

    def update_template_editor_settings(self, font_family, font_size, text_color, background_color):
        """Update template editor settings."""
        if "template_editor" not in self.settings:
            self.settings["template_editor"] = {}
        self.settings["template_editor"].update({
            "font_family": font_family,
            "font_size": font_size,
            "text_color": text_color,
            "background_color": background_color
        })
        self.save_settings()

    def apply_template_editor_settings(self, text_edit):
        """Apply template editor settings to the editor."""
        settings = self.get_template_editor_settings()

        # Set font
        font = QFont(settings["font_family"], settings["font_size"])
        text_edit.setFont(font)

        # Determine the widget type for the stylesheet
        widget_type = "QPlainTextEdit" if hasattr(text_edit, "setLineWrapMode") and hasattr(text_edit, "setTabStopDistance") else "QTextEdit"

        # Set colors with full styling
        text_edit.setStyleSheet(f"""
            {widget_type} {{
                background-color: {settings['background_color']};
                color: {settings['text_color']};
                border: none;
                padding: 10px;
                font-family: '{settings['font_family']}';
            }}
        """)

    def get_tutorial_editor_settings(self):
        """Get tutorial editor settings."""
        defaults = {
            "password": "euler123",
            "font_family": "Courier New",
            "font_size": 12,
            "text_color": "#FFFF00",
            "background_color": "#000066"
        }

        # Get existing settings and merge with defaults
        existing = self.settings.get("tutorial_editor", {})
        merged = defaults.copy()
        merged.update(existing)
        return merged

    def get_tutorial_editor_password(self):
        """Get the password for the tutorial editor."""
        tutorial_settings = self.get_tutorial_editor_settings()
        return tutorial_settings.get("password", "euler123")

    def update_tutorial_editor_password(self, password):
        """Update the tutorial editor password."""
        if "tutorial_editor" not in self.settings:
            self.settings["tutorial_editor"] = {}
        self.settings["tutorial_editor"]["password"] = password
        self.save_settings()

    def update_tutorial_editor_settings(self, font_family, font_size, text_color, background_color):
        """Update tutorial editor settings."""
        if "tutorial_editor" not in self.settings:
            self.settings["tutorial_editor"] = {"password": "euler123"}

        self.settings["tutorial_editor"].update({
            "font_family": font_family,
            "font_size": font_size,
            "text_color": text_color,
            "background_color": background_color
        })
        self.save_settings()

    def apply_tutorial_editor_settings(self, widget):
        """Apply tutorial editor settings to a widget."""
        settings = self.get_tutorial_editor_settings()
        font = QFont(settings["font_family"], settings["font_size"])
        widget.setFont(font)

        # Determine the widget type for the stylesheet
        widget_type = "QDialog"
        if hasattr(widget, "setLineWrapMode") and hasattr(widget, "setTabStopDistance"):
            widget_type = "QPlainTextEdit"
        elif hasattr(widget, "toPlainText"):
            widget_type = "QTextEdit"
        elif hasattr(widget, "text"):
            widget_type = "QLineEdit"
        elif hasattr(widget, "addItem"):
            widget_type = "QListWidget"

        widget.setStyleSheet(f"""
            {widget_type} {{
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
                background-color: {self._lighten_color(settings['background_color'])};
            }}
            QPushButton:pressed {{
                background-color: {self._lighten_color(settings['background_color'], 0.4)};
            }}
            QLabel {{
                color: {settings['text_color']};
                font-weight: bold;
                font-family: '{settings['font_family']}';
                font-size: {settings['font_size']}px;
            }}
        """)

    def _lighten_color(self, color_hex, factor=0.2):
        """Lighten a hex color by a given factor."""
        try:
            # Remove the # if present
            color_hex = color_hex.lstrip('#')
            # Convert to RGB
            r = int(color_hex[0:2], 16)
            g = int(color_hex[2:4], 16)
            b = int(color_hex[4:6], 16)
            # Lighten
            r = min(255, int(r + (255 - r) * factor))
            g = min(255, int(g + (255 - g) * factor))
            b = min(255, int(b + (255 - b) * factor))
            # Convert back to hex
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color_hex  # Return original if conversion fails

    def get_formatting_settings(self):
        """Get the code formatting settings."""
        return self.settings.get("code_formatting", {
            "auto_format_on_save": False,
            "line_length": 88,
            "skip_string_normalization": False
        })

    def get_linting_settings(self):
        """Get the code linting settings."""
        return self.settings.get("code_linting", {
            "auto_lint_on_save": False,
            "disabled_checks": "",
            "threshold": 7
        })

    def update_formatting_settings(self, settings):
        """Update the code formatting settings."""
        if "code_formatting" not in self.settings:
            self.settings["code_formatting"] = {}
        self.settings["code_formatting"].update(settings)
        self.save_settings()

    def update_linting_settings(self, settings):
        """Update the code linting settings."""
        if "code_linting" not in self.settings:
            self.settings["code_linting"] = {}
        self.settings["code_linting"].update(settings)
        self.save_settings()
