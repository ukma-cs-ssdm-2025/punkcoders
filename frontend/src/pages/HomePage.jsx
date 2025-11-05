import { Link } from 'react-router-dom';
import Header from '../Common.jsx';

function HomePage() {
  return (
    <>
      <Header />
      
      <main>
        <section className="hero" style={{ backgroundImage: "url(/content/pizza-bg.jpg)" }}>
          <div className="hero-overlay"></div>
          <div className="hero-content">
            <span className="hero-badge">Beyond Speedy 🍕</span>
            <h1>
              Ensure Your <span className="highlight">Food</span> is <br />
              Delivered with Speed
            </h1>
            <p>
              Our mission is to satisfy your appetite with delectable dishes,
              delivered swiftly and at no extra cost.
            </p>
            <Link to="/menu" className="view-menu-btn">View Full Menu</Link>
          </div>
        </section>
        
        <section className="offerings">
          <div className="container">
            <p className="section-subtitle">OUR OFFERINGS</p>
            <h2 className="section-title">Your Preferred Food Delivery Companion</h2>

            <div className="offerings-grid">
              <div className="offering-card">
                <img src="/content/delivery-guy1.png" alt="Convenient Ordering" />
                <h3>Convenient Ordering</h3>
                <p>Ordering food requires just a few simple steps</p>
              </div>

              <div className="offering-card active">
                <img src="/content/delivery-scooter.png" alt="Quickest Delivery" />
                <h3>Quickest Delivery</h3>
                <p>Consistently Timely Delivery, Even Faster</p>
              </div>

              <div className="offering-card">
                <img src="/content/delivery-quality.png" alt="Superior Quality" />
                <h3>Superior Quality</h3>
                <p>For us, quality is paramount, not just speed</p>
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
    </>
  );
}

export default HomePage;