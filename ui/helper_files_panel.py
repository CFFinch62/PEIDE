from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QListWidget, QMessageBox, QInputDialog, QLineEdit)
from PyQt6.QtCore import pyqtSignal
from ui.code_editor import CodeEditor
import ast

class HelperFilesPanel(QWidget):
    """Panel for managing helper files."""

    # Signal emitted when a helper file is selected
    helper_file_selected = pyqtSignal(str)

    def __init__(self, settings_manager, problem_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.problem_manager = problem_manager
        self.current_problem_number = None

        self._create_ui()
        self._apply_settings()

    def _create_ui(self):
        """Create the UI components."""
        layout = QVBoxLayout(self)

        # Helper files controls
        controls_layout = QHBoxLayout()
        self.add_helper_button = QPushButton("Add Helper File")
        self.delete_helper_button = QPushButton("Delete Helper File")
        self.test_helper_button = QPushButton("Test Helper Function")
        self.save_helper_button = QPushButton("Save Helper File")
        self.load_helper_button = QPushButton("Load Helper File")

        controls_layout.addWidget(self.add_helper_button)
        controls_layout.addWidget(self.delete_helper_button)
        controls_layout.addWidget(self.test_helper_button)
        controls_layout.addWidget(self.save_helper_button)
        controls_layout.addWidget(self.load_helper_button)

        # Helper files list
        self.helper_files_list = QListWidget()
        self.helper_files_list.setStyleSheet("""
            QListWidget {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: none;
                padding: 5px;
            }
        """)
        self.helper_files_list.setFixedHeight(100)

        # Helper editor
        self.helpers_editor = CodeEditor(settings_manager=self.settings_manager)
        self.helpers_editor.set_problem_manager(self.problem_manager)

        # Add widgets to layout
        layout.addLayout(controls_layout)
        layout.addWidget(self.helper_files_list)
        layout.addWidget(self.helpers_editor)

        # Connect signals
        self.add_helper_button.clicked.connect(self.add_helper_file)
        self.delete_helper_button.clicked.connect(self.delete_helper_file)
        self.test_helper_button.clicked.connect(self.test_helper_function)
        self.save_helper_button.clicked.connect(self.save_current_helper_file)
        self.load_helper_button.clicked.connect(self.load_shared_helper_file)
        self.helper_files_list.currentItemChanged.connect(self._handle_helper_file_selection)

        # Apply settings to helper editor from saved settings
        self.settings_manager.apply_helper_editor_settings(self.helpers_editor)

    def _apply_settings(self):
        """Apply settings to the panel."""
        self.settings_manager.apply_helper_editor_settings(self.helpers_editor)

    def _handle_helper_file_selection(self, current, _):
        """Handle selection of a helper file from the list."""
        if current is None:
            return

        # Prevent recursion with a flag
        if hasattr(self, '_handling_selection') and self._handling_selection:
            return
            
        try:
            self._handling_selection = True
            
            filename = current.text()
            self.helper_file_selected.emit(filename)

            # Load the helper file content
            if self.current_problem_number:
                helper_files = self.problem_manager.load_helper_files(self.current_problem_number)
                if filename in helper_files:
                    self.helpers_editor.setPlainText(helper_files[filename])
                    self.settings_manager.apply_helper_editor_settings(self.helpers_editor)
        finally:
            self._handling_selection = False

    def update_problem(self, problem_number):
        """Update the panel for a new problem."""
        self.current_problem_number = problem_number
        self.update_helper_files_list(problem_number)

    def update_helper_files_list(self, problem_number):
        """Update the helper files list for the current problem."""
        # Prevent recursion with a flag
        if hasattr(self, '_updating_list') and self._updating_list:
            return
            
        try:
            self._updating_list = True
            
            self.helper_files_list.clear()
            helper_files = self.problem_manager.load_helper_files(problem_number)
            for filename in helper_files.keys():
                self.helper_files_list.addItem(filename)
            if self.helper_files_list.count() > 0:
                self.helper_files_list.setCurrentRow(0)
        finally:
            self._updating_list = False

    def add_helper_file(self):
        """Add a new helper file."""
        if not self.current_problem_number:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return

        # Get filename from user
        filename, ok = QInputDialog.getText(
            self,
            "Add Helper File",
            "Enter filename (e.g., gpf.py):",
            QLineEdit.EchoMode.Normal,
            "gpf.py"
        )

        if ok and filename:
            if not filename.endswith('.py'):
                filename += '.py'

            # Create template content
            template = '''"""
Helper functions for Project Euler problems
"""

def example_function(arg1, arg2=None):
    """
    Example helper function.

    Args:
        arg1: First argument
        arg2: Optional second argument

    Returns:
        Result of the operation
    """
    # Your code here
    pass

# Add more helper functions below
'''

            # Save the helper file
            if self.problem_manager.save_helper_file(filename, template):
                QMessageBox.information(self, "Success", f"Helper file {filename} created successfully")

                # Ask if user wants to assign it to the current problem
                reply = QMessageBox.question(
                    self,
                    "Assign Helper File",
                    f"Do you want to assign this helper file to problem {self.current_problem_number}?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    if self.problem_manager.assign_helper_to_problem(self.current_problem_number, filename):
                        self.update_helper_files_list(self.current_problem_number)
                        QMessageBox.information(self, "Success", f"Helper file {filename} assigned to problem {self.current_problem_number}")
                    else:
                        QMessageBox.critical(self, "Error", f"Failed to assign helper file {filename}")
            else:
                QMessageBox.critical(self, "Error", "Failed to create helper file")

    def delete_helper_file(self):
        """Delete the selected helper file."""
        if not self.current_problem_number:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return

        current_item = self.helper_files_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "No helper file selected")
            return

        filename = current_item.text()

        reply = QMessageBox.question(
            self,
            "Delete Helper File",
            f"Are you sure you want to remove {filename} from problem {self.current_problem_number}?\n"
            f"This will not delete the helper file itself, just remove it from this problem.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.problem_manager.unassign_helper_from_problem(self.current_problem_number, filename):
                    self.update_helper_files_list(self.current_problem_number)
                    self.helpers_editor.clear()
                    QMessageBox.information(self, "Success", f"Helper file {filename} removed from problem {self.current_problem_number}")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to remove helper file {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error removing helper file: {str(e)}")

    def test_helper_function(self):
        """Test a function from the current helper file."""
        if not self.current_problem_number:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return

        current_item = self.helper_files_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "No helper file selected")
            return

        filename = current_item.text()

        # Get the helper file content to extract function names
        helper_files = self.problem_manager.load_helper_files(self.current_problem_number)
        if filename not in helper_files:
            QMessageBox.warning(self, "Warning", f"Helper file {filename} not found")
            return

        file_content = helper_files[filename]

        # Extract function names using ast module
        function_names = []
        try:
            tree = ast.parse(file_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_names.append(node.name)
            function_names.sort()  # Sort alphabetically for consistency
        except SyntaxError:
            QMessageBox.warning(self, "Warning", f"Syntax error in helper file {filename}")
            return

        if not function_names:
            QMessageBox.warning(self, "Warning", f"No functions found in helper file {filename}")
            return

        # Create dialog to select function
        dialog = QInputDialog()
        dialog.setWindowTitle("Test Helper Function")
        dialog.setLabelText("Select function to test:")
        dialog.setComboBoxItems(function_names)
        dialog.setComboBoxEditable(False)

        if dialog.exec() != QInputDialog.DialogCode.Accepted:
            return

        function_name = dialog.textValue()
        if not function_name:
            return

        # Get function arguments from user
        args_text, ok = QInputDialog.getText(
            self,
            "Test Helper Function",
            "Enter function arguments (comma-separated):",
            QLineEdit.EchoMode.Normal
        )

        if not ok:
            return

        # Parse arguments
        args = []
        kwargs = {}

        if args_text.strip():
            try:
                # Split by commas but preserve those within quotes
                parts = []
                current = ""
                in_quotes = False
                for char in args_text:
                    if char in ['"', "'"]:
                        in_quotes = not in_quotes
                        current += char
                    elif char == ',' and not in_quotes:
                        parts.append(current.strip())
                        current = ""
                    else:
                        current += char
                if current:
                    parts.append(current.strip())

                # Process each part
                for part in parts:
                    if '=' in part and not any(c in part for c in ['"', "'", '(', ')']):
                        # Keyword argument
                        key, value = part.split('=', 1)
                        kwargs[key.strip()] = eval(value.strip())
                    else:
                        # Positional argument
                        args.append(eval(part.strip()))

                # Special handling for hamming_weight function
                if function_name == "hamming_weight" and len(args) > 1:
                    # The hamming_weight function only takes one argument
                    # Show a warning and only use the first argument
                    QMessageBox.warning(
                        self,
                        "Warning",
                        f"The hamming_weight function only takes one argument. Only the first argument will be used."
                    )
                    args = [args[0]]
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Invalid arguments: {str(e)}")
                return

        # Get the run manager to use debug panel
        if hasattr(self.problem_manager, 'run_manager') and self.problem_manager.run_manager:
            run_manager = self.problem_manager.run_manager
            debug_panel = run_manager.debug_panel
            
            # Switch to debug tab to show results
            if 'tab_widget' in run_manager.ui:
                run_manager.ui['tab_widget'].setCurrentIndex(4)  # Debug tab index
                
                # Highlight the debug tab if main window is available
                main_window = run_manager.ui['tab_widget'].parent()
                while main_window and not hasattr(main_window, 'highlight_debug_tab'):
                    main_window = main_window.parent()
                if main_window and hasattr(main_window, 'highlight_debug_tab'):
                    main_window.highlight_debug_tab()
            
            # Add test start message to debug panel
            debug_panel.add_debug_message("=" * 60, "info")
            debug_panel.add_debug_message(f"Testing helper function: {function_name}()", "info")
            debug_panel.add_debug_message(f"Arguments: {args}, Kwargs: {kwargs}", "info")
            debug_panel.add_debug_message("=" * 60, "info")

        # Run the test using run manager
        result = self.problem_manager.test_helper_function(
            self.current_problem_number,
            function_name,
            *args,  # Unpack the args list to pass individual arguments
            **kwargs
        )

        # Display result in debug panel and also show a brief message box
        if result["success"]:
            if hasattr(self.problem_manager, 'run_manager') and self.problem_manager.run_manager:
                debug_panel = self.problem_manager.run_manager.debug_panel
                debug_panel.add_debug_message("", "info")  # Empty line for spacing
                debug_panel.add_debug_message("🎉 HELPER FUNCTION TEST SUCCESSFUL! 🎉", "important")
                debug_panel.add_debug_message(f"Result: {result['result']}", "important")
                debug_panel.add_debug_message(f"Execution time: {result['execution_time']:.6f} seconds", "info")
                debug_panel.add_debug_message("=" * 60, "info")
            
            # Show brief success message
            msg = QMessageBox()
            msg.setWindowTitle("Test Result")
            msg.setText(f"✅ Test successful!\nResult: {result['result']}\nExecution Time: {result['execution_time']:.6f} seconds")
            msg.exec()
        else:
            if hasattr(self.problem_manager, 'run_manager') and self.problem_manager.run_manager:
                debug_panel = self.problem_manager.run_manager.debug_panel
                debug_panel.add_debug_message("", "error")  # Empty line for spacing
                debug_panel.add_debug_message("❌ HELPER FUNCTION TEST FAILED! ❌", "error")
                debug_panel.add_debug_message(f"Error: {result['error']}", "error")
                
                if 'traceback' in result and result['traceback']:
                    debug_panel.add_debug_message("Traceback:", "error")
                    for line in result['traceback'].splitlines():
                        debug_panel.add_debug_message(f"    {line}", "error")
                
                debug_panel.add_debug_message("=" * 60, "error")
            
            # Show error message
            error_msg = f"❌ Test failed!\nError: {result['error']}"
            if 'traceback' in result and result['traceback']:
                error_msg += f"\n\nSee Debug Output tab for full traceback."

            msg = QMessageBox()
            msg.setWindowTitle("Test Error")
            msg.setText(error_msg)
            msg.exec()

    def save_current_helper_file(self):
        """Save the current helper file."""
        if not self.current_problem_number:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return

        current_item = self.helper_files_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "No helper file selected")
            return

        filename = current_item.text()
        content = self.helpers_editor.toPlainText()
        
        # Check if we should auto-format
        if self.helpers_editor.code_formatter.should_auto_format():
            # Format the code before saving
            self.helpers_editor.format_code()
            # The actual save will happen after formatting is complete
            return
        
        # Save the helper file
        if self.problem_manager.save_helper_file(filename, content):
            QMessageBox.information(self, "Success", f"Helper file {filename} saved successfully")
            
            # Apply auto-lint if enabled
            if self.helpers_editor.code_formatter.should_auto_lint():
                self.helpers_editor.lint_code()
        else:
            QMessageBox.critical(self, "Error", f"Failed to save helper file {filename}")

    def load_shared_helper_file(self):
        """Load a helper file and assign it to the current problem."""
        if not self.current_problem_number:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return

        # Get list of available helper files
        available_files = self.problem_manager.get_available_helper_files()
        if not available_files:
            QMessageBox.information(self, "Info", "No helper files available")
            return

        # Create dialog to select helper file
        dialog = QInputDialog()
        dialog.setWindowTitle("Load Helper File")
        dialog.setLabelText("Select helper file to load:")
        dialog.setComboBoxItems(available_files)
        dialog.setComboBoxEditable(False)

        if dialog.exec() == QInputDialog.DialogCode.Accepted:
            filename = dialog.textValue()
            # Assign the helper file to the problem
            if self.problem_manager.assign_helper_to_problem(self.current_problem_number, filename):
                self.update_helper_files_list(self.current_problem_number)
                QMessageBox.information(self, "Success", f"Helper file {filename} assigned to problem {self.current_problem_number}")
            else:
                QMessageBox.critical(self, "Error", f"Failed to assign helper file {filename}")

    def clear(self):
        """Clear the panel content."""
        self.helper_files_list.clear()
        self.helpers_editor.clear()
        self.current_problem_number = None