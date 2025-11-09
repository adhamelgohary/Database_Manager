# base_manager.py


class BaseManager:
    """
    A base class for all database managers. It defines a common interface
    but does not implement any functionality.
    """

    def __init__(self):
        self._check_driver()

    def _check_driver(self):
        """Checks if the required database driver is installed."""
        raise NotImplementedError("Subclasses must implement _check_driver()")

    def connect(self, db_config):
        """Establishes a connection to the database."""
        raise NotImplementedError("Subclasses must implement connect()")

    def disconnect(self):
        """Closes the database connection."""
        raise NotImplementedError("Subclasses must implement disconnect()")

    def list_databases(self):
        """Retrieves a list of all databases from the server."""
        raise NotImplementedError("Subclasses must implement list_databases()")

    def list_tables(self):
        """Retrieves a list of tables from the connected database."""
        raise NotImplementedError("Subclasses must implement list_tables()")
