import React, { useState } from 'react';
import { Menu, Plus } from 'lucide-react';
import { Button } from '../common/Button';
import { NewConnectionModal } from '../connections/NewConnectionModal';
import { useAppStore } from '../../store/appStore';

export const Header: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const toggleSidebar = useAppStore((state) => state.toggleSidebar);

  return (
    <>
      <header className="h-14 bg-indigo-600 text-white flex items-center justify-between px-4 shadow-md">
        <div className="flex items-center gap-3">
          <button
            onClick={toggleSidebar}
            className="p-2 hover:bg-indigo-700 rounded-lg transition-colors"
          >
            <Menu className="w-5 h-5" />
          </button>
          <h1 className="text-lg font-semibold">Database Manager</h1>
        </div>

        <Button
          size="sm"
          variant="secondary"
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          New Connection
        </Button>
      </header>

      <NewConnectionModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </>
  );
};