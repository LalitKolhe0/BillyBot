import React, { useState } from 'react';
import Login from './Login';
import Signup from './Signup';

const AuthWrapper = () => {
  const [isLogin, setIsLogin] = useState(true);

  const toggleMode = () => {
    setIsLogin(!isLogin);
  };

  return (
    <div>
      {isLogin ? (
        <Login onToggleMode={toggleMode} />
      ) : (
        <Signup onToggleMode={toggleMode} />
      )}
    </div>
  );
};

export default AuthWrapper;
