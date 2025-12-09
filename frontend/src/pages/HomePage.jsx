import { Link } from 'react-router-dom';
import Header from '../components/Header.jsx';
import Footer from '../components/Footer.jsx';


function HomePage() {
  return (
    <>
      <Header />
      
      <main>
        <section className="hero" style={{ backgroundImage: "url(/content/pizza-bg.jpg)" }}>
          <div className="hero-overlay"></div>
          <div className="hero-content">
            <span className="hero-badge">Більше, ніж швидкість 🍕</span>
            <h1>
              Забезпечуємо <span className="highlight"> їжу </span> швидкою <br /> доставкою 
            </h1>
            <p>
              Наша місія — задовольнити ваш апетит смачними стравами,
              які доставляються швидко і без додаткових витрат.
            </p>
            <Link to="/menu" className="view-menu-btn">Дивитися повне меню</Link>
          </div>
        </section>
        
        <section className="offerings">
          <div className="container">
            <p className="section-subtitle">НАШІ ПРОПОЗИЦІЇ</p>
            <h2 className="section-title">Ваш улюблений сервіс доставки їжі</h2>

            <div className="offerings-grid">
              <div className="offering-card">
                <img src="/content/delivery-guy1.png" alt="Convenient Ordering" />
                <h3>Зручне замовлення</h3>
                <p>Замовлення їжі вимагає лише кількох простих кроків</p>
              </div>

              <div className="offering-card active">
                <img src="/content/delivery-scooter.png" alt="Quickest Delivery" />
                <h3>Найшвидша доставка</h3>
                <p>Постійно вчасна доставка</p>
              </div>

              <div className="offering-card">
                <img src="/content/delivery-quality.png" alt="Superior Quality" />
                <h3>Висока якість</h3>
                <p>Для нас найважливішою є якість, а не лише швидкість</p>
              </div>
            </div>
          </div>

          <img src="/content/shape-red.png" className="shape shape1" alt="decorative shape" />
          <img src="/content/shape-yellow.png" className="shape shape2" alt="decorative shape" />
          <img src="/content/shape-red.png" className="shape shape3" alt="decorative shape" />
          <img src="/content/shape-yellow.png" className="shape shape4" alt="decorative shape" />
        </section>

        {/* <section className="menu-section">
          <p className="section-subtitle">OUR SELECTION</p>
          <h2 className="section-title">A Menu That Will Always<br />Capture Your Heart</h2>

          <div className="category-tabs">
            <button className="tab-pill">🍕 Pizza</button>
            <button className="tab-pill">🥤 Drinks</button>
            <button className="tab-pill">🧂 Sauces</button>
          </div>

          <div className="menu-cards">
            <div className="card">
              <img src="/content/heart-filled.png" className="fav-icon" alt="favorite" />
              <img src="/content/sausage-pizza.png" alt="Sausage Pizza" className="card-img" />
              <div className="cart-btn">
                <img src="/content/cart.png" alt="add to cart" />
              </div>

              <div className="card-content">
                <h3 className="product-title">Sausage Pizza</h3>
                <p className="product-price">7.49₴</p>
                <div className="stars">⭐️⭐️⭐️⭐️</div>
                <button className="read-btn">read more</button>
              </div>
            </div>

            <div className="card">
              <img src="/content/heart.png" className="fav-icon" alt="favorite" />
              <img src="/content/margarita-pizza.png" alt="Margherita Pizza" className="card-img" />
              <div className="cart-btn">
                <img src="/content/cart.png" alt="add to cart" />
              </div>

              <div className="card-content">
                <h3 className="product-title">Margherita pizza</h3>
                <p className="product-price">6.40₴</p>
                <div className="stars">⭐️⭐️⭐️</div>
                <button className="read-btn">read more</button>
              </div>
            </div>

            <div className="card">
              <img src="/content/heart.png" className="fav-icon" alt="favorite" />
              <img src="/content/margarita-pizza.png" alt="Meatlovers Pizza" className="card-img" />
              <div className="cart-btn">
                <img src="/content/cart.png" alt="add to cart" />
              </div>

              <div className="card-content">
                <h3 className="product-title">Meatlovers pizza</h3>
                <p className="product-price">9.17₴</p>
                <div className="stars">⭐️⭐️⭐️⭐️</div>
                <button className="read-btn">read more</button>
              </div>
            </div>
          </div>

          <div className="arrow-right">
            <img src="/content/arrow-right.png" alt="next" />
          </div>

          <div className="view-btn-container">
            <button className="view-menu-btn">View Full Menu</button>
          </div>
        </section> */}
      </main>

      <Footer />
    </>
  );
}

export default HomePage;