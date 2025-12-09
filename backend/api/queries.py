"""
Query execution API endpoints (PHASE 2 Under <__DEV__>)
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from api.tables import logger
from services.connection_manager import connection_manager
from sqlalchemy import text
import logging

logger = logging.Logger(__name__)
router = APIRouter()


class QueryExecuteRequest(BaseModel):
    connection_id: str
    query: str
    limit : Optional[int] = 1000


class QueryResult(BaseModel):
    columns: List[str]
    rows : List[Dict]
    rows_count: int
    excution_time: float
    query_type: str

class TableDataRequest(BaseModel):
    connection_id : str
    
