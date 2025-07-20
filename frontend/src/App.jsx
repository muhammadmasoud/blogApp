import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import './App.css'

function App() {
  return (
    <Router>
      <nav style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '2rem' }}>
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </nav>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<div>Welcome to the Blog App!</div>} />
      </Routes>
    </Router>
  );
}

export default App;
