# main_window.py

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,  # QPushButton is new
    QSplitter,
    QListWidget,
    QTextEdit,
    QTableWidget,
    QDialog,
)
from PyQt6.QtCore import Qt
from database_manager import DatabaseManager  # NEW: Import our manager
from connection_dialog import ConnectionDialog


class MainWindow(QMainWindow):
    """Our main application window."""

    def __init__(self):
        """Initializer."""
        super().__init__()

        self.setWindowTitle("SQL Client")
        self.setGeometry(100, 100, 1200, 800)
        self.db_manager = DatabaseManager()

        # --- Load Icons ---
        # We load icons once and reuse them to be efficient.
        self.db_icon = QIcon("icons/database.svg")
        self.table_icon = QIcon("icons/table.svg")

        # --- Create Widgets ---

        # 1. Sidebar Search Bar
        self.sidebar_search = QLineEdit()
        self.sidebar_search.setPlaceholderText("Search for item...")

        # 2. Sidebar Tree Widget (The biggest change!)
        self.sidebar_tree = QTreeWidget()
        self.sidebar_tree.setHeaderHidden(True)  # Hides the column title bar

        # 3. Connect Button (We will keep it for now but disconnect its action)
        self.connect_button = QPushButton("Connect to DB")
        # self.connect_button.clicked.connect(self.on_connect_clicked) # Temporarily disabled

        # 4. Main Content Area (For now, just a placeholder)
        self.query_editor = QTextEdit()
        self.query_editor.setPlaceholderText("SELECT * FROM your_table;")

        self.results_table = QTableWidget()

        # --- Populate Sidebar with Static Placeholder Data ---
        # This demonstrates how the tree structure works.

        # Top-level item for the MySQL connection
        mysql_connection = QTreeWidgetItem(self.sidebar_tree)
        mysql_connection.setText(0, "mysql")
        mysql_connection.setIcon(0, self.db_icon)

        # Child item for the "Tables" category
        tables_category = QTreeWidgetItem(mysql_connection)
        tables_category.setText(0, "Tables")

        # Example table names as children of the "Tables" category
        table_names = [
            "columns_priv",
            "comments",
            "component",
            "db",
            "default_roles",
            "engine_cost",
            "func",
            "general_log",
            "global_grants",
        ]
        for name in table_names:
            table_item = QTreeWidgetItem(tables_category)
            table_item.setText(0, name)
            table_item.setIcon(0, self.table_icon)

        # Expand the tree to show the tables by default
        mysql_connection.setExpanded(True)
        tables_category.setExpanded(True)

        # --- Create Layouts ---

        # Sidebar Layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(5, 5, 5, 5)  # Add a little padding
        sidebar_layout.addWidget(self.connect_button)  # We'll replace this later
        sidebar_layout.addWidget(self.sidebar_search)
        sidebar_layout.addWidget(self.sidebar_tree)

        sidebar_container = QWidget()
        sidebar_container.setLayout(sidebar_layout)
        # Set a max width for the sidebar to look better
        sidebar_container.setMaximumWidth(250)

        # Main Layout (for now, just the editor and results)
        main_content_layout = QVBoxLayout()
        main_content_layout.addWidget(self.query_editor)
        main_content_layout.addWidget(self.results_table)
        main_content_container = QWidget()
        main_content_container.setLayout(main_content_layout)

        # Main Splitter
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.addWidget(sidebar_container)
        content_splitter.addWidget(main_content_container)  # Use the new container
        content_splitter.setSizes([250, 950])  # Adjust initial sizes

        self.setCentralWidget(content_splitter)

    def on_connect_clicked(self):
        """Handles the connect button click event by opening the connection dialog."""
        print("1. 'Connect' button clicked. Opening dialog...")
        dialog = ConnectionDialog(self)

        result = dialog.exec()

        print(f"2. Dialog closed. Result code: {result}")

        if result == QDialog.DialogCode.Accepted:
            print("3. User clicked 'OK'.")
            db_config = dialog.get_connection_details()
            print(f"4. Connection details received: {db_config}")

            if self.db_manager.connect(db_config):
                print("5. Connection to DB Manager successful.")

                # If a database was specified, list its tables.
                # If not, list all available databases.
                if db_config.get("database"):
                    print("6a. Database was specified. Listing tables...")
                    tables = self.db_manager.list_tables()
                    print(f"7a. Tables received: {tables}")
                    self._update_sidebar_tables(tables)
                else:
                    print("6b. No database specified. Listing databases...")
                    databases = self.db_manager.list_databases()
                    print(f"7b. Databases received: {databases}")
                    self._update_sidebar_databases(databases)

            else:
                print("5. Connection to DB Manager FAILED. Check console.")
                self.databases_list_widget.clear()
                self.tables_list_widget.clear()
        else:
            print("3. User clicked 'Cancel' or closed the dialog.")

    def _update_sidebar_tables(self, tables):
        """Populates the sidebar list widget with table names."""
        # This now correctly updates the *tables* list
        self.tables_list_widget.clear()
        self.tables_list_widget.addItem("--- TABLES ---")  # Add a header
        for table_name in tables:
            self.tables_list_widget.addItem(table_name)

    def _update_sidebar_databases(self, databases):
        """Populates the sidebar list widget with database names."""
        # This now correctly updates the *databases* list
        self.databases_list_widget.clear()
        self.databases_list_widget.addItem("--- DATABASES ---")  # Add a header
        for database_name in databases:
            self.databases_list_widget.addItem(database_name)
