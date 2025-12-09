import { create } from 'zustand';
import type { Connection, DatabaseInfo, TableInfo } from '../types';

interface AppState {
  connections: Connection[];
  selectedConnection: Connection | null;
  databases: DatabaseInfo[];
  selectedDatabase: string | null;
  tables: TableInfo[];
  selectedTable: string | null;
  sidebarOpen: boolean;

  setConnections: (connections: Connection[]) => void;
  addConnection: (connection: Connection) => void;
  removeConnection: (connectionId: string) => void;
  selectConnection: (connection: Connection | null) => void;
  
  setDatabases: (databases: DatabaseInfo[]) => void;
  selectDatabase: (database: string | null) => void;
  
  setTables: (tables: TableInfo[]) => void;
  selectTable: (table: string | null) => void;
  
  toggleSidebar: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  connections: JSON.parse(localStorage.getItem('connections') || '[]'),
  selectedConnection: null,
  databases: [],
  selectedDatabase: null,
  tables: [],
  selectedTable: null,
  sidebarOpen: true,

  setConnections: (connections) => {
    localStorage.setItem('connections', JSON.stringify(connections));
    set({ connections });
  },
  
  addConnection: (connection) =>
    set((state) => {
      const newConnections = [...state.connections, connection];
      localStorage.setItem('connections', JSON.stringify(newConnections));
      return { connections: newConnections };
    }),
  
  removeConnection: (connectionId) =>
    set((state) => {
      const newConnections = state.connections.filter(
        (c) => c.connection_id !== connectionId
      );
      localStorage.setItem('connections', JSON.stringify(newConnections));
      return { connections: newConnections };
    }),
  
  selectConnection: (connection) => 
    set({ 
      selectedConnection: connection,
      databases: [],
      selectedDatabase: null,
      tables: [],
      selectedTable: null
    }),
  
  setDatabases: (databases) => set({ databases }),
  selectDatabase: (database) => set({ selectedDatabase: database, tables: [], selectedTable: null }),
  
  setTables: (tables) => set({ tables }),
  selectTable: (table) => set({ selectedTable: table }),
  
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}));