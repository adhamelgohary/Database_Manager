# src/ui/object_explorer.py

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal

from src.ui.new_database_dialog import NewDatabaseDialog


class ObjectExplorer(QWidget):
    # This component no longer creates databases, that logic is in WelcomeWindow
    # but we can leave the signal for future features if needed.
    database_creation_requested = pyqtSignal(str)
    table_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.manager = None
        self.table_icon = QIcon("src/resources/icons/table.svg")

        # --- Create Widgets ---
        # The create button is removed, as this action now happens on the Welcome screen
        self.tables_btn = QPushButton("Tables")
        self.queries_btn = QPushButton("Queries")
        self.history_btn = QPushButton("History")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for a table...")

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)

        # --- Assemble Layout ---
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.tables_btn)
        button_layout.addWidget(self.queries_btn)
        button_layout.addWidget(self.history_btn)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.tree)

        # --- Connect Signals ---
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)

    def populate_tables(self, adapter, db_name):
        """
        Public method to populate the tree with tables from a specific database.
        """
        self.manager = adapter
        self.tree.clear()

        if not self.manager:
            return

        # Tell the adapter to use the selected database
        self.manager.connection.cmd_init_db(db_name)

        tables = self.manager.list_tables()
        for table_name in tables:
            item = QTreeWidgetItem(self.tree)
            item.setText(0, table_name)
            item.setIcon(0, self.table_icon)

    def _on_item_double_clicked(self, item, column):
        """Emits a signal when a table item is double-clicked."""
        # Ensure it's a valid item and not the header
        if item:
            table_name = item.text(0)
            self.table_selected.emit(table_name)
