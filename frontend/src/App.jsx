import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AdminPage from './pages/AdminPage';
import LoginPage from './pages/LoginPage'; 

import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <>
      <ToastContainer
          position="top-right"
          autoClose={4000}
          theme="light"
        />

      <Routes>
        <Route path="/" element={<HomePage />} />
        
        <Route path="/login" element={<LoginPage />} />
        
        <Route path="/admin/*" element={<AdminPage />} />
      </Routes>
    </>
  );
}

export default App;