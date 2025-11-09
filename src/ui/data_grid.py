# src/ui/data_grid.py

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

class DataGrid(QTableWidget):
    """A reusable widget for displaying tabular data."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Read-only
        self.setAlternatingRowColors(True) # Improves readability

    def populate_data(self, headers, data):
        """Clears the grid and fills it with new data."""
        self.clear()
        self.setRowCount(0)

        if not data:
            return

        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

        self.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                # Convert all data to string for display
                item = QTableWidgetItem(str(cell_data))
                self.setItem(row_index, col_index, item)
        
        # Resize columns to fit the content for better viewing
        self.resizeColumnsToContents()