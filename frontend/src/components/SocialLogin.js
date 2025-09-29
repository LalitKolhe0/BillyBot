import React from 'react';
import { Chrome, Facebook, Apple } from 'lucide-react';

const SocialLogin = ({ onSocialLogin }) => {
  const handleGoogleLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/auth/google');
      const data = await response.json();
      window.location.href = data.auth_url;
    } catch (error) {
      console.error('Google login failed:', error);
    }
  };

  const handleFacebookLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/auth/facebook');
      const data = await response.json();
      window.location.href = data.auth_url;
    } catch (error) {
      console.error('Facebook login failed:', error);
    }
  };

  const handleAppleLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/auth/apple');
      const data = await response.json();
      window.location.href = data.auth_url;
    } catch (error) {
      console.error('Apple login failed:', error);
    }
  };

  return (
    <div className="space-y-3">
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-300" />
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-white text-gray-500">Or continue with</span>
        </div>
      </div>

      <div className="space-y-3">
        <button
          onClick={handleGoogleLogin}
          className="w-full flex justify-center items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <Chrome className="h-5 w-5 mr-2 text-red-500" />
          Continue with Google
        </button>

        <button
          onClick={handleFacebookLogin}
          className="w-full flex justify-center items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <Facebook className="h-5 w-5 mr-2 text-blue-600" />
          Continue with Facebook
        </button>

        <button
          onClick={handleAppleLogin}
          className="w-full flex justify-center items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <Apple className="h-5 w-5 mr-2 text-gray-900" />
          Continue with Apple
        </button>
      </div>
    </div>
  );
};

export default SocialLogin;
