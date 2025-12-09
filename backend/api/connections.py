"""
Connection management API endpoints
"""
from fastapi import APIRouter, HTTPException
from models.schemas import (
    ConnectionCreate, ConnectionTest, ConnectionResponse
)
from services.connection_manager import connection_manager
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/test", response_model=ConnectionResponse)
async def test_connection(connection: ConnectionTest):
    """Test a database connection without saving it"""
    try:
        # Create temporary connection
        temp_id = "temp_test"
        service = connection_manager.create_connection(
            connection_id=temp_id,
            db_type=connection.db_type,
            host=connection.host,
            port=connection.port,
            username=connection.username,
            password=connection.password,
            database=connection.database
        )
        
        # Test it
        is_connected = service.test_connection()
        
        # Clean up
        connection_manager.close_connection(temp_id)
        
        if is_connected:
            return ConnectionResponse(
                status="success",
                message="Connection successful"
            )
        else:
            raise HTTPException(status_code=400, detail="Connection test failed")
            
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create", response_model=ConnectionResponse)
async def create_connection(connection: ConnectionCreate):
    """Create and save a new database connection"""
    try:
        service = connection_manager.create_connection(
            connection_id=connection.connection_id,
            db_type=connection.db_type,
            host=connection.host,
            port=connection.port,
            username=connection.username,
            password=connection.password,
            database=connection.database
        )
        
        return ConnectionResponse(
            status="success",
            message="Connection created successfully",
            connection_id=connection.connection_id
        )
        
    except Exception as e:
        logger.error(f"Failed to create connection: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{connection_id}", response_model=ConnectionResponse)
async def close_connection(connection_id: str):
    """Close a database connection"""
    try:
        connection_manager.close_connection(connection_id)
        return ConnectionResponse(
            status="success",
            message="Connection closed"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Connection not found")

@router.get("/{connection_id}/status")
async def get_connection_status(connection_id: str):
    """Check if connection is active"""
    service = connection_manager.get_connection(connection_id)
    if not service:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    is_active = service.test_connection()
    return {
        "connection_id": connection_id,
        "active": is_active
    }