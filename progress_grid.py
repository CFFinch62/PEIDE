from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, 
                          QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette
import re
import math

class ProblemGrid(QWidget):
    problem_selected = pyqtSignal(int)  # Signal emitted when a problem is selected
    square_clicked_signal = pyqtSignal(int)  # Renamed signal
    
    def __init__(self, problem_manager, parent=None):
        super().__init__(parent)
        self.problem_manager = problem_manager  # Store the problem manager
        self.mode = "basic"  # Default to basic mode (1-100)
        self.max_problem = 100  # Default max problem is 100 for basic mode
        self.max_total_problems = 945  # Total number of problems available
        self.current_group = 1  # Current group (1 = problems 1-100, 2 = problems 101-200, etc.)
        self.setup_ui()
        
        # Set tooltip style for the entire widget
        self.setStyleSheet("""
            QToolTip {
                background-color: #2D2D2D;
                color: #D4D4D4;
                border: 1px solid #3D3D3D;
                padding: 5px;
            }
        """)
        
    def setup_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add navigation controls
        nav_layout = QHBoxLayout()
        
        # Group label
        self.group_label = QLabel("Problems 1-100")
        self.group_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.group_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        # Navigation buttons
        self.prev_button = QPushButton("◀ Previous")
        self.prev_button.clicked.connect(self.show_previous_group)
        self.prev_button.setEnabled(False)  # Initially disabled
        
        self.next_button = QPushButton("Next ▶")
        self.next_button.clicked.connect(self.show_next_group)
        self.next_button.setEnabled(False)  # Initially disabled in basic mode
        
        # Add to navigation layout
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.group_label)
        nav_layout.addWidget(self.next_button)
        
        # Add navigation to main layout
        main_layout.addLayout(nav_layout)
        
        # Create grid layout for problem squares
        grid_widget = QWidget()
        self.layout = QGridLayout(grid_widget)
        self.layout.setSpacing(0)  # Remove spacing between grid items
        
        # Add grid to main layout
        main_layout.addWidget(grid_widget)
        
        # Initialize variables
        self.problem_squares = {}
        self.current_square = None  # Track the current square
        self.solved_problems = set()  # Track solved problems
        self.attempted_problems = set()
        self.verified_problems = set()  # Track verified problems
        self.original_colors = {}  # Store original colors for filtering
        
        # Create grid of problem squares
        self.create_grid()
        
    def create_grid(self):
        """Create the 10x10 problem grid for the current group."""
        # Clear existing grid
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.problem_squares = {}
        
        # Calculate start and end problem numbers for the current group
        start_problem = (self.current_group - 1) * 100 + 1
        end_problem = min(self.current_group * 100, self.max_total_problems)
        
        # Update group label
        self.group_label.setText(f"Problems {start_problem}-{end_problem}")
        
        # Update navigation buttons
        self.prev_button.setEnabled(self.current_group > 1)
        max_groups = math.ceil(self.max_problem / 100)
        self.next_button.setEnabled(self.mode == "max" and self.current_group < max_groups)
        
        # Create 10x10 grid of problem squares
        for i in range(10):
            for j in range(10):
                problem_number = (self.current_group - 1) * 100 + i * 10 + j + 1
                
                # Skip if problem number exceeds the maximum
                if problem_number > self.max_total_problems or problem_number > self.max_problem:
                    # Add empty spacer
                    spacer = QFrame()
                    spacer.setStyleSheet("background-color: transparent;")
                    self.layout.addWidget(spacer, i, j)
                    continue
                
                # Create the problem square
                self.create_square(problem_number, i, j)
    
    def create_square(self, problem_number, row, col):
        """Create a single problem square."""
        square = QFrame()
        square.setFrameShape(QFrame.Shape.Box)
        square.setLineWidth(1)
        square.setMinimumSize(40, 40)  # Set minimum size for better visibility
        square.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                border: 1px solid #3D3D3D;
            }
            QFrame:hover {
                background-color: #3D3D3D;
            }
        """)
        
        # Create layout for the square - horizontal instead of vertical
        square_layout = QHBoxLayout(square)
        square_layout.setContentsMargins(2, 2, 2, 2)  # Small margins
        square_layout.setSpacing(2)  # Small spacing between number and checkmark
        square_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the content
        
        # Add problem number label
        number_label = QLabel(str(problem_number))
        number_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        number_label.setStyleSheet("""
            QLabel {
                color: #A0A0A0;
                font-size: 14px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
            }
        """)
        square_layout.addWidget(number_label)
        
        # Add checkmark icon for verified problems (hidden by default)
        checkmark_label = QLabel("✓")
        checkmark_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        checkmark_label.setStyleSheet("""
            QLabel {
                color: #55FFAA;
                font-size: 14px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
                background: transparent;
            }
        """)
        checkmark_label.setVisible(False)  # Hide by default
        square_layout.addWidget(checkmark_label)
        
        # Store references
        self.problem_squares[problem_number] = square
        square.number_label = number_label
        square.checkmark_label = checkmark_label
        
        # Add to grid
        self.layout.addWidget(square, row, col)
        
        # Connect click event
        square.mousePressEvent = lambda event, pn=problem_number: self.square_clicked(pn)

    def set_mode(self, mode):
        """Set the grid mode (basic or max) and update the UI."""
        if mode not in ["basic", "max"]:
            return
            
        if self.mode == mode:
            return
            
        self.mode = mode
        
        # Set the max problem limit based on mode
        self.max_problem = 100 if mode == "basic" else self.max_total_problems
        
        # Reset to first group if switching to basic mode and was on a higher group
        if mode == "basic" and self.current_group > 1:
            self.current_group = 1
        
        # Recreate grid
        self.create_grid()
        
        # Apply any current colors/highlights
        self.update_progress(
            list(self.solved_problems), 
            list(self.attempted_problems),
            list(self.verified_problems)
        )
        
        # Update square for current problem if necessary
        if self.current_square:
            if self.current_square <= self.max_problem:
                # Check if current square is in the current group
                group = math.ceil(self.current_square / 100)
                if group == self.current_group:
                    self.square_clicked(self.current_square)
                else:
                    # Navigate to the correct group
                    self.navigate_to_problem(self.current_square)
            else:
                # Reset if current problem is outside range
                self.current_square = None
    
    def navigate_to_problem(self, problem_number):
        """Navigate to the group containing the specified problem."""
        if problem_number < 1 or problem_number > self.max_problem:
            return
            
        # Calculate which group contains this problem
        group = math.ceil(problem_number / 100)
        
        # If already on the correct group, just highlight the problem
        if group == self.current_group:
            # Use _square_clicked_internal to avoid emitting signal and causing recursion
            self._square_clicked_internal(problem_number)
            return
            
        # Otherwise, switch to the correct group
        self.current_group = group
        self.create_grid()
        
        # Update progress indicators
        self.update_progress(
            list(self.solved_problems), 
            list(self.attempted_problems),
            list(self.verified_problems)
        )
        
        # Highlight the problem without emitting signal
        self._square_clicked_internal(problem_number)

    def show_next_group(self):
        """Show the next group of problems."""
        max_groups = math.ceil(self.max_problem / 100)
        if self.current_group < max_groups:
            self.current_group += 1
            self.create_grid()
            
            # Update progress indicators
            self.update_progress(
                list(self.solved_problems), 
                list(self.attempted_problems),
                list(self.verified_problems)
            )
            
            # Check if current square is in this new group
            if self.current_square:
                group = math.ceil(self.current_square / 100)
                if group == self.current_group:
                    self._square_clicked_internal(self.current_square)

    def show_previous_group(self):
        """Show the previous group of problems."""
        if self.current_group > 1:
            self.current_group -= 1
            self.create_grid()
            
            # Update progress indicators
            self.update_progress(
                list(self.solved_problems), 
                list(self.attempted_problems),
                list(self.verified_problems)
            )
            
            # Check if current square is in this new group
            if self.current_square:
                group = math.ceil(self.current_square / 100)
                if group == self.current_group:
                    self._square_clicked_internal(self.current_square)

    def square_clicked(self, problem_number):
        """Handle square click event."""
        # Update internal state and visual appearance
        self._square_clicked_internal(problem_number)
        
        # Emit the signal (only here, not in _square_clicked_internal)
        self.square_clicked_signal.emit(problem_number)

    def _square_clicked_internal(self, problem_number):
        """Update the visual state without emitting signals (to avoid recursion)."""
        # Update the current square
        self.current_square = problem_number
        
        # Update the grid to show the current problem while preserving progress colors
        for square_number, square in self.problem_squares.items():
            # Base style for the square
            if square_number in self.verified_problems:
                base_color = "#388E3C"  # Darker green for verified
                hover_color = "#2E7D32"
                text_color = "#FFFFFF"
            elif square_number in self.solved_problems:
                base_color = "#4CAF50"  # Green for solved
                hover_color = "#45A049"
                text_color = "#FFFFFF"
            elif square_number in self.attempted_problems:
                base_color = "#FFC107"  # Yellow for attempted
                hover_color = "#FFB300"
                text_color = "#000000"
            else:
                base_color = "#2D2D2D"  # Gray for not attempted
                hover_color = "#3D3D3D"
                text_color = "#A0A0A0"
            
            # If this is the selected square, add highlight border
            if square_number == problem_number:
                square.setStyleSheet(f"""
                    QFrame {{
                        background-color: {base_color};
                        border: 2px solid #569CD6;
                    }}
                    QFrame:hover {{
                        background-color: {hover_color};
                    }}
                """)
                square.number_label.setStyleSheet(f"""
                    QLabel {{
                        color: {text_color};
                        font-size: 14px;
                        font-weight: bold;
                        padding: 0px;
                        margin: 0px;
                    }}
                """)
            else:
                square.setStyleSheet(f"""
                    QFrame {{
                        background-color: {base_color};
                        border: 1px solid #3D3D3D;
                    }}
                    QFrame:hover {{
                        background-color: {hover_color};
                    }}
                """)
                square.number_label.setStyleSheet(f"""
                    QLabel {{
                        color: {text_color};
                        font-size: 14px;
                        font-weight: bold;
                        padding: 0px;
                        margin: 0px;
                    }}
                """)
            
            # Store original color if not already stored
            if square_number not in self.original_colors:
                self.original_colors[square_number] = base_color
    
    def get_current_square(self):
        """Get the currently selected problem square."""
        if self.current_square is None:
            return None
        return self.problem_squares.get(self.current_square)

    def update_progress(self, solved_problems, attempted_problems, verified_problems=None):
        """Update the visual state of problem squares based on progress."""
        self.solved_problems = set(solved_problems)  # Store solved problems
        self.attempted_problems = set(attempted_problems)  # Store attempted problems
        
        # Handle verified problems (optional for backward compatibility)
        if verified_problems is not None:
            self.verified_problems = set(verified_problems)
        
        for problem_number, square in self.problem_squares.items():
            if problem_number in self.verified_problems:
                color = "#388E3C"  # Darker green for verified
                hover_color = "#2E7D32"
                text_color = "#FFFFFF"
                # Show the checkmark for verified problems
                square.checkmark_label.setVisible(True)
            elif problem_number in solved_problems:
                color = "#4CAF50"  # Green for solved
                hover_color = "#45A049"
                text_color = "#FFFFFF"
                # Hide the checkmark for non-verified problems
                square.checkmark_label.setVisible(False)
            elif problem_number in attempted_problems:
                color = "#FFC107"  # Yellow for attempted
                hover_color = "#FFB300"
                text_color = "#000000"
                square.checkmark_label.setVisible(False)
            else:
                color = "#2D2D2D"  # Gray for not attempted
                hover_color = "#3D3D3D"
                text_color = "#A0A0A0"
                square.checkmark_label.setVisible(False)
            
            # Store original color if not already stored
            if problem_number not in self.original_colors:
                self.original_colors[problem_number] = color
            
            # Update number label color
            square.number_label.setStyleSheet(f"""
                QLabel {{
                    color: {text_color};
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0px;
                    margin: 0px;
                }}
            """)
            
            # If this is the current square, add highlight border
            if problem_number == self.current_square:
                square.setStyleSheet(f"""
                    QFrame {{
                        background-color: {color};
                        border: 2px solid #569CD6;
                    }}
                    QFrame:hover {{
                        background-color: {hover_color};
                    }}
                """)
            else:
                square.setStyleSheet(f"""
                    QFrame {{
                        background-color: {color};
                        border: 1px solid #3D3D3D;
                    }}
                    QFrame:hover {{
                        background-color: {hover_color};
                    }}
                """)
    
    def update_tooltip(self, problem_number, difficulty, percentage):
        """Update the tooltip for a specific problem square."""
        square = self.problem_squares.get(problem_number)
        if square:
            difficulty_stars = '★' * difficulty + '☆' * (5 - difficulty)
            square.setToolTip(f"Problem {problem_number}\nDifficulty: {difficulty_stars} ({percentage}%)")
    
    def filter_by_difficulty(self, difficulty):
        """Filter grid squares by difficulty."""
        for problem_number, square in self.problem_squares.items():
            if square:
                # Get the difficulty from the problem manager
                current_difficulty = self.problem_manager.get_problem_difficulty(problem_number)
                
                if current_difficulty == difficulty:
                    # Highlight matching difficulty
                    square.setStyleSheet("""
                        QFrame {
                            background-color: #FFD700;
                            border: 1px solid #3D3D3D;
                        }
                        QFrame:hover {
                            background-color: #FFC000;
                        }
                    """)
                else:
                    # Restore original color based on problem status
                    if problem_number in self.solved_problems:
                        color = "#4CAF50"  # Green for solved
                        hover_color = "#45A049"
                    elif problem_number in self.attempted_problems:
                        color = "#FFC107"  # Yellow for attempted
                        hover_color = "#FFB300"
                    else:
                        color = "#2D2D2D"  # Gray for not attempted
                        hover_color = "#3D3D3D"
                    
                    square.setStyleSheet(f"""
                        QFrame {{
                            background-color: {color};
                            border: 1px solid #3D3D3D;
                        }}
                        QFrame:hover {{
                            background-color: {hover_color};
                        }}
                    """)
    
    def reset_difficulty_filter(self):
        """Reset any applied difficulty filters, restoring original colors."""
        for problem_number, square in self.problem_squares.items():
            if square:
                # Restore original color based on problem status
                if problem_number in self.solved_problems:
                    color = "#4CAF50"  # Green for solved
                    hover_color = "#45A049"
                elif problem_number in self.attempted_problems:
                    color = "#FFC107"  # Yellow for attempted
                    hover_color = "#FFB300"
                else:
                    color = "#2D2D2D"  # Gray for not attempted
                    hover_color = "#3D3D3D"
                
                # If this is the current square, add highlight border
                if problem_number == self.current_square:
                    square.setStyleSheet(f"""
                        QFrame {{
                            background-color: {color};
                            border: 2px solid #569CD6;
                        }}
                        QFrame:hover {{
                            background-color: {hover_color};
                        }}
                    """)
                else:
                    square.setStyleSheet(f"""
                        QFrame {{
                            background-color: {color};
                            border: 1px solid #3D3D3D;
                        }}
                        QFrame:hover {{
                            background-color: {hover_color};
                        }}
                    """) 