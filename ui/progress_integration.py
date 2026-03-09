from PyQt6.QtWidgets import QToolBar, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QObject

class ProgressIntegration(QObject):
    """Class to handle progress grid integration and related functionality."""
    
    # Signal emitted when a problem is selected
    problem_selected = pyqtSignal(int)
    
    def __init__(self, main_window, problem_manager, progress_grid, status_bar):
        super().__init__()  # Initialize QObject
        self.main_window = main_window
        self.problem_manager = problem_manager
        self.progress_grid = progress_grid
        self.status_bar = status_bar
        
        # Connect progress grid signals
        self.progress_grid.square_clicked_signal.connect(self._handle_problem_selection)
        
        # Create difficulty filter toolbar
        self._create_difficulty_toolbar()
        
    def _create_difficulty_toolbar(self):
        """Create the difficulty filter toolbar."""
        self.difficulty_toolbar = QToolBar("Difficulty Filter")
        self.main_window.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.difficulty_toolbar)
        
        # Add label to the toolbar
        difficulty_label = QLabel("Filter by difficulty: ")
        self.difficulty_toolbar.addWidget(difficulty_label)
        
        # Add star buttons for each difficulty level (1-5)
        for i in range(1, 6):
            star_button = QPushButton('★' * i)
            star_button.setFixedWidth(60)
            star_button.setToolTip(f"Show only problems with difficulty level {i}")
            # Use a lambda with default argument to avoid lambda capture issues
            star_button.clicked.connect(lambda checked, d=i: self.filter_by_difficulty(d))
            self.difficulty_toolbar.addWidget(star_button)
        
        # Add reset button
        reset_button = QPushButton("Reset Filter")
        reset_button.setToolTip("Clear difficulty filter")
        reset_button.clicked.connect(self.reset_difficulty_filter)
        self.difficulty_toolbar.addWidget(reset_button)
        
    def _handle_problem_selection(self, problem_number):
        """Handle when a problem is selected in the grid."""
        self.problem_selected.emit(problem_number)
        
    def filter_by_difficulty(self, star_number):
        """Filter grid squares by difficulty when a star is clicked."""
        self.progress_grid.filter_by_difficulty(star_number)
        
    def reset_difficulty_filter(self):
        """Reset any applied difficulty filters."""
        self.progress_grid.reset_difficulty_filter()
        
    def update_progress(self):
        """Update the progress grid with solved and attempted problems."""
        progress = self.problem_manager.get_progress()
        self.progress_grid.update_progress(
            progress["solved_problems"],
            progress["attempted_problems"]
        )
        
        # Update the current square's color if it exists
        if self.progress_grid.current_square:
            current_number = self.progress_grid.current_square
            self.progress_grid.update_progress(
                progress["solved_problems"],
                progress["attempted_problems"]
            )
            
    def update_status_bar(self, problem_number):
        """Update the status bar with problem information."""
        progress = self.problem_manager.get_progress()
        status = f"Problem {problem_number}"
        if self.problem_manager.is_problem_solved(problem_number):
            status += " ✓"
        # Use main window's styled status message instead of direct access
        if hasattr(self.main_window, 'show_status_message'):
            self.main_window.show_status_message(status)
        else:
            self.status_bar.showMessage(status)
        
    def update_grid_tooltips(self):
        """Update tooltips for all grid squares with difficulty information."""
        for i in range(1, 101):
            difficulty = self.problem_manager.get_problem_difficulty(i)
            percentage = self.problem_manager.get_problem_difficulty_percentage(i)
            self.progress_grid.update_tooltip(i, difficulty, percentage)
            
    def get_current_problem_number(self):
        """Get the currently selected problem number."""
        current_square = self.progress_grid.get_current_square()
        if current_square:
            return int(current_square.number_label.text())
        return None 