import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import apiClient from '../api';
import './ChefPage.css';

export default function ChefPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch orders from API
  const fetchOrders = useCallback(async () => {
    try {
      const response = await apiClient.get('/menu/kitchen/orders/');
      setOrders(response.data);
    } catch (error) {
      console.error('Error fetching kitchen orders:', error);
      if (error.response?.status !== 401) {
        toast.error('Не вдалося завантажити замовлення');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchOrders();
    // Poll for new orders every 10 seconds
    const interval = setInterval(fetchOrders, 10000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  // Start preparing order
  const startPreparing = async (orderId) => {
    try {
      await apiClient.post(`/menu/kitchen/orders/${orderId}/start/`);
      toast.success('Замовлення взято в роботу!');
      fetchOrders();
    } catch (error) {
      console.error('Error starting order:', error);
      const msg = error.response?.data?.detail || 'Помилка при оновленні статусу';
      toast.error(msg);
    }
  };

  // Complete order
  const completeOrder = async (orderId) => {
    try {
      await apiClient.post(`/menu/kitchen/orders/${orderId}/complete/`);
      toast.success('Замовлення готове!');
      fetchOrders();
    } catch (error) {
      console.error('Error completing order:', error);
      const msg = error.response?.data?.detail || 'Помилка при оновленні статусу';
      toast.error(msg);
    }
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString('uk-UA', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Map status to display values
  const getStatusDisplay = (status) => {
    switch (status) {
      case 'new': return { text: 'Нове', class: 'new' };
      case 'in_progress': return { text: 'Готується', class: 'preparing' };
      default: return { text: status, class: 'new' };
    }
  };

  return (
    <div className="chef-dashboard">
      <header className="chef-header">
        <div className="container header-flex">
          <div className="logo-area">
            <img src="/content/logo-clock.png" alt="Logo" width="40" />
            <h2>Кухня</h2>
          </div>
          <div className="chef-stats">
            <span>Активні: {orders.length}</span>
            <button onClick={fetchOrders} style={{ marginLeft: '1rem', padding: '0.5rem 1rem' }}>
              🔄 Оновити
            </button>
            <Link to="/" className="exit-btn">Вихід</Link>
          </div>
        </div>
      </header>

      <main className="container">
        {loading ? (
          <div className="loading-state">Завантаження замовлень...</div>
        ) : orders.length === 0 ? (
          <div className="empty-state">
            <div className="pulsing-circle"></div>
            <h3>Наразі замовлень немає</h3>
            <p>Очікуємо нових замовлень...</p>
          </div>
        ) : (
          <div className="orders-grid">
            {orders.map((order) => {
              const statusInfo = getStatusDisplay(order.status);
              return (
                <div key={order.id} className={`order-ticket status-${statusInfo.class} fade-in`}>
                  <div className="ticket-header">
                    <span className="order-id">#{order.id}</span>
                    <span className="order-time">{formatTime(order.created_at)}</span>
                  </div>

                  <div className="ticket-type">
                    {order.self_pickup ? '🏃 Самовивіз' : `🚗 ${order.delivery_address || 'Доставка'}`}
                  </div>

                  <div className="ticket-body">
                    <ul className="ticket-items">
                      {order.dishes?.map((dish, index) => (
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
                        onClick={() => startPreparing(order.id)}
                      >
                        🍳 Почати готувати
                      </button>
                    )}

                    {order.status === 'in_progress' && (
                      <button
                        className="chef-btn btn-done"
                        onClick={() => completeOrder(order.id)}
                      >
                        ✅ Готово
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}