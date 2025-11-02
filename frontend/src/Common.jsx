export default function Header() {
  return (
    <header className="site-header">
      <div className="container">
        <a href="/" className="header-logo">
          {/* Assuming /content/ path is correct */}
          <img src="/content/Shopicons_Light_Stars.png" alt="Star-Logo" />
          <h5>ClickEat</h5>
        </a>

        <nav className="header-navigation">
          <ul>
            <li><a href="/menu">Меню</a></li>
            <li><a href="/faq">FAQ</a></li>
          </ul>
        </nav>

        <div className="header-search">
          <img src="/content/Shopicons_Light_Search.png" alt="Search-Icon" />
          <input type="text" placeholder="Пошук..." />
        </div>

        <div className="header-actions">
          <button className="theme-toggle" aria-label="Перемкнути тему">
            <img src="/content/Shopicons_Light_Sun.png" alt="Sun-Logo-Light_Theme" />
          </button>

          <a href="/login" className="btn btn-secondary">
            Log in <img src="/content/Shopicons_Light_Account.png" alt="" />
          </a>

          <a href="/cart" className="btn btn-secondary header-cart-button">
            <span> <img src="/content/Shopicons_Light_Cart6.png" alt="" /></span>
            <span className="cart-counter">0</span>
          </a>
        </div>
      </div>
    </header>
  );
}