import React from 'react';
import { Bot, Sun, Moon } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const { isDark, toggle } = useTheme();
  const navigate = useNavigate();

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <Bot className="h-8 w-8 text-primary-600" />
            </div>
            <div>
              <button 
                onClick={() => navigate('/')}
                className="text-xl font-semibold text-gray-900 dark:text-white transition-colors hover:text-primary-600 dark:hover:text-primary-400"
              >
                BillyBot
              </button>
              <p className="text-sm text-gray-500 dark:text-gray-400 transition-colors">
                Knowledge Base Chatbot (Ollama + Chroma)
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {localStorage.getItem("isLoggedIn") && (
              <button
                onClick={() => {
                  localStorage.removeItem("isLoggedIn");
                  navigate('/');
                }}
                className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
              >
                Logout
              </button>
            )}
            <button
              onClick={toggle}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-300 transition-colors"
              aria-label="Toggle theme"
            >
              {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
