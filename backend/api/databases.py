"""
Database operations API endpoints
"""
from fastapi import APIRouter, HTTPException
from models.schemas import DatabaseInfo
from services.connection_manager import connection_manager
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{connection_id}/list", response_model=List[DatabaseInfo])
async def list_databases(connection_id: str):
    """Get list of all databases for a connection"""
    try:
        service = connection_manager.get_connection(connection_id)
        if not service:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        databases = service.get_databases()
        
        # Get additional info for each database
        db_info_list = []
        for db_name in databases:
            try:
                size = service.get_database_size(db_name)
                table_count = service.get_table_count(db_name)
                db_info_list.append(DatabaseInfo(
                    name=db_name,
                    size=size,
                    tables_count=table_count
                ))
            except Exception as e:
                logger.warning(f"Could not get info for database {db_name}: {e}")
                db_info_list.append(DatabaseInfo(name=db_name))
        
        return db_info_list
        
    except Exception as e:
        logger.error(f"Failed to list databases: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{connection_id}/create")
async def create_database(connection_id: str, database_name: str):
    """Create a new database"""
    try:
        service = connection_manager.get_connection(connection_id)
        if not service:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        service.create_database(database_name)
        
        return {
            "status": "success",
            "message": f"Database '{database_name}' created successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to create database: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{connection_id}/{database_name}")
async def drop_database(connection_id: str, database_name: str):
    """Drop a database"""
    try:
        service = connection_manager.get_connection(connection_id)
        if not service:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        service.drop_database(database_name)
        
        return {
            "status": "success",
            "message": f"Database '{database_name}' dropped successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to drop database: {e}")
        raise HTTPException(status_code=400, detail=str(e))