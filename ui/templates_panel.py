from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QListWidget, QMessageBox, QInputDialog, QLineEdit,
                            QLabel)
from PyQt6.QtCore import pyqtSignal
from ui.code_editor import CodeEditor
import traceback
import time
import ast
from pathlib import Path

class TemplatesPanel(QWidget):
    """Panel for managing code templates."""

    def __init__(self, settings_manager, problem_manager, main_code_editor=None, tab_widget=None):
        super().__init__()
        self.settings_manager = settings_manager
        self.problem_manager = problem_manager
        self.main_code_editor = main_code_editor
        self.tab_widget = tab_widget
        self.current_template_name = None

        self._create_ui()
        self._apply_settings()

    def _create_ui(self):
        """Create the UI components."""
        layout = QVBoxLayout(self)

        # Templates controls
        controls_layout = QHBoxLayout()
        self.new_template_button = QPushButton("New Template")
        self.save_template_button = QPushButton("Save Template")
        self.delete_template_button = QPushButton("Delete Template")
        self.insert_template_button = QPushButton("Insert Template")
        self.test_template_button = QPushButton("Test Template")

        controls_layout.addWidget(self.new_template_button)
        controls_layout.addWidget(self.save_template_button)
        controls_layout.addWidget(self.delete_template_button)
        controls_layout.addWidget(self.insert_template_button)
        controls_layout.addWidget(self.test_template_button)

        # Templates list
        self.templates_list = QListWidget()
        self.templates_list.setStyleSheet("""
            QListWidget {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: none;
                padding: 5px;
            }
        """)
        self.templates_list.setFixedHeight(100)

        # Template code preview
        self.template_code_preview = CodeEditor(settings_manager=self.settings_manager)
        self.template_code_preview.set_problem_manager(self.problem_manager)

        # Add widgets to layout
        layout.addLayout(controls_layout)
        layout.addWidget(self.templates_list)
        layout.addWidget(QLabel("Code:"))
        layout.addWidget(self.template_code_preview)

        # Connect signals
        self.new_template_button.clicked.connect(self.create_new_template)
        self.save_template_button.clicked.connect(self.save_current_template)
        self.delete_template_button.clicked.connect(self.delete_template)
        self.insert_template_button.clicked.connect(self.insert_template)
        self.test_template_button.clicked.connect(self.test_template)
        self.templates_list.currentItemChanged.connect(self.show_template_details)

        # Apply settings to template editor from saved settings
        self.settings_manager.apply_template_editor_settings(self.template_code_preview)

    def _apply_settings(self):
        """Apply settings to the panel."""
        self.settings_manager.apply_template_editor_settings(self.template_code_preview)

    def show_template_details(self, current, previous):
        """Show the details of the selected template."""
        if current is None:
            self.template_code_preview.clear()
            return

        try:
            # Get the template name from the list item
            template_name = current.text()

            # Clean import of templates_manager
            import importlib
            import sys
            if 'templates_manager' in sys.modules:
                importlib.reload(sys.modules['templates_manager'])
            from templates_manager import TemplatesManager

            # Create a fresh manager to ensure we're getting the latest templates
            templates_manager = TemplatesManager()

            # Find the template that matches this name
            templates = templates_manager.load_templates(force_reload=True)
            template_data = None

            # First, try exact match on name
            for key, template in templates.items():
                if template["name"] == template_name:
                    template_data = template
                    break

            # If not found, try case-insensitive match
            if template_data is None:
                for key, template in templates.items():
                    if template["name"].lower() == template_name.lower():
                        template_data = template
                        break

            if template_data:
                # Only update the code preview and current_template_name if we have valid data
                code = template_data["code"]
                self.template_code_preview.setPlainText(code)
                self.current_template_name = template_name
            else:
                self.template_code_preview.clear()
        except Exception as e:
            traceback.print_exc()

    def create_new_template(self):
        """Create a new template using the inline editor."""
        # Ask for template name
        name, ok = QInputDialog.getText(
            self,
            "New Template",
            "Enter name for new template:",
            QLineEdit.EchoMode.Normal,
            "New Template"
        )

        if not ok or not name:
            return

        # Create a temporary item for the new template
        self.templates_list.addItem(name)
        new_item = self.templates_list.item(self.templates_list.count() - 1)
        self.templates_list.setCurrentItem(new_item)

        # Show empty template
        self.template_code_preview.clear()

        # Store current template name
        self.current_template_name = name

        # Set focus to the code editor
        self.template_code_preview.setFocus()

    def save_current_template(self):
        """Save the currently edited template."""
        if not self.current_template_name:
            return

        try:
            # Get content from fields
            name = self.current_template_name
            
            # Check if we should auto-format
            if self.template_code_preview.code_formatter.should_auto_format():
                # Format the code before saving
                self.template_code_preview.format_code()
                # We will continue after formatting completes
                return
            
            code = self.template_code_preview.toPlainText().strip()

            # Ask user if they want to rename the template
            new_name, ok = QInputDialog.getText(
                self,
                "Save Template",
                "Template name (leave as is or enter new name):",
                QLineEdit.EchoMode.Normal,
                name
            )

            if not ok:
                return

            if new_name:
                name = new_name

            # Validate input
            if not name:
                QMessageBox.warning(self, "Warning", "Template name cannot be empty")
                return

            if not code:
                QMessageBox.warning(self, "Warning", "Template code cannot be empty")
                return

            # Clean import of templates_manager
            import importlib
            import sys
            if 'templates_manager' in sys.modules:
                importlib.reload(sys.modules['templates_manager'])
            from templates_manager import TemplatesManager

            # Always create a fresh manager
            templates_manager = TemplatesManager()

            # Get description from existing template if available
            description = ""
            templates = templates_manager.load_templates(force_reload=True)
            for key, template in templates.items():
                if template["name"] == self.current_template_name:
                    description = template.get("description", "")
                    break

            # If there was no description and this is a rename, try with the new name
            if not description and name != self.current_template_name:
                for key, template in templates.items():
                    if template["name"] == name:
                        description = template.get("description", "")
                        break

            # Create template data
            template_data = {
                "name": name,
                "description": description,
                "code": code
            }

            # Make sure templates directory exists
            templates_dir = Path("templates")
            templates_dir.mkdir(exist_ok=True)

            # Delete the old template if the name changed
            if name != self.current_template_name:
                templates_manager.delete_template(self.current_template_name)

            # Save the template
            success = templates_manager.add_template(name, template_data)

            if success:
                # Update the current template name
                self.current_template_name = name

                # Show success message
                QMessageBox.information(self, "Success", f"Template '{name}' saved successfully")

                # Force reload templates to show updated list
                self.load_templates(force_reload=True)

                # Find and select the item with the new name
                for i in range(self.templates_list.count()):
                    if self.templates_list.item(i).text() == name:
                        self.templates_list.setCurrentRow(i)
                        break
                        
                # Apply auto-lint if enabled
                if self.template_code_preview.code_formatter.should_auto_lint():
                    self.template_code_preview.lint_code()
            else:
                QMessageBox.critical(self, "Error", f"Failed to save template '{name}'")
        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Error saving template: {str(e)}")

    def delete_template(self):
        """Delete the selected template."""
        current_item = self.templates_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "Please select a template first")
            return

        template_name = current_item.text()

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Delete Template",
            f"Are you sure you want to delete the template '{template_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Delete the template
        success = self.templates_manager.delete_template(template_name)

        if success:
            # Reload templates
            self.load_templates()
            # Clear the preview
            self.template_code_preview.clear()
            # Clear the current template name
            self.current_template_name = None
        else:
            QMessageBox.warning(self, "Warning", f"Could not delete template '{template_name}'")

    def insert_template(self):
        """Insert the selected template into the editor."""
        if not self.main_code_editor:
            QMessageBox.warning(self, "Warning", "Cannot insert template: No code editor available")
            return

        current_item = self.templates_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "Please select a template first")
            return

        # Get the template name from the list item
        template_name = current_item.text()

        # Find the template that matches this name
        templates = self.templates_manager.load_templates()
        template_data = None

        for key, template in templates.items():
            if template["name"] == template_name:
                template_data = template
                break

        if template_data:
            self.main_code_editor.insertPlainText(template_data["code"])

            # Switch to solution tab if tab widget is available
            if self.tab_widget:
                self.tab_widget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Warning", "Could not find the selected template")

    def _extract_function_names(self, code):
        """Extract function names from code."""
        function_names = []
        try:
            # Parse the code
            tree = ast.parse(code)

            # Find all function definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_names.append(node.name)

            return function_names
        except Exception as e:
            print(f"Error parsing code: {e}")
            return []

    def test_template(self):
        """Test the selected template code."""
        # Get the current template code
        template_code = self.template_code_preview.toPlainText()

        if not template_code.strip():
            QMessageBox.warning(self, "Warning", "No template code to test")
            return

        # Get function name from user
        function_names = self._extract_function_names(template_code)

        if not function_names:
            QMessageBox.warning(self, "Warning", "No functions found in template code")
            return

        # Create dialog to select function
        dialog = QInputDialog()
        dialog.setWindowTitle("Test Template Function")
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
            "Test Template Function",
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
                # Handle both positional and keyword arguments
                if '=' in args_text:
                    # Mix of positional and keyword args
                    parts = []
                    in_string = False
                    string_char = None
                    current_part = ""

                    # Parse the arguments string carefully
                    for char in args_text:
                        if char in ['"', "'"]:
                            if not in_string:
                                in_string = True
                                string_char = char
                            elif char == string_char:
                                in_string = False
                                string_char = None

                        if char == ',' and not in_string:
                            parts.append(current_part.strip())
                            current_part = ""
                        else:
                            current_part += char

                    if current_part:
                        parts.append(current_part.strip())

                    # Process each part
                    for part in parts:
                        if '=' in part:
                            key, value = part.split('=', 1)
                            key = key.strip()
                            # Evaluate the value
                            kwargs[key] = eval(value)
                        else:
                            # Evaluate the positional arg
                            args.append(eval(part))
                else:
                    # Only positional args
                    args_text = f"[{args_text}]"
                    args = eval(args_text)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Invalid arguments: {str(e)}")
                return

        # Run the test
        try:
            # Create a namespace with the template code
            namespace = {}

            # Add debug function if available
            debug_panel = None
            if hasattr(self.problem_manager, 'run_manager') and hasattr(self.problem_manager.run_manager, 'debug_panel'):
                debug_panel = self.problem_manager.run_manager.debug_panel
                
                # Clear debug output and switch to debug tab
                debug_panel.clear_debug_output()
                
                # Switch to debug tab
                if hasattr(self.problem_manager.run_manager, 'ui') and 'tab_widget' in self.problem_manager.run_manager.ui:
                    self.problem_manager.run_manager.ui['tab_widget'].setCurrentIndex(4)  # Index of debug tab
                    
                    # Highlight the debug tab if main window is available
                    main_window = self.problem_manager.run_manager.ui['tab_widget'].parent()
                    while main_window and not hasattr(main_window, 'highlight_debug_tab'):
                        main_window = main_window.parent()
                    if main_window and hasattr(main_window, 'highlight_debug_tab'):
                        main_window.highlight_debug_tab()
                
                # Add test start message to debug panel
                debug_panel.add_debug_message("=" * 60, "info")
                debug_panel.add_debug_message(f"Testing template function: {function_name}()", "info")
                debug_panel.add_debug_message(f"Arguments: {args}, Kwargs: {kwargs}", "info")
                debug_panel.add_debug_message("=" * 60, "info")
                
                if debug_panel.is_debug_enabled():
                    namespace['debug'] = debug_panel.get_debug_function()

            # Execute the template code
            exec(template_code, namespace)

            # Check if the function exists
            if function_name not in namespace:
                if debug_panel:
                    debug_panel.add_debug_message(f"❌ Function '{function_name}' not found in template code", "error")
                QMessageBox.warning(self, "Warning", f"Function '{function_name}' not found in template code")
                return

            # Test the function
            start_time = time.time()
            result = namespace[function_name](*args, **kwargs)
            execution_time = time.time() - start_time

            # Display result in debug panel
            if debug_panel:
                debug_panel.add_debug_message("", "info")  # Empty line for spacing
                debug_panel.add_debug_message("🎉 TEMPLATE FUNCTION TEST SUCCESSFUL! 🎉", "important")
                debug_panel.add_debug_message(f"Result: {result}", "important")
                debug_panel.add_debug_message(f"Execution time: {execution_time:.6f} seconds", "info")
                debug_panel.add_debug_message("=" * 60, "info")

            # Show brief success message
            msg = QMessageBox()
            msg.setWindowTitle("Test Result")
            msg.setText(f"✅ Test successful!\nResult: {result}\nExecution Time: {execution_time:.6f} seconds")
            msg.exec()

        except Exception as e:
            # Display error in debug panel
            if debug_panel:
                debug_panel.add_debug_message("", "error")  # Empty line for spacing
                debug_panel.add_debug_message("❌ TEMPLATE FUNCTION TEST FAILED! ❌", "error")
                debug_panel.add_debug_message(f"Error: {str(e)}", "error")
                debug_panel.add_debug_message("Traceback:", "error")
                for line in traceback.format_exc().splitlines():
                    debug_panel.add_debug_message(f"    {line}", "error")
                debug_panel.add_debug_message("=" * 60, "error")
            
            # Show error message
            msg = QMessageBox()
            msg.setWindowTitle("Test Error")
            msg.setText(f"❌ Test failed!\nError: {str(e)}\n\nSee Debug Output tab for full traceback.")
            msg.exec()

    def load_templates(self, force_reload=False):
        """Load templates into the list widget."""
        try:
            # Clean import of templates_manager - don't use old cached versions
            import importlib
            import sys
            if 'templates_manager' in sys.modules:
                importlib.reload(sys.modules['templates_manager'])
            from templates_manager import TemplatesManager

            # Always create a fresh TemplatesManager
            self.templates_manager = TemplatesManager()

            # Clear the current list
            self.templates_list.clear()

            # Load templates with force_reload option
            templates = self.templates_manager.load_templates(force_reload=True)

            # Save current selection name if any
            current_selection = None
            if self.templates_list.currentItem():
                current_selection = self.templates_list.currentItem().text()

            # Add templates to the list
            for key, template in templates.items():
                name = template.get("name", "Unknown")
                self.templates_list.addItem(name)

            # Restore selection if possible
            if current_selection:
                for i in range(self.templates_list.count()):
                    if self.templates_list.item(i).text() == current_selection:
                        self.templates_list.setCurrentRow(i)
                        break
        except Exception:
            traceback.print_exc()

    def clear(self):
        """Clear the panel content."""
        self.templates_list.clear()
        self.template_code_preview.clear()
        self.current_template_name = None