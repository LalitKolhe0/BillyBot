import React from "react";
import { useNavigate } from "react-router-dom";


const LogOut = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <button onClick={handleLogout}
      className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
      Log Out
    </button>
  );
};

export default LogOut;