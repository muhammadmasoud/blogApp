import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import React, { Suspense, lazy } from 'react';
import Login from './Login';
import Register from './Register';
import { AuthProvider } from './AuthContext';
import Navbar from './components/Navbar';
import './App.css';

const Home = lazy(() => import('./Home'));
const CategoryPosts = lazy(() => import('./CategoryPosts'));

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <div style={{ minHeight: '80vh' }}>
          <Suspense fallback={<div style={{textAlign:'center',marginTop:'4rem',fontSize:'2rem',color:'#646cff'}}>Loading...</div>}>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/" element={<Home />} />
              <Route path="/category/:id" element={<CategoryPosts />} />
            </Routes>
          </Suspense>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
