# src/ui/connection_dialog.py

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QComboBox,
)
from PyQt6.QtCore import pyqtSignal


class ConnectionDialog(QDialog):
    # Signal to request a connection test. It carries the details dict.
    test_connection_requested = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connection Details")

        self.db_type_combo = QComboBox()
        self.db_type_combo.addItems(["MySQL", "PostgreSQL (not implemented)"])
        self.host_input = QLineEdit("127.0.0.1")
        self.port_input = QLineEdit("3306")
        self.user_input = QLineEdit("root")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # --- Create Buttons ---
        self.button_box = QDialogButtonBox()
        self.test_button = self.button_box.addButton(
            "Test Connection", QDialogButtonBox.ActionRole
        )
        self.continue_button = self.button_box.addButton(
            "Continue", QDialogButtonBox.AcceptRole
        )
        self.continue_button.setEnabled(False)  # Disabled by default
        self.cancel_button = self.button_box.addButton(
            QDialogButtonBox.StandardButton.Cancel
        )

        # --- Connect Signals ---
        self.test_button.clicked.connect(self._on_test_clicked)
        self.continue_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # --- Assemble Layout ---
        form_layout = QFormLayout()
        form_layout.addRow("Database Type:", self.db_type_combo)
        form_layout.addRow("Host:", self.host_input)
        form_layout.addRow("Port:", self.port_input)
        form_layout.addRow("User:", self.user_input)
        form_layout.addRow("Password:", self.password_input)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.button_box)

    def _on_test_clicked(self):
        """Gathers details and emits the test signal."""
        self.continue_button.setEnabled(False)  # Always reset on new test
        details = self.get_connection_details()
        self.test_connection_requested.emit(details)

    def on_test_success(self):
        """Public slot for the parent window to call on successful test."""
        self.continue_button.setEnabled(True)

    def get_connection_details(self):
        """Public method to retrieve the entered text."""
        # Note: We no longer include a database name here
        return {
            "db_type": self.db_type_combo.currentText(),
            "host": self.host_input.text(),
            "port": int(self.port_input.text()),
            "user": self.user_input.text(),
            "password": self.password_input.text(),
        }
