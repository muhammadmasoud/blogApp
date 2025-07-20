import React from 'react';
import './Home.css';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Home({ posts, loading, error }) {
  const [search, setSearch] = React.useState('');
  const [searching, setSearching] = React.useState(false);
  const { user } = useAuth();
  const navigate = useNavigate();

  // Search logic can be implemented to call setPage(1) and filter at the App level if needed

  const handleSearch = (e) => {
    e.preventDefault();
    setSearching(true);
    // Optionally, trigger a search at the App level
    setSearching(false);
  };

  return (
    <div className="home-hero">
      {!user && (
        <div className="home-content" style={{ position: 'absolute', left: '50%', top: '50%', transform: 'translate(-50%, -50%)', zIndex: 2 }}>
          <h1 className="home-title">Welcome to <span>Blogify</span></h1>
          <p className="home-subtitle">Share your stories, connect with others, and explore a world of ideas.</p>
          <div className="home-actions">
            <a href="/register" className="home-btn home-btn-primary">Get Started</a>
            <a href="/login" className="home-btn home-btn-secondary">Sign In</a>
          </div>
        </div>
      )}
      <div className="home-bg-blob"></div>
      {user && (
        <div className="posts-section">
          <h2 className="posts-title">Latest Posts</h2>
          {/* Search Bar (optional, not functional now) */}
          <form className="posts-search-bar" onSubmit={handleSearch} style={{ marginBottom: 24 }}>
            <input
              type="text"
              placeholder="Search by title or tag..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{ padding: 8, width: 250, borderRadius: 4, border: '1px solid #ccc', marginRight: 8 }}
            />
            <button type="submit" style={{ padding: '8px 16px', borderRadius: 4, border: 'none', background: '#007bff', color: '#fff' }} disabled={searching}>
              {searching ? 'Searching...' : 'Search'}
            </button>
          </form>
          {loading && <div className="posts-loading">Loading posts...</div>}
          {error && <div className="posts-error">{error}</div>}
          {!loading && !error && posts.length === 0 && <div className="posts-empty">No posts yet.</div>}
          <div className="posts-list">
            {posts.map(post => (
              <div
                className="post-card"
                key={post.id}
                style={{ cursor: 'pointer' }}
                onClick={() => navigate(`/post/${post.id}`)}
              >
                <h3 className="post-title">{post.title}</h3>
                <div className="post-meta">
                  <span>By {post.author?.username || 'Unknown'}</span>
                  <span> | {new Date(post.publish_date || post.created_at).toLocaleDateString()}</span>
                </div>
                <p className="post-content">{post.content?.slice(0, 180)}{post.content && post.content.length > 180 ? '...' : ''}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 