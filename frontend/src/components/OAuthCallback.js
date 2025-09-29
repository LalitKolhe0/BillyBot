import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { CheckCircle, XCircle, Loader } from 'lucide-react';

const OAuthCallback = () => {
  const [status, setStatus] = useState('processing');
  const [message, setMessage] = useState('Processing authentication...');
  const { login } = useAuth();

  useEffect(() => {
    const handleOAuthCallback = async () => {
      try {
        // Get the URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        const provider = window.location.pathname.split('/').pop(); // Extract provider from URL

        if (!code) {
          throw new Error('No authorization code received');
        }

        // Determine the callback endpoint based on the provider
        let callbackEndpoint;
        switch (provider) {
          case 'google':
            callbackEndpoint = '/auth/callback/google';
            break;
          case 'facebook':
            callbackEndpoint = '/auth/callback/facebook';
            break;
          case 'apple':
            callbackEndpoint = '/auth/callback/apple';
            break;
          default:
            throw new Error('Unknown OAuth provider');
        }

        // Call the backend callback endpoint
        const response = await fetch(`http://localhost:8000${callbackEndpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ code }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Authentication failed');
        }

        const data = await response.json();
        
        // Store the token and update auth context
        localStorage.setItem('token', data.access_token);
        
        // Get user info and update context
        const userResponse = await fetch('http://localhost:8000/me', {
          headers: {
            'Authorization': `Bearer ${data.access_token}`,
          },
        });
        
        if (userResponse.ok) {
          const userData = await userResponse.json();
          setStatus('success');
          setMessage('Authentication successful! Redirecting...');
          
          // Redirect to main app after a short delay
          setTimeout(() => {
            window.location.href = '/';
          }, 2000);
        } else {
          throw new Error('Failed to get user information');
        }

      } catch (error) {
        console.error('OAuth callback error:', error);
        setStatus('error');
        setMessage(error.message || 'Authentication failed');
      }
    };

    handleOAuthCallback();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          {status === 'processing' && (
            <>
              <Loader className="h-12 w-12 mx-auto mb-4 text-primary-600 animate-spin" />
              <h2 className="text-2xl font-bold text-gray-900">Processing Authentication</h2>
              <p className="mt-2 text-gray-600">{message}</p>
            </>
          )}
          
          {status === 'success' && (
            <>
              <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-600" />
              <h2 className="text-2xl font-bold text-gray-900">Success!</h2>
              <p className="mt-2 text-gray-600">{message}</p>
            </>
          )}
          
          {status === 'error' && (
            <>
              <XCircle className="h-12 w-12 mx-auto mb-4 text-red-600" />
              <h2 className="text-2xl font-bold text-gray-900">Authentication Failed</h2>
              <p className="mt-2 text-gray-600">{message}</p>
              <div className="mt-6">
                <button
                  onClick={() => window.location.href = '/'}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Return to Login
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default OAuthCallback;
