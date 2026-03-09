from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QScrollArea, QToolTip, QMenu
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QPainter, QTextFormat, QTextCursor, QAction
from PyQt6.QtCore import Qt, QRect, QSize, pyqtSignal, QPoint
import re
from ui.syntax_highlighter import PythonHighlighter
import os
import ast
from ui.code_formatter import CodeFormatter

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-right: 1px solid #3d3d3d;
            }
        """)
        self.show()  # Explicitly show the widget

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

class CodeEditor(QPlainTextEdit):
    # Add a custom signal for when we need to switch back to the solution tab
    switch_to_tab = pyqtSignal(int)

    def __init__(self, parent=None, settings_manager=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.current_problem_number = None
        self.tab_widget = None  # Will be set by the main window
        self.problem_manager = None  # Will be set by the main window
        self.debug_panel = None  # Will be set by the main window

        # Set initial font and style
        self.setFont(QFont("Consolas", 12))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setTabStopDistance(40)  # 4 spaces
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                border: none;
                padding: 10px;
            }
        """)

        # Line number area
        self.line_number_area = LineNumberArea(self)
        self.line_number_area.show()  # Explicitly show the line number area
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width(0)

        # Syntax highlighter
        self.highlighter = PythonHighlighter(self.document(), settings_manager)

        # Error highlighting
        self.error_lines = {}  # Dictionary to store error lines and their messages
        self.error_format = QTextCharFormat()
        self.error_format.setBackground(QColor("#4a1f1f"))
        self.error_format.setUnderlineColor(QColor("#ff6b6b"))
        self.error_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)

        # Auto-indentation
        self.textChanged.connect(self.handle_text_change)
        self.last_cursor_position = 0

        # Initialize code formatter with settings manager
        self.code_formatter = CodeFormatter(settings_manager=self.settings_manager)
        self.code_formatter.formatting_complete.connect(self.handle_formatting_complete)
        self.code_formatter.linting_complete.connect(self.handle_linting_complete)

        # Set up context menu - restore the original approach
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # Track document modification
        self.document().modificationChanged.connect(self.handle_modification_change)

        # Set up Tab/Shift+Tab handling
        self.setup_tab_handling()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return max(space, 30)  # Ensure minimum width of 30 pixels

    def update_line_number_area_width(self, _):
        """Update the viewport margins based on line number width."""
        # Prevent recursion by setting a flag
        if hasattr(self, '_updating_width') and self._updating_width:
            return

        try:
            self._updating_width = True
            width = self.line_number_area_width()
            self.setViewportMargins(width, 0, 0, 0)
        finally:
            self._updating_width = False

    def update_line_number_area(self, rect, dy):
        """Update the line number area on scroll or text change."""
        # Prevent recursion by using a flag
        if hasattr(self, '_updating_area') and self._updating_area:
            return

        try:
            self._updating_area = True

            if dy:
                self.line_number_area.scroll(0, dy)
            else:
                self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

            # Only update width if containing full viewport and not already updating width
            if rect.contains(self.viewport().rect()) and not (hasattr(self, '_updating_width') and self._updating_width):
                self.update_line_number_area_width(0)
        finally:
            self._updating_area = False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), width, cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#2d2d2d"))

        # Use the same font as the editor
        painter.setFont(self.font())

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)

                # Check if this line has an error
                if block_number in self.error_lines:
                    # Use red color for line numbers with errors
                    painter.setPen(QColor("#ff6b6b"))
                else:
                    # Use normal color for other line numbers
                    painter.setPen(QColor("#d4d4d4"))

                painter.drawText(0, int(top), self.line_number_area.width() - 5, self.fontMetrics().height(),
                               Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_error_line(self, line_number, error_message):
        """Highlight a specific line with an error message."""
        # Convert line number to block number (0-based)
        block_number = line_number - 1

        # Store the error message
        self.error_lines[block_number] = error_message

        # Get the block
        block = self.document().findBlockByNumber(block_number)
        if block.isValid():
            # Create a cursor for the block
            cursor = QTextCursor(block)
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)

            # Apply the error format
            cursor.mergeCharFormat(self.error_format)

            # Update the line number area
            self.line_number_area.update()

    def clear_error_highlights(self):
        """Clear all error highlights."""
        # Clear the error lines dictionary
        self.error_lines.clear()

        # Clear the formatting
        cursor = QTextCursor(self.document())
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())

        # Clear the tooltip
        QToolTip.hideText()

        # Update the line number area
        self.line_number_area.update()

        # Force rehighlight to restore normal syntax highlighting
        if hasattr(self, 'highlighter'):
            self.highlighter.rehighlight()

        # Debug message if debug panel is available
        if self.debug_panel:
            self.debug_panel.add_debug_message("Cleared all linting error highlights", "info")

    def mouseMoveEvent(self, event):
        """Show error tooltip when hovering over error lines."""
        # Get the cursor position
        cursor = self.cursorForPosition(event.pos())
        block_number = cursor.blockNumber()

        # Check if this line has an error
        if block_number in self.error_lines:
            # Show the error message as a tooltip
            QToolTip.showText(event.globalPosition().toPoint(), self.error_lines[block_number])
        else:
            QToolTip.hideText()

        super().mouseMoveEvent(event)

    def get_indentation_level(self, text):
        """Calculate the indentation level of a line of text."""
        return len(text) - len(text.lstrip())

    def should_increase_indent(self, text):
        """Check if the current line should increase indentation for the next line."""
        # Remove comments and whitespace
        text = text.split('#')[0].strip()
        if not text:
            return False

        # Check for statements that should increase indentation
        increase_patterns = [
            r':\s*$',  # Ends with colon
            r'def\s+\w+\s*\(',  # Function definition
            r'class\s+\w+\s*\(?',  # Class definition
            r'if\s+.+:',  # If statement
            r'elif\s+.+:',  # Elif statement
            r'else\s*:',  # Else statement
            r'for\s+.+:',  # For loop
            r'while\s+.+:',  # While loop
            r'try\s*:',  # Try block
            r'except\s+.+:',  # Except block
            r'finally\s*:',  # Finally block
            r'with\s+.+:'  # With statement
        ]

        for pattern in increase_patterns:
            if re.search(pattern, text):
                return True
        return False

    def should_decrease_indent(self, text):
        """Check if the current line should decrease indentation for the next line."""
        # Remove comments and whitespace
        text = text.split('#')[0].strip()
        if not text:
            return False

        # Check for statements that should decrease indentation
        decrease_patterns = [
            r'^\s*(return|break|continue|pass)\s*$',  # Control flow statements
            r'^\s*raise\s+.+$',  # Raise statement
            r'^\s*return\s+.+$'  # Return with value
        ]

        for pattern in decrease_patterns:
            if re.search(pattern, text):
                return True
        return False

    def handle_text_change(self):
        """Handle text changes and implement auto-indentation."""
        # Mark document as modified to ensure proper save handling
        self.document().setModified(True)

        cursor = self.textCursor()
        current_position = cursor.position()

        # Check if we just added a new line (Enter/Return was pressed)
        if current_position > self.last_cursor_position and self.toPlainText()[current_position-1] == '\n':
            # Get the current block (line)
            current_block = cursor.block()
            previous_block = current_block.previous()

            if previous_block.isValid():
                # Get the text of the previous line
                previous_text = previous_block.text()

                # Calculate base indentation
                base_indent = self.get_indentation_level(previous_text)

                # Check if we should increase or decrease indentation
                if self.should_increase_indent(previous_text):
                    base_indent += 4  # Increase by one level (4 spaces)
                elif self.should_decrease_indent(previous_text):
                    base_indent = max(0, base_indent - 4)  # Decrease by one level

                # Apply the indentation
                cursor.insertText(' ' * base_indent)

        # Update the last cursor position
        self.last_cursor_position = current_position

    def update_highlighting(self):
        """Update the syntax highlighting."""
        if self.highlighter:
            self.highlighter.update_highlighting_rules()
            self.highlighter.rehighlight()

    def create_problem_template(self, problem_number):
        """Create a template for a new problem."""
        self.current_problem_number = problem_number

        # Create basic template for new problems
        template = f"""# Project Euler Problem {problem_number}
# https://projecteuler.net/problem={problem_number}

import time
import os

def solve():
    # Your solution code here
    return None  # Replace with your solution

if __name__ == "__main__":
    start_time = time.time()
    result = solve()
    execution_time = time.time() - start_time

    # Important: These print statements are used to extract the result and execution time
    print(f"Result: {{result}}")
    print(f"Execution time: {{execution_time:.6f}} seconds")
"""
        self.setPlainText(template)

        # Position cursor at the solution code placeholder
        document = self.document()
        find_cursor = document.find("# Your solution code here", 0)
        if not find_cursor.isNull():
            cursor = self.textCursor()
            cursor.setPosition(find_cursor.position())
            cursor.movePosition(cursor.MoveOperation.StartOfLine)
            cursor.movePosition(cursor.MoveOperation.Down)
            cursor.movePosition(cursor.MoveOperation.StartOfLine)
            self.setTextCursor(cursor)

        return template

    def add_import_statement_for_helper(self, helper_filename, helper_filepath):
        """Add an import statement for the helper file to the code editor."""
        if not helper_filename.endswith('.py'):
            return

        # Get current code from editor
        current_code = self.toPlainText()

        # Extract the module name (remove .py extension)
        module_name = helper_filename[:-3]

        # Check if this import already exists in the code
        import_patterns = [
            f"import helpers.{module_name}",
            f"import {module_name}",
            f"from helpers.{module_name} import",
            f"from {module_name} import",
        ]

        # Skip if any pattern is already in the code
        if any(pattern in current_code for pattern in import_patterns):
            return

        # Get the helper file content to extract function names
        try:
            with open(helper_filepath, 'r') as f:
                file_content = f.read()

            # Extract function names using ast module
            function_names = []
            try:
                tree = ast.parse(file_content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        function_names.append(node.name)
                function_names.sort()  # Sort alphabetically for consistency
            except SyntaxError:
                # If parsing fails, fall back to wildcard import
                import_statement = f"from helpers.{module_name} import *  # All functions\n"

            if function_names:
                # Create import statement with explicit function list
                # Break into multiple lines if too many functions
                if len(function_names) <= 4:
                    functions_str = ", ".join(function_names)
                    import_statement = f"from helpers.{module_name} import {functions_str}\n"
                else:
                    # Format multiline import with each function on separate line
                    functions_str = ", ".join(function_names)
                    import_statement = f"from helpers.{module_name} import (\n    "
                    import_statement += ",\n    ".join(function_names)
                    import_statement += "\n)\n"
            else:
                # No functions found, use wildcard import
                import_statement = f"from helpers.{module_name} import *  # No functions found\n"
        except Exception as e:
            # Fall back to wildcard import on any error
            import_statement = f"from helpers.{module_name} import *  # Fallback import\n"

        # Find a good place to insert the import statement
        # Check if there are already other imports
        lines = current_code.split('\n')

        # Look for the best insertion point
        insert_position = 0

        # First, look for existing imports
        import_section_end = -1
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_section_end = i

        if import_section_end >= 0:
            # Insert after the last import
            insert_position = sum(len(line) + 1 for line in lines[:import_section_end+1])
            import_statement = '\n' + import_statement
        else:
            # Look for a docstring or shebang
            for i, line in enumerate(lines):
                if i == 0 and line.startswith('#!'):
                    # Skip shebang line
                    continue
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    # Find the end of the docstring
                    for j in range(i+1, len(lines)):
                        if '"""' in lines[j] or "'''" in lines[j]:
                            # Insert after the docstring
                            insert_position = sum(len(line) + 1 for line in lines[:j+1])
                            import_statement = '\n\n' + import_statement
                            break
                    break

            # If no docstring found, insert at the beginning with a blank line after
            if insert_position == 0:
                import_statement = import_statement + '\n'

        # Insert the import statement
        cursor = self.textCursor()
        cursor.setPosition(insert_position)
        cursor.insertText(import_statement)

        # Update the cursor position
        self.setTextCursor(cursor)

        # Switch to solution tab if we have a tab widget
        if self.tab_widget:
            solution_tab_index = 0  # Index of solution tab
            self.switch_to_tab.emit(solution_tab_index)

    def insert_data_loading_code(self, data_method=None):
        """Insert the data loading code into the code editor.

        Args:
            data_method (str): The method to use for loading data.
        """
        if not data_method:
            return

        # Create the loading code
        loading_code = f"# Load the data file\n{data_method} = problem_manager.{data_method}()\n"

        # Get current cursor position
        cursor = self.textCursor()

        # Find the solve function
        document = self.document()
        find_cursor = document.find("def solve():", 0)
        if not find_cursor.isNull():
            # Move cursor to the start of the solve function
            cursor.setPosition(find_cursor.position())
            cursor.movePosition(cursor.MoveOperation.Down)
            cursor.movePosition(cursor.MoveOperation.EndOfLine)
            cursor.insertText("\n" + loading_code)
        else:
            # If solve function not found, insert at cursor position
            cursor.insertText(loading_code)

        # Update the cursor
        self.setTextCursor(cursor)

        # Switch to solution tab (emit signal if tab_widget is set)
        if self.tab_widget:
            solution_tab_index = 0  # Index of solution tab
            self.switch_to_tab.emit(solution_tab_index)

    def load_solution(self, solution_text):
        """Load a solution into the editor."""
        if solution_text:
            self.setPlainText(solution_text)
        return True

    def get_solution_text(self):
        """Get the current solution text."""
        return self.toPlainText()

    def save_solution_with_execution_time(self, execution_time=None):
        """Save the solution with the execution time and apply auto-format/lint if enabled."""
        # Clear any existing linting highlights before saving
        self.clear_error_highlights()

        # Check if we should auto-format
        if self.settings_manager and self.code_formatter.should_auto_format():
            # Format the code before saving
            self.format_code()
            # Note: The actual save will happen after the formatting is complete via signal
            return True

        # Save the solution as usual
        if self.current_problem_number and self.problem_manager:
            solution = self.toPlainText()

            # Add execution time comment if provided
            if execution_time is not None:
                # Check if there's already an execution time comment
                lines = solution.split('\n')
                has_time_comment = False

                for i, line in enumerate(lines):
                    if "# Execution time:" in line:
                        # Update the existing comment
                        lines[i] = f"# Execution time: {execution_time:.6f} seconds"
                        has_time_comment = True
                        break

                if not has_time_comment:
                    # Add a new comment at the end
                    lines.append(f"# Execution time: {execution_time:.6f} seconds")

                solution = '\n'.join(lines)

            # Save the solution
            success = self.problem_manager.save_solution(self.current_problem_number, solution)

            # Mark document as unmodified to trigger the proper handling
            self.document().setModified(False)

            # If auto-lint is enabled, lint the code after saving
            if success and self.settings_manager and self.code_formatter.should_auto_lint():
                self.lint_code()

            return success

        return False

    def prepare_for_execution(self):
        """Prepare the code for execution and return it."""
        # Get code from the editor
        code = self.get_solution_text()

        # Clear any previous error highlights
        self.clear_error_highlights()

        return code

    def handle_execution_error(self, error_info):
        """Handle execution error by highlighting the error line."""
        if 'line_number' in error_info and 'message' in error_info:
            line_number = error_info['line_number']
            message = error_info['message']

            # Check if line_number is None or not an integer
            if line_number is None or not isinstance(line_number, int):
                self.add_debug_message(f"Error: {message}", "error")
                return False

            self.highlight_error_line(line_number, message)

            # Move cursor to error line
            cursor = self.textCursor()
            block = self.document().findBlockByLineNumber(line_number - 1)
            if block.isValid():
                cursor.setPosition(block.position())
                self.setTextCursor(cursor)
                self.centerCursor()

            # Switch to solution tab if we have a tab widget
            if self.tab_widget:
                solution_tab_index = 0  # Index of solution tab
                self.switch_to_tab.emit(solution_tab_index)

            return True
        return False

    def set_problem_manager(self, problem_manager):
        """Set the problem manager instance."""
        self.problem_manager = problem_manager

    def set_tab_widget(self, tab_widget):
        """Set the tab widget instance for tab switching."""
        self.tab_widget = tab_widget

    def set_current_problem(self, problem_number):
        """Set the current problem number."""
        self.current_problem_number = problem_number

    def add_debug_message(self, message, level="debug"):
        """Add a debug message to the debug panel if available."""
        # If connected to a debug panel through the main application, use it
        if hasattr(self, 'debug_panel') and self.debug_panel:
            self.debug_panel.add_debug_message(message, level)
        # Otherwise just print to console for now
        else:
            print(f"[{level}] {message}")

    def set_debug_panel(self, debug_panel):
        """Set the debug panel instance."""
        self.debug_panel = debug_panel
        # Also set it for the code formatter
        self.code_formatter.debug_panel = debug_panel

    def format_code(self):
        """Format the code using Black."""
        code = self.toPlainText()
        if not code.strip():
            return

        # Format the code
        self.code_formatter.format_code(code)

    def lint_code(self):
        """Lint the code using Pylint."""
        code = self.toPlainText()
        if not code.strip():
            return

        # Clear any previous error highlights
        self.clear_error_highlights()

        # Lint the code
        self.code_formatter.lint_code(code)

    def handle_formatting_complete(self, formatted_code):
        """Handle the completion of code formatting."""
        if not formatted_code:
            return

        # Save cursor position
        cursor = self.textCursor()
        position = cursor.position()

        # Update the text
        self.setPlainText(formatted_code)

        # Try to restore cursor position
        cursor = self.textCursor()
        if position < len(formatted_code):
            cursor.setPosition(position)
            self.setTextCursor(cursor)

        # Show message in debug panel if available
        if self.debug_panel:
            self.debug_panel.add_debug_message("Code formatted with Black", "info")

        # If this was auto-format on save, then save the solution
        if self.settings_manager and self.code_formatter.should_auto_format():
            # Save the formatted solution
            if self.current_problem_number and self.problem_manager:
                solution = self.toPlainText()
                success = self.problem_manager.save_solution(self.current_problem_number, solution)

                # Mark document as unmodified after saving
                self.document().setModified(False)

                # If auto-lint is enabled, lint the code after saving
                if success and self.code_formatter.should_auto_lint():
                    self.lint_code()

    def handle_linting_complete(self, lint_results):
        """Handle the completion of code linting."""
        if not lint_results:
            if self.debug_panel:
                self.debug_panel.add_debug_message("No linting issues found", "info")
            return

        # Clear any previous error highlights
        self.clear_error_highlights()

        # Highlight the errors
        for error in lint_results:
            line = error.get('line', 0)
            message = f"{error.get('type', 'error')}: {error.get('message', '')} ({error.get('symbol', '')})"

            # Highlight the error line
            self.highlight_error_line(line, message)

        # Show message in debug panel if available
        if self.debug_panel:
            # First display a summary
            self.debug_panel.add_debug_message(f"Found {len(lint_results)} linting issues", "warning")

            # Then add each individual issue with details
            for error in lint_results:
                line = error.get('line', 0)
                message = f"Line {line}: {error.get('type', 'error')}: {error.get('message', '')} ({error.get('symbol', '')})"
                self.debug_panel.add_debug_message(message, "detail")

    def show_context_menu(self, pos):
        """Show the custom context menu with additional options for linting errors."""
        # Get cursor at the clicked position
        cursor = self.cursorForPosition(pos)
        block_number = cursor.blockNumber()

        # Create standard context menu
        menu = self.createStandardContextMenu()
        menu.addSeparator()

        # Check if clicked on a line with error
        if block_number in self.error_lines:
            # Add action to show error details
            error_action = QAction("View Linting Error Details", self)
            error_action.triggered.connect(lambda: self.show_linting_error_dialog(block_number))
            menu.addAction(error_action)
            menu.addSeparator()

        # Add formatting action
        format_action = QAction("Format with Black", self)
        format_action.triggered.connect(self.format_code)
        menu.addAction(format_action)

        # Add linting action
        lint_action = QAction("Lint with Pylint", self)
        lint_action.triggered.connect(self.lint_code)
        menu.addAction(lint_action)

        # Add clear linting highlights action, but only if there are highlights
        if hasattr(self, 'error_lines') and self.error_lines:
            # Add separator
            menu.addSeparator()

            # Add clear highlights action
            clear_action = QAction("Clear Linting Highlights", self)
            clear_action.triggered.connect(self.clear_error_highlights)
            menu.addAction(clear_action)

        # Add separator for text editing actions
        menu.addSeparator()

        # Add indent action
        indent_action = QAction("Indent", self)
        indent_action.triggered.connect(self.indent_selected_text)
        indent_action.setShortcut("Tab")
        menu.addAction(indent_action)

        # Add dedent action
        dedent_action = QAction("Dedent", self)
        dedent_action.triggered.connect(self.dedent_selected_text)
        dedent_action.setShortcut("Shift+Tab")
        menu.addAction(dedent_action)

        # Show the menu
        menu.exec(self.mapToGlobal(pos))

    def indent_selected_text(self):
        """Indent the selected text or current line."""
        cursor = self.textCursor()

        if cursor.hasSelection():
            # Get selection boundaries
            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            # Move cursor to start of selection
            cursor.setPosition(start)
            cursor.movePosition(cursor.MoveOperation.StartOfBlock)
            start_block = cursor.blockNumber()

            # Move cursor to end of selection
            cursor.setPosition(end)
            cursor.movePosition(cursor.MoveOperation.StartOfBlock)
            end_block = cursor.blockNumber()

            # Begin edit block for undo/redo
            cursor.beginEditBlock()

            # Indent each line in the selection
            for block_num in range(start_block, end_block + 1):
                cursor.setPosition(self.document().findBlockByNumber(block_num).position())
                cursor.insertText("    ")  # Insert 4 spaces

            cursor.endEditBlock()

            # Restore selection (adjusted for added indentation)
            new_start = self.document().findBlockByNumber(start_block).position()
            new_end = self.document().findBlockByNumber(end_block).position() + \
                     self.document().findBlockByNumber(end_block).length() - 1
            cursor.setPosition(new_start)
            cursor.setPosition(new_end, cursor.MoveMode.KeepAnchor)
            self.setTextCursor(cursor)
        else:
            # No selection, indent current line
            cursor.movePosition(cursor.MoveOperation.StartOfBlock)
            cursor.insertText("    ")  # Insert 4 spaces
            self.setTextCursor(cursor)

    def dedent_selected_text(self):
        """Dedent the selected text or current line."""
        cursor = self.textCursor()

        if cursor.hasSelection():
            # Get selection boundaries
            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            # Move cursor to start of selection
            cursor.setPosition(start)
            cursor.movePosition(cursor.MoveOperation.StartOfBlock)
            start_block = cursor.blockNumber()

            # Move cursor to end of selection
            cursor.setPosition(end)
            cursor.movePosition(cursor.MoveOperation.StartOfBlock)
            end_block = cursor.blockNumber()

            # Begin edit block for undo/redo
            cursor.beginEditBlock()

            # Dedent each line in the selection
            for block_num in range(start_block, end_block + 1):
                block = self.document().findBlockByNumber(block_num)
                text = block.text()

                # Remove up to 4 spaces or 1 tab from the beginning
                if text.startswith("    "):
                    # Remove 4 spaces
                    cursor.setPosition(block.position())
                    cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, 4)
                    cursor.removeSelectedText()
                elif text.startswith("\t"):
                    # Remove 1 tab
                    cursor.setPosition(block.position())
                    cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, 1)
                    cursor.removeSelectedText()
                elif text.startswith(" "):
                    # Remove available spaces (up to 4)
                    spaces_to_remove = 0
                    for char in text[:4]:
                        if char == " ":
                            spaces_to_remove += 1
                        else:
                            break
                    if spaces_to_remove > 0:
                        cursor.setPosition(block.position())
                        cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, spaces_to_remove)
                        cursor.removeSelectedText()

            cursor.endEditBlock()

            # Restore selection (adjusted for removed indentation)
            new_start = self.document().findBlockByNumber(start_block).position()
            new_end = self.document().findBlockByNumber(end_block).position() + \
                     self.document().findBlockByNumber(end_block).length() - 1
            cursor.setPosition(new_start)
            cursor.setPosition(new_end, cursor.MoveMode.KeepAnchor)
            self.setTextCursor(cursor)
        else:
            # No selection, dedent current line
            cursor.movePosition(cursor.MoveOperation.StartOfBlock)
            block = cursor.block()
            text = block.text()

            # Remove up to 4 spaces or 1 tab from the beginning
            if text.startswith("    "):
                # Remove 4 spaces
                cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, 4)
                cursor.removeSelectedText()
            elif text.startswith("\t"):
                # Remove 1 tab
                cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, 1)
                cursor.removeSelectedText()
            elif text.startswith(" "):
                # Remove available spaces (up to 4)
                spaces_to_remove = 0
                for char in text[:4]:
                    if char == " ":
                        spaces_to_remove += 1
                    else:
                        break
                if spaces_to_remove > 0:
                    cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, spaces_to_remove)
                    cursor.removeSelectedText()

            self.setTextCursor(cursor)

    def show_linting_error_dialog(self, block_number):
        """Show a dialog with details of the linting error."""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser

        # Get the error message
        error_message = self.error_lines.get(block_number, "Unknown error")

        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Linting Error Details")
        dialog.setMinimumSize(400, 200)

        # Create layout
        layout = QVBoxLayout(dialog)

        # Add the line number
        line_label = QLabel(f"<b>Line {block_number + 1}:</b>")
        layout.addWidget(line_label)

        # Add the error text in a scrollable text browser
        error_browser = QTextBrowser()
        error_browser.setHtml(f"<p style='color: #ff4444;'>{error_message}</p>")
        layout.addWidget(error_browser)

        # Add a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        # Log the error to the debug panel if available
        if self.debug_panel:
            self.debug_panel.add_debug_message(f"Line {block_number + 1}: {error_message}", "error")

        # Show the dialog
        dialog.exec()

    def handle_modification_change(self, modified):
        """Handle document modification changes."""
        # If document was modified and then saved (modification state changes to False)
        if not modified and hasattr(self, 'error_lines') and self.error_lines:
            # Clear linting highlights when document is saved
            self.clear_error_highlights()
            if self.debug_panel:
                self.debug_panel.add_debug_message("Linting highlights cleared after save", "info")

    def setup_tab_handling(self):
        """Set up Tab and Shift+Tab key handling."""
        # Tab handling will be done in keyPressEvent
        pass

    def keyPressEvent(self, event):
        """Handle key press events, including Tab and Shift+Tab for indent/dedent."""
        from PyQt6.QtCore import Qt

        # Handle Tab key for indentation
        if event.key() == Qt.Key.Key_Tab and event.modifiers() == Qt.KeyboardModifier.NoModifier:
            cursor = self.textCursor()
            if cursor.hasSelection():
                # If text is selected, indent the selection
                self.indent_selected_text()
            else:
                # If no selection, insert 4 spaces (or handle auto-indentation)
                cursor.insertText("    ")
            return

        # Handle Shift+Tab for dedentation
        elif event.key() == Qt.Key.Key_Backtab or (event.key() == Qt.Key.Key_Tab and event.modifiers() == Qt.KeyboardModifier.ShiftModifier):
            self.dedent_selected_text()
            return

        # For all other keys, use the default behavior
        super().keyPressEvent(event)
