from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QPushButton, QDialog
from PyQt6.QtCore import pyqtSignal, Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QIcon
import os

class ProblemDisplayPanel(QWidget):
    """Panel for displaying problem description and related information."""
    
    # Signal emitted when data file is clicked
    data_file_clicked = pyqtSignal()
    
    def __init__(self, problem_manager):
        super().__init__()
        self.problem_manager = problem_manager
        self.current_download_url = None
        self.current_hints = None
        self.current_problem_number = None
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the UI components."""
        layout = QVBoxLayout(self)
        
        # Problem description
        self.problem_description = QTextEdit()
        self.problem_description.setReadOnly(True)
        self.problem_description.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #FFFFFF;
                border: none;
                padding: 10px;
                font-family: Arial;
                font-size: 12pt;
            }
        """)
        layout.addWidget(self.problem_description)
        
        # Data file indicator
        self.data_file_indicator = QLabel()
        self.data_file_indicator.setStyleSheet("""
            QLabel {
                background-color: #2D2D2D;
                color: #569CD6;
                padding: 5px;
                border: 1px solid #3D3D3D;
                border-radius: 3px;
            }
        """)
        self.data_file_indicator.setVisible(False)
        self.data_file_indicator.mousePressEvent = self._handle_data_file_click
        layout.addWidget(self.data_file_indicator)
        
    def _handle_data_file_click(self, event):
        """Handle click on data file indicator to download missing file."""
        if self.current_download_url:
            QDesktopServices.openUrl(QUrl(self.current_download_url))
        # Call the parent class's event handler
        QLabel.mousePressEvent(self.data_file_indicator, event)
    
    def show_fullscreen(self):
        """Public method to show problem description in a fullscreen dialog."""
        if not self.problem_description.toPlainText():
            return  # Don't open dialog if no text
            
        dialog = FullscreenProblemDialog(self)
        dialog.setWindowTitle(f"Problem {self.current_problem_number}" if self.current_problem_number else "Problem Description")
        dialog.set_content(self.problem_description.toPlainText())
        
        # Get the main window (parent of parent)
        main_window = self.window()
        if main_window:
            # Set the dialog size and position to match the main window
            dialog.setGeometry(main_window.geometry())
            
        dialog.exec()
        
    def load_problem(self, problem_number):
        """Load and display a problem by its number."""
        try:
            # Save the current problem number
            self.current_problem_number = problem_number
            
            # Load problem description
            problem_data = self.problem_manager.load_problem(problem_number)
            self.problem_text = problem_data["text"]
            
            # Get difficulty information
            difficulty = self.problem_manager.get_problem_difficulty(problem_number)
            difficulty_percentage = self.problem_manager.get_problem_difficulty_percentage(problem_number)
            
            # Add difficulty information to the display
            difficulty_text = f"\n\nDifficulty: {'★' * difficulty}{'☆' * (5 - difficulty)} ({difficulty_percentage}%)"
            display_text = self.problem_text + difficulty_text
            
            # Extract hints from the problem text
            hint_start = self.problem_text.find("Hint:")
            if hint_start != -1:
                self.current_hints = self.problem_text[hint_start:].strip()
                display_text = display_text[:hint_start].strip() + difficulty_text
            else:
                self.current_hints = "No hints available for this problem."
            
            # Check for info file and add simple indicator
            info_path = f"info/{problem_number:03d}_overview.pdf"
            if os.path.exists(info_path):
                display_text += "\n\n📄 Additional information is available for this problem in the info directory."
            
            # Display the problem text
            self.problem_description.setPlainText(display_text)
            
            # Check for data file requirements
            data_info = self.problem_manager.get_problem_data_info(problem_number)
            
            # Update data file indicator
            if data_info['has_data']:
                # Check if the data file exists
                try:
                    status = self.problem_manager.check_data_file(data_info['file'])
                    if not status['exists']:
                        self.data_file_indicator.setText(
                            f"⚠️ This problem requires a data file that is missing:\n"
                            f"File: {data_info['file']}\n"
                            f"Click here to download it"
                        )
                        self.data_file_indicator.setStyleSheet("""
                            QLabel {
                                background-color: #2D2D2D;
                                color: #FF6B6B;
                                padding: 5px;
                                border: 1px solid #3D3D3D;
                                border-radius: 3px;
                            }
                        """)
                        self.current_download_url = status['download_url']
                        self.data_file_indicator.setCursor(Qt.CursorShape.PointingHandCursor)
                    else:
                        self.data_file_indicator.setText(
                            f"This problem uses external data: {data_info['description']}\n"
                            f"File: {data_info['file']}\n"
                            f"Use: {data_info['method']}()"
                        )
                        self.data_file_indicator.setStyleSheet("""
                            QLabel {
                                background-color: #2D2D2D;
                                color: #569CD6;
                                padding: 5px;
                                border: 1px solid #3D3D3D;
                                border-radius: 3px;
                            }
                        """)
                        self.current_download_url = None
                        self.data_file_indicator.setCursor(Qt.CursorShape.ArrowCursor)
                except Exception as e:
                    self.data_file_indicator.setText(f"Error checking data file: {str(e)}")
                    self.data_file_indicator.setStyleSheet("""
                        QLabel {
                            background-color: #2D2D2D;
                            color: #FF6B6B;
                            padding: 5px;
                            border: 1px solid #3D3D3D;
                            border-radius: 3px;
                        }
                    """)
                    self.current_download_url = None
                    self.data_file_indicator.setCursor(Qt.CursorShape.ArrowCursor)
                
                self.data_file_indicator.setVisible(True)
            else:
                self.data_file_indicator.setVisible(False)
                
            return data_info
            
        except Exception as e:
            self.problem_description.setPlainText(f"Error loading problem {problem_number}: {str(e)}")
            self.data_file_indicator.setVisible(False)
            return None
            
    def get_current_hints(self):
        """Get the current problem's hints."""
        return self.current_hints
        
    def clear(self):
        """Clear the panel content."""
        self.problem_description.clear()
        self.data_file_indicator.setVisible(False)
        self.current_download_url = None
        self.current_hints = None
        self.current_problem_number = None


class FullscreenProblemDialog(QDialog):
    """Dialog for displaying problem descriptions in fullscreen mode."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Problem Description")
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Create text edit for problem description
        self.description = QTextEdit()
        self.description.setReadOnly(True)
        self.description.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #FFFFFF;
                border: none;
                padding: 15px;
                font-family: Arial;
                font-size: 14pt;
            }
        """)
        layout.addWidget(self.description)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Add stretch to push button to the right
        button_layout.addStretch()
        
        # Create close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def set_content(self, text):
        """Set the content of the dialog."""
        self.description.setPlainText(text) 