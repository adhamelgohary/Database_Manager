# mysql_manager.py

from base_manager import BaseManager

try:
    import mysql.connector
    from mysql.connector import errorcode

    MYSQL_DRIVER_INSTALLED = True
except ImportError:
    MYSQL_DRIVER_INSTALLED = False


class MySQLManager(BaseManager):
    """Manages the connection to a MySQL database."""

    def __init__(self):
        self.connection = None
        self.cursor = None
        super().__init__()

    def _check_driver(self):
        """Overrides the base method to check for the MySQL driver."""
        if not MYSQL_DRIVER_INSTALLED:
            raise ConnectionError(
                "MySQL driver not installed. Please run: pip install mysql-connector-python"
            )

    def connect(self, db_config):
        """Establishes a connection to the database."""
        try:
            config = db_config.copy()
            if not config.get("database"):
                config.pop("database", None)
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
            print("MySQL connection successful.")
            return True
        except mysql.connector.Error as err:
            print(f"MySQL connection error: {err}")
            return False

    def disconnect(self):
        """Closes the database connection."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed.")

    def list_databases(self):
        """Retrieves a list of all databases from the server."""
        if not (self.connection and self.connection.is_connected()):
            return []
        try:
            self.cursor.execute("SHOW DATABASES;")
            system_dbs = ["information_schema", "mysql", "performance_schema", "sys"]
            databases = [
                db[0] for db in self.cursor.fetchall() if db[0] not in system_dbs
            ]
            return databases
        except mysql.connector.Error as err:
            print(f"Failed to list MySQL databases: {err}")
            return []

    def list_tables(self):
        """Retrieves a list of tables from the connected database."""
        if not (self.connection and self.connection.is_connected()):
            return []
        try:
            self.cursor.execute("SHOW TABLES;")
            tables = [table[0] for table in self.cursor.fetchall()]
            return tables
        except mysql.connector.Error as err:
            print(f"Failed to list MySQL tables: {err}")
            return []
