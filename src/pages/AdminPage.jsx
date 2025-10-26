import React from 'react';
import { Routes, Route, NavLink, Navigate } from 'react-router-dom';
import AdminMenuManagement from './AdminMenuManagement';
import AdminReports from './AdminReports';
import AdminSettings from './AdminSettings';
import '../Admin.css';

function AdminPage() {
  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <h3>Панель Менеджера</h3>
        <nav>
          <ul>
            <li>
              <NavLink to="/admin/menu">Керування меню</NavLink>
            </li>
            <li>
              <NavLink to="/admin/reports">Звіти</NavLink>
            </li>
            <li>
              <NavLink to="/admin/settings">Налаштування</NavLink>
            </li>
            <li>
              <hr />
              <a href="/">Повернутись на сайт</a>
            </li>
          </ul>
        </nav>
      </aside>
      
      <main className="admin-content">
        <Routes>
          <Route path="/" element={<Navigate to="menu" replace />} />
          
          <Route path="menu" element={<AdminMenuManagement />} /> 
          
          <Route path="reports" element={<AdminReports />} /> 
          
          <Route path="settings" element={<AdminSettings />} /> 
        </Routes>
      </main>
    </div>
  );
}

export default AdminPage;