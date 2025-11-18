import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/api"; 


const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await loginUser(email, password);
      if (!response.access_token) {
        throw new Error('Login failed');
      }
      localStorage.setItem("token", response.access_token);   
      localStorage.setItem("isLoggedIn", "true");
      navigate("/app");
    } catch (error) {
      alert("Invalid credentials");
    }   
  };

  const handleRegister = (e) => {
    e.preventDefault();
    navigate("/register");
  };     

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <form
        onSubmit={handleLogin}
        className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md w-80"
      >
        <h2 className="text-2xl font-semibold mb-6 text-center text-gray-900 dark:text-white">Login</h2>
        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 mb-4 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 mb-6 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          Login
        </button>
                <p className="text-center mt-4 text-gray-600 dark:text-gray-400">Don't have an account?</p>
        <button
          type="button"
          onClick={handleRegister}
          className="w-full bg-gray-200 text-gray-800 py-2 mt-2 rounded hover:bg-gray-300"
        >
          Register
        </button>
      </form>
    </div>
  );
};




export default Login;
