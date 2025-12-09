"""
Table operations API endpoints
"""
from fastapi import APIRouter, HTTPException
from models.schemas import TableInfo, TableStructure, ColumnInfo
from services.connection_manager import connection_manager
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{connection_id}/list", response_model=List[TableInfo])
async def list_tables(connection_id: str):
    """Get list of all tables in current database"""
    try:
        service = connection_manager.get_connection(connection_id)
        if not service:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        tables = service.get_tables()
        
        # Return table info
        return [TableInfo(name=table) for table in tables]
        
    except Exception as e:
        logger.error(f"Failed to list tables: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{connection_id}/{table_name}/structure", response_model=TableStructure)
async def get_table_structure(connection_id: str, table_name: str):
    """Get table structure (columns, keys, indexes)"""
    try:
        service = connection_manager.get_connection(connection_id)
        if not service:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        structure = service.get_table_structure(table_name)
        
        # Convert to response model
        columns = [
            ColumnInfo(
                name=col['name'],
                type=str(col['type']),
                nullable=col.get('nullable', True),
                key=col.get('key'),
                default=str(col.get('default')) if col.get('default') is not None else None,
                extra=col.get('autoincrement')
            )
            for col in structure['columns']
        ]
        
        return TableStructure(
            columns=columns,
            primary_keys=structure['primary_keys'],
            indexes=structure['indexes'],
            foreign_keys=structure['foreign_keys']
        )
        
    except Exception as e:
        logger.error(f"Failed to get table structure: {e}")
        raise HTTPException(status_code=500, detail=str(e))