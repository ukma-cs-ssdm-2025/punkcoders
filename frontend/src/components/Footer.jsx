export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="container">
        <div className="footer-top">
          
          <div className="footer-column">
            <h4>Замовлення</h4>
            <ul>
              <li><a href="/menu">Переглянути меню</a></li>
            </ul>
          </div>

          <div className="footer-column">
            <h4>Компанія</h4>
            <ul>
              <li><a href="/faq">Питання та відповіді</a></li>
            </ul>
          </div>

          <div className="footer-column">
            <h4>Допомога</h4>
            <ul>
              <li><a href="/account">Мій кабінет</a></li>
              <li><a href="/contact">Зв'язатися з нами</a></li>
            </ul>
          </div>

          <div className="footer-column brand-column">
            <a href="/" className="footer-logo">
              <img src="/content/logo-clock.png" alt="Pizzateria" /> 
              <span>ClickEat</span>
            </a>
            <p className="brand-desc">
              Наша місія — втамувати твій голод смачною їжею, доставленою швидко й без додаткових витрат.
            </p>
            <div className="social-icons">
              <a href="#"><img src="/content/instagram-icon.png" alt="Instagram" /></a>
              <a href="#"><img src="/content/facebook-icon.png" alt="Facebook" /></a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p>2025. Усі права захищено</p>
        </div>
      </div>
    </footer>
  );
}
