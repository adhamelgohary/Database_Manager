"""
Manages active database connections
"""
from services.mysql_service import MySQLService
from services.postgresql_service import PostgreSQLService
from services.sqlite_service import SQLiteService
from models.schemas import DatabaseType
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, any] = {}
    
    def create_connection_string(self, db_type: DatabaseType, host: str, port: int, 
                                  username: str, password: str, database: str = None) -> str:
        """Create database connection string"""
        
        if db_type == DatabaseType.sqlite:
            return f"sqlite:///{database}"
        
        # Set default ports
        if not port:
            port = 3306 if db_type == DatabaseType.mysql else 5432
        
        # Database string (optional for initial connection)
        db_part = f"/{database}" if database else ""
        
        if db_type == DatabaseType.mysql:
            return f"mysql+pymysql://{username}:{password}@{host}:{port}{db_part}"
        elif db_type == DatabaseType.postgresql:
            return f"postgresql+psycopg2://{username}:{password}@{host}:{port}{db_part}"
        
        raise ValueError(f"Unsupported database type: {db_type}")
    
    def get_service_class(self, db_type: DatabaseType):
        """Get appropriate service class for database type"""
        services = {
            DatabaseType.mysql: MySQLService,
            DatabaseType.postgresql: PostgreSQLService,
            DatabaseType.sqlite: SQLiteService
        }
        return services.get(db_type)
    
    def create_connection(self, connection_id: str, db_type: DatabaseType, 
                          host: str, port: int, username: str, password: str, 
                          database: str = None):
        """Create and store a new connection"""
        try:
            # Create connection string
            conn_string = self.create_connection_string(
                db_type, host, port, username, password, database
            )
            
            # Get service class
            service_class = self.get_service_class(db_type)
            if not service_class:
                raise ValueError(f"Unsupported database type: {db_type}")
            
            # Create service instance
            service = service_class(conn_string)
            service.connect()
            
            # Store connection
            self.connections[connection_id] = {
                'service': service,
                'db_type': db_type,
                'host': host,
                'port': port,
                'username': username,
                'database': database
            }
            
            logger.info(f"Connection {connection_id} created successfully")
            return service
            
        except Exception as e:
            logger.error(f"Failed to create connection {connection_id}: {e}")
            raise
    
    def get_connection(self, connection_id: str) -> Optional[any]:
        """Get an existing connection"""
        conn = self.connections.get(connection_id)
        return conn['service'] if conn else None
    
    def close_connection(self, connection_id: str):
        """Close and remove a connection"""
        if connection_id in self.connections:
            conn = self.connections[connection_id]
            conn['service'].disconnect()
            del self.connections[connection_id]
            logger.info(f"Connection {connection_id} closed")
    
    def close_all(self):
        """Close all connections"""
        for conn_id in list(self.connections.keys()):
            self.close_connection(conn_id)

# Global connection manager instance
connection_manager = ConnectionManager()