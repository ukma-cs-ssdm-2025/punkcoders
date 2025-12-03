import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AdminPage from './pages/admin/AdminPage';
import LoginPage from './pages/LoginPage'; 
import MenuPage from './pages/MenuPage';
import ChefPage from './pages/ChefPage';
import ProtectedRoute from './components/ProtectedRoute';
import NotFound from './pages/errors/NotFound';
import Unauthorized from './pages/errors/Unauthorized';

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
        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route path="/admin/*" element={
          <ProtectedRoute allowedRoles={["MANAGER"]}>
            <AdminPage />
          </ProtectedRoute>
        } />
        <Route path="/menu/:categorySlug?" element={<MenuPage />} />
        <Route path="/chef" element={
          <ProtectedRoute allowedRoles={["MANAGER", "KITCHEN"]}>
            <ChefPage />
          </ProtectedRoute>
        } />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

export default App;