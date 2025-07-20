import React, { useEffect, useState } from 'react';
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:8000/posts/categories/';
const SUBSCRIBE_URL = 'http://127.0.0.1:8000/user/subscribe/';
const UNSUBSCRIBE_URL = 'http://127.0.0.1:8000/user/unsubscribe/';

export default function Sidebar() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const { user, token } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    setError('');
    fetch(API_URL, {
      headers: user && token ? { 'Authorization': `Bearer ${token}` } : {},
    })
      .then(async res => {
        if (!res.ok) {
          // If unauthorized or error, return empty array
          setError('Failed to load categories.');
          setCategories([]);
          setLoading(false);
          return;
        }
        const data = await res.json();
        if (Array.isArray(data)) {
          setCategories(data);
        } else {
          setCategories([]);
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load categories.');
        setCategories([]);
        setLoading(false);
      });
  }, [token, user]);

  const handleSubscribe = async (categoryId, subscribed) => {
    const url = subscribed ? UNSUBSCRIBE_URL : SUBSCRIBE_URL;
    const action = subscribed ? 'unsubscribed' : 'subscribed';
    const cat = categories.find(c => c.id === categoryId);
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ category_id: categoryId }),
      });
      if (res.ok) {
        setCategories(categories =>
          categories.map(cat =>
            cat.id === categoryId ? { ...cat, subscribed: !subscribed } : cat
          )
        );
        setMessage(`You ${action} to ${cat?.name || 'this'} category`);
        setTimeout(() => setMessage(''), 2000);
      }
    } catch {
      // Optionally show error
    }
  };

  const handleCategoryClick = (categoryId) => {
    navigate(`/category/${categoryId}`);
  };

  if (!user) {
    return null; // Or show a message for guests
  }

  return (
    <aside style={{
      width: '240px',
      background: 'rgba(30,32,60,0.92)',
      color: '#fff',
      padding: '2rem 1rem',
      borderRadius: '18px',
      margin: '2rem 1rem',
      minHeight: '60vh',
      boxShadow: '0 4px 32px #646cff22',
      position: 'relative',
    }}>
      <h3 style={{ color: '#ffb86c', marginBottom: '1.5rem', fontWeight: 700 }}>Categories</h3>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'salmon' }}>{error}</div>}
      <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
        {Array.isArray(categories) && categories.map(cat => (
          <li key={cat.id} style={{ display: 'flex', alignItems: 'center', marginBottom: '1.1rem' }}>
            <button
              onClick={() => handleCategoryClick(cat.id)}
              style={{
                background: 'none',
                border: 'none',
                color: '#fff',
                fontWeight: 600,
                fontSize: '1.08rem',
                cursor: 'pointer',
                flex: 1,
                textAlign: 'left',
                padding: 0,
              }}
            >
              {cat.name}
            </button>
            {user && (
              <button
                onClick={() => handleSubscribe(cat.id, cat.subscribed)}
                style={{
                  marginLeft: '1rem',
                  background: cat.subscribed ? '#ff6a6a' : '#646cff',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '8px',
                  padding: '0.3rem 0.8rem',
                  cursor: 'pointer',
                  fontWeight: 600,
                  fontSize: '0.95rem',
                  transition: 'background 0.2s',
                }}
              >
                {cat.subscribed ? 'Unsubscribe' : 'Subscribe'}
              </button>
            )}
          </li>
        ))}
      </ul>
      {message && (
        <div style={{
          marginTop: '1rem',
          background: '#222',
          color: '#ffb86c',
          padding: '0.7rem 1rem',
          borderRadius: '8px',
          textAlign: 'center',
          fontWeight: 600,
          boxShadow: '0 2px 8px #646cff33',
        }}>{message}</div>
      )}
    </aside>
  );
} 