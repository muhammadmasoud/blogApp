import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import React, { Suspense, lazy } from 'react';
import Login from './Login';
import Register from './Register';
import { AuthProvider } from './AuthContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import './App.css';

const Home = lazy(() => import('./Home'));
const CategoryPosts = lazy(() => import('./CategoryPosts'));
const PostDetail = lazy(() => import('./PostDetail'));

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <div style={{ minHeight: '80vh', display: 'flex', flexDirection: 'row' }}>
          <Sidebar />
          <div style={{ flex: 1 }}>
            <Suspense fallback={<div style={{textAlign:'center',marginTop:'4rem',fontSize:'2rem',color:'#646cff'}}>Loading...</div>}>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/" element={<Home />} />
                <Route path="/category/:id" element={<CategoryPosts />} />
                <Route path="/post/:id" element={<PostDetail />} />
              </Routes>
            </Suspense>
          </div>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
