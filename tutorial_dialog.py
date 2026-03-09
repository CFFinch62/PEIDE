from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QTextEdit, QMessageBox, QProgressBar,
                            QTextBrowser, QScrollArea, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont

class TutorialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tutorial")
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        # Set a reasonable default size
        self.resize(800, 600)

        # Store reference to main window
        self.main_window = parent

        # Initialize highlight variables
        self.highlighted_elements = []  # List to store highlighted elements
        self.original_styles = {}  # Dictionary to store original styles

        # Set global style for the dialog to match dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
        """)

        # Create layout
        layout = QVBoxLayout()
        # Add some spacing and margins for better appearance
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create title label with improved styling
        self.title_label = QLabel()
        self.title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #56a0d3;
            padding: 5px;
            border-bottom: 1px solid #3d3d3d;
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Create content area with scrolling capability
        self.content_browser = QTextBrowser()
        self.content_browser.setOpenExternalLinks(True)
        self.content_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3d3d3d;
                padding: 10px;
                font-size: 14px;
            }
        """)
        # Set a minimum height for the content area
        self.content_browser.setMinimumHeight(200)
        layout.addWidget(self.content_browser)

        # Create progress bar with improved styling
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                text-align: center;
                height: 20px;
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #007acc;
                border-radius: 5px;
            }
        """)
        self.progress_bar.setFormat("Step %v of %m")
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        # Create navigation buttons with improved styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Define button style for dark theme
        button_style = """
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0098ff;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #6d6d6d;
            }
        """

        self.prev_button = QPushButton("← Previous")
        self.prev_button.setStyleSheet(button_style)
        self.prev_button.clicked.connect(self.previous_step)

        self.next_button = QPushButton("Next →")
        self.next_button.setStyleSheet(button_style)
        self.next_button.clicked.connect(self.next_step)

        self.close_button = QPushButton("Close Tutorial")
        self.close_button.setStyleSheet(button_style)
        self.close_button.clicked.connect(self.close)

        button_layout.addWidget(self.prev_button)
        button_layout.addStretch(1)  # Add stretch for better spacing
        button_layout.addWidget(self.next_button)
        button_layout.addStretch(1)  # Add stretch for better spacing
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Initialize tutorial state
        self.current_tutorial = None
        self.current_step = 0

        # No animation is used for highlighting - we use simple yellow borders and text

        # Load tutorials
        self.load_tutorials()

    def load_tutorials(self):
        """Load tutorials from the tutorial manager."""
        from tutorial_manager import TutorialManager
        self.tutorial_manager = TutorialManager()
        self.tutorials = self.tutorial_manager.load_tutorials()

    def start_tutorial(self, tutorial_name):
        """Start a specific tutorial."""
        self.current_tutorial = self.tutorial_manager.get_tutorial(tutorial_name)
        if self.current_tutorial:
            self.current_step = 0
            self.update_display()
            self.show()

    def update_display(self):
        """Update the display with current tutorial step."""
        if not self.current_tutorial:
            return

        step = self.current_tutorial["steps"][self.current_step]
        self.title_label.setText(step["title"])

        # Set content in the QTextBrowser, which supports HTML formatting and scrolling
        content = step["content"]
        # Convert newlines to HTML breaks for proper formatting
        content = content.replace("\n", "<br>")
        # Wrap content in a div with explicit styling for dark theme
        formatted_content = f"""
        <div style="color: #d4d4d4; font-size: 14px; line-height: 1.5;">
            {content}
        </div>
        """
        self.content_browser.setHtml(formatted_content)

        # Update progress bar
        total_steps = len(self.current_tutorial["steps"])
        self.progress_bar.setMaximum(total_steps - 1)
        self.progress_bar.setValue(self.current_step)

        # Update button states
        self.prev_button.setEnabled(self.current_step > 0)
        self.next_button.setEnabled(self.current_step < total_steps - 1)

        # Handle step actions
        self.handle_step_action(step)

    def handle_step_action(self, step):
        """Handle the action specified in the current step."""
        action_str = step.get("action", "none")
        params = step.get("params", {})

        # Clear any existing highlights
        self.clear_highlights()

        # Handle multiple actions separated by commas
        if "," in action_str:
            actions = action_str.split(",")
            for action in actions:
                self._execute_single_action(action.strip(), params)
        else:
            self._execute_single_action(action_str, params)

    def _execute_single_action(self, action, params):
        """Execute a single action with the given parameters."""
        if action == "highlight_areas":
            areas = params.get("areas", [])
            self.highlight_interface_areas(areas)
        elif action == "highlight_button":
            button = params.get("button")
            self.highlight_button(button)
        elif action == "select_problem":
            problem_number = params.get("problem_number")
            if problem_number and self.main_window:
                self.main_window.load_problem_by_number(problem_number)
        elif action == "run_code":
            if self.main_window:
                self.main_window.run_code()
        elif action == "show_dialog":
            dialog_name = params.get("dialog")
            self.show_dialog(dialog_name)
        elif action == "show_welcome":
            self.show_dialog("welcome")

    def highlight_interface_areas(self, areas=None):
        """Highlight different areas of the interface with yellow borders or bold yellow text."""
        if not self.main_window or not areas:
            return

        # Clear any existing highlights
        self.clear_highlights()

        # Map area names to labels or descriptions based on tutorial_editor_guide.md
        area_labels = {
            "problem_description": "Problem Description",
            "progress_grid": "Progress Grid",
            "data_file_indicator": "Data File Indicator",
            "status_bar": "Status Bar"
        }

        # Map area names to UI elements
        area_widgets = {
            "problem_description": self.main_window.problem_display.problem_description if hasattr(self.main_window, 'problem_display') else None,
            "progress_grid": self.main_window.progress_grid if hasattr(self.main_window, 'progress_grid') else None,
            "data_file_indicator": self.main_window.problem_display.data_file_indicator if hasattr(self.main_window, 'problem_display') else None,
            "status_bar": self.main_window.status_bar if hasattr(self.main_window, 'status_bar') else None
        }

        # Add a message to the tutorial text highlighting the areas
        highlight_message = "Please look at the following areas:\n"

        # Process each area
        for area_name in areas:
            label = area_labels.get(area_name)
            widget = area_widgets.get(area_name)

            if label:
                highlight_message += f"• <span style='color: #FFD700; font-weight: bold;'>{label}</span>\n"

            # Apply custom highlighting based on the area type
            if widget:
                # Store the original style
                self.original_styles[area_name] = widget.styleSheet()

                # Apply different highlighting based on the area type
                if area_name == "progress_grid" and hasattr(self.main_window, 'progress_grid'):
                    # For progress grid, make all squares yellow
                    progress_grid = self.main_window.progress_grid

                    # Store original square styles and make all squares yellow
                    for problem_number, square in progress_grid.problem_squares.items():
                        # Store the original style
                        self.original_styles[f"grid_square_{problem_number}"] = square.styleSheet()

                        # Make the square yellow
                        square.setStyleSheet("""
                            QFrame {
                                background-color: #FFD700;
                                border: 1px solid #3D3D3D;
                            }
                            QFrame:hover {
                                background-color: #FFC000;
                            }
                        """)

                    # Add progress grid to highlighted elements
                    self.highlighted_elements.append("progress_grid_squares")
                elif area_name == "problem_description" and hasattr(self.main_window, 'problem_display'):
                    # For problem description, make the text bold and yellow
                    problem_description = self.main_window.problem_display.problem_description

                    # Store the original text and style
                    self.original_styles["problem_description_text"] = problem_description.toPlainText()
                    self.original_styles["problem_description_style"] = problem_description.styleSheet()

                    # Apply bold yellow style to the text
                    problem_description.setStyleSheet("""
                        QTextEdit {
                            color: #FFD700;
                            font-weight: bold;
                            background-color: #000000;
                            border: none;
                            padding: 10px;
                            font-family: Arial;
                            font-size: 12pt;
                        }
                    """)

                    # Add to highlighted elements
                    self.highlighted_elements.append("problem_description_text")

                elif area_name == "data_file_indicator" and hasattr(self.main_window, 'problem_display'):
                    # For data file indicator, make the text bold and yellow
                    data_file_indicator = self.main_window.problem_display.data_file_indicator
                    if data_file_indicator.isVisible():
                        # Store the original text and style
                        self.original_styles["data_file_indicator_text"] = data_file_indicator.text()
                        self.original_styles["data_file_indicator_style"] = data_file_indicator.styleSheet()

                        # Apply bold yellow style
                        data_file_indicator.setStyleSheet("""
                            QLabel {
                                color: #FFD700;
                                font-weight: bold;
                                background-color: #2D2D2D;
                                padding: 5px;
                                border: 1px solid #3D3D3D;
                                border-radius: 3px;
                            }
                        """)

                        # Add to highlighted elements
                        self.highlighted_elements.append("data_file_indicator_text")
                else:
                    # For other widgets, apply standard yellow border
                    widget.setStyleSheet(widget.styleSheet() + """
                        border: 2px solid #FFD700;
                        border-radius: 4px;
                    """)

        # Add the highlight message to the current content
        current_html = self.content_browser.toHtml()
        if "<hr>" in current_html:
            # Insert before the horizontal rule
            current_html = current_html.replace("<hr>", f"<p>{highlight_message}</p><hr>")
        else:
            # Append to the end
            current_html += f"<p>{highlight_message}</p>"

        self.content_browser.setHtml(current_html)

        # Store the highlighted areas
        self.highlighted_elements.extend(areas)

    def highlight_button(self, button_name):
        """Highlight a specific button with a simple yellow box (non-blinking)."""
        if not self.main_window or not button_name:
            return

        # Clear any existing highlights
        self.clear_highlights()

        # Map button names to UI elements based on tutorial_editor_guide.md
        button_map = {
            "run": self.main_window.run_button if hasattr(self.main_window, 'run_button') else None,
            "hint": self.main_window.hint_button if hasattr(self.main_window, 'hint_button') else None,
            "save": self.main_window.save_button if hasattr(self.main_window, 'save_button') else None,
            "mark_solved": self.main_window.mark_solved_button if hasattr(self.main_window, 'mark_solved_button') else None,
            "run_button": self.main_window.run_button if hasattr(self.main_window, 'run_button') else None
        }

        # Map button names to display names
        button_display_names = {
            "run": "Run Code",
            "hint": "Get Hint",
            "save": "Save Solution",
            "mark_solved": "Mark as Solved",
            "run_button": "Run Code"
        }

        # Handle tab buttons if tab_widget exists
        if hasattr(self.main_window, 'tab_widget') and self.main_window.tab_widget:
            tab_widget = self.main_window.tab_widget

            # Map tab button names to tab indices
            tab_button_map = {
                "solution_tab": self.main_window.solution_tab_index if hasattr(self.main_window, 'solution_tab_index') else None,
                "helper_files_tab": self.main_window.helpers_tab_index if hasattr(self.main_window, 'helpers_tab_index') else None,
                "code_templates_tab": self.main_window.templates_tab_index if hasattr(self.main_window, 'templates_tab_index') else None,
                "data_files_tab": self.main_window.data_files_tab_index if hasattr(self.main_window, 'data_files_tab_index') else None,
                "debug_tab": self.main_window.debug_tab_index if hasattr(self.main_window, 'debug_tab_index') else None
            }

            # Map tab button names to display names
            tab_button_display_names = {
                "solution_tab": "Solution",
                "helper_files_tab": "Helper Files",
                "code_templates_tab": "Code Templates",
                "data_files_tab": "Data Files",
                "debug_tab": "Debug Output"
            }

            # Check if this is a tab button
            if button_name in tab_button_map:
                tab_index = tab_button_map.get(button_name)
                if tab_index is not None:
                    # Switch to the tab
                    tab_widget.setCurrentIndex(tab_index)

                    # Get the tab bar
                    tab_bar = tab_widget.tabBar()

                    # Store the original style
                    self.original_styles[button_name] = tab_bar.tabTextColor(tab_index)

                    # Set the tab text to bold yellow
                    tab_bar.setTabTextColor(tab_index, QColor("#FFD700"))

                    # Make the tab text bold
                    font = tab_bar.font()
                    font.setBold(True)
                    tab_bar.setFont(font)

                    # Add a message to the tutorial text
                    display_name = tab_button_display_names.get(button_name, button_name)
                    self.add_highlight_message(f"Please click on the <span style='color: #FFD700; font-weight: bold;'>{display_name}</span> tab")

                    # Store the highlighted button
                    self.highlighted_elements.append(button_name)

                    # Return early since we've handled this tab button
                    return

        # Highlight the button with a simple yellow box (non-blinking)
        button = button_map.get(button_name)
        if button and button.isVisible():
            # Store the original style
            self.original_styles[button_name] = button.styleSheet()

            # Apply a simple yellow box (non-blinking)
            button.setStyleSheet(button.styleSheet() + """
                border: 2px solid #FFD700;
                border-radius: 4px;
            """)

            # Add a message to the tutorial text
            display_name = button_display_names.get(button_name, button_name)
            self.add_highlight_message(f"Please click on the <span style='color: #FFD700; font-weight: bold;'>{display_name}</span> button")

            # Store the highlighted button
            self.highlighted_elements.append(button_name)

    def add_highlight_message(self, message):
        """Add a highlight message to the tutorial text."""
        current_html = self.content_browser.toHtml()
        if "<hr>" in current_html:
            # Insert before the horizontal rule
            current_html = current_html.replace("<hr>", f"<p>{message}</p><hr>")
        else:
            # Append to the end
            current_html += f"<p>{message}</p>"

        self.content_browser.setHtml(current_html)

    def clear_highlights(self):
        """Clear all highlights."""
        # Map button names to UI elements based on tutorial_editor_guide.md
        button_map = {
            "run": self.main_window.run_button if hasattr(self.main_window, 'run_button') else None,
            "hint": self.main_window.hint_button if hasattr(self.main_window, 'hint_button') else None,
            "save": self.main_window.save_button if hasattr(self.main_window, 'save_button') else None,
            "mark_solved": self.main_window.mark_solved_button if hasattr(self.main_window, 'mark_solved_button') else None,
            "run_button": self.main_window.run_button if hasattr(self.main_window, 'run_button') else None
        }

        # Map area names to UI elements
        area_widgets = {
            "problem_description": self.main_window.problem_display.problem_description if hasattr(self.main_window, 'problem_display') else None,
            "progress_grid": self.main_window.progress_grid if hasattr(self.main_window, 'progress_grid') else None,
            "data_file_indicator": self.main_window.problem_display.data_file_indicator if hasattr(self.main_window, 'problem_display') else None,
            "status_bar": self.main_window.status_bar if hasattr(self.main_window, 'status_bar') else None
        }

        # Tab indices map for tab buttons
        tab_map = {
            "solution_tab": self.main_window.solution_tab_index if hasattr(self.main_window, 'solution_tab_index') else None,
            "helper_files_tab": self.main_window.helpers_tab_index if hasattr(self.main_window, 'helpers_tab_index') else None,
            "code_templates_tab": self.main_window.templates_tab_index if hasattr(self.main_window, 'templates_tab_index') else None,
            "data_files_tab": self.main_window.data_files_tab_index if hasattr(self.main_window, 'data_files_tab_index') else None,
            "debug_tab": self.main_window.debug_tab_index if hasattr(self.main_window, 'debug_tab_index') else None
        }

        # Restore original styles for all elements
        for element_name, original_style in self.original_styles.items():
            # Check if it's a button
            button = button_map.get(element_name)
            if button:
                button.setStyleSheet(original_style)
                continue

            # Check if it's an area widget
            widget = area_widgets.get(element_name)
            if widget:
                widget.setStyleSheet(original_style)
                continue

            # Check if it's a progress grid square
            if element_name.startswith("grid_square_") and hasattr(self.main_window, 'progress_grid'):
                problem_number = int(element_name.replace("grid_square_", ""))
                square = self.main_window.progress_grid.problem_squares.get(problem_number)
                if square:
                    square.setStyleSheet(original_style)
                continue

            # Check if it's the problem description text
            if element_name == "problem_description_text" and hasattr(self.main_window, 'problem_display'):
                problem_description = self.main_window.problem_display.problem_description
                # Restore the original style
                problem_description.setStyleSheet(self.original_styles.get("problem_description_style", ""))
                continue

            # Check if it's the data file indicator text
            if element_name == "data_file_indicator_text" and hasattr(self.main_window, 'problem_display'):
                data_file_indicator = self.main_window.problem_display.data_file_indicator
                # Restore the original style
                data_file_indicator.setStyleSheet(self.original_styles.get("data_file_indicator_style", ""))
                continue

            # Check if it's a tab
            tab_index = tab_map.get(element_name)
            if tab_index is not None and hasattr(self.main_window, 'tab_widget'):
                tab_bar = self.main_window.tab_widget.tabBar()

                # Restore tab text color
                if isinstance(original_style, QColor):
                    tab_bar.setTabTextColor(tab_index, original_style)

                # Restore font weight
                font = tab_bar.font()
                font.setBold(False)
                tab_bar.setFont(font)

        # Clear the lists
        self.highlighted_elements = []
        self.original_styles = {}

    def show_dialog(self, dialog_name):
        """Show a specific dialog."""
        if not self.main_window or not dialog_name:
            return

        # Map dialog names to methods
        dialog_map = {
            "welcome": self.main_window.show_welcome_dialog if hasattr(self.main_window, 'show_welcome_dialog') else None,
            "settings": self.main_window.show_settings_dialog if hasattr(self.main_window, 'show_settings_dialog') else None,
            "progress": self.main_window.show_progress_dialog if hasattr(self.main_window, 'show_progress_dialog') else None,
            "about": self.main_window.show_about_dialog if hasattr(self.main_window, 'show_about_dialog') else None,
            "info": self.main_window.show_info_dialog if hasattr(self.main_window, 'show_info_dialog') else None
        }

        # Call the method if it exists
        method = dialog_map.get(dialog_name)
        if method:
            method()

    def previous_step(self):
        """Go to the previous step in the tutorial."""
        # Clear any existing highlights
        self.clear_highlights()

        if self.current_step > 0:
            self.current_step -= 1
            self.update_display()

    def next_step(self):
        """Go to the next step in the tutorial."""
        # Clear any existing highlights
        self.clear_highlights()

        if self.current_step < len(self.current_tutorial["steps"]) - 1:
            self.current_step += 1
            self.update_display()
        else:
            self.close()

    # No animation is used for highlighting - we use simple yellow borders and text

    def closeEvent(self, event):
        """Handle the dialog close event."""
        # Clear any highlights before closing
        self.clear_highlights()

        # Accept the close event
        event.accept()