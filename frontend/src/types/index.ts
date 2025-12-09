
export enum DatabaseType {
  MYSQL = 'mysql',
  POSTGRESQL = 'postgresql',
  SQLITE = 'sqlite'
}

export interface Connection {
  connection_id: string;
  name: string;
  db_type: DatabaseType;
  host: string;
  port: number;
  username?: string;
  database?: string;
}

export interface ConnectionCreate {
  connection_id: string;
  name: string;
  db_type: DatabaseType;
  host: string;
  port?: number;
  username?: string;
  password?: string;
  database?: string;
  ssl?: boolean;
}

export interface ConnectionTest {
  db_type: DatabaseType;
  host: string;
  port?: number;
  username?: string;
  password?: string;
  database?: string;
}

export interface DatabaseInfo {
  name: string;
  size?: string;
  tables_count?: number;
}

export interface TableInfo {
  name: string;
  row_count?: number;
  size?: string;
}

export interface ColumnInfo {
  name: string;
  type: string;
  nullable: boolean;
  key?: string;
  default?: string;
  extra?: string;
}

export interface TableStructure {
  columns: ColumnInfo[];
  primary_keys: string[];
  indexes: any[];
  foreign_keys: any[];
}