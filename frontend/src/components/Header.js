import React, { useState } from 'react';
import { Bot, Sun, Moon } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';
import Login from './Login';

const Header = () => {
  const { isDark, toggle } = useTheme();
  const { logout, user } = useAuth();
  const [showLogin, setShowLogin] = useState(false);

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <Bot className="h-8 w-8 text-primary-600" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white transition-colors">
                BillyBot
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 transition-colors">
                Knowledge Base Chatbot (Ollama + Chroma)
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  Welcome, {user.username}
                </span>
                <button
                  onClick={logout}
                  className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
                >
                  Logout
                </button>
              </>
            ) : (
              <button
                onClick={() => setShowLogin(true)}
                className="text-sm bg-primary-500 text-white px-3 py-1 rounded hover:bg-primary-700 transition-colors"
              >
                Login
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

      {showLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-96 max-w-md mx-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Login</h2>
              <button
                onClick={() => setShowLogin(false)}
                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
              >
                ✕
              </button>
            </div>
            <Login onClose={() => setShowLogin(false)} />
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
