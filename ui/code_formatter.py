import subprocess
import tempfile
import os
from PyQt6.QtCore import QObject, pyqtSignal

class CodeFormatter(QObject):
    """Utility class for formatting Python code with Black and linting with Pylint."""
    
    # Signal emitted when linting is complete
    linting_complete = pyqtSignal(list)  # List of linting errors/warnings
    
    # Signal emitted when formatting is complete
    formatting_complete = pyqtSignal(str)  # Formatted code
    
    def __init__(self, debug_panel=None, settings_manager=None):
        super().__init__()
        self.debug_panel = debug_panel
        self.settings_manager = settings_manager
    
    def format_code(self, code):
        """Format code using Black."""
        try:
            # Get formatting settings
            formatting_settings = {}
            if self.settings_manager:
                formatting_settings = self.settings_manager.get_formatting_settings()
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(code.encode('utf-8'))
            
            # Build Black command with settings
            black_cmd = ['black', '-q']
            
            # Add line length parameter if specified
            if formatting_settings.get('line_length'):
                black_cmd.extend(['--line-length', str(formatting_settings.get('line_length', 88))])
            
            # Add skip string normalization if enabled
            if formatting_settings.get('skip_string_normalization'):
                black_cmd.append('--skip-string-normalization')
            
            # Add the file path
            black_cmd.append(temp_file_path)
            
            # Format the code using Black
            process = subprocess.run(
                black_cmd,
                capture_output=True,
                text=True
            )
            
            # Read the formatted code
            with open(temp_file_path, 'r') as f:
                formatted_code = f.read()
            
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            # Emit the formatted code
            self.formatting_complete.emit(formatted_code)
            
            return formatted_code
            
        except Exception as e:
            if self.debug_panel:
                self.debug_panel.add_debug_message(f"Formatting error: {str(e)}", "error")
            return code
    
    def lint_code(self, code, filename="temp.py"):
        """Lint code using Pylint."""
        try:
            # Get linting settings
            linting_settings = {}
            if self.settings_manager:
                linting_settings = self.settings_manager.get_linting_settings()
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(code.encode('utf-8'))
            
            # Build Pylint command with settings
            pylint_cmd = ['pylint', '--output-format=json']
            
            # Add disabled checks if specified
            if linting_settings.get('disabled_checks'):
                disabled_checks = linting_settings.get('disabled_checks')
                pylint_cmd.extend(['--disable', disabled_checks])
            
            # Add the file path
            pylint_cmd.append(temp_file_path)
            
            # Lint the code using Pylint
            process = subprocess.run(
                pylint_cmd,
                capture_output=True,
                text=True
            )
            
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            # Process the linting results
            import json
            if process.stdout:
                try:
                    lint_results = json.loads(process.stdout)
                    
                    # Convert to a simpler format
                    errors = []
                    for result in lint_results:
                        errors.append({
                            'line': result.get('line', 0),
                            'column': result.get('column', 0),
                            'type': result.get('type', 'error'),
                            'symbol': result.get('symbol', ''),
                            'message': result.get('message', '')
                        })
                    
                    # Sort by line number
                    errors.sort(key=lambda x: x.get('line', 0))
                    
                    # Emit the linting results
                    self.linting_complete.emit(errors)
                    
                    return errors
                except json.JSONDecodeError:
                    if self.debug_panel:
                        self.debug_panel.add_debug_message(f"Error parsing linting results: {process.stdout}", "error")
                    return []
            
            return []
            
        except Exception as e:
            if self.debug_panel:
                self.debug_panel.add_debug_message(f"Linting error: {str(e)}", "error")
            return []
    
    def should_auto_format(self):
        """Check if auto-format on save is enabled."""
        if self.settings_manager:
            formatting_settings = self.settings_manager.get_formatting_settings()
            return formatting_settings.get('auto_format_on_save', False)
        return False
    
    def should_auto_lint(self):
        """Check if auto-lint on save is enabled."""
        if self.settings_manager:
            linting_settings = self.settings_manager.get_linting_settings()
            return linting_settings.get('auto_lint_on_save', False)
        return False 