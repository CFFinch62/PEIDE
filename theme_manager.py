"""
Theme Manager module for Project Euler Editor.
Handles application-wide theming (dark/light modes).
"""
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt


class ThemeManager:
    """
    Manages application-wide theming, including dark and light modes.
    Handles setting colors and persisting theme preferences.
    """
    
    def __init__(self, settings_manager=None):
        """
        Initialize the Theme Manager.
        
        Args:
            settings_manager: The settings manager for persisting theme preferences
        """
        self.settings_manager = settings_manager
        self.current_theme = 'dark'  # Default theme
    
    def load_theme(self):
        """
        Load the saved theme from settings and apply it.
        Should be called once during application startup.
        """
        if not self.settings_manager:
            return
            
        # Get saved theme from settings, default to dark
        theme_setting = self.settings_manager.settings.get('theme', 'dark')
        self.current_theme = theme_setting
        
        # Apply the theme
        if theme_setting == 'light':
            return self.create_light_palette()
        else:
            return self.create_dark_palette()
    
    def create_dark_palette(self):
        """
        Create and return a dark theme palette.
        
        Returns:
            QPalette: The dark theme palette
        """
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        return palette
    
    def create_light_palette(self):
        """
        Create and return a light theme palette.
        
        Returns:
            QPalette: The light theme palette
        """
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 102, 204))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(51, 153, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        return palette
    
    def apply_dark_theme(self, app, status_bar=None):
        """
        Apply the dark theme to the application.
        
        Args:
            app: The QApplication instance
            status_bar: Optional status bar for displaying a message
        """
        palette = self.create_dark_palette()
        app.setPalette(palette)
        
        # Save theme preference
        if self.settings_manager:
            self.settings_manager.settings['theme'] = 'dark'
            self.settings_manager.save_settings()
            self.current_theme = 'dark'
        
        # Notify user if status bar is provided
        if status_bar:
            status_bar.showMessage("Dark theme applied", 3000)
    
    def apply_light_theme(self, app, status_bar=None):
        """
        Apply the light theme to the application.
        
        Args:
            app: The QApplication instance
            status_bar: Optional status bar for displaying a message
        """
        palette = self.create_light_palette()
        app.setPalette(palette)
        
        # Save theme preference
        if self.settings_manager:
            self.settings_manager.settings['theme'] = 'light'
            self.settings_manager.save_settings()
            self.current_theme = 'light'
        
        # Notify user if status bar is provided
        if status_bar:
            status_bar.showMessage("Light theme applied", 3000)
    
    def toggle_theme(self, app, status_bar=None):
        """
        Toggle between dark and light themes.
        
        Args:
            app: The QApplication instance
            status_bar: Optional status bar for displaying a message
        """
        if self.current_theme == 'dark':
            self.apply_light_theme(app, status_bar)
        else:
            self.apply_dark_theme(app, status_bar)
    
    def get_current_theme(self):
        """
        Get the current theme name.
        
        Returns:
            str: 'dark' or 'light'
        """
        return self.current_theme 