"""
SQLite specific database operations
"""
from services.base_service import BaseDatabaseService
from sqlalchemy import text
from typing import List
import os

class SQLiteService(BaseDatabaseService):
    
    def get_databases(self) -> List[str]:
        """SQLite has only one database per file"""
        return ["main"]
    
    def get_tables(self, database: str = None) -> List[str]:
        """Get list of tables"""
        with self.engine.connect() as conn:
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            ))
            return [row[0] for row in result.fetchall()]
    
    def create_database(self, database_name: str):
        """SQLite creates database when connecting to a file"""
        raise NotImplementedError("SQLite databases are file-based")
    
    def drop_database(self, database_name: str):
        """SQLite: delete the database file"""
        raise NotImplementedError("SQLite databases are file-based")
    
    def get_database_size(self, database_name: str = None) -> str:
        """Get database file size"""
        # Extract file path from connection string
        db_path = self.connection_string.replace('sqlite:///', '')
        if os.path.exists(db_path):
            size_bytes = os.path.getsize(db_path)
            size_mb = size_bytes / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        return "0 MB"
    
    def get_table_count(self, database_name: str = None) -> int:
        """Get number of tables"""
        return len(self.get_tables())