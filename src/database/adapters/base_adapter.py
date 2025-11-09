# src/database/adapters/base_adapter.py

# UPDATED: Class name changed to BaseAdapter
class BaseAdapter:
    """
    A base class for all database adapters. Defines a common interface.
    """
    def __init__(self):
        self._check_driver()

    def _check_driver(self):
        raise NotImplementedError("Subclasses must implement _check_driver()")

    def connect(self, db_config):
        raise NotImplementedError("Subclasses must implement connect()")

    def disconnect(self):
        raise NotImplementedError("Subclasses must implement disconnect()")

    def list_databases(self):
        raise NotImplementedError("Subclasses must implement list_databases()")

    def list_tables(self):
        raise NotImplementedError("Subclasses must implement list_tables()")

    def create_database(self, db_name):
        raise NotImplementedError("Subclasses must implement create_database()")

    def get_table_content(self, table_name):
        """Fetches the headers and a limited number of rows from a table."""
        raise NotImplementedError("Subclasses must implement get_table_content()")