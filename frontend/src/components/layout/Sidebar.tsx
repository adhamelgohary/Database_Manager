import React from 'react';
import { ConnectionList } from '../connections/ConnectionList';
import { DatabaseTree } from '../databases/DatabaseTree';
import { useAppStore } from '../../store/appStore';
import clsx from 'clsx';

export const Sidebar: React.FC = () => {
  const sidebarOpen = useAppStore((state) => state.sidebarOpen);
  const selectedConnection = useAppStore((state) => state.selectedConnection);

  return (
    <aside
      className={clsx(
        'bg-white border-r border-gray-200 transition-all duration-300',
        {
          'w-80': sidebarOpen,
          'w-0': !sidebarOpen,
        }
      )}
    >
      {sidebarOpen && (
        <div className="h-full flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <h2 className="font-semibold text-gray-900">Connections</h2>
          </div>

          <div className="flex-1 overflow-y-auto">
            <ConnectionList />
            
            {selectedConnection && (
              <div className="mt-4 border-t border-gray-200">
                <div className="p-4 bg-gray-50">
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">
                    Databases
                  </h3>
                  <DatabaseTree />
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </aside>
  );
};