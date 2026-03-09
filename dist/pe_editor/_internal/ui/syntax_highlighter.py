from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import re

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, settings_manager=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.highlighting_rules = []
        self.document = parent
        self.update_highlighting_rules()

    def update_highlighting_rules(self):
        """Update highlighting rules based on current settings"""
        self.highlighting_rules = []
        
        # Get colors from settings or use defaults
        colors = {
            'keywords': self.settings_manager.get_highlighting_color('keywords') if self.settings_manager else '#569CD6',
            'strings': self.settings_manager.get_highlighting_color('strings') if self.settings_manager else '#CE9178',
            'numbers': self.settings_manager.get_highlighting_color('numbers') if self.settings_manager else '#E07912',
            'comments': self.settings_manager.get_highlighting_color('comments') if self.settings_manager else '#6A9955',
            'operators': self.settings_manager.get_highlighting_color('operators') if self.settings_manager else '#DCDCAA',
            'functions': self.settings_manager.get_highlighting_color('functions') if self.settings_manager else '#DCDCAA',
            'variables': self.settings_manager.get_highlighting_color('variables') if self.settings_manager else '#9CDCFE',
            'punctuation': self.settings_manager.get_highlighting_color('punctuation') if self.settings_manager else '#D4D4D4'
        }
        
        # Comments (highest priority)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(colors['comments']))
        self.highlighting_rules.append((re.compile(r'#[^\n]*'), comment_format))
        
        # Strings (second highest priority)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(colors['strings']))
        self.highlighting_rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))
        
        # Numbers (third priority)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(colors['numbers']))
        self.highlighting_rules.append((re.compile(r'\b[0-9]+\b'), number_format))
        
        # Keywords
        keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def',
                   'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
                   'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
                   'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
                   'True', 'try', 'while', 'with', 'yield']
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(colors['keywords']))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        for word in keywords:
            pattern = re.compile(r'\b' + word + r'\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Functions/Methods
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(colors['functions']))
        self.highlighting_rules.append((re.compile(r'\b\w+(?=\s*\()'), function_format))
        
        # Operators
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor(colors['operators']))
        operators = r'[+\-*/%=<>!&|^~]'
        self.highlighting_rules.append((re.compile(operators), operator_format))
        
        # Punctuation
        punctuation_format = QTextCharFormat()
        punctuation_format.setForeground(QColor(colors['punctuation']))
        self.highlighting_rules.append((re.compile(r'[,;:()\[\]{}]'), punctuation_format))
        
        # Force rehighlighting after updating rules
        if self.document:
            self.rehighlight()

    def highlightBlock(self, text):
        """Apply highlighting rules to the text block"""
        # First, apply comments and strings (highest priority)
        for pattern, format in self.highlighting_rules[:3]:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)
        
        # Then apply all other rules
        for pattern, format in self.highlighting_rules[3:]:
            for match in pattern.finditer(text):
                start, end = match.span()
                # Only apply formatting if the text isn't in a comment
                if not any(self.format(i).foreground().color() == QColor(self.settings_manager.get_highlighting_color('comments') if self.settings_manager else '#6A9955') for i in range(start, end)):
                    self.setFormat(start, end - start, format) 