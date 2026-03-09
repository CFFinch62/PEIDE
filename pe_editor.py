"""
Project Euler Solutions Editor - Main application module.

This module contains the main window and application logic for the
Project Euler Solutions Editor (PE Editor RF 7).
"""

import os
import sys
import traceback
from datetime import datetime

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel,
                            QSplitter, QMessageBox,
                            QProgressBar, QStatusBar, QTabWidget, QDialog, QToolBar,
                            QListWidget)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction, QDesktopServices, QIcon

from problem_manager import ProblemManager
from progress_grid import ProblemGrid
from settings_manager import SettingsManager
from settings_dialog import SettingsDialog
from theme_manager import ThemeManager
from run_manager import RunManager
from ui.code_editor import CodeEditor
from ui.syntax_highlighter import PythonHighlighter
from ui.main_menu import MainMenuBuilder
from ui.data_file_panel import DataFilePanel
from ui.helper_files_panel import HelperFilesPanel
from ui.templates_panel import TemplatesPanel
from ui.problem_display_panel import ProblemDisplayPanel
from ui.progress_integration import ProgressIntegration
from ui.debug_panel import DebugPanel
from ui.debug_integration import DebugIntegration

# Set Qt platform plugin path
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = (
    '/opt/anaconda3/lib/python3.12/site-packages/PyQt6/Qt6/plugins/platforms'
)


class MainWindow(QMainWindow):
    """
    Main window for the Project Euler Solutions Editor.

    This class provides the main interface for solving Project Euler problems,
    including code editing, testing, verification, and progress tracking.
    """
    def __init__(self):
        super().__init__()

        # Initialize managers first
        self.settings_manager = SettingsManager()
        self.problem_manager = ProblemManager()
        self.theme_manager = ThemeManager(self.settings_manager)

        # Set current mode (basic or max)
        self.current_mode = self.settings_manager.settings.get(
            'problem_mode', 'basic'
        )

        # Initialize problem manager mode
        self.problem_manager.set_problem_mode(self.current_mode)

        # Set up the main window
        self.update_window_title()
        self.setGeometry(100, 100, 1200, 800)

        # Set application icon
        app_icon = QIcon("PEIDE.png")
        self.setWindowIcon(app_icon)
        QApplication.instance().setWindowIcon(app_icon)

        # Create menu bar using MainMenuBuilder
        self.menu_builder = MainMenuBuilder(self)

        # Set initial mode menu checkmarks based on current mode
        self.menu_builder.basic_mode_action.setChecked(
            self.current_mode == 'basic'
        )
        self.menu_builder.max_mode_action.setChecked(
            self.current_mode == 'max'
        )

        # Create toolbars with movable property
        self.create_toolbars()

        # Create status bar
        self.status_bar = QStatusBar()
        # Set default styling for all status bar messages to improve visibility
        self.status_bar.setStyleSheet(
            "QStatusBar { color: white; font-weight: bold; }"
        )
        self.setStatusBar(self.status_bar)

        # Add mode indicator label to status bar
        self.mode_indicator = QLabel()
        self.update_mode_indicator()  # Set initial text
        self.status_bar.addPermanentWidget(self.mode_indicator)

        # Add progress bar to status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(100)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Add execution time label to status bar
        self.execution_time_label = QLabel()
        self.execution_time_label.setVisible(False)
        self.execution_time_label.setStyleSheet("color: lightgreen; font-weight: bold;")
        self.status_bar.addPermanentWidget(self.execution_time_label)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Create splitter for left and right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel (Problem description and progress grid)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Create problem display panel
        self.problem_display = ProblemDisplayPanel(self.problem_manager)
        left_layout.addWidget(self.problem_display)

        # Progress grid
        self.progress_grid = ProblemGrid(self.problem_manager)
        self.progress_grid.setFixedHeight(400)  # Limit the height

        # Initialize progress grid mode to match current mode
        self.progress_grid.set_mode(self.current_mode)

        left_layout.addWidget(self.progress_grid)

        # Create progress integration
        self.progress_integration = ProgressIntegration(
            self,
            self.problem_manager,
            self.progress_grid,
            self.status_bar
        )
        # Connect the signal ONLY to load_problem_by_number (avoid circular refs)
        self.progress_integration.problem_selected.connect(
            self.load_problem_by_number
        )

        # Don't wire the square_clicked_signal directly to load_problem_by_number
        # The connection is handled through ProgressIntegration now

        # Update the view menu to include the difficulty toolbar toggle now that it exists
        self.update_view_menu()

        # Right panel (Code editor and helper files)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Tab widget for solution, helper files, and data files
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setMovable(False)
        self.tab_widget.setDocumentMode(True)

        # Add mouse press event handler
        self.tab_widget.mousePressEvent = self.handle_tab_widget_click

        # Solution tab
        solution_tab = QWidget()
        solution_layout = QVBoxLayout(solution_tab)
        self.code_editor = CodeEditor(settings_manager=self.settings_manager)
        solution_layout.addWidget(self.code_editor)
        self.tab_widget.addTab(solution_tab, "Solution")
        self.solution_tab_index = 0  # Store the index for reference

        # Set up references to code editor for integration
        self.code_editor.set_problem_manager(self.problem_manager)
        self.code_editor.set_tab_widget(self.tab_widget)
        self.code_editor.switch_to_tab.connect(self.tab_widget.setCurrentIndex)

        # Helper files tab
        helpers_tab = QWidget()
        helpers_layout = QVBoxLayout(helpers_tab)
        self.helper_files_panel = HelperFilesPanel(self.settings_manager, self.problem_manager)
        helpers_layout.addWidget(self.helper_files_panel)

        # Add helpers tab to tab widget
        self.tab_widget.addTab(helpers_tab, "Helper Files")
        self.helpers_tab_index = 1  # Store the index for reference

        # Connect helper file selection signal
        self.helper_files_panel.helper_file_selected.connect(self.add_import_statement_for_helper)

        # Templates tab
        templates_tab = QWidget()
        templates_layout = QVBoxLayout(templates_tab)

        # Create templates panel
        self.templates_panel = TemplatesPanel(
            self.settings_manager,
            self.problem_manager,
            main_code_editor=self.code_editor,
            tab_widget=self.tab_widget
        )
        templates_layout.addWidget(self.templates_panel)

        # Add templates tab to tab widget
        self.tab_widget.addTab(templates_tab, "Code Templates")
        self.templates_tab_index = 2  # Store the index for reference

        # Add data files tab
        data_files_tab = QWidget()
        data_files_layout = QVBoxLayout(data_files_tab)
        data_files_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Create data file panel
        self.data_file_panel = DataFilePanel(self.settings_manager)
        self.data_file_panel.insert_code_requested.connect(self.insert_data_loading_code)
        data_files_layout.addWidget(self.data_file_panel)

        # Add data files tab to tab widget
        self.tab_widget.addTab(data_files_tab, "Data Files")
        self.data_files_tab_index = 3  # Store the index for reference

        # Add debug output tab
        debug_tab = QWidget()
        debug_layout = QVBoxLayout(debug_tab)

        # Create the debug panel
        self.debug_panel = DebugPanel(self.settings_manager)
        debug_layout.addWidget(self.debug_panel)

        # Connect the debug panel to the code editor
        self.code_editor.set_debug_panel(self.debug_panel)

        # Create debug integration
        self.debug_integration = DebugIntegration(self.debug_panel, self)

        # Connect the debug panel to the other code editors
        self.helper_files_panel.helpers_editor.set_debug_panel(self.debug_panel)
        self.templates_panel.template_code_preview.set_debug_panel(self.debug_panel)

        # Add debug tab to tab widget
        self.tab_widget.addTab(debug_tab, "Debug Output")
        self.debug_tab_index = 4  # Store the index for reference

        # Debug output for tab indices
        self.debug_panel.add_debug_message(
            "Initializing tab indices:", level="info"
        )
        self.debug_panel.add_debug_message(
            f"Solution tab index: {self.solution_tab_index}", level="info"
        )
        self.debug_panel.add_debug_message(
            f"Helpers tab index: {self.helpers_tab_index}", level="info"
        )
        self.debug_panel.add_debug_message(
            f"Templates tab index: {self.templates_tab_index}", level="info"
        )
        self.debug_panel.add_debug_message(
            f"Data files tab index: {self.data_files_tab_index}", level="info"
        )
        self.debug_panel.add_debug_message(
            f"Debug tab index: {self.debug_tab_index}", level="info"
        )

        # Connect tab change signal
        self.tab_widget.currentChanged.connect(self.handle_tab_change)

        # Add tab widget to right panel
        right_layout.addWidget(self.tab_widget)

        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        # Set initial splitter sizes
        splitter.setSizes([400, 800])

        # Add splitter to main layout
        main_layout.addWidget(splitter)

        # Create bottom bar with buttons
        bottom_bar = QHBoxLayout()
        self.run_button = QPushButton("Run Code")
        self.hint_button = QPushButton("Get Hint")
        self.save_button = QPushButton("Save Solution")
        self.mark_solved_button = QPushButton("Mark as Solved")
        self.verify_button = QPushButton("Verify Answer")
        bottom_bar.addWidget(self.run_button)
        bottom_bar.addWidget(self.hint_button)
        bottom_bar.addWidget(self.save_button)
        bottom_bar.addWidget(self.mark_solved_button)
        bottom_bar.addWidget(self.verify_button)

        # Initially hide the Mark as Solved button since default is problem 1
        self.mark_solved_button.setVisible(False)

        # Add bottom bar to main layout
        main_layout.addLayout(bottom_bar)

        # Set up syntax highlighters
        self.highlighter = PythonHighlighter(self.code_editor.document(), self.settings_manager)

        # Connect signals
        self.run_button.clicked.connect(self.run_code)
        self.hint_button.clicked.connect(self.show_hint)
        self.save_button.clicked.connect(self.save_solution)
        self.mark_solved_button.clicked.connect(self.mark_problem_solved)
        self.verify_button.clicked.connect(self.verify_solution)

        # Load templates
        self.load_templates()

        # Apply settings after all UI components are created
        self.apply_settings()

        # Force rehighlighting of both editors to apply saved settings
        if hasattr(self, 'highlighter'):
            self.highlighter.update_highlighting_rules()
            self.highlighter.rehighlight()

        # Initialize run manager
        self.run_manager = RunManager(
            self.problem_manager,
            self.debug_panel,
            {
                'status_bar': self.status_bar,
                'progress_bar': self.progress_bar,
                'execution_time_label': self.execution_time_label,
                'code_editor': self.code_editor,
                'helpers_editor': self.helper_files_panel.helpers_editor,
                'tab_widget': self.tab_widget
            }
        )

        # Load the first problem
        self.load_problem_by_number(1)

        # Load and apply saved theme
        palette = self.theme_manager.load_theme()
        QApplication.instance().setPalette(palette)

    def handle_tab_change(self, index):
        """Handle tab changes in the tab widget."""
        # Get the tab name
        tab_name = self.tab_widget.tabText(index)

        # If switching to debug tab, remove any highlight
        if index == self.debug_tab_index:
            self.remove_debug_tab_highlight()

        # If switching to data files tab, ensure it's properly enabled
        if index == self.data_files_tab_index:
            problem_number = self.progress_integration.get_current_problem_number()
            if problem_number:
                data_info = self.problem_manager.get_problem_data_info(problem_number)

                if data_info['has_data']:
                    # Enable the tab and panel
                    self.tab_widget.setTabEnabled(index, True)
                    self.data_file_panel.setEnabled(True)

                    # Update the panel with data info
                    self.data_file_panel.update_data_info(data_info)

                    # Try to load data preview
                    try:
                        data_content = self.problem_manager.load_data_file_preview(data_info['file'])
                        self.data_file_panel.update_data_preview(data_content)
                    except Exception as e:
                        self.data_file_panel.update_data_preview(f"Error loading data preview: {str(e)}")
                else:
                    # Disable the tab and panel
                    self.tab_widget.setTabEnabled(index, False)
                    self.data_file_panel.setEnabled(False)
                    self.data_file_panel.clear()

                    # Switch back to solution tab
                    self.tab_widget.setCurrentIndex(self.solution_tab_index)
            else:
                self.tab_widget.setTabEnabled(index, False)
                self.data_file_panel.setEnabled(False)
                self.data_file_panel.clear()

                # Switch back to solution tab
                self.tab_widget.setCurrentIndex(self.solution_tab_index)

    def load_problem_by_number(self, problem_number):
        """Load a problem by its number."""
        # Prevent recursion with a flag
        if hasattr(self, '_loading_problem') and self._loading_problem:
            print(f"Warning: Recursive call to load_problem_by_number({problem_number}) detected")
            return

        try:
            self._loading_problem = True

            # Set the current problem in the debug panel
            self.debug_integration.set_current_problem(problem_number)

            # Navigate to the correct problem group in the grid
            if hasattr(self.progress_grid, 'navigate_to_problem'):
                self.progress_grid.navigate_to_problem(problem_number)

            # Load problem using the problem display panel
            data_info = self.problem_display.load_problem(problem_number)

            # Update data file panel with the data info
            self.data_file_panel.update_data_info(data_info)

            # Update data files tab state
            if data_info and data_info['has_data']:
                # Enable data files tab
                self.tab_widget.setTabEnabled(self.data_files_tab_index, True)

                # If we're currently on the data files tab, update its content
                if self.tab_widget.currentIndex() == self.data_files_tab_index:
                    self.data_file_panel.update_data_info(data_info)
                    try:
                        data_content = self.problem_manager.load_data_file_preview(data_info['file'])
                        self.data_file_panel.update_data_preview(data_content)
                    except Exception as e:
                        self.data_file_panel.update_data_preview(f"Error loading data preview: {str(e)}")
                        self.debug_integration.log_data_preview_error(e)
            else:
                # Disable data files tab
                self.tab_widget.setTabEnabled(self.data_files_tab_index, False)
                # Clear data file panel
                self.data_file_panel.clear()

            # Load solution if it exists
            solution = self.problem_manager.load_solution(problem_number)

            # Record whether we loaded a solution or created a template
            had_solution = bool(solution)

            # Set current problem number in code editor
            self.code_editor.set_current_problem(problem_number)

            if solution:
                self.code_editor.load_solution(solution)
            else:
                # Create a template for new problems
                self.code_editor.create_problem_template(problem_number)

            # Finish loading problem
            self.debug_integration.finish_loading_problem(had_solution)

            # Load helper files list
            self.helper_files_panel.update_problem(problem_number)

            # Update status
            self.progress_integration.update_status_bar(problem_number)

            # Update the grid to show the current problem and its status
            self.progress_grid.current_square = problem_number
            self.progress_integration.update_progress()

            # Update button visibility based on problem number
            self.update_button_visibility()

        except Exception as e:
            # Avoid QMessageBox here as it can lead to recursion
            # Instead, just print to console and log the error
            print(f"Error loading problem {problem_number}: {str(e)}")
            traceback.print_exc()

            # Use direct logging without UI components if possible
            if hasattr(self, 'debug_integration'):
                try:
                    self.debug_integration.log_error(f"Error loading problem: {str(e)}", e, False)
                except Exception:
                    print("Additional error occurred during error logging")
        finally:
            # Always reset the flag to prevent permanent lockout
            self._loading_problem = False

    def run_code(self):
        """Run the current solution code."""
        # Get current problem number
        problem_number = self.progress_integration.get_current_problem_number()

        # No problem selected
        if problem_number is None:
            QMessageBox.warning(
                self, "No Problem Selected", "Please select a problem first."
            )
            return

        # Get the user's code
        code = self.code_editor.toPlainText()

        # Set up necessary UI components for RunManager
        ui_components = {
            "status_bar": self.status_bar,
            "progress_bar": self.progress_bar,
            "execution_time_label": self.execution_time_label,
            "code_editor": self.code_editor,
            "helpers_editor": self.helper_files_panel.helpers_editor,
            "tab_widget": self.tab_widget
        }

        # Create a run manager if it doesn't exist
        if not hasattr(self, 'run_manager'):
            self.run_manager = RunManager(
                self.problem_manager, self.debug_panel, ui_components
            )

        # Always switch to debug tab when running code to show results
        self.tab_widget.setCurrentIndex(self.debug_tab_index)

        # Highlight the debug tab to indicate new results
        self.highlight_debug_tab()

        # Add execution start message to debug panel
        self.debug_panel.add_debug_message("=" * 60, "info")
        self.debug_panel.add_debug_message(
            f"Running solution for Problem {problem_number}...", "info"
        )
        self.debug_panel.add_debug_message("=" * 60, "info")

        # Run the solution
        result = self.run_manager.run_solution(problem_number, code)

        # Handle results and display prominently in debug panel
        if result["success"]:
            # Display success results prominently in debug panel
            self.debug_panel.add_debug_message("", "info")  # Empty line
            self.debug_panel.add_debug_message(
                "🎉 EXECUTION SUCCESSFUL! 🎉", "important"
            )
            self.debug_panel.add_debug_message(
                f"Result: {result['result']}", "important"
            )
            self.debug_panel.add_debug_message(
                f"Execution time: {result['execution_time']:.6f} seconds", "info"
            )

            # Add performance feedback
            if result['execution_time'] < 0.001:
                self.debug_panel.add_debug_message(
                    "⚡ Excellent performance! (< 1ms)", "info"
                )
            elif result['execution_time'] < 0.01:
                self.debug_panel.add_debug_message(
                    "✅ Good performance! (< 10ms)", "info"
                )
            elif result['execution_time'] < 1.0:
                self.debug_panel.add_debug_message(
                    "👍 Acceptable performance (< 1s)", "info"
                )
            elif result['execution_time'] < 60.0:
                self.debug_panel.add_debug_message(
                    "⚠️ Slow execution (> 1s)", "warning"
                )
            else:
                self.debug_panel.add_debug_message(
                    "🐌 Very slow execution (> 1 minute)", "error"
                )

            self.debug_panel.add_debug_message("=" * 60, "info")

            # Also update status bar (but debug panel is primary display)
            self.show_status_message(
                f"Execution successful. Result: {result['result']}"
            )
            self.execution_time_label.setText(
                f"Execution time: {result['execution_time']:.6f} seconds"
            )
            self.execution_time_label.setVisible(True)

            # Save the solution with execution time
            self.problem_manager.save_solution(
                problem_number, code, result["execution_time"]
            )

            # Store the last result for use by verify_solution
            self.last_run_result = result
        else:
            # Display error results prominently in debug panel
            self.debug_panel.add_debug_message("", "error")  # Empty line
            self.debug_panel.add_debug_message("❌ EXECUTION FAILED! ❌", "error")
            if result["error"]:
                self.debug_panel.add_debug_message(
                    f"Error: {result['error']}", "error"
                )
                self.show_status_message(f"Error: {result['error']}")
            else:
                self.debug_panel.add_debug_message("Unknown execution error", "error")
                self.show_status_message("Execution failed.")

            # Add line number information if available
            if result.get("line_number"):
                self.debug_panel.add_debug_message(
                    f"Error at line {result['line_number']}", "error"
                )

            self.debug_panel.add_debug_message("=" * 60, "error")

            # Clear the last result
            self.last_run_result = None

        # Update the progress grid
        self.update_progress()

    def show_hint(self):
        """Show the hint for the current problem."""
        hints = self.problem_display.get_current_hints()
        if not hints:
            QMessageBox.information(self, "Hint", "No hints available for this problem.")
            return

        msg = QMessageBox()
        msg.setWindowTitle("Hint")
        msg.setText(hints)
        msg.exec()

    def save_solution(self):
        """Save the current solution."""
        problem_number = self.progress_integration.get_current_problem_number()
        if not problem_number:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return

        # Save the solution using the code editor
        if self.code_editor.save_solution_with_execution_time():
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Solution saved successfully!")
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Failed to save solution.")
            msg.exec()

    def mark_problem_solved(self):
        """Mark the current problem as solved."""
        problem_number = self.progress_integration.get_current_problem_number()
        if not problem_number:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return

        self.problem_manager.mark_problem_solved(problem_number)

        # Update streak information
        today = datetime.now().strftime('%Y-%m-%d')
        last_solved_date = self.settings_manager.settings.get('last_solved_date', None)

        if last_solved_date:
            last_date = datetime.strptime(last_solved_date, '%Y-%m-%d')
            today_date = datetime.strptime(today, '%Y-%m-%d')
            if (today_date - last_date).days == 1:
                # Consecutive day
                current_streak = self.settings_manager.settings.get(
                    'current_streak', 0
                ) + 1
                self.settings_manager.settings['current_streak'] = current_streak
                longest_streak = self.settings_manager.settings.get(
                    'longest_streak', 0
                )
                if current_streak > longest_streak:
                    self.settings_manager.settings['longest_streak'] = current_streak
            elif (today_date - last_date).days > 1:
                # Streak broken
                self.settings_manager.settings['current_streak'] = 1
        else:
            # First problem solved
            self.settings_manager.settings['current_streak'] = 1
            self.settings_manager.settings['longest_streak'] = 1

        self.settings_manager.settings['last_solved_date'] = today
        self.settings_manager.save_settings()

        self.progress_integration.update_progress()
        self.progress_integration.update_status_bar(problem_number)

        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText(f"Problem {problem_number} marked as solved!")
        msg.exec()

    def update_progress(self):
        """Update the progress grid with current status."""
        progress = self.problem_manager.get_progress()
        solved_problems = progress["solved_problems"]
        attempted_problems = progress["attempted_problems"]
        verified_problems = progress.get("verified_problems", [])

        # Update the progress grid with all progress information
        self.progress_grid.update_progress(
            solved_problems, attempted_problems, verified_problems
        )

        # Update tooltips for the progress grid
        self.update_grid_tooltips()

    def update_status_bar(self, problem_number):
        """Update the status bar with problem information."""
        progress = self.problem_manager.get_progress()
        status = f"Problem {problem_number}"
        if self.problem_manager.is_problem_solved(problem_number):
            status += " ✓"
        self.show_status_message(status)

    def show_settings_dialog(self):
        """Show the settings dialog and apply changes if accepted."""
        dialog = SettingsDialog(self)
        dialog.set_settings(self.settings_manager.settings)

        # Save current debug settings before showing dialog
        self.save_debug_settings()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_settings = dialog.get_settings()
            self.settings_manager.settings = new_settings
            self.settings_manager.save_settings()

            # Update syntax highlighting colors
            if "syntax_highlighting" in new_settings:
                self.settings_manager.update_highlighting_colors(new_settings["syntax_highlighting"])

            # Apply all settings
            self.apply_settings()

            # Force rehighlighting of both editors
            if hasattr(self, 'highlighter'):
                self.highlighter.update_highlighting_rules()
                self.highlighter.rehighlight()

    def show_progress_dialog(self):
        """Show the progress dialog with statistics and achievements."""
        from ui.progress_dialog import ProgressDialog
        dialog = ProgressDialog(self)
        dialog.exec()

    def show_welcome_dialog(self):
        """Show the welcome dialog for first-time users."""
        from dialogs.welcome_dialog import WelcomeDialog
        WelcomeDialog.show(self)

    def save_debug_settings(self):
        """Save the current debug settings. Delegates to debug_panel."""
        self.debug_panel.save_debug_settings()

    def apply_settings(self):
        """Apply current settings to the UI."""
        settings = self.settings_manager.settings

        # Apply theme settings
        theme = settings.get('theme', 'dark')
        if theme == 'light':
            self.theme_manager.apply_light_theme(QApplication.instance(), self.status_bar)
        else:
            self.theme_manager.apply_dark_theme(QApplication.instance(), self.status_bar)

        # Problem text now has fixed styling, no need to apply settings

        # Apply code editor settings
        self.settings_manager.apply_code_editor_settings(self.code_editor)
        # Force line number area update for code editor
        self.code_editor.update_line_number_area_width(0)

        # Apply template editor settings through the templates panel
        self.templates_panel._apply_settings()

        # Apply helper editor settings
        self.helper_files_panel._apply_settings()

        # Apply data files settings
        self.settings_manager.apply_data_files_settings(self.data_file_panel)

        # Debug panel will handle its own settings

    def add_import_statement_for_helper(self, filename):
        """Add an import statement for the helper file to the code editor."""
        if not filename.endswith('.py'):
            return

        # Get full path to the helper file - avoid using os.path.join to prevent recursion
        file_path = self.problem_manager.helpers_dir + os.sep + filename

        # Use the CodeEditor's method to add the import statement
        self.code_editor.add_import_statement_for_helper(filename, file_path)

    def insert_data_loading_code(self):
        """Insert the data loading code into the code editor."""
        if not self.data_file_panel.current_data_info or not self.data_file_panel.current_data_info.get('has_data', False):
            return

        # Get the loading method from the data info
        method = self.data_file_panel.current_data_info['method']

        # Use the CodeEditor's method to insert the data loading code
        self.code_editor.insert_data_loading_code(method)

    def update_grid_tooltips(self):
        """Update tooltips for all grid squares with difficulty information."""
        for i in range(1, 101):
            difficulty = self.problem_manager.get_problem_difficulty(i)
            percentage = self.problem_manager.get_problem_difficulty_percentage(i)
            self.progress_grid.update_tooltip(i, difficulty, percentage)

    def show_about_dialog(self):
        """Show the About dialog."""
        from dialogs.about_dialog import AboutDialog
        AboutDialog.show(self)

    def show_info_dialog(self):
        """Show the Info dialog with README.md contents."""
        from dialogs.info_dialog import InfoDialog
        InfoDialog.show(self)

    def open_project_euler_website(self):
        """Open the Project Euler website in the default browser."""
        url = QUrl("https://projecteuler.net/")
        QDesktopServices.openUrl(url)

    def show_project_euler_status(self):
        """Show the Project Euler status dialog with profile information."""
        from dialogs.project_euler_status import ProjectEulerStatusDialog
        ProjectEulerStatusDialog.show(self)

    # _convert_markdown_to_simple_html method has been moved to InfoDialog

    def show_tutorials_dialog(self):
        """Show the tutorials dialog with a list of available tutorials."""
        from tutorial_dialog import TutorialDialog
        from tutorial_manager import TutorialManager

        # Create tutorial manager to get available tutorials
        tutorial_manager = TutorialManager()
        tutorials = tutorial_manager.load_tutorials()

        if not tutorials:
            QMessageBox.warning(self, "Warning", "No tutorials available")
            return

        # Create dialog to select tutorial
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Tutorial")
        dialog.setMinimumWidth(400)
        dialog.setMinimumHeight(300)
        layout = QVBoxLayout()

        # Create list widget for tutorials
        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        for tutorial_name, tutorial_data in tutorials.items():
            list_widget.addItem(f"{tutorial_name} - {tutorial_data['title']}")
        layout.addWidget(list_widget)

        # Add buttons
        button_layout = QHBoxLayout()
        start_button = QPushButton("Start Tutorial")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(start_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Connect buttons
        start_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_item = list_widget.currentItem()
            if selected_item:
                # Extract tutorial name from the selected item
                tutorial_name = selected_item.text().split(" - ")[0]
                # Create and show the tutorial dialog
                tutorial_dialog = TutorialDialog(self)
                tutorial_dialog.start_tutorial(tutorial_name)

    def show_template_details(self, current, previous):
        """Show the details of the selected template."""
        self.templates_panel.show_template_details(current, previous)

    def create_new_template(self):
        """Create a new template using the inline editor."""
        self.templates_panel.create_new_template()

    def save_current_template(self):
        """Save the currently edited template."""
        self.templates_panel.save_current_template()

    def delete_template(self):
        """Delete the selected template."""
        self.templates_panel.delete_template()

    def insert_template(self):
        """Insert the selected template into the editor."""
        self.templates_panel.insert_template()

    def load_templates(self, force_reload=False):
        """Load templates into the list widget."""
        self.templates_panel.load_templates(force_reload)

    def set_dark_theme(self):
        """Set the application to dark theme using ThemeManager."""
        self.theme_manager.apply_dark_theme(QApplication.instance(), self.status_bar)

    def set_light_theme(self):
        """Set the application to light theme using ThemeManager."""
        self.theme_manager.apply_light_theme(QApplication.instance(), self.status_bar)

    def clear_debug_output(self):
        """Clear the debug output panel. Delegates to debug_panel."""
        self.debug_panel.clear_debug_output()

    def add_debug_message(self, message, level="debug"):
        """Add a message to the debug output panel. Delegates to debug_panel."""
        self.debug_panel.add_debug_message(message, level)

    def handle_tab_widget_click(self, event):
        """Handle mouse clicks on the tab widget."""
        # Get the tab under the click
        tab_index = self.tab_widget.tabBar().tabAt(event.pos())
        if tab_index >= 0:
            tab_name = self.tab_widget.tabText(tab_index)
            self.debug_integration.log_tab_event(tab_name, tab_index)

            # If clicking the data files tab
            if tab_index == self.data_files_tab_index:
                self.debug_integration.log_data_files_tab_click()
                problem_number = self.progress_integration.get_current_problem_number()
                if problem_number:
                    data_info = self.problem_manager.get_problem_data_info(problem_number)

                    if data_info['has_data']:
                        # Switch to the data files tab
                        self.tab_widget.setCurrentIndex(tab_index)
                        # Update the panel
                        self.data_file_panel.update_data_info(data_info)
                        try:
                            data_content = self.problem_manager.load_data_file_preview(data_info['file'])
                            self.data_file_panel.update_data_preview(data_content)
                        except Exception as e:
                            self.debug_integration.log_data_preview_error(e)
                            self.data_file_panel.update_data_preview(f"Error loading data preview: {str(e)}")
                    else:
                        self.debug_integration.log_no_data_available()
                        # Switch back to solution tab
                        self.tab_widget.setCurrentIndex(self.solution_tab_index)
                else:
                    self.debug_integration.log_no_problem_selected()
                    # Switch back to solution tab
                    self.tab_widget.setCurrentIndex(self.solution_tab_index)

        # Call the parent class's event handler
        QTabWidget.mousePressEvent(self.tab_widget, event)

    def create_toolbars(self):
        """Create all toolbars with movable property and visibility control."""
        # Create formatting/linting toolbar
        self.code_tools_toolbar = QToolBar("Code Tools")
        self.code_tools_toolbar.setObjectName("codeToolsToolbar")
        self.code_tools_toolbar.setMovable(True)
        self.code_tools_toolbar.setFloatable(True)
        self.addToolBar(self.code_tools_toolbar)

        # Format with Black action
        format_action = QAction("Format with Black", self)
        format_action.triggered.connect(self.format_current_code)
        format_action.setShortcut("Ctrl+Alt+F")
        self.code_tools_toolbar.addAction(format_action)

        # Lint with Pylint action
        lint_action = QAction("Lint with Pylint", self)
        lint_action.triggered.connect(self.lint_current_code)
        lint_action.setShortcut("Ctrl+Alt+L")
        self.code_tools_toolbar.addAction(lint_action)

        # Clear lint highlights action
        clear_lint_action = QAction("Clear Lint Highlights", self)
        clear_lint_action.triggered.connect(self.clear_lint_highlights)
        clear_lint_action.setShortcut("Ctrl+Alt+C")
        self.code_tools_toolbar.addAction(clear_lint_action)

        # Create view toolbar
        self.view_toolbar = QToolBar("View Tools")
        self.view_toolbar.setObjectName("viewToolsToolbar")
        self.view_toolbar.setMovable(True)
        self.view_toolbar.setFloatable(True)
        self.addToolBar(self.view_toolbar)

        # Fullscreen problem description action
        fullscreen_action = QAction("Fullscreen Problem", self)
        fullscreen_action.setToolTip("View problem description in fullscreen mode")
        fullscreen_action.triggered.connect(self.show_problem_fullscreen)
        fullscreen_action.setShortcut("F11")
        self.view_toolbar.addAction(fullscreen_action)

        # Update the existing View menu with toolbar toggles
        self.update_view_menu()

    def update_view_menu(self):
        """Update the existing View menu with toolbar toggles."""
        # Get the View menu created by MainMenuBuilder
        view_menu = self.menu_builder.view_menu

        if not view_menu:
            return

        # Add toolbar toggle actions (keep existing items)
        code_tools_action = self.code_tools_toolbar.toggleViewAction()
        code_tools_action.setText("Show Code Tools Toolbar")
        view_menu.addAction(code_tools_action)

        # Add the view toolbar toggle
        view_tools_action = self.view_toolbar.toggleViewAction()
        view_tools_action.setText("Show View Tools Toolbar")
        view_menu.addAction(view_tools_action)

        # Add toggle for the existing difficulty toolbar from progress_integration
        if hasattr(self, 'progress_integration') and hasattr(self.progress_integration, 'difficulty_toolbar'):
            difficulty_action = self.progress_integration.difficulty_toolbar.toggleViewAction()
            difficulty_action.setText("Show Difficulty Filter Toolbar")
            view_menu.addAction(difficulty_action)

    def format_current_code(self):
        """Format the code in the current tab with Black."""
        current_tab = self.tab_widget.currentIndex()

        # Handle based on current tab
        if current_tab == self.solution_tab_index:
            self.code_editor.format_code()
        elif current_tab == self.helpers_tab_index:
            self.helper_files_panel.helpers_editor.format_code()
        elif current_tab == self.templates_tab_index:
            self.templates_panel.template_code_preview.format_code()
        else:
            # Not a code editor tab
            self.debug_panel.add_debug_message("Cannot format: current tab does not contain code.", "warning")

    def lint_current_code(self):
        """Lint the code in the current tab with Pylint."""
        current_tab = self.tab_widget.currentIndex()

        # Handle based on current tab
        if current_tab == self.solution_tab_index:
            self.code_editor.lint_code()
        elif current_tab == self.helpers_tab_index:
            self.helper_files_panel.helpers_editor.lint_code()
        elif current_tab == self.templates_tab_index:
            self.templates_panel.template_code_preview.lint_code()
        else:
            # Not a code editor tab
            self.debug_panel.add_debug_message("Cannot lint: current tab does not contain code.", "warning")

    def clear_lint_highlights(self):
        """Clear all lint highlighting in the current code editor."""
        current_tab = self.tab_widget.currentIndex()

        # Handle based on current tab
        if current_tab == self.solution_tab_index:
            self.code_editor.clear_error_highlights()
            self.debug_panel.add_debug_message("Cleared lint highlights in solution editor", "info")
        elif current_tab == self.helpers_tab_index:
            self.helper_files_panel.helpers_editor.clear_error_highlights()
            self.debug_panel.add_debug_message("Cleared lint highlights in helper editor", "info")
        elif current_tab == self.templates_tab_index:
            self.templates_panel.template_code_preview.clear_error_highlights()
            self.debug_panel.add_debug_message("Cleared lint highlights in template editor", "info")
        else:
            # Not a code editor tab
            self.debug_panel.add_debug_message("Cannot clear highlights: current tab does not contain code.", "warning")

    def verify_solution(self):
        """Verify the current solution against the known answer."""
        # Get current problem number
        problem_number = self.progress_integration.get_current_problem_number()

        # No problem selected
        if problem_number is None:
            QMessageBox.warning(self, "No Problem Selected", "Please select a problem first.")
            return

        # Check if we have a last run result
        if not hasattr(self, 'last_run_result') or self.last_run_result is None:
            QMessageBox.warning(self, "No Solution Run",
                               "Please run your solution first to get a result to verify.")
            return

        # Get the run manager
        ui_components = {
            "status_bar": self.status_bar,
            "progress_bar": self.progress_bar,
            "execution_time_label": self.execution_time_label,
            "code_editor": self.code_editor,
            "helpers_editor": self.helper_files_panel.helpers_editor,
            "tab_widget": self.tab_widget
        }

        if not hasattr(self, 'run_manager'):
            self.run_manager = RunManager(self.problem_manager, self.debug_panel, ui_components)

        # Switch to debug tab to show verification results
        self.tab_widget.setCurrentIndex(self.debug_tab_index)

        # Highlight the debug tab to indicate new results
        self.highlight_debug_tab()

        # Add verification start message to debug panel
        self.debug_panel.add_debug_message("", "info")  # Empty line for spacing
        self.debug_panel.add_debug_message("🔍 VERIFYING SOLUTION...", "info")
        self.debug_panel.add_debug_message(f"Problem {problem_number} - Result: {self.last_run_result.get('result', 'N/A')}", "info")

        # Verify the solution
        verification = self.run_manager.verify_solution(problem_number, self.last_run_result)

        # Display verification results prominently in debug panel
        if verification["verified"]:
            self.debug_panel.add_debug_message("", "important")  # Empty line for spacing
            self.debug_panel.add_debug_message("🎯 SOLUTION VERIFIED! 🎯", "important")
            self.debug_panel.add_debug_message("✅ Your answer is CORRECT!", "important")
            self.debug_panel.add_debug_message(f"Problem {problem_number} has been marked as verified.", "info")
            self.debug_panel.add_debug_message("=" * 60, "important")

            # Show success dialog
            QMessageBox.information(self, "Solution Verified", verification["message"])
            # Update the progress display
            self.update_progress()
        else:
            self.debug_panel.add_debug_message("", "error")  # Empty line for spacing
            self.debug_panel.add_debug_message("❌ VERIFICATION FAILED", "error")
            self.debug_panel.add_debug_message(f"❌ {verification['message']}", "error")
            self.debug_panel.add_debug_message("Try reviewing your solution and run it again.", "warning")
            self.debug_panel.add_debug_message("=" * 60, "error")

            # Show failure dialog
            QMessageBox.warning(self, "Verification Failed", verification["message"])

        # Update status bar
        self.show_status_message(verification["message"])

    def indent_current_editor(self):
        """Indent text in the currently active editor."""
        current_tab = self.tab_widget.currentIndex()

        # Handle based on current tab
        if current_tab == self.solution_tab_index:
            self.code_editor.indent_selected_text()
        elif current_tab == self.helpers_tab_index:
            self.helper_files_panel.helpers_editor.indent_selected_text()
        elif current_tab == self.templates_tab_index:
            self.templates_panel.template_code_preview.indent_selected_text()
        else:
            # Not a code editor tab
            self.debug_panel.add_debug_message("Cannot indent: current tab does not contain code.", "warning")

    def dedent_current_editor(self):
        """Dedent text in the currently active editor."""
        current_tab = self.tab_widget.currentIndex()

        # Handle based on current tab
        if current_tab == self.solution_tab_index:
            self.code_editor.dedent_selected_text()
        elif current_tab == self.helpers_tab_index:
            self.helper_files_panel.helpers_editor.dedent_selected_text()
        elif current_tab == self.templates_tab_index:
            self.templates_panel.template_code_preview.dedent_selected_text()
        else:
            # Not a code editor tab
            self.debug_panel.add_debug_message("Cannot dedent: current tab does not contain code.", "warning")

    def update_window_title(self):
        """Update the window title based on the current mode."""
        if self.current_mode == "max":
            self.setWindowTitle("Project Euler Solutions Editor - Max Edition")
        else:
            self.setWindowTitle("Project Euler Solutions Editor")

    def set_problem_mode(self, mode):
        """
        Set the problem mode (basic or max) and update the UI.

        Args:
            mode: The mode to set ('basic' or 'max')
        """
        if mode not in ['basic', 'max']:
            return

        # If mode is the same, no need to change
        if self.current_mode == mode:
            return

        # Update the mode
        self.current_mode = mode

        # Update menu checkmarks
        self.menu_builder.basic_mode_action.setChecked(mode == 'basic')
        self.menu_builder.max_mode_action.setChecked(mode == 'max')

        # Update window title and mode indicator
        self.update_window_title()
        self.update_mode_indicator()

        # Save the setting
        self.settings_manager.settings['problem_mode'] = mode
        self.settings_manager.save_settings()

        # Update problem manager mode
        self.problem_manager.set_problem_mode(mode)

        # Update progress grid mode
        self.progress_grid.set_mode(mode)

        # Reload current problem if possible
        current_problem = self.progress_integration.get_current_problem_number()
        if current_problem:
            # If switching to basic mode and current problem is > 100, switch to problem 1
            if mode == 'basic' and current_problem > 100:
                self.load_problem_by_number(1)
            else:
                self.load_problem_by_number(current_problem)

        # Update button visibility
        self.update_button_visibility()

        # Show confirmation message
        max_problems = 945 if mode == 'max' else 100
        self.show_status_message(f"Switched to {mode} mode ({max_problems} problems available)", 3000)

    def update_mode_indicator(self):
        """Update the mode indicator label in the status bar."""
        if self.current_mode == "max":
            self.mode_indicator.setText("MAX MODE")
            self.mode_indicator.setStyleSheet("color: gold; font-weight: bold;")
        else:
            self.mode_indicator.setText("BASIC MODE")
            self.mode_indicator.setStyleSheet("color: lightblue; font-weight: bold;")

    # Helper method to show styled status bar messages
    def show_status_message(self, message, timeout=0):
        """Show a styled message in the status bar."""
        self.status_bar.showMessage(message, timeout)

    def show_problem_fullscreen(self):
        """Show the problem description in fullscreen mode."""
        if hasattr(self, 'problem_display') and self.problem_display:
            self.problem_display.show_fullscreen()
        else:
            self.show_status_message("Problem display not available", 3000)

    def update_button_visibility(self):
        """Update the visibility of the Mark as Solved button based on current mode."""
        # Show the button only in max mode, hide it in basic mode
        if self.current_mode == 'max':
            self.mark_solved_button.setVisible(True)
        else:
            self.mark_solved_button.setVisible(False)

    def highlight_debug_tab(self):
        """Highlight the debug tab to indicate new results are available."""
        try:
            # Change the tab text to include an indicator
            original_text = "Debug Output"
            highlighted_text = "🔍 Debug Output"

            # Only change if not already highlighted
            current_text = self.tab_widget.tabText(self.debug_tab_index)
            if not current_text.startswith("🔍"):
                self.tab_widget.setTabText(self.debug_tab_index, highlighted_text)

                # Set up a timer to remove the highlight after a few seconds if user doesn't switch
                if not hasattr(self, 'debug_highlight_timer'):
                    from PyQt6.QtCore import QTimer
                    self.debug_highlight_timer = QTimer()
                    self.debug_highlight_timer.setSingleShot(True)
                    self.debug_highlight_timer.timeout.connect(self.remove_debug_tab_highlight)

                # Reset the timer
                self.debug_highlight_timer.start(10000)  # Remove highlight after 10 seconds

        except Exception as e:
            # Silently fail to avoid disrupting execution
            pass

    def remove_debug_tab_highlight(self):
        """Remove the highlight from the debug tab."""
        try:
            original_text = "Debug Output"
            self.tab_widget.setTabText(self.debug_tab_index, original_text)
        except Exception as e:
            # Silently fail
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Set application icon
    app_icon = QIcon("PEIDE.png")
    app.setWindowIcon(app_icon)

    # Create the main window
    window = MainWindow()

    # Apply theme from settings (will default to dark if not specified)
    palette = window.theme_manager.load_theme()
    app.setPalette(palette)

    window.show()
    sys.exit(app.exec())
