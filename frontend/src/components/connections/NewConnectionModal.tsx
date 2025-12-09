import React, { useState } from 'react';
import { Modal } from '../common/Modal';
import { Input } from '../common/Input';
import { Button } from '../common/Button';
import { DatabaseType, type ConnectionCreate } from '../../types';
import { connectionAPI } from '../../api/endpoints';
import { useAppStore } from '../../store/appStore';

interface NewConnectionModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const NewConnectionModal: React.FC<NewConnectionModalProps> = ({
  isOpen,
  onClose,
}) => {
  const addConnection = useAppStore((state) => state.addConnection);
  
  const [formData, setFormData] = useState({
    name: '',
    db_type: DatabaseType.MYSQL,
    host: 'localhost',
    port: 3306,
    username: 'root',
    password: '',
    database: '',
  });

  const [loading, setLoading] = useState(false);
  const [testing, setTesting] = useState(false);
  const [error, setError] = useState('');
  const [testSuccess, setTestSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'port' ? parseInt(value) || 0 : value,
    }));
    setError('');
    setTestSuccess(false);
  };

  const handleDbTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const dbType = e.target.value as DatabaseType;
    setFormData((prev) => ({
      ...prev,
      db_type: dbType,
      port: dbType === DatabaseType.MYSQL ? 3306 : dbType === DatabaseType.POSTGRESQL ? 5432 : 0,
    }));
  };

  const handleTest = async () => {
    setTesting(true);
    setError('');
    setTestSuccess(false);

    try {
      await connectionAPI.test({
        db_type: formData.db_type,
        host: formData.host,
        port: formData.port,
        username: formData.username,
        password: formData.password,
        database: formData.database || undefined,
      });
      setTestSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Connection test failed');
    } finally {
      setTesting(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const connectionData: ConnectionCreate = {
        connection_id: `conn_${Date.now()}`,
        name: formData.name,
        db_type: formData.db_type,
        host: formData.host,
        port: formData.port,
        username: formData.username,
        password: formData.password,
        database: formData.database || undefined,
      };

      await connectionAPI.create(connectionData);

      // Add to store (without password)
      addConnection({
        connection_id: connectionData.connection_id,
        name: connectionData.name,
        db_type: connectionData.db_type,
        host: connectionData.host,
        port: connectionData.port,
        username: connectionData.username,
        database: connectionData.database,
      });

      onClose();
      
      // Reset form
      setFormData({
        name: '',
        db_type: DatabaseType.MYSQL,
        host: 'localhost',
        port: 3306,
        username: 'root',
        password: '',
        database: '',
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create connection');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="New Connection" size="md">
      <form onSubmit={handleSubmit}>
        <Input
          label="Connection Name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="My Database"
          required
        />

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Database Type
          </label>
          <select
            name="db_type"
            value={formData.db_type}
            onChange={handleDbTypeChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value={DatabaseType.MYSQL}>MySQL</option>
            <option value={DatabaseType.POSTGRESQL}>PostgreSQL</option>
            <option value={DatabaseType.SQLITE}>SQLite</option>
          </select>
        </div>

        {formData.db_type !== DatabaseType.SQLITE && (
          <>
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Host"
                name="host"
                value={formData.host}
                onChange={handleChange}
                required
              />
              <Input
                label="Port"
                name="port"
                type="number"
                value={formData.port}
                onChange={handleChange}
                required
              />
            </div>

            <Input
              label="Username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />

            <Input
              label="Password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
            />
          </>
        )}

        <Input
          label={formData.db_type === DatabaseType.SQLITE ? 'Database File Path' : 'Database (optional)'}
          name="database"
          value={formData.database}
          onChange={handleChange}
          placeholder={formData.db_type === DatabaseType.SQLITE ? '/path/to/database.db' : 'Leave empty to connect without selecting a database'}
        />

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">
            {error}
          </div>
        )}

        {testSuccess && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-sm text-green-600">
            ✓ Connection test successful!
          </div>
        )}

        <div className="flex justify-between gap-3">
          <Button
            type="button"
            variant="secondary"
            onClick={handleTest}
            disabled={testing || loading}
          >
            {testing ? 'Testing...' : 'Test Connection'}
          </Button>
          
          <div className="flex gap-3">
            <Button type="button" variant="ghost" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading || testing}>
              {loading ? 'Connecting...' : 'Connect'}
            </Button>
          </div>
        </div>
      </form>
    </Modal>
  );
};