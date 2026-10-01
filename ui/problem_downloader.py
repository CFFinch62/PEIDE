"""
Download new problems from projecteuler.net without blocking the UI.
"""

from PyQt6.QtCore import QThread, pyqtSignal

from tools.import_problems import import_problems


class ProblemDownloadThread(QThread):
    """Imports problems that don't have a problem file yet."""

    progress = pyqtSignal(str)  # one message per problem

    def __init__(self, problems_dir, parent=None):
        super().__init__(parent)
        self.problems_dir = problems_dir
        self.imported = []
        self.failed = []
        self.error = None

    def run(self):
        try:
            self.imported, self.failed = import_problems(
                self.problems_dir, new=True, report=self.progress.emit)
        except Exception as e:  # e.g. no internet connection
            self.error = str(e)
