import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useAppStore } from '../../store/appStore';
import { tableAPI } from '../../api/endpoints';
import { Loading } from '../common/Loading';
import { EmptyState } from '../common/EmptyState';
import { Table } from 'lucide-react';

export const TableViewer: React.FC = () => {
  const selectedConnection = useAppStore((state) => state.selectedConnection);
  const selectedTable = useAppStore((state) => state.selectedTable);

  const { data: structure, isLoading } = useQuery({
    queryKey: ['table-structure', selectedConnection?.connection_id, selectedTable],
    queryFn: () => 
      tableAPI.getStructure(selectedConnection!.connection_id, selectedTable!).then(res => res.data),
    enabled: !!selectedConnection && !!selectedTable,
  });

  if (!selectedTable) {
    return (
      <EmptyState
        icon={<Table className="w-16 h-16" />}
        title="No Table Selected"
        description="Select a table from the sidebar to view its structure"
      />
    );
  }

  if (isLoading) {
    return <Loading text="Loading table structure..." />;
  }

  if (!structure) {
    return (
      <EmptyState
        title="Failed to Load Table"
        description="Could not load the table structure"
      />
    );
  }

  return (
    <div className="h-full overflow-auto">
      <div className="p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{selectedTable}</h2>
          <p className="text-sm text-gray-500">
            {structure.columns.length} columns • {structure.primary_keys.length} primary keys • {structure.indexes.length} indexes
          </p>
        </div>

        {/* Columns Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
            <h3 className="text-sm font-semibold text-gray-900">Columns</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nullable
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Key
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Default
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Extra
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {structure.columns.map((column) => (
                  <tr key={column.name} className="hover:bg-gray-50">
                    <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                      {column.name}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                      <code className="px-2 py-1 bg-gray-100 rounded text-xs">
                        {column.type}
                      </code>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                      {column.nullable ? (
                        <span className="text-green-600">Yes</span>
                      ) : (
                        <span className="text-red-600">No</span>
                      )}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm">
                      {column.key && (
                        <span className="px-2 py-1 bg-indigo-100 text-indigo-800 rounded text-xs font-medium">
                          {column.key}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                      {column.default || '-'}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                      {column.extra || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Primary Keys */}
        {structure.primary_keys.length > 0 && (
          <div className="mt-6 bg-white rounded-lg shadow p-4">
            <h3 className="text-sm font-semibold text-gray-900 mb-2">Primary Keys</h3>
            <div className="flex flex-wrap gap-2">
              {structure.primary_keys.map((key) => (
                <span
                  key={key}
                  className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm"
                >
                  {key}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Indexes */}
        {structure.indexes.length > 0 && (
          <div className="mt-6 bg-white rounded-lg shadow p-4">
            <h3 className="text-sm font-semibold text-gray-900 mb-3">Indexes</h3>
            <div className="space-y-2">
              {structure.indexes.map((index, idx) => (
                <div
                  key={idx}
                  className="p-3 bg-gray-50 rounded border border-gray-200"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-sm text-gray-900">
                      {index.name}
                    </span>
                    {index.unique && (
                      <span className="px-2 py-0.5 bg-green-100 text-green-800 rounded text-xs">
                        Unique
                      </span>
                    )}
                  </div>
                  <div className="mt-1 text-xs text-gray-600">
                    Columns: {index.column_names?.join(', ') || 'N/A'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Foreign Keys */}
        {structure.foreign_keys.length > 0 && (
          <div className="mt-6 bg-white rounded-lg shadow p-4">
            <h3 className="text-sm font-semibold text-gray-900 mb-3">Foreign Keys</h3>
            <div className="space-y-2">
              {structure.foreign_keys.map((fk, idx) => (
                <div
                  key={idx}
                  className="p-3 bg-gray-50 rounded border border-gray-200"
                >
                  <div className="text-sm">
                    <span className="font-medium text-gray-900">
                      {fk.constrained_columns?.join(', ')}
                    </span>
                    <span className="text-gray-500 mx-2">→</span>
                    <span className="text-gray-700">
                      {fk.referred_table}.{fk.referred_columns?.join(', ')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};