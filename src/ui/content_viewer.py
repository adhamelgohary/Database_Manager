# src/ui/content_viewer.py

from PyQt6.QtWidgets import QWidget, QStackedWidget, QTextEdit, QListWidget
from .data_grid import DataGrid # Import our new custom grid

class ContentViewer(QWidget):
    """The UI for the content viewer (Column 3). Manages different views."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the pages
        self.data_grid_page = DataGrid()
        self.query_page = QTextEdit()
        self.history_page = QListWidget()

        # Create and configure the stacked widget
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.data_grid_page)
        self.stack.addWidget(self.query_page)
        self.stack.addWidget(self.history_page)
        
        # The ContentViewer itself doesn't need a layout,
        # we will set the stack widget to be its main layout in MainWindow.
        # A better way is to set a layout here.
        from PyQt6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.stack)


    def show_data_grid(self):
        self.stack.setCurrentWidget(self.data_grid_page)

    def show_query_editor(self):
        self.stack.setCurrentWidget(self.query_page)

    def show_history(self):
        self.stack.setCurrentWidget(self.history_page)