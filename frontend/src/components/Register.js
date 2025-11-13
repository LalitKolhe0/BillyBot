import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../services/api"; 


const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

    const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = registerUser(email, password);
      

      if (!response.ok) {
        const errorData = response.json();
        throw new Error(errorData.message || 'Registration failed');
      }

      const data = response.json();
      console.log('Registration successful:', data);
      // Handle successful registration (e.g., redirect to login)
    } catch (err) {
      console.error('Error during registration:', err.message);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form
        onSubmit={handleRegister}
        className="bg-white p-8 rounded-lg shadow-md w-80"
      >
        <h2 className="text-2xl font-semibold mb-6 text-center">Register</h2>

        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 mb-4 border border-gray-300 rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 mb-4 border border-gray-300 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Confirm Password"
          className="w-full p-2 mb-6 border border-gray-300 rounded"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600"
        >
          Register
        </button>

        <p className="text-center mt-4 text-gray-600">
          Already have an account?
        </p>
        <button
          type="button"
          onClick={() => navigate("/login")}
          className="w-full bg-gray-200 text-gray-800 py-2 mt-2 rounded hover:bg-gray-300"
        >
          Login
        </button>
      </form>
    </div>
  );
};



export default Register;        
