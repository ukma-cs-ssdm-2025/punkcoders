export default function Footer() {
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