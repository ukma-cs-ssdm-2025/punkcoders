import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AdminPage from './pages/AdminPage';

function App() {
  return (
    <Routes>
      {/* Маршрут для головної сторінки */}
      <Route path="/" element={<HomePage />} />
      
      {/* Маршрут для адмін-панелі. 
          Ми використовуємо "/*", щоб дозволити вкладені маршрути всередині AdminPage */}
      <Route path="/admin/*" element={<AdminPage />} />
    </Routes>
  );
}

export default App;