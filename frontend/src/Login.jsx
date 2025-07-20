import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

const API_URL = 'http://127.0.0.1:8000';

export default function Login() {
  const [form, setForm] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);
    try {
      const res = await fetch(`${API_URL}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (res.ok && data.access) {
        setSuccess(true);
        login({ username: form.username, is_admin: data.is_admin }, data.access);
        setTimeout(() => navigate('/'), 800);
      } else {
        setError(data.detail || data.message || 'Login failed');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: 'auto', background: 'white', borderRadius: 16, boxShadow: '0 4px 32px #0001', padding: 32, marginTop: 64 }}>
      <h2 style={{ textAlign: 'center', color: '#646cff' }}>Login</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        <input
          name="username"
          type="text"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          required
          style={{ padding: 12, borderRadius: 8, border: '1px solid #ccc', fontSize: 16 }}
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
          style={{ padding: 12, borderRadius: 8, border: '1px solid #ccc', fontSize: 16 }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{ background: 'linear-gradient(90deg, #646cff, #61dafb)', color: 'white', border: 'none', borderRadius: 8, padding: 12, fontSize: 18, fontWeight: 'bold', cursor: 'pointer', boxShadow: '0 2px 8px #646cff33' }}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
        {error && <div style={{ color: 'red', textAlign: 'center' }}>{error}</div>}
        {success && <div style={{ color: 'green', textAlign: 'center' }}>Login successful!</div>}
      </form>
    </div>
  );
} 