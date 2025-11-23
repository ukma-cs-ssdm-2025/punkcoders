import { useState, useEffect } from 'react';

export default function Header() {
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
            <span className="cart-counter">0</span>
          </a>
        </div>
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="container">
        <div className="footer-top">
          
          <div className="footer-column">
            <h4>Order</h4>
            <ul>
              <li><a href="/menu">View menu</a></li>
            </ul>
          </div>

            <div className="footer-column">
            <h4>Enterprise</h4>
            <ul>
              <li><a href="/faq">FAQ</a></li>
            </ul>
          </div>


          <div className="footer-column">
            <h4>Assistance</h4>
            <ul>
              <li><a href="/account">Account</a></li>
              <li><a href="/contact">Contact Us</a></li>
            </ul>
          </div>


          <div className="footer-column brand-column">
            <a href="/" className="footer-logo">
              <img src="/content/logo-clock.png" alt="Pizzateria" /> 
              <span>CleakEat</span>
            </a>
            <p className="brand-desc">
              Our mission is to satisfy your hunger with tasty food, delivered quickly and at no charge
            </p>
            <div className="social-icons">
              <a href="#"><img src="/content/instagram-icon.png" alt="Instagram" /></a>
              <a href="#"><img src="/content/facebook-icon.png" alt="Facebook" /></a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p>2025. All rights reserved</p>
        </div>
      </div>
    </footer>
  );
}