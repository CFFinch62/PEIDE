"""
Debug integration module for Project Euler Editor.
Handles integration of debug functionality with the main application.
"""
from datetime import datetime
import traceback
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt, QObject, QUrl
from PyQt6.QtGui import QDesktopServices

class DebugIntegration:
    """
    Handles integration of debug functionality with the main application.
    Acts as a bridge between the debug panel and various application components.
    """

    def __init__(self, debug_panel, main_window=None):
        """
        Initialize the debug integration.

        Args:
            debug_panel: The debug panel instance
            main_window: The main window instance (for displaying message boxes)
        """
        self.debug_panel = debug_panel
        self.main_window = main_window

    def set_current_problem(self, problem_number):
        """Set the current problem number in the debug panel."""
        # Update problem number directly but add logging and timing separately
        try:
            self.debug_panel.set_current_problem(problem_number)
            
            # Only log if debug is enabled to prevent unnecessary calls
            if self.debug_panel.is_debug_enabled():
                self.debug_panel.add_debug_message(f"Loading problem {problem_number}", level="info")
                self.add_timing_marker("Start Loading Problem")
        except RecursionError:
            # If recursion occurs, log directly without trying to use debug panel methods
            print(f"Recursion detected while setting problem {problem_number}")

    def finish_loading_problem(self, had_solution=False):
        """Log completion of problem loading."""
        if had_solution:
            self.debug_panel.add_debug_message("Loaded existing solution", level="info")
        else:
            self.debug_panel.add_debug_message("Created new solution template", level="info")

        # Clear variable tracking for new problem
        self.debug_panel.clear_variable_tracking()
        self.add_timing_marker("Problem Loading Complete")

    def log_error(self, message, exception=None, show_messagebox=True):
        """Log an error to the debug panel and optionally show a message box."""
        self.debug_panel.add_debug_message(message, level="error")

        if exception:
            error_traceback = traceback.format_exc()
            self.debug_panel.add_debug_message(error_traceback, level="detail")

        if show_messagebox and self.main_window:
            QMessageBox.critical(self.main_window, "Error", message)

    def start_code_execution(self, problem_number):
        """Log the start of code execution."""
        # Clear the debug output before starting a new execution
        self.debug_panel.clear_debug_output()
        self.add_timing_marker("Code Execution Start")
        self.debug_panel.add_debug_message("Running solution code...", level="important")
        return problem_number is not None

    def finish_code_execution(self, success, result=None):
        """Log the completion of code execution."""
        if success:
            # Add timing marker for execution completion
            self.add_timing_marker("Code Execution Complete")

            # Log the result in debug panel
            if result:
                self.debug_panel.add_debug_message(f"Result: {result.get('result', 'N/A')}", level="important")
                self.debug_panel.add_debug_message(f"Execution time: {result.get('execution_time', 0):.6f} seconds", level="info")

                # Add warning if execution time is too long
                if "warning" in result:
                    self.debug_panel.add_debug_message("Warning: Solution execution time exceeds 1 minute!", level="error")
        else:
            # Mark execution failure in debug panel
            self.add_timing_marker("Code Execution Failed")
            if result:
                self.debug_panel.add_debug_message(f"Error: {result.get('error', 'Unknown error')}", level="error")

                if 'line_number' in result:
                    self.debug_panel.add_debug_message(f"Error at line {result['line_number']}", level="error")

                # If this is a missing data file error
                if result.get("is_missing_data", False) and result.get("download_url"):
                    self.debug_panel.add_debug_message(f"Missing data file. Download URL: {result['download_url']}", level="info")

        self.add_timing_marker("Run Operation Complete")

    def log_data_file_download(self):
        """Log that a data file download has been initiated."""
        self.debug_panel.add_debug_message("Opening browser to download data file", level="info")

    def add_timing_marker(self, marker_name):
        """Add a timing marker in the debug output."""
        try:
            # Only add markers if debug is enabled to avoid unnecessary processing
            if self.debug_panel.is_debug_enabled():
                self.debug_panel.add_timing_marker(marker_name)
        except Exception as e:
            # Silently fail on error to prevent recursion
            print(f"Error adding timing marker: {str(e)}")

    def log_data_preview_error(self, error):
        """Log an error loading data preview."""
        self.debug_panel.add_debug_message(f"Error loading data preview: {str(error)}", level="error")

    def log_tab_event(self, tab_name, index):
        """Log a tab widget event."""
        self.debug_panel.add_debug_message(f"Tab selected: {tab_name} at index {index}", level="info")

    def log_data_files_tab_click(self):
        """Log a click on the data files tab."""
        self.debug_panel.add_debug_message("Data files tab clicked", level="info")

    def log_no_data_available(self):
        """Log that no data is available for a problem."""
        self.debug_panel.add_debug_message("No data available for this problem", level="warning")

    def log_no_problem_selected(self):
        """Log that no problem is selected."""
        self.debug_panel.add_debug_message("No current problem selected", level="warning")