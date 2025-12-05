import { useState, useEffect } from 'react';
import { useCart } from '../context/CartContext';

export default function Header() {
  const { cartCount } = useCart();
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'light';
  });

  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  const cartIconSrc = theme === 'light'
    ? "/content/Shopicons_Light_Cart6.png"
    : "/content/white-cart.png";

  return (
    <header className="site-header">
      <div className="container">
        <a href="/" className="header-logo">
          {/* Assuming /content/ path is correct */}
          <img src="/content/logo-clock.png" alt="Star-Logo" />
          <h5>ClickEat</h5>
        </a>

        <nav className="header-navigation">
          <ul>
            <li><a href="/menu">Menu</a></li>
            <li><a href="/faq">FAQ</a></li>
          </ul>
        </nav>

        {/* <div className="header-search">
          <img src="/content/Shopicons_Light_Search.png" alt="Search-Icon" />
          <input type="text" placeholder="Пошук..." />
        </div> */}

        <div className="header-actions">
          <button
            className="theme-toggle"
            aria-label="Перемкнути тему"
            onClick={toggleTheme}
          >
            <img
              src={theme === 'light' ? "/content/Shopicons_Light_Sun.png" : "/content/Shopicons_Light_Sun.png"}
              alt="Theme Toggle"
              style={{ filter: theme === 'dark' ? 'invert(1)' : 'none' }} // Простий трюк: інверсія кольору для ночі, якщо немає окремої іконки місяця
            />
          </button>

          {/* <a href="/login" className="button button-secondary">
            Log in <img src="/content/Shopicons_Light_Account.png" alt="" />
          </a> */}

          <a href="/cart" className="header-cart-button">
            <span><img src={cartIconSrc} alt="Cart" /></span>
            <span className="cart-counter">{cartCount}</span>
          </a>
        </div>
      </div>
    </header>
  );
}