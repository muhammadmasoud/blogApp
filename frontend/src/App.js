import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Configure axios base URL
axios.defaults.baseURL = 'http://127.0.0.1:8000';

function App() {
  const [posts, setPosts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [signupForm, setSignupForm] = useState({ username: '', email: '', password: '' });
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  // Fetch posts on component mount
  useEffect(() => {
    fetchPosts();
    fetchCategories();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await axios.get('/posts/');
      setPosts(response.data.results || response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch posts');
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get('/categories/');
      setCategories(response.data);
    } catch (err) {
      console.error('Failed to fetch categories:', err);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/login/', loginForm);
      localStorage.setItem('token', response.data.access);
      setUser(response.data.user);
      setShowLogin(false);
      setLoginForm({ username: '', password: '' });
    } catch (err) {
      setError('Login failed');
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/signup/', signupForm);
      localStorage.setItem('token', response.data.access);
      setUser(response.data.user);
      setShowSignup(false);
      setSignupForm({ username: '', email: '', password: '' });
    } catch (err) {
      setError('Signup failed');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Blog Application</h1>
        <div className="auth-buttons">
          {!user ? (
            <>
              <button onClick={() => setShowLogin(true)}>Login</button>
              <button onClick={() => setShowSignup(true)}>Signup</button>
            </>
          ) : (
            <div className="user-info">
              <span>Welcome, {user.username}!</span>
              <button onClick={handleLogout}>Logout</button>
            </div>
          )}
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      {/* Login Modal */}
      {showLogin && (
        <div className="modal">
          <div className="modal-content">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
              <input
                type="text"
                placeholder="Username"
                value={loginForm.username}
                onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
              />
              <input
                type="password"
                placeholder="Password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
              />
              <button type="submit">Login</button>
              <button type="button" onClick={() => setShowLogin(false)}>Cancel</button>
            </form>
          </div>
        </div>
      )}

      {/* Signup Modal */}
      {showSignup && (
        <div className="modal">
          <div className="modal-content">
            <h2>Signup</h2>
            <form onSubmit={handleSignup}>
              <input
                type="text"
                placeholder="Username"
                value={signupForm.username}
                onChange={(e) => setSignupForm({...signupForm, username: e.target.value})}
              />
              <input
                type="email"
                placeholder="Email"
                value={signupForm.email}
                onChange={(e) => setSignupForm({...signupForm, email: e.target.value})}
              />
              <input
                type="password"
                placeholder="Password"
                value={signupForm.password}
                onChange={(e) => setSignupForm({...signupForm, password: e.target.value})}
              />
              <button type="submit">Signup</button>
              <button type="button" onClick={() => setShowSignup(false)}>Cancel</button>
            </form>
          </div>
        </div>
      )}

      <main className="App-main">
        <div className="categories">
          <h2>Categories</h2>
          <div className="category-list">
            {categories.map(category => (
              <div key={category.id} className="category-item">
                {category.name}
              </div>
            ))}
          </div>
        </div>

        <div className="posts">
          <h2>Blog Posts</h2>
          <div className="post-list">
            {posts.map(post => (
              <div key={post.id} className="post-item">
                <h3>{post.title}</h3>
                <p className="post-meta">
                  By {post.author?.username || 'Anonymous'} | 
                  {new Date(post.publish_date).toLocaleDateString()}
                </p>
                <p className="post-content">{post.content}</p>
                {post.image && (
                  <img src={`http://127.0.0.1:8000${post.image}`} alt={post.title} className="post-image" />
                )}
                <div className="post-actions">
                  <button>Like</button>
                  <button>Comment</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
