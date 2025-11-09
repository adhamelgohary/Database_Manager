# main.py

import sys
from PyQt6.QtWidgets import QApplication

# MODIFIED: Import the new startup window
from src.ui.welcome_window import WelcomeWindow
from src.ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Create and show the WelcomeWindow first
    welcome_win = WelcomeWindow()
    # .exec() shows the dialog modally and waits for it to close
    result = welcome_win.exec()

    # If the user successfully selected a database, launch the MainWindow
    if result == welcome_win.accepted:
        # Pass the pre-configured adapter and selected DB to the MainWindow
        main_win = MainWindow(
            adapter=welcome_win.successful_adapter,
            database=welcome_win.selected_database
        )
        main_win.show()
        sys.exit(app.exec())
    else:
        # If user cancelled, just exit the application
        sys.exit(0)