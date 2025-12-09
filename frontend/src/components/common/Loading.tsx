import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingProps {
  text?: string;
}

export const Loading: React.FC<LoadingProps> = ({ text = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
      <p className="mt-2 text-sm text-gray-600">{text}</p>
    </div>
  );
};