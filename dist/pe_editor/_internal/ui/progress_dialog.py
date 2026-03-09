from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QLabel, QPushButton, QListWidget, QSplitter, QProgressBar, QTextEdit, QWidget, QSizePolicy)
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta

class ProgressDialog(QDialog):
    """
    A dialog that shows progress information for Project Euler problems,
    including statistics, achievements, and streaks.
    """
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.problem_manager = main_window.problem_manager
        
        self.setWindowTitle("Progress")
        self.setMinimumWidth(800)  # Reduced from 1000
        self.setMinimumHeight(600)
        
        # Create main layout with splitter
        main_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel (Statistics and Achievements)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Statistics group
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()
        
        # Add progress bars and labels
        self.solved_bar = QProgressBar()
        self.solved_bar.setMinimum(0)
        self.solved_bar.setMaximum(100)
        stats_layout.addWidget(QLabel("Problems Solved:"))
        stats_layout.addWidget(self.solved_bar)
        
        self.attempted_bar = QProgressBar()
        self.attempted_bar.setMinimum(0)
        self.attempted_bar.setMaximum(100)
        stats_layout.addWidget(QLabel("Problems Attempted:"))
        stats_layout.addWidget(self.attempted_bar)
        
        # Add streak information
        self.streak_label = QLabel()
        stats_layout.addWidget(self.streak_label)
        
        stats_group.setLayout(stats_layout)
        left_layout.addWidget(stats_group)
        
        # Achievements group (now under statistics)
        achievements_group = QGroupBox("Achievements")
        achievements_layout = QVBoxLayout()
        achievements_layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
        achievements_layout.setSpacing(2)  # Reduce spacing
        
        self.achievements_text = QTextEdit()
        self.achievements_text.setReadOnly(True)
        self.achievements_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Allow vertical expansion
        achievements_layout.addWidget(self.achievements_text)
        
        achievements_group.setLayout(achievements_layout)
        left_layout.addWidget(achievements_group)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        left_layout.addWidget(close_button)
        
        # Right panel (Performance)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Performance group
        performance_group = QGroupBox("Performance")
        performance_layout = QVBoxLayout()
        
        # Average execution time
        self.avg_time_label = QLabel()
        performance_layout.addWidget(self.avg_time_label)
        
        # All solved problems with execution times
        self.solved_problems_label = QLabel("Solved Problems with Execution Times:")
        performance_layout.addWidget(self.solved_problems_label)
        
        self.solved_problems_list = QListWidget()
        performance_layout.addWidget(self.solved_problems_list)
        
        # Slow solutions list
        self.slow_solutions_label = QLabel("Slow Solutions (over 60 seconds):")
        performance_layout.addWidget(self.slow_solutions_label)
        
        self.slow_solutions_list = QListWidget()
        performance_layout.addWidget(self.slow_solutions_list)
        
        performance_group.setLayout(performance_layout)
        right_layout.addWidget(performance_group)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes (60% left, 40% right)
        splitter.setSizes([480, 320])  # Adjusted ratio to give less space to performance area
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        
        # Populate data
        self.populate_data()
        
    def populate_data(self):
        """Populate the dialog with progress data."""
        progress = self.problem_manager.get_progress()
        
        # Update progress bars
        total_problems = 100  # Total number of Project Euler problems
        solved_percentage = (len(progress["solved_problems"]) / total_problems) * 100
        attempted_percentage = (len(progress["attempted_problems"]) / total_problems) * 100
        
        self.solved_bar.setValue(int(solved_percentage))
        self.solved_bar.setFormat(f"{len(progress['solved_problems'])}/{total_problems} ({solved_percentage:.1f}%)")
        
        self.attempted_bar.setValue(int(attempted_percentage))
        self.attempted_bar.setFormat(f"{len(progress['attempted_problems'])}/{total_problems} ({attempted_percentage:.1f}%)")
        
        # Update streak information
        current_streak = self.main_window.settings_manager.settings.get('current_streak', 0)
        longest_streak = self.main_window.settings_manager.settings.get('longest_streak', 0)
        last_solved_date = self.main_window.settings_manager.settings.get('last_solved_date', None)
        
        streak_text = f"Current Streak: {current_streak} days\n"
        streak_text += f"Longest Streak: {longest_streak} days\n"
        if last_solved_date:
            streak_text += f"Last Solved: {last_solved_date}"
        
        self.streak_label.setText(streak_text)
        
        # Update performance information
        execution_times = progress.get("execution_times", {})
        if execution_times:
            avg_time = sum(execution_times.values()) / len(execution_times)
            self.avg_time_label.setText(f"Average Execution Time: {avg_time:.3f} seconds")
            
            # Update solved problems list with execution times
            self.solved_problems_list.clear()
            solved_with_times = []
            for problem in progress["solved_problems"]:
                time = execution_times.get(str(problem), "N/A")
                if isinstance(time, (int, float)):
                    solved_with_times.append((problem, time))
                else:
                    solved_with_times.append((problem, float('inf')))  # Put problems without times at the end
            
            # Sort by problem number
            solved_with_times.sort(key=lambda x: x[0])
            
            for problem, time in solved_with_times:
                if isinstance(time, (int, float)):
                    self.solved_problems_list.addItem(f"Problem {problem}: {time:.3f} seconds")
                else:
                    self.solved_problems_list.addItem(f"Problem {problem}: N/A")
            
            # Update slow solutions list
            self.slow_solutions_list.clear()
            slow_solutions = [(p, t) for p, t in execution_times.items() if t > 60]
            if slow_solutions:
                for problem, time in sorted(slow_solutions, key=lambda x: x[1], reverse=True):
                    self.slow_solutions_list.addItem(f"Problem {problem}: {time:.1f} seconds")
                self.slow_solutions_label.setVisible(True)
                self.slow_solutions_list.setVisible(True)
            else:
                self.slow_solutions_label.setVisible(False)
                self.slow_solutions_list.setVisible(False)
        else:
            self.avg_time_label.setText("No execution time data available")
            self.solved_problems_list.clear()
            self.slow_solutions_label.setVisible(False)
            self.slow_solutions_list.setVisible(False)
        
        # Generate and display achievements
        achievements = self.generate_achievements(progress)
        self.achievements_text.setPlainText(achievements)
        
    def generate_achievements(self, progress):
        """Generate achievement text based on progress."""
        achievements = []
        
        # Count solved problems
        solved_count = len(progress["solved_problems"])
        
        # Add achievements based on number of problems solved
        if solved_count >= 1:
            achievements.append("🎯 First Problem Solved")
        if solved_count >= 10:
            achievements.append("🌟 Decade Master")
        if solved_count >= 25:
            achievements.append("🏆 Quarter Century")
        if solved_count >= 50:
            achievements.append("👑 Half Century")
        if solved_count >= 75:
            achievements.append("💫 Three Quarters")
        if solved_count >= 100:
            achievements.append("🏅 Century Club")
            
        # Add streak achievements
        current_streak = self.main_window.settings_manager.settings.get('current_streak', 0)
        if current_streak >= 3:
            achievements.append("🔥 3-Day Streak")
        if current_streak >= 7:
            achievements.append("🔥 7-Day Streak")
        if current_streak >= 30:
            achievements.append("🔥 30-Day Streak")
            
        # Add difficulty achievements
        solved_difficulties = set()
        for problem in progress["solved_problems"]:
            difficulty = self.problem_manager.get_problem_difficulty(problem)
            solved_difficulties.add(difficulty)
            
        if 1 in solved_difficulties:
            achievements.append("⭐ First Star")
        if 2 in solved_difficulties:
            achievements.append("⭐⭐ Two Stars")
        if 3 in solved_difficulties:
            achievements.append("⭐⭐⭐ Three Stars")
        if 4 in solved_difficulties:
            achievements.append("⭐⭐⭐⭐ Four Stars")
        if 5 in solved_difficulties:
            achievements.append("⭐⭐⭐⭐⭐ Five Stars")
            
        # Add performance achievements
        execution_times = progress.get("execution_times", {})
        if execution_times:
            avg_time = sum(execution_times.values()) / len(execution_times)
            if avg_time < 1:
                achievements.append("⚡ Speed Demon: Average solution time under 1 second")
            if avg_time < 0.1:
                achievements.append("🚀 Lightning Fast: Average solution time under 0.1 seconds")
            
            # Check for individual fast solutions
            fast_solutions = [p for p, t in execution_times.items() if t < 0.01]
            if len(fast_solutions) >= 10:
                achievements.append("⚡ Quick Draw: 10 solutions under 0.01 seconds")
            
        # Format achievements
        if achievements:
            return "Achievements:\n" + "\n".join(f"✓ {achievement}" for achievement in achievements)
        else:
            return "No achievements yet. Keep solving problems!"
    
    def exec(self):
        """Show the dialog with updated data."""
        self.populate_data()
        return super().exec() 