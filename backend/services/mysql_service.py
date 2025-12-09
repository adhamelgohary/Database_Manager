"""
MySQL specific database operations
"""
from services.base_service import BaseDatabaseService
from sqlalchemy import text
from typing import List

class MySQLService(BaseDatabaseService):
    
    def get_databases(self) -> List[str]:
        """Get list of all databases"""
        with self.engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES"))
            databases = [row[0] for row in result.fetchall()]
            # Filter out system databases
            system_dbs = ['information_schema', 'mysql', 'performance_schema', 'sys']
            return [db for db in databases if db not in system_dbs]
    
    def create_database(self, database_name: str, charset: str = 'utf8mb4', collation: str = 'utf8mb4_unicode_ci'):
        """Create a new database"""
        with self.engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE `{database_name}` CHARACTER SET {charset} COLLATE {collation}"))
            conn.commit()
    
    def drop_database(self, database_name: str):
        """Drop a database"""
        with self.engine.connect() as conn:
            conn.execute(text(f"DROP DATABASE `{database_name}`"))
            conn.commit()
    
    def get_database_size(self, database_name: str) -> str:
        """Get database size"""
        query = text("""
            SELECT 
                ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
            FROM information_schema.tables 
            WHERE table_schema = :db_name
        """)
        with self.engine.connect() as conn:
            result = conn.execute(query, {"db_name": database_name}).fetchone()
            return f"{result[0]} MB" if result and result[0] else "0 MB"
    
    def get_table_count(self, database_name: str) -> int:
        """Get number of tables in database"""
        query = text("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = :db_name AND table_type = 'BASE TABLE'
        """)
        with self.engine.connect() as conn:
            result = conn.execute(query, {"db_name": database_name}).fetchone()
            return result[0] if result else 0