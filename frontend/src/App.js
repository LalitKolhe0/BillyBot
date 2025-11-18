import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "./components/Login";
import Register from "./components/Register";
import MainApp from './components/MainApp';
import Header from "./components/Header";
import { ThemeProvider } from './context/ThemeContext';

const PrivateRoute = ({ children }) => {
  const isLoggedIn = localStorage.getItem("isLoggedIn");
  return isLoggedIn ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Header />
          <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/app" element={<PrivateRoute><MainApp /></PrivateRoute>} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;