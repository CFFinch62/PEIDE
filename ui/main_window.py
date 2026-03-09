import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTextEdit, QPushButton, QLabel, QSplitter,
                            QMessageBox, QStatusBar, QTabWidget, QListWidget,
                            QInputDialog, QLineEdit)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor, QAction, QDesktopServices
from problem_manager import ProblemManager
from progress_grid import ProblemGrid
from settings_manager import SettingsManager
from settings_dialog import SettingsDialog
from ui.code_editor import CodeEditor
from ui.theme import apply_dark_theme

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Euler Problem Solving Editor for Python 3")
        self.setMinimumSize(800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create splitter for problem description and code editor
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)
        
        # Problem description area
        description_scroll = QScrollArea()
        description_scroll.setWidgetResizable(True)
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("""
            QLabel {
                color: #d4d4d4;
                padding: 10px;
            }
        """)
        description_scroll.setWidget(self.description_label)
        splitter.addWidget(description_scroll)
        
        # Solution area with tabs
        solution_widget = QWidget()
        solution_layout = QVBoxLayout(solution_widget)
        
        # Create tab widget for solution side
        self.solution_tabs = QTabWidget()
        
        # Code tab
        code_tab = QWidget()
        code_layout = QVBoxLayout(code_tab)
        self.code_editor = CodeEditor()
        code_layout.addWidget(self.code_editor)
        
        # Data Files tab
        data_files_tab = QWidget()
        data_files_layout = QVBoxLayout(data_files_tab)
        self.data_files_text = QTextEdit()
        self.data_files_text.setReadOnly(True)
        data_files_layout.addWidget(self.data_files_text)
        
        # Add tabs in correct order
        self.solution_tabs.addTab(code_tab, "Code")
        self.solution_tabs.addTab(data_files_tab, "Data Files")
        
        solution_layout.addWidget(self.solution_tabs)
        splitter.addWidget(solution_widget)
        
        # Set initial sizes
        splitter.setSizes([200, 400])
        
        # Apply dark theme
        apply_dark_theme(self)
        
        # Store current problem number
        self.current_problem = None

    def load_problem_by_number(self, problem_number):
        """Load a problem by its number."""
        try:
            # Load problem description
            description = self.problem_manager.get_problem_description(problem_number)
            
            # Check if info file exists and add indicator to description
            info_path = os.path.join("info", f"{problem_number:03d}_overview.pdf")
            if os.path.exists(info_path):
                description += "\n\n📄 Additional information is available for this problem."
            
            self.description_label.setText(description)
            
            # Load solution if it exists
            solution = self.problem_manager.get_solution(problem_number)
            if solution:
                self.code_editor.setPlainText(solution)
            else:
                self.code_editor.setPlainText("")
            
            # Load data files info
            data_files = self.problem_manager.get_data_files(problem_number)
            if data_files:
                self.data_files_text.setPlainText("\n".join(data_files))
            else:
                self.data_files_text.setPlainText("No data files required for this problem.")
            
            # Update status
            self.update_problem_status(problem_number)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load problem {problem_number}: {str(e)}")