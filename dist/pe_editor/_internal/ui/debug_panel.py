from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                            QPushButton, QLabel, QCheckBox, QLineEdit, QFileDialog,
                            QComboBox, QSplitter, QToolButton, QMenu)
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QIcon, QTextCursor, QAction
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal, QPoint
from datetime import datetime
import os
import re
import json

class DebugPanel(QWidget):
    """
    A widget that provides debug output functionality with level filtering,
    styling, search, variable inspection, and storage of debug settings.
    """
    def __init__(self, settings_manager=None):
        super().__init__()
        self.settings_manager = settings_manager
        self.variable_values = {}  # Store tracked variables
        self.current_problem_number = None
        
        # Setup UI first, as it creates the UI elements with default values
        self.setup_ui()
        
        # Then load settings to override the defaults
        if self.settings_manager:
            # Ensure all signals are blocked during initialization to prevent feedback loops
            self.debug_enabled_checkbox.blockSignals(True)
            self.show_timestamp_checkbox.blockSignals(True)
            for checkbox in self.debug_level_checkboxes.values():
                checkbox.blockSignals(True)
                
            # Load and apply settings
            self.load_debug_settings()
            
            # Re-enable signals now that initialization is complete
            self.debug_enabled_checkbox.blockSignals(False)
            self.show_timestamp_checkbox.blockSignals(False)
            for checkbox in self.debug_level_checkboxes.values():
                checkbox.blockSignals(False)
        
    def setup_ui(self):
        """Set up the debug panel UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Debug controls
        debug_controls = QHBoxLayout()
        self.debug_enabled_checkbox = QCheckBox("Enable Debug")
        self.debug_enabled_checkbox.setChecked(True)
        
        # Clear button
        self.clear_debug_button = QPushButton("Clear")
        self.clear_debug_button.setToolTip("Clear debug output")
        self.clear_debug_button.setShortcut("Ctrl+Shift+X")
        
        # Save button
        self.save_debug_button = QPushButton("Save")
        self.save_debug_button.setToolTip("Save debug output to file (Ctrl+S)")
        self.save_debug_button.setShortcut("Ctrl+S")
        
        # Search field
        self.search_label = QLabel("Search:")
        self.search_field = QLineEdit()
        self.search_field.setClearButtonEnabled(True)
        self.search_field.setPlaceholderText("Search in debug output... (Ctrl+F)")
        self.search_field.setFixedWidth(200)
        
        # Add controls to layout
        debug_controls.addWidget(self.debug_enabled_checkbox)
        debug_controls.addWidget(self.clear_debug_button)
        debug_controls.addWidget(self.save_debug_button)
        debug_controls.addStretch()
        debug_controls.addWidget(self.search_label)
        debug_controls.addWidget(self.search_field)
        
        main_layout.addLayout(debug_controls)
        
        # Debug level filters
        debug_filters = QHBoxLayout()
        debug_filters.addWidget(QLabel("Show levels:"))
        
        # Create checkboxes for each debug level
        self.debug_level_checkboxes = {}
        for level, color in [
            ("debug", "#FFFFFF"),     # Regular debug - White
            ("important", "#FFAA55"), # Important - Orange
            ("info", "#55FFAA"),      # Info - Light green
            ("error", "#FF5555"),     # Error - Red
            ("detail", "#AAAAAA"),    # Detail - Gray
            ("trace", "#00AAFF")      # Trace - Blue
        ]:
            checkbox = QCheckBox(level.capitalize())
            checkbox.setChecked(True)
            # Set a bit of colored styling to help identify the levels
            checkbox.setStyleSheet(f"QCheckBox {{ color: {color}; }}")
            # Connect the checkbox to save settings when it changes
            checkbox.stateChanged.connect(self.save_debug_settings)
            self.debug_level_checkboxes[level] = checkbox
            debug_filters.addWidget(checkbox)
        
        # Timestamp toggle
        self.show_timestamp_checkbox = QCheckBox("Show Timestamps")
        self.show_timestamp_checkbox.setChecked(True)
        self.show_timestamp_checkbox.stateChanged.connect(self.save_debug_settings)
        debug_filters.addWidget(self.show_timestamp_checkbox)
        
        # Connect master debug checkbox to save settings
        self.debug_enabled_checkbox.stateChanged.connect(self.save_debug_settings)
        
        main_layout.addLayout(debug_filters)
        
        # Create splitter for main area
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setChildrenCollapsible(False)
        
        # Debug output text area
        self.debug_output = QTextEdit()
        self.debug_output.setReadOnly(True)
        self.debug_output.setFont(QFont("Consolas", 11))
        self.debug_output.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #CCCCCC;
                border: none;
                padding: 5px;
            }
        """)
        
        # Setup context menu for debug output
        self.debug_output.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.debug_output.customContextMenuRequested.connect(self.show_debug_context_menu)
        
        splitter.addWidget(self.debug_output)
        
        # Variable inspector
        self.variable_inspector = QTextEdit()
        self.variable_inspector.setReadOnly(True)
        self.variable_inspector.setFont(QFont("Consolas", 11))
        self.variable_inspector.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #CCCCCC;
                border: none;
                padding: 5px;
            }
        """)
        self.variable_inspector.setMaximumHeight(150)
        self.variable_inspector.setHtml("<span style='color:#55AAFF;'>Variable Inspector</span><br>No variables tracked yet")
        
        # Setup context menu for variable inspector
        self.variable_inspector.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.variable_inspector.customContextMenuRequested.connect(self.show_variable_context_menu)
        
        splitter.addWidget(self.variable_inspector)
        
        # Set initial splitter sizes (more space for debug output)
        splitter.setSizes([800, 200])
        
        main_layout.addWidget(splitter)
        
        # Connect signals
        self.clear_debug_button.clicked.connect(self.clear_debug_output)
        self.save_debug_button.clicked.connect(self.save_debug_output)
        self.search_field.textChanged.connect(self.search_debug_output)
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """Set up keyboard shortcuts for the debug panel."""
        # Ctrl+F for focus on search
        search_shortcut = QAction("Search", self)
        search_shortcut.setShortcut("Ctrl+F")
        search_shortcut.triggered.connect(self.focus_search)
        self.addAction(search_shortcut)
        
        # Escape to clear search
        escape_shortcut = QAction("Clear Search", self)
        escape_shortcut.setShortcut("Esc")
        escape_shortcut.triggered.connect(self.clear_search)
        self.addAction(escape_shortcut)
    
    def focus_search(self):
        """Set focus to the search field."""
        self.search_field.setFocus()
        self.search_field.selectAll()
    
    def clear_search(self):
        """Clear the search field."""
        self.search_field.clear()
        
    def show_debug_context_menu(self, position):
        """Show context menu for the debug output."""
        menu = QMenu()
        
        copy_action = menu.addAction("Copy")
        copy_action.triggered.connect(self.copy_debug_selection)
        
        select_all_action = menu.addAction("Select All")
        select_all_action.triggered.connect(self.debug_output.selectAll)
        
        menu.addSeparator()
        
        clear_action = menu.addAction("Clear Debug Output")
        clear_action.triggered.connect(self.clear_debug_output)
        
        save_action = menu.addAction("Save Debug Output...")
        save_action.triggered.connect(self.save_debug_output)
        
        menu.addSeparator()
        
        search_action = menu.addAction("Search...")
        search_action.triggered.connect(self.focus_search)
        
        menu.exec(self.debug_output.mapToGlobal(position))
    
    def show_variable_context_menu(self, position):
        """Show context menu for the variable inspector."""
        menu = QMenu()
        
        copy_action = menu.addAction("Copy")
        copy_action.triggered.connect(self.copy_variable_selection)
        
        select_all_action = menu.addAction("Select All")
        select_all_action.triggered.connect(self.variable_inspector.selectAll)
        
        menu.addSeparator()
        
        clear_action = menu.addAction("Clear Variables")
        clear_action.triggered.connect(self.clear_variable_tracking)
        
        menu.exec(self.variable_inspector.mapToGlobal(position))
    
    def copy_debug_selection(self):
        """Copy selected text from debug output to clipboard."""
        self.debug_output.copy()
    
    def copy_variable_selection(self):
        """Copy selected text from variable inspector to clipboard."""
        self.variable_inspector.copy()
        
    def clear_debug_output(self):
        """Clear the debug output panel."""
        self.debug_output.clear()
        self.debug_output.append("<span style='color:#55AAFF;'>Debug output cleared</span>")
        
    def save_debug_output(self):
        """Save the debug output to a file."""
        if not self.current_problem_number:
            problem_str = "unknown"
        else:
            problem_str = str(self.current_problem_number)
            
        default_filename = f"debug_output_problem_{problem_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Debug Output",
            default_filename,
            "HTML Files (*.html);;Text Files (*.txt);;All Files (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    if filename.lower().endswith('.html'):
                        # Save as HTML with styles
                        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Debug Output</title>
    <style>
        body { 
            background-color: #1E1E1E; 
            color: #CCCCCC; 
            font-family: Consolas, monospace; 
            padding: 20px;
        }
        .timestamp { color: #777777; }
        .debug { color: #FFFFFF; }
        .important { color: #FFAA55; }
        .info { color: #55FFAA; }
        .error { color: #FF5555; }
        .detail { color: #AAAAAA; }
        .trace { color: #00AAFF; }
    </style>
</head>
<body>
    <h1>Debug Output for Problem {}</h1>
    <p>Generated on: {}</p>
    <div id="debug-content">
        {}
    </div>
</body>
</html>""".format(
                            problem_str,
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            self.debug_output.toHtml()
                        )
                        f.write(html_content)
                    else:
                        # Save as plain text
                        f.write(self.debug_output.toPlainText())
                
                self.add_debug_message(f"Debug output saved to {filename}", "info")
            except Exception as e:
                self.add_debug_message(f"Error saving debug output: {str(e)}", "error")
        
    def search_debug_output(self, search_text):
        """Search in the debug output and highlight matches."""
        # Reset previous formatting
        cursor = self.debug_output.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())
        
        if not search_text:
            return
            
        # Create format for matches
        match_format = QTextCharFormat()
        match_format.setBackground(QColor("#553300"))  # Dark orange background
        
        # Find all matches
        cursor = self.debug_output.textCursor()
        cursor.setPosition(0)
        
        regex = re.compile(re.escape(search_text), re.IGNORECASE)
        plain_text = self.debug_output.toPlainText()
        
        for match in regex.finditer(plain_text):
            start_pos = match.start()
            end_pos = match.end()
            
            cursor.setPosition(start_pos)
            cursor.setPosition(end_pos, QTextCursor.MoveMode.KeepAnchor)
            cursor.setCharFormat(match_format)
        
    def add_debug_message(self, message, level="debug"):
        """Add a message to the debug output panel."""
        # Prevent debug function from being called if debugging is disabled
        if not self.debug_enabled_checkbox.isChecked():
            return
            
        # Check if the specific level is enabled
        if level not in self.debug_level_checkboxes or not self.debug_level_checkboxes[level].isChecked():
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Set color based on debug level
        if level == "important":
            color = "#FFAA55"  # Orange
        elif level == "info":
            color = "#55FFAA"  # Light green
        elif level == "error":
            color = "#FF5555"  # Red
        elif level == "detail":
            color = "#AAAAAA"  # Gray
        elif level == "trace":
            color = "#00AAFF"  # Blue
        else:
            color = "#FFFFFF"  # White
            
        # Format the debug message with HTML
        if self.show_timestamp_checkbox.isChecked():
            formatted_message = f"<span style='color:#777777;'>[{timestamp}]</span> <span style='color:{color};'>{message}</span>"
        else:
            formatted_message = f"<span style='color:{color};'>{message}</span>"
        
        # Add the message to the debug output
        self.debug_output.append(formatted_message)
        
        # Auto-scroll to the bottom
        scrollbar = self.debug_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # Check for variable tracking patterns with recursion protection
        try:
            self._check_for_variables(message, level)
        except Exception as e:
            # If we get an exception while checking variables, show it but don't try to check 
            # this error message for variables (would cause infinite recursion)
            self.debug_output.append(f"<span style='color:#FF5555;'>Error in variable tracking: {str(e)}</span>")
            scrollbar.setValue(scrollbar.maximum())
        
    def _check_for_variables(self, message, level):
        """Check if the message contains variable tracking patterns and extract values."""
        # Prevent recursion by checking if this is debug output about variables
        if message.startswith("variable =") or message.startswith("var:") or "[Tracking]" in message:
            return
            
        # Look for patterns like 'variable = value' or 'variable: value'
        # More precise patterns to avoid matching patterns in error messages or other output
        variable_patterns = [
            r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^=]+)$',  # var = value (strict, must start line)
            r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*([^:]+)$',  # var: value (strict, must start line)
            r'\[var\]\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^=]+)$',  # [var] name = value
        ]
        
        # Only track variables from debug, important, and info levels
        if level not in ['debug', 'important', 'info']:
            return
            
        for pattern in variable_patterns:
            matches = re.search(pattern, message)
            if matches:
                var_name = matches.group(1).strip()
                var_value = matches.group(2).strip()
                
                # Skip tracking if variable name is too generic or contains suspicious patterns
                if var_name in ['error', 'exception', 'traceback', 'line'] or len(var_name) < 2:
                    continue
                    
                # Update the variable in our dictionary
                self.variable_values[var_name] = {
                    'value': var_value,
                    'timestamp': datetime.now(),
                    'level': level
                }
                
                # Update the variable inspector
                self._update_variable_inspector()
                break
                
    def _update_variable_inspector(self):
        """Update the variable inspector with current variable values."""
        if not self.variable_values:
            self.variable_inspector.setHtml("<span style='color:#55AAFF;'>Variable Inspector</span><br>No variables tracked yet")
            return
            
        html = "<span style='color:#55AAFF;'>Variable Inspector</span><br><table width='100%'>"
        html += "<tr><th align='left'>Name</th><th align='left'>Value</th><th align='left'>Last Updated</th></tr>"
        
        # Sort variables by name
        sorted_vars = sorted(self.variable_values.items())
        
        for var_name, var_info in sorted_vars:
            # Set color based on level
            if var_info['level'] == 'important':
                color = "#FFAA55"  # Orange
            elif var_info['level'] == 'info':
                color = "#55FFAA"  # Light green
            else:
                color = "#FFFFFF"  # White
                
            # Format timestamp
            timestamp = var_info['timestamp'].strftime("%H:%M:%S")
            
            html += f"<tr><td><span style='color:{color};'>{var_name}</span></td>"
            html += f"<td><span style='color:{color};'>{var_info['value']}</span></td>"
            html += f"<td><span style='color:#777777;'>{timestamp}</span></td></tr>"
            
        html += "</table>"
        self.variable_inspector.setHtml(html)
        
    def save_debug_settings(self):
        """Save the current debug settings."""
        if not self.settings_manager:
            return
            
        # Create debug settings structure if it doesn't exist
        if 'debug' not in self.settings_manager.settings:
            self.settings_manager.settings['debug'] = {}
            
        # Save master debug toggle state
        self.settings_manager.settings['debug']['enabled'] = self.debug_enabled_checkbox.isChecked()
        
        # Save individual level states
        self.settings_manager.settings['debug']['levels'] = {}
        for level, checkbox in self.debug_level_checkboxes.items():
            self.settings_manager.settings['debug']['levels'][level] = checkbox.isChecked()
            
        # Save timestamp visibility - explicitly get the checkbox state
        timestamp_visible = self.show_timestamp_checkbox.isChecked()
        self.settings_manager.settings['debug']['show_timestamps'] = bool(timestamp_visible)
            
        # Save the settings
        self.settings_manager.save_settings()
        
    def load_debug_settings(self):
        """Load debug settings from the settings manager."""
        if not self.settings_manager:
            return
            
        settings = self.settings_manager.settings
        
        # Apply debug settings if they exist
        if 'debug' in settings:
            debug_settings = settings['debug']
            
            # Set master debug toggle
            if 'enabled' in debug_settings:
                self.debug_enabled_checkbox.setChecked(debug_settings['enabled'])
                
            # Set individual level checkboxes
            if 'levels' in debug_settings:
                for level, enabled in debug_settings['levels'].items():
                    if level in self.debug_level_checkboxes:
                        self.debug_level_checkboxes[level].setChecked(enabled)
                        
            # Set timestamp visibility - explicitly force the checkbox state
            if 'show_timestamps' in debug_settings:
                # Temporarily disconnect signals to prevent triggering save while loading
                self.show_timestamp_checkbox.blockSignals(True)
                # Explicitly cast to bool in case it's stored as another type
                timestamp_value = bool(debug_settings['show_timestamps'])
                # Set checkbox state - use setChecked which is more reliable than setting checked property
                self.show_timestamp_checkbox.setChecked(timestamp_value)
                # Re-enable signals
                self.show_timestamp_checkbox.blockSignals(False)
                        
    def is_debug_enabled(self):
        """Return whether debug output is enabled."""
        return self.debug_enabled_checkbox.isChecked()
        
    def get_debug_function(self):
        """
        Returns a callable function that can be passed to code execution
        to handle debug output.
        """
        return lambda message, level="debug": self.add_debug_message(message, level)
        
    def set_current_problem(self, problem_number):
        """Set the current problem number for context."""
        self.current_problem_number = problem_number
        
        # Add a separator in the debug output when changing problems
        if problem_number:
            self.add_debug_message(f"--- Problem {problem_number} Selected ---", "info")
            
    def add_timing_marker(self, marker_name="Timing Marker"):
        """Add a timing marker in the debug output."""
        # Direct output to avoid potential recursion through add_debug_message
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        formatted_message = f"<span style='color:#00AAFF;'>⏱️ {marker_name}: {timestamp}</span>"
        
        # Add directly to debug output instead of calling add_debug_message
        self.debug_output.append(formatted_message)
        
        # Auto-scroll to the bottom
        scrollbar = self.debug_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def clear_variable_tracking(self):
        """Clear all tracked variables."""
        self.variable_values.clear()
        self._update_variable_inspector()
        self.add_debug_message("Variable tracking cleared", "info")
        
    def set_timestamp_visibility(self, visible):
        """
        Directly set the timestamp visibility checkbox state.
        This is mainly for testing purposes.
        
        Args:
            visible: Boolean indicating whether to show timestamps
        """
        # Block signals to prevent triggering settings save
        self.show_timestamp_checkbox.blockSignals(True)
        # Set the state explicitly
        self.show_timestamp_checkbox.setChecked(visible)
        # Re-enable signals
        self.show_timestamp_checkbox.blockSignals(False)
        # Force save if we have a settings manager
        if self.settings_manager:
            self.save_debug_settings() 