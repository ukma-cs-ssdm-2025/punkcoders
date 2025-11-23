import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function ChefPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [soundEnabled, setSoundEnabled] = useState(false);

  useEffect(() => {
    const enableSound = () => {
      setSoundEnabled(true);
      window.removeEventListener("click", enableSound);
    };

    window.addEventListener("click", enableSound);
    
    return () => window.removeEventListener("click", enableSound);
  }, []);
  
  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 1000);


    const timer = setTimeout(() => {
      const newOrder = {
        id: 1024,
        user_id: 5,
        status: 'new',
        created_at: new Date().toLocaleTimeString(),
        dishes: [
          { id: 1, name: 'Sausage Pizza', notes: 'Без цибулі, будь ласка', qty: 1 },
          { id: 3, name: 'Coca-Cola 0.5', notes: '', qty: 2 }
        ],
        total_price: 250
      };
      
      setOrders(prev => [newOrder, ...prev]);
      
      const audio = new Audio('/content/bell.mp3');
      audio.play().catch(e => console.log("Audio blocked"));
      
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  const updateStatus = (orderId, newStatus) => {
    setOrders(orders.map(order => 
      order.id === orderId ? { ...order, status: newStatus } : order
    ).filter(order => newStatus !== 'completed'));
  };

  return (
    <div className="chef-dashboard">
      <header className="chef-header">
        <div className="container header-flex">
          <div className="logo-area">
            <img src="/content/logo-clock.png" alt="Logo" width="40" />
            <h2>Kitchen View</h2>
          </div>
          <div className="chef-stats">
            <span>Active: {orders.length}</span>
            <Link to="/" className="exit-btn">Exit</Link>
          </div>
        </div>
      </header>

      <main className="container">
        {loading ? (
          <div className="loading-state">Завантаження системи...</div>
        ) : orders.length === 0 ? (
          <div className="empty-state">
            <div className="pulsing-circle"></div>
            <h3>Наразі замовлень немає</h3>
            <p>Очікуємо нових замовлень...</p>
          </div>
        ) : (
          <div className="orders-grid">
            {orders.map((order) => (
              <div key={order.id} className={`order-ticket status-${order.status} fade-in`}>
                <div className="ticket-header">
                  <span className="order-id">#{order.id}</span>
                  <span className="order-time">{order.created_at}</span>
                </div>
                
                <div className="ticket-body">
                  <ul className="ticket-items">
                    {order.dishes.map((dish, index) => (
                      <li key={index}>
                        <div className="item-row">
                          <span className="item-qty">{dish.qty}x</span>
                          <span className="item-name">{dish.name}</span>
                        </div>
                        {dish.notes && (
                          <div className="item-notes">⚠️ {dish.notes}</div>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="ticket-footer">
                  {order.status === 'new' && (
                    <button 
                      className="chef-btn btn-start"
                      onClick={() => updateStatus(order.id, 'preparing')}
                    >
                      Почати готувати
                    </button>
                  )}
                  
                  {order.status === 'preparing' && (
                    <button 
                      className="chef-btn btn-done"
                      onClick={() => updateStatus(order.id, 'completed')}
                    >
                      Готово до видачі ✅
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}