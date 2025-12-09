"""
Base database service with common functionality
"""
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.pool import NullPool
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseDatabaseService:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = None
    
    def connect(self):
        """Create database engine connection"""
        try:
            self.engine = create_engine(
                self.connection_string,
                poolclass=NullPool,
                echo=False
            )
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            self.engine = None
    
    def test_connection(self) -> bool:
        """Test if connection is valid"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except:
            return False
    
    def execute_query(self, query: str, params: Dict = None):
        """Execute a query and return results"""
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            if result.returns_rows:
                return result.fetchall()
            return result.rowcount
    
    def get_databases(self) -> List[str]:
        """Get list of databases - must be implemented by subclass"""
        raise NotImplementedError
    
    def get_tables(self, database: str = None) -> List[str]:
        """Get list of tables in database"""
        inspector = inspect(self.engine)
        return inspector.get_table_names()
    
    def get_table_structure(self, table_name: str) -> Dict[str, Any]:
        """Get table structure details"""
        inspector = inspect(self.engine)
        
        columns = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        indexes = inspector.get_indexes(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)
        
        return {
            "columns": columns,
            "primary_keys": pk_constraint.get('constrained_columns', []),
            "indexes": indexes,
            "foreign_keys": foreign_keys
        }