import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import './Navbar.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/" className="navbar-logo">Blogify</Link>
        <Link to="/" className="navbar-link">Home</Link>
      </div>
      <div className="navbar-right">
        {user ? (
          <>
            <span className="navbar-username">👤 {user.username}</span>
            {user.is_admin && (
              <a href="http://localhost:8000/admin" className="navbar-link" target="_blank" rel="noopener noreferrer">Manage Blog</a>
            )}
            <button className="navbar-logout" onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="navbar-link">Login</Link>
            <Link to="/register" className="navbar-link">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
} 