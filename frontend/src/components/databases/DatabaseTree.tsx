import React, { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ChevronRight, ChevronDown, Database, Table } from 'lucide-react';
import { useAppStore } from '../../store/appStore';
import { databaseAPI, tableAPI } from '../../api/endpoints';
import { Loading } from '../common/Loading';
import clsx from 'clsx';

export const DatabaseTree: React.FC = () => {
  const selectedConnection = useAppStore((state) => state.selectedConnection);
  const databases = useAppStore((state) => state.databases);
  const setDatabases = useAppStore((state) => state.setDatabases);
  const selectedDatabase = useAppStore((state) => state.selectedDatabase);
  const selectDatabase = useAppStore((state) => state.selectDatabase);
  const tables = useAppStore((state) => state.tables);
  const setTables = useAppStore((state) => state.setTables);
  const selectedTable = useAppStore((state) => state.selectedTable);
  const selectTable = useAppStore((state) => state.selectTable);

  const { data: databasesData, isLoading: loadingDatabases } = useQuery({
    queryKey: ['databases', selectedConnection?.connection_id],
    queryFn: () => databaseAPI.list(selectedConnection!.connection_id).then(res => res.data),
    enabled: !!selectedConnection,
  });

  const { data: tablesData, isLoading: loadingTables } = useQuery({
    queryKey: ['tables', selectedConnection?.connection_id, selectedDatabase],
    queryFn: () => tableAPI.list(selectedConnection!.connection_id).then(res => res.data),
    enabled: !!selectedConnection && !!selectedDatabase,
  });

  useEffect(() => {
    if (databasesData) {
      setDatabases(databasesData);
    }
  }, [databasesData, setDatabases]);

  useEffect(() => {
    if (tablesData) {
      setTables(tablesData);
    }
  }, [tablesData, setTables]);

  const handleDatabaseClick = (dbName: string) => {
    if (selectedDatabase === dbName) {
      selectDatabase(null);
      setTables([]);
    } else {
      selectDatabase(dbName);
    }
  };

  const handleTableClick = (tableName: string) => {
    selectTable(tableName);
  };

  if (loadingDatabases) {
    return <Loading text="Loading databases..." />;
  }

  if (!databases || databases.length === 0) {
    return (
      <div className="text-sm text-gray-500 text-center py-4">
        No databases found
      </div>
    );
  }

  return (
    <div className="space-y-1">
      {databases.map((db) => (
        <div key={db.name}>
          {/* Database Item */}
          <div
            onClick={() => handleDatabaseClick(db.name)}
            className={clsx(
              'flex items-center gap-2 px-2 py-1.5 rounded cursor-pointer hover:bg-gray-100 transition-colors',
              {
                'bg-indigo-50': selectedDatabase === db.name,
              }
            )}
          >
            {selectedDatabase === db.name ? (
              <ChevronDown className="w-4 h-4 text-gray-500" />
            ) : (
              <ChevronRight className="w-4 h-4 text-gray-500" />
            )}
            <Database className="w-4 h-4 text-blue-600" />
            <span className="text-sm font-medium text-gray-900 flex-1">
              {db.name}
            </span>
            {db.tables_count !== undefined && (
              <span className="text-xs text-gray-500">{db.tables_count}</span>
            )}
          </div>

          {/* Tables List */}
          {selectedDatabase === db.name && (
            <div className="ml-6 mt-1 space-y-0.5">
              {loadingTables ? (
                <div className="text-xs text-gray-500 py-2">Loading tables...</div>
              ) : tables.length === 0 ? (
                <div className="text-xs text-gray-500 py-2">No tables</div>
              ) : (
                tables.map((table) => (
                  <div
                    key={table.name}
                    onClick={() => handleTableClick(table.name)}
                    className={clsx(
                      'flex items-center gap-2 px-2 py-1 rounded cursor-pointer hover:bg-gray-100 transition-colors',
                      {
                        'bg-indigo-100': selectedTable === table.name,
                      }
                    )}
                  >
                    <Table className="w-3.5 h-3.5 text-gray-500" />
                    <span className="text-sm text-gray-700">{table.name}</span>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};