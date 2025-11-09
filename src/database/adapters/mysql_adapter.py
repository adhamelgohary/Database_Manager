# src/database/adapters/mysql_adapter.py

import re
# UPDATED: Use absolute import path from the src root
from src.database.adapters.base_adapter import BaseAdapter

try:
    import mysql.connector
    from mysql.connector import errorcode
    MYSQL_DRIVER_INSTALLED = True
except ImportError:
    MYSQL_DRIVER_INSTALLED = False

# UPDATED: Class name changed to MySQLAdapter and inherits from BaseAdapter
class MySQLAdapter(BaseAdapter):
    """Manages the connection to a MySQL database."""
    def __init__(self):
        self.connection = None
        self.cursor = None
        super().__init__()

    def _check_driver(self):
        if not MYSQL_DRIVER_INSTALLED:
            raise ConnectionError("MySQL driver not installed. Please run: pip install mysql-connector-python")

    def connect(self, db_config):
        try:
            config = db_config.copy()
            if not config.get('database'):
                config.pop('database', None)
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
            return True
        except mysql.connector.Error as err:
            print(f"MySQL connection error: {err}")
            return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def list_databases(self):
        if not (self.connection and self.connection.is_connected()): return []
        try:
            self.cursor.execute("SHOW DATABASES;")
            system_dbs = ['information_schema', 'mysql', 'performance_schema', 'sys']
            return [db[0] for db in self.cursor.fetchall() if db[0] not in system_dbs]
        except mysql.connector.Error as err:
            print(f"Failed to list MySQL databases: {err}")
            return []

    def list_tables(self):
        if not (self.connection and self.connection.is_connected()): return []
        try:
            self.cursor.execute("SHOW TABLES;")
            return [table[0] for table in self.cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Failed to list MySQL tables: {err}")
            return []
    
    def create_database(self, db_name):
        if not (self.connection and self.connection.is_connected()):
            return False, "Not connected to a database."

        if not re.match(r'^[a-zA-Z0-9_]+$', db_name):
            return False, f"Invalid database name: '{db_name}'. Use only letters, numbers, and underscores."

        try:
            self.cursor.execute(f"CREATE DATABASE {db_name}")
            return True, f"Database '{db_name}' created successfully."
        except mysql.connector.Error as err:
            return False, str(err)


    def get_table_content(self, table_name):
        """Fetches headers and first 100 rows from a MySQL table."""
        if not (self.connection and self.connection.is_connected()):
            return [], [] # Return empty lists if not connected

        try:
            # Use backticks for table names to handle reserved keywords and special chars
            # LIMIT 100 is crucial to prevent freezing the UI on large tables.
            query = f"SELECT * FROM `{table_name}` LIMIT 100;"
            self.cursor.execute(query)
            
            # Get column headers from the cursor description
            headers = [desc[0] for desc in self.cursor.description]
            
            # Fetch all the rows
            data = self.cursor.fetchall()
            
            return headers, data
        except mysql.connector.Error as err:
            print(f"Failed to get content for table {table_name}: {err}")
            return [], [] # Return empty lists on error