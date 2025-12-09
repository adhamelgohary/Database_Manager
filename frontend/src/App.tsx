import React from 'react';
import { Header } from './components/layout/Header';
import { Sidebar } from './components/layout/Sidebar';
import { TableViewer } from './components/tables/TableViewer';
import { EmptyState } from './components/common/EmptyState';
import { useAppStore } from './store/appStore';
import { Database } from 'lucide-react';

function App() {
  const selectedConnection = useAppStore((state) => state.selectedConnection);

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <Header />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar />

        <main className="flex-1 overflow-hidden">
          {!selectedConnection ? (
            <div className="h-full flex items-center justify-center">
              <EmptyState
                icon={<Database className="w-20 h-20" />}
                title="No Connection Selected"
                description="Create a new connection or select an existing one from the sidebar"
              />
            </div>
          ) : (
            <TableViewer />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;