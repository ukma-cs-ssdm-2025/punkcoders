import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useUser } from '../hooks/useUser'; // Assuming this hook exists based on ProtectedRoute
import { useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-toastify';
import apiClient from '../api';
import { useCart } from '../context/CartContext';

export default function Header() {
  const { cartCount } = useCart();
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'light';
  });

  const { data: user } = useUser();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  useEffect(() => {
    document.body.dataset.theme = theme;
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  const handleLogout = () => {
    const refreshData = new FormData();
    refreshData.append('refresh_token', localStorage.getItem('refreshToken'));
    apiClient.post("/logout/", refreshData);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    queryClient.removeQueries(['user']);
    toast.info("Ви вийшли з системи");
    navigate('/');
  };

  const cartIconSrc = theme === 'light'
    ? "/content/Shopicons_Light_Cart6.png"
    : "/content/white-cart.png";

  return (
    <header className="site-header">
      <div className="container">
        <Link to="/" className="header-logo">
          <img src="/content/logo-clock.png" alt="Star-Logo" />
          <h5>ClickEat</h5>
        </Link>

        <nav className="header-navigation">
          <ul>
            <li><Link to="/menu">Меню</Link></li>
            
            {user?.role === 'MANAGER' && (
              <li><Link to="/admin">Керування сайтом</Link></li>
            )}
            {user?.role === 'KITCHEN_STAFF' && (
              <li><Link to="/chef">Замовлення для приготування</Link></li>
            )}
            {user?.role === 'COURIER' && (
              <li><Link to="/courier">Замовлення для доставки</Link></li>
            )}
          </ul>
        </nav>

        <div className="header-actions">
          <button
            className="theme-toggle"
            aria-label="Перемкнути тему"
            onClick={toggleTheme}
          >
            <img 
              src={theme === 'light' ? "/content/Shopicons_Light_Sun.png" : "/content/Shopicons_Light_MoonHalf.png"} 
              alt="Theme Toggle" 
              style={{ filter: theme === 'dark' ? 'invert(1)' : 'none' }} 
            />
          </button>

          {user ? (
            <div className="user-controls" style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <Link to="/profile" className="button button-secondary" style={{textDecoration: 'none'}}>
                {user.first_name + " " + user.last_name || 'Профіль'}
              </Link>
              <button onClick={handleLogout} className="admin-button admin-button-secondary" style={{padding: '0.4rem 0.8rem', fontSize: '0.9rem'}}>
                Вийти
              </button>
            </div>
          ) : (
            <Link to="/login" className="button button-secondary">
              Увійти <img src="/content/Shopicons_Light_Account.png" alt="" style={{width:'16px', marginLeft:'5px'}}/>
            </Link>
          )}

          <a href="/cart" className="header-cart-button">
            <span><img src={cartIconSrc} alt="Cart" /></span>
            <span className="cart-counter">{cartCount}</span>
          </a>
        </div>
      </div>
    </header>
  );
}