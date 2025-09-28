import React from 'react';
import { Settings, Database, Cpu, FileText } from 'lucide-react';
import { useSettings } from '../context/SettingsContext';

const SettingsPanel = () => {
  const { settings, updateSetting } = useSettings();

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center space-x-2 mb-6">
        <Settings className="h-5 w-5 text-gray-600" />
        <h2 className="text-lg font-semibold text-gray-900">Settings</h2>
      </div>

      <div className="space-y-6">
        {/* Chroma Settings */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <Database className="h-4 w-4 text-gray-500" />
            <h3 className="text-sm font-medium text-gray-700">Chroma Database</h3>
          </div>
          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Persist Directory
              </label>
              <input
                type="text"
                value={settings.persistDir}
                onChange={(e) => updateSetting('persistDir', e.target.value)}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        {/* Model Settings */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <Cpu className="h-4 w-4 text-gray-500" />
            <h3 className="text-sm font-medium text-gray-700">Models</h3>
          </div>
          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Embedding Model
              </label>
              <input
                type="text"
                value={settings.embeddingModel}
                onChange={(e) => updateSetting('embeddingModel', e.target.value)}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                LLM Model
              </label>
              <input
                type="text"
                value={settings.llmModel}
                onChange={(e) => updateSetting('llmModel', e.target.value)}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        {/* Processing Settings */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <FileText className="h-4 w-4 text-gray-500" />
            <h3 className="text-sm font-medium text-gray-700">Processing</h3>
          </div>
          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Top-k Retrieved Chunks: {settings.topK}
              </label>
              <input
                type="range"
                min="1"
                max="10"
                value={settings.topK}
                onChange={(e) => updateSetting('topK', parseInt(e.target.value))}
                className="w-full"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Chunk Size (chars)
              </label>
              <input
                type="number"
                value={settings.chunkSize}
                onChange={(e) => updateSetting('chunkSize', parseInt(e.target.value))}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Chunk Overlap (chars)
              </label>
              <input
                type="number"
                value={settings.chunkOverlap}
                onChange={(e) => updateSetting('chunkOverlap', parseInt(e.target.value))}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPanel;
