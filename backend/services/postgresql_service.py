"""
PostgreSQL specific database operations
"""
from services.base_service import BaseDatabaseService
from sqlalchemy import text
from typing import List

class PostgreSQLService(BaseDatabaseService):
    
    def get_databases(self) -> List[str]:
        """Get list of all databases"""
        with self.engine.connect() as conn:
            result = conn.execute(text(
                "SELECT datname FROM pg_database WHERE datistemplate = false"
            ))
            databases = [row[0] for row in result.fetchall()]
            # Filter out postgres system database
            return [db for db in databases if db != 'postgres']
    
    def create_database(self, database_name: str):
        """Create a new database"""
        # PostgreSQL requires autocommit for CREATE DATABASE
        with self.engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(text(f'CREATE DATABASE "{database_name}"'))
    
    def drop_database(self, database_name: str):
        """Drop a database"""
        with self.engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(text(f'DROP DATABASE "{database_name}"'))
    
    def get_database_size(self, database_name: str) -> str:
        """Get database size"""
        query = text("""
            SELECT pg_size_pretty(pg_database_size(:db_name))
        """)
        with self.engine.connect() as conn:
            result = conn.execute(query, {"db_name": database_name}).fetchone()
            return result[0] if result else "0 bytes"
    
    def get_table_count(self, database_name: str) -> int:
        """Get number of tables in database"""
        query = text("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_catalog = :db_name 
            AND table_schema = 'public' 
            AND table_type = 'BASE TABLE'
        """)
        with self.engine.connect() as conn:
            result = conn.execute(query, {"db_name": database_name}).fetchone()
            return result[0] if result else 0