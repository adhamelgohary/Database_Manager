import React from 'react';
import { Database, Trash2 } from 'lucide-react';
import { useAppStore } from '../../store/appStore';
import { DatabaseType } from '../../types';
import clsx from 'clsx';

export const ConnectionList: React.FC = () => {
  const connections = useAppStore((state) => state.connections);
  const selectedConnection = useAppStore((state) => state.selectedConnection);
  const selectConnection = useAppStore((state) => state.selectConnection);
  const removeConnection = useAppStore((state) => state.removeConnection);

  const getDbIcon = (type: DatabaseType) => {
    const colors = {
      [DatabaseType.MYSQL]: 'text-blue-600',
      [DatabaseType.POSTGRESQL]: 'text-purple-600',
      [DatabaseType.SQLITE]: 'text-green-600',
    };
    return colors[type] || 'text-gray-600';
  };

  const handleDelete = (e: React.MouseEvent, connectionId: string) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this connection?')) {
      removeConnection(connectionId);
      if (selectedConnection?.connection_id === connectionId) {
        selectConnection(null);
      }
    }
  };

  if (connections.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500 text-sm">
        No connections yet. Click "New Connection" to add one.
      </div>
    );
  }

  return (
    <div className="divide-y divide-gray-200">
      {connections.map((conn) => (
        <div
          key={conn.connection_id}
          onClick={() => selectConnection(conn)}
          className={clsx(
            'p-3 cursor-pointer hover:bg-gray-50 transition-colors group',
            {
              'bg-indigo-50 border-l-4 border-indigo-600': 
                selectedConnection?.connection_id === conn.connection_id,
            }
          )}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3 flex-1 min-w-0">
              <Database className={clsx('w-5 h-5 mt-0.5 flex-shrink-0', getDbIcon(conn.db_type))} />
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">{conn.name}</p>
                <p className="text-xs text-gray-500 truncate">
                  {conn.host}:{conn.port}
                </p>
                {conn.database && (
                  <p className="text-xs text-gray-400 truncate mt-0.5">
                    {conn.database}
                  </p>
                )}
              </div>
            </div>
            <button
              onClick={(e) => handleDelete(e, conn.connection_id)}
              className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-600 transition-all"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};