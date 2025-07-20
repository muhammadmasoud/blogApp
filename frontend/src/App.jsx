import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import React, { Suspense, lazy, useState, useEffect } from 'react';
import Login from './Login';
import Register from './Register';
import { AuthProvider } from './AuthContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';
import './App.css';
import axios from 'axios';

const Home = lazy(() => import('./Home'));
const CategoryPosts = lazy(() => import('./CategoryPosts'));
const PostDetail = lazy(() => import('./PostDetail'));

const API_URL = 'http://127.0.0.1:8000/api/posts/';

function App() {
  // Pagination state
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrev, setHasPrev] = useState(false);

  useEffect(() => {
    setLoading(true);
    setError('');
    axios.get(`${API_URL}?page=${page}&page_size=5`)
      .then(res => {
        setPosts(res.data.results || res.data.posts || []);
        setHasNext(!!res.data.next);
        setHasPrev(!!res.data.previous);
        setLoading(false);
      })
      .catch(() => {
        setPosts([]);
        setHasNext(false);
        setHasPrev(page > 1);
        setError('Failed to load posts.');
        setLoading(false);
      });
  }, [page]);

  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <div className="main-content">
          <Sidebar />
          <div style={{ flex: 1 }}>
            <Suspense fallback={<div style={{textAlign:'center',marginTop:'4rem',fontSize:'2rem',color:'#646cff'}}>Loading...</div>}>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/" element={<Home posts={posts} loading={loading} error={error} />} />
                <Route path="/category/:id" element={<CategoryPosts />} />
                <Route path="/post/:id" element={<PostDetail />} />
              </Routes>
            </Suspense>
          </div>
        </div>
        <Footer page={page} setPage={setPage} hasNext={hasNext} hasPrev={hasPrev} />
      </Router>
    </AuthProvider>
  );
}

export default App;
