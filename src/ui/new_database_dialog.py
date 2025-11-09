# src/ui/new_database_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, 
    QLineEdit, QVBoxLayout
)

class NewDatabaseDialog(QDialog):
    """A dialog for getting a new database name from the user."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Database")

        # The input field for the database name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., my_new_project")

        # The standard OK/Cancel buttons
        # The .accepted and .rejected signals are automatically connected
        # to the dialog's accept() and reject() slots.
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # The layout
        form_layout = QFormLayout()
        form_layout.addRow("Database Name:", self.name_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def get_database_name(self):
        """Public method to retrieve the entered text."""
        # .strip() removes any leading/trailing whitespace
        return self.name_input.text().strip()