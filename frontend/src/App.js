import React, { useState } from 'react';
import Header from './components/Header';
import SettingsPanel from './components/SettingsPanel';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import { SettingsProvider } from './context/SettingsContext';

function App() {
  const [activeTab, setActiveTab] = useState('upload');

  return (
    <SettingsProvider>
      <div className="min-h-screen bg-gray-50">
        <Header />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Settings Sidebar */}
            <div className="lg:col-span-1">
              <SettingsPanel />
            </div>
            
            {/* Main Content */}
            <div className="lg:col-span-3">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                {/* Tab Navigation */}
                <div className="border-b border-gray-200">
                  <nav className="flex space-x-8 px-6" aria-label="Tabs">
                    <button
                      onClick={() => setActiveTab('upload')}
                      className={`py-4 px-1 border-b-2 font-medium text-sm ${
                        activeTab === 'upload'
                          ? 'border-primary-500 text-primary-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      📄 Upload PDFs
                    </button>
                    <button
                      onClick={() => setActiveTab('chat')}
                      className={`py-4 px-1 border-b-2 font-medium text-sm ${
                        activeTab === 'chat'
                          ? 'border-primary-500 text-primary-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      💬 Ask Questions
                    </button>
                  </nav>
                </div>

                {/* Tab Content */}
                <div className="p-6">
                  {activeTab === 'upload' && <FileUpload />}
                  {activeTab === 'chat' && <ChatInterface />}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </SettingsProvider>
  );
}

export default App;
