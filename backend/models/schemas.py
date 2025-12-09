"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class DatabaseType(str, Enum):
    mysql = "mysql"
    postgresql = "postgresql"
    sqlite = "sqlite"

class ConnectionCreate(BaseModel):
    connection_id: str
    name: str
    db_type: DatabaseType
    host: str = "localhost"
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    ssl: bool = False

class ConnectionTest(BaseModel):
    db_type: DatabaseType
    host: str = "localhost"
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None

class ConnectionResponse(BaseModel):
    status: str
    message: str
    connection_id: Optional[str] = None

class DatabaseInfo(BaseModel):
    name: str
    size: Optional[str] = None
    tables_count: Optional[int] = None

class TableInfo(BaseModel):
    name: str
    row_count: Optional[int] = None
    size: Optional[str] = None

class ColumnInfo(BaseModel):
    name: str
    type: str
    nullable: bool
    key: Optional[str] = None
    default: Optional[str] = None
    extra: Optional[str] = None

class TableStructure(BaseModel):
    columns: List[ColumnInfo]
    primary_keys: List[str]
    indexes: List[Dict[str, Any]]
    foreign_keys: List[Dict[str, Any]]
    