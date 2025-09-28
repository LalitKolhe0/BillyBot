import React from 'react';
import { Bot } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <Bot className="h-8 w-8 text-primary-600" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-900">
                BillyBot
              </h1>
              <p className="text-sm text-gray-500">
                Policy Chatbot (Ollama + Chroma)
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
