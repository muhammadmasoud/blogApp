import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import './Navbar.css';
import Footer from './Footer';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-center">
          <Link to="/" className="navbar-logo">Blogify</Link>
          {user ? (
            <>
              <span className="navbar-username">{user.username}</span>
              {user.is_admin && (
                <a href="http://127.0.0.1:8000/admin" className="navbar-link">Manage Blog</a>
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
      <Footer />
    </>
  );
} 