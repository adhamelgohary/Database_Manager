# src/ui/connection_switcher.py

from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon


class ConnectionSwitcher(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setIconSize(QSize(32, 32))
        self.setMovement(QListWidget.Movement.Static)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)

    def add_connection(self, name, icon):
        """Public method to add a new connection item to the list."""
        item = QListWidgetItem(name)
        item.setIcon(icon)
        item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.addItem(item)
