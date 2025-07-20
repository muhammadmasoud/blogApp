import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

export default function CategoryPosts() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);
  const [category, setCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetch(`http://127.0.0.1:8000/api/posts/categories/${id}/`).then(res => res.json()),
      fetch('http://127.0.0.1:8000/posts/categories/').then(res => res.json()),
    ])
      .then(([postsData, categories]) => {
        setPosts(postsData.results || postsData);
        const cat = categories.find(c => c.id === parseInt(id));
        setCategory(cat);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load posts or category.');
        setLoading(false);
      });
  }, [id]);

  return (
    <div className="posts-section" style={{ maxWidth: 900, margin: '0 auto', marginTop: '3rem', padding: '2rem 1rem 4rem 1rem' }}>
      {loading && <div className="posts-loading">Loading posts...</div>}
      {error && <div className="posts-error">{error}</div>}
      {category && <h2 className="posts-title">{category.name} Posts</h2>}
      {!loading && !error && posts.length === 0 && <div className="posts-empty">No posts in this category yet.</div>}
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
  );
} 