import React, { useEffect, useState } from 'react';
import './Home.css';
import { useAuth } from './AuthContext';

const API_URL = 'http://127.0.0.1:8000/api/posts/';

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    fetch(API_URL)
      .then(res => res.json())
      .then(data => {
        // If paginated, data.results; else data
        setPosts(data.results || data);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load posts.');
        setLoading(false);
      });
  }, []);

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
          {loading && <div className="posts-loading">Loading posts...</div>}
          {error && <div className="posts-error">{error}</div>}
          {!loading && !error && posts.length === 0 && <div className="posts-empty">No posts yet.</div>}
          <div className="posts-list">
            {posts.map(post => (
              <div className="post-card" key={post.id}>
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