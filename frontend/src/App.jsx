import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AdminPage from './pages/AdminPage';
import LoginPage from './pages/LoginPage'; 

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      
      <Route path="/login" element={<LoginPage />} />
      
      <Route path="/admin/*" element={<AdminPage />} />
    </Routes>
  );
}

export default App;