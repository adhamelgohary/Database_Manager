import apiClient from './client';
import type {
    ConnectionTest,
    ConnectionCreate,
    DatabaseInfo,
    TableInfo,
    TableStructure
} from '../types';

export const connectionAPI = {
  test: (data: ConnectionTest) => 
    apiClient.post('/connections/test', data),
  
  create: (data: ConnectionCreate) => 
    apiClient.post('/connections/create', data),
  
  close: (connectionId: string) => 
    apiClient.delete(`/connections/${connectionId}`),
  
  getStatus: (connectionId: string) => 
    apiClient.get(`/connections/${connectionId}/status`),
};

export const databaseAPI = {
  list: (connectionId: string) => 
    apiClient.get<DatabaseInfo[]>(`/databases/${connectionId}/list`),
  
  create: (connectionId: string, databaseName: string) => 
    apiClient.post(`/databases/${connectionId}/create`, null, {
      params: { database_name: databaseName }
    }),
  
  drop: (connectionId: string, databaseName: string) => 
    apiClient.delete(`/databases/${connectionId}/${databaseName}`),
};

export const tableAPI = {
  list: (connectionId: string) => 
    apiClient.get<TableInfo[]>(`/tables/${connectionId}/list`),
  
  getStructure: (connectionId: string, tableName: string) => 
    apiClient.get<TableStructure>(`/tables/${connectionId}/${tableName}/structure`),
};