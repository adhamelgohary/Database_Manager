# src/ui/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QToolBar,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from src.ui.connection_switcher import ConnectionSwitcher
from src.ui.object_explorer import ObjectExplorer
from src.ui.content_viewer import ContentViewer

# Note: ConnectionDialog and Adapters are no longer needed by MainWindow itself.


class MainWindow(QMainWindow):
    # The constructor now accepts the pre-configured adapter and connection details
    def __init__(self, adapter, conn_details, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SQL Client")
        self.setGeometry(100, 100, 1200, 800)

        # Set the active adapter from the WelcomeWindow
        self.active_adapter = adapter
        self.connection_details = conn_details

        # --- Load Icons ---
        self.db_icon = QIcon("src/resources/icons/database.svg")

        # --- Create UI Components ---
        self.col1_widget = ConnectionSwitcher()
        self.col2_widget = ObjectExplorer()
        self.col3_widget = ContentViewer()
        self.top_bar = self._create_top_bar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_bar)

        # --- Assemble Layout ---
        self.content_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.content_splitter.addWidget(self.col2_widget)
        self.content_splitter.addWidget(self.col3_widget)

        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(self.col1_widget)
        self.main_splitter.addWidget(self.content_splitter)

        # --- Set Sizes and Constraints ---
        self.main_splitter.setSizes([65, 1135])
        self.content_splitter.setSizes([250, 885])
        self.col1_widget.setFixedWidth(65)
        self.col2_widget.setMinimumWidth(200)

        self.setCentralWidget(self.main_splitter)
        self._apply_styles()

        # --- Set Object Names for Styling ---
        self.col1_widget.setObjectName("ConnectionList")
        self.col2_widget.setObjectName("ObjectExplorer")
        self.col2_widget.tables_btn.setProperty("pos", "left")
        self.col2_widget.queries_btn.setProperty("pos", "mid")
        self.col2_widget.history_btn.setProperty("pos", "right")
        self.col2_widget.tables_btn.setObjectName("SegmentedButton")
        self.col2_widget.queries_btn.setObjectName("SegmentedButton")
        self.col2_widget.history_btn.setObjectName("SegmentedButton")
        self.col2_widget.tables_btn.setCheckable(True)
        self.col2_widget.queries_btn.setCheckable(True)
        self.col2_widget.history_btn.setCheckable(True)
        self.col2_widget.tables_btn.setChecked(True)

        # --- Connect Signals to Slots ---
        self.col2_widget.table_selected.connect(self._on_table_selected)
        self.col2_widget.queries_btn.clicked.connect(self.col3_widget.show_query_editor)
        self.col2_widget.tables_btn.clicked.connect(self.col3_widget.show_data_grid)
        self.col2_widget.history_btn.clicked.connect(self.col3_widget.show_history)

        # --- Populate UI with Initial Data ---
        self._load_initial_state()

    # NEW version in src/ui/main_window.py

    def _load_initial_state(self):
        """Uses the initial adapter and details to populate the UI on startup."""
        if not self.active_adapter:
            return

        # Get the specific database name chosen in the WelcomeWindow
        db_name = self.connection_details.get("database")

        # Get the user@host for the top bar label
        conn_name = f"{self.connection_details.get('user')}@{self.connection_details.get('host')}"

        # --- Populate Column 1 ---
        # Clear any previous items and add the new database workspace
        self.col1_widget.clear()
        self.col1_widget.add_connection(db_name, self.db_icon)
        # TODO: We can add logic to automatically select this new item.
        # self.col1_widget.setCurrentRow(0)

        # --- Populate Column 2 ---
        # Tell the ObjectExplorer to list the tables for this specific database
        self.col2_widget.populate_tables(self.active_adapter, db_name)

        # --- Update the Top Bar Label ---
        # Display the full connection path for clarity
        self.connection_label.setText(f"{conn_name} : {db_name}")

    def _on_table_selected(self, table_name):
        """Handles the signal to view a table's content."""
        if not self.active_adapter:
            return

        headers, data = self.active_adapter.get_table_content(table_name)

        # Show grid even if the table is just empty
        if headers is not None and data is not None:
            self.col3_widget.show_data_grid()
            self.col3_widget.data_grid_page.populate_data(headers, data)

            # Update the top bar to show the table name
            db_name = self.connection_details.get("database")
            conn_name = f"{self.connection_details.get('user')}@{self.connection_details.get('host')}"
            self.connection_label.setText(f"{conn_name} : {db_name} : {table_name}")
        else:
            QMessageBox.warning(
                self, "Error", f"Could not retrieve data for table '{table_name}'."
            )

    def _create_top_bar(self):
        """Builds the main top toolbar widget."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)

        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        container.setLayout(layout)

        # In this window, the Add Connection button is not needed
        # We keep some placeholders for future functionality
        self.close_conn_btn = QPushButton(QIcon("src/resources/icons/x-circle.svg"), "")
        self.refresh_btn = QPushButton(QIcon("src/resources/icons/refresh-cw.svg"), "")

        layout.addWidget(self.close_conn_btn)
        layout.addStretch()

        self.connection_label = QLabel("Not Connected")
        self.connection_label.setObjectName("ConnectionLabel")
        layout.addWidget(self.connection_label)

        layout.addStretch()
        layout.addWidget(self.refresh_btn)

        toolbar.addWidget(container)
        return toolbar

    def _apply_styles(self):
        """Loads and applies the main stylesheet from an external file."""
        try:
            with open("src/resources/styles/macos_light.qss", "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print(
                "Stylesheet not found. Please ensure 'macos_light.qss' exists in 'src/resources/styles/'."
            )
