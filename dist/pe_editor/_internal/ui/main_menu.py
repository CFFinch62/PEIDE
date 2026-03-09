"""
Main Menu Builder module for Project Euler Editor.
Handles creation and management of the application's main menu.
"""
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QAction


class MainMenuBuilder:
    """
    Builds and manages the main menu for the Project Euler Editor.
    Handles menu creation, action setup, and signal connections.
    """

    def __init__(self, main_window):
        """
        Initialize the Main Menu Builder.

        Args:
            main_window: The main window instance
        """
        self.main_window = main_window
        self.menu_bar = QMenuBar()
        self.main_window.setMenuBar(self.menu_bar)

        # Create menus
        self._create_file_menu()
        self._create_edit_menu()
        self._create_mode_menu()
        self._create_theme_menu()
        self._create_view_menu()
        self._create_help_menu()

    def _create_file_menu(self):
        """Create the File menu with its actions."""
        file_menu = self.menu_bar.addMenu("File")

        # Settings action
        settings_action = QAction("Settings", self.main_window)
        settings_action.triggered.connect(self.main_window.show_settings_dialog)
        file_menu.addAction(settings_action)

        # Exit action
        exit_action = QAction("Exit", self.main_window)
        exit_action.triggered.connect(self.main_window.close)
        exit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(exit_action)

    def _create_edit_menu(self):
        """Create the Edit menu with text editing actions."""
        edit_menu = self.menu_bar.addMenu("Edit")

        # Indent action
        indent_action = QAction("Indent", self.main_window)
        indent_action.triggered.connect(self.main_window.indent_current_editor)
        indent_action.setShortcut("Tab")
        edit_menu.addAction(indent_action)

        # Dedent action
        dedent_action = QAction("Dedent", self.main_window)
        dedent_action.triggered.connect(self.main_window.dedent_current_editor)
        dedent_action.setShortcut("Shift+Tab")
        edit_menu.addAction(dedent_action)

    def _create_mode_menu(self):
        """Create the Mode menu with Basic and Max options."""
        self.mode_menu = self.menu_bar.addMenu("Mode")

        # Basic mode action
        self.basic_mode_action = QAction("Basic (100 Problems)", self.main_window)
        self.basic_mode_action.setCheckable(True)
        self.basic_mode_action.triggered.connect(lambda: self.main_window.set_problem_mode("basic"))
        self.mode_menu.addAction(self.basic_mode_action)

        # Max mode action
        self.max_mode_action = QAction("Max (All 945 Problems)", self.main_window)
        self.max_mode_action.setCheckable(True)
        self.max_mode_action.triggered.connect(lambda: self.main_window.set_problem_mode("max"))
        self.mode_menu.addAction(self.max_mode_action)

        # Set default selection
        self.basic_mode_action.setChecked(True)

    def _create_theme_menu(self):
        """Create the Theme menu with its actions."""
        theme_menu = self.menu_bar.addMenu("Theme")

        # Dark theme action
        dark_theme_action = QAction("Dark Mode", self.main_window)
        dark_theme_action.triggered.connect(self.main_window.set_dark_theme)
        theme_menu.addAction(dark_theme_action)

        # Light theme action
        light_theme_action = QAction("Light Mode", self.main_window)
        light_theme_action.triggered.connect(self.main_window.set_light_theme)
        theme_menu.addAction(light_theme_action)

    def _create_view_menu(self):
        """Create the View menu with its actions."""
        view_menu = self.menu_bar.addMenu("&View")

        # Progress action
        progress_action = QAction("Progress", self.main_window)
        progress_action.triggered.connect(self.main_window.show_progress_dialog)
        view_menu.addAction(progress_action)

        # Add separator for toolbar toggles
        view_menu.addSeparator()

        # Toolbar toggles will be added by MainWindow.update_view_menu

        # Store the view_menu reference for later updates
        self.view_menu = view_menu

    def _create_help_menu(self):
        """Create the Help menu with its actions."""
        help_menu = self.menu_bar.addMenu("Help")

        # Welcome action
        welcome_action = QAction("Welcome", self.main_window)
        welcome_action.triggered.connect(self.main_window.show_welcome_dialog)
        help_menu.addAction(welcome_action)

        # Tutorials action
        tutorials_action = QAction("Tutorials", self.main_window)
        tutorials_action.triggered.connect(self.main_window.show_tutorials_dialog)
        help_menu.addAction(tutorials_action)

        # Tutorial Editor action removed

        # Info action
        info_action = QAction("Info", self.main_window)
        info_action.triggered.connect(self.main_window.show_info_dialog)
        help_menu.addAction(info_action)

        # Project Euler submenu
        project_euler_menu = help_menu.addMenu("Project Euler")

        # Website action
        website_action = QAction("Website", self.main_window)
        website_action.triggered.connect(self.main_window.open_project_euler_website)
        project_euler_menu.addAction(website_action)

        # Official Status action
        status_action = QAction("Official Status", self.main_window)
        status_action.triggered.connect(self.main_window.show_project_euler_status)
        project_euler_menu.addAction(status_action)

        # About action
        about_action = QAction("About", self.main_window)
        about_action.triggered.connect(self.main_window.show_about_dialog)
        help_menu.addAction(about_action)