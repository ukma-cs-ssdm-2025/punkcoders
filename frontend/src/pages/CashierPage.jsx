import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import apiClient from '../api';
import './CashierPage.css';

const POLL_INTERVAL = 15000;

export default function CashierPage() {
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchOrders = useCallback(async () => {
    try {
      const response = await apiClient.get('/cashier/orders/');
      const readyOrders = response.data;
      setOrders(readyOrders);

      if (selectedOrder) {
        const refreshed = readyOrders.find((order) => order.id === selectedOrder.id);
        setSelectedOrder(refreshed || null);
      }
    } catch (error) {
      console.error('Error fetching cashier orders:', error);
      if (error.response?.status !== 401) {
        toast.error('Не вдалося завантажити замовлення');
      }
    } finally {
      setLoading(false);
    }
  }, [selectedOrder]);

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  const handleSelect = (order) => {
    setSelectedOrder(order);
  };

  const markPickedUp = async (orderId) => {
    try {
      await apiClient.post(`/cashier/orders/${orderId}/mark_picked_up/`);
      toast.success(`Замовлення #${orderId} видано`);
      setSelectedOrder(null);
      fetchOrders();
    } catch (error) {
      console.error('Error marking order picked up:', error);
      const msg = error.response?.data?.detail || 'Не вдалося оновити статус замовлення';
      toast.error(msg);
    }
  };

  const formatTime = (dateString) => new Date(dateString).toLocaleTimeString('uk-UA', {
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div className="cashier-dashboard">
      <header className="cashier-header">
        <div className="container header-flex">
          <div className="logo-area">
            <img src="/content/logo-clock.png" alt="Logo" width="40" />
            <h2>Каса — Самовивіз</h2>
          </div>
          <div className="cashier-stats">
            <span className="stat-badge ready">Готові: {orders.length}</span>
            <Link to="/" className="exit-btn">Вихід</Link>
          </div>
        </div>
      </header>

      <main className="container cashier-content">
        {loading ? (
          <div className="loading-state">Завантаження готових замовлень...</div>
        ) : (
          <div className="cashier-layout">
            <div className="orders-list">
              {orders.length === 0 ? (
                <div className="empty-state">
                  <div className="pulsing-circle"></div>
                  <h3>Немає готових замовлень</h3>
                  <p>Очікуємо клієнтів</p>
                </div>
              ) : (
                orders.map((order) => (
                  <div
                    key={order.id}
                    className={`order-card ${selectedOrder?.id === order.id ? 'selected' : ''}`}
                    onClick={() => handleSelect(order)}
                  >
                    <div className="order-card-header">
                      <span className="order-id">#{order.id}</span>
                      <span className="order-time">{formatTime(order.created_at)}</span>
                    </div>
                    <div className="order-address">📞 {order.phone}</div>
                    <div className="order-card-footer">
                      <span className="payment-badge">Самовивіз</span>
                      <span className="status-pill">{order.kitchen_status}</span>
                    </div>
                    <button className="btn-assign" onClick={(e) => { e.stopPropagation(); markPickedUp(order.id); }}>
                      Видано клієнту
                    </button>
                  </div>
                ))
              )}
            </div>

            <aside className="order-details-panel">
              {selectedOrder ? (
                <div>
                  <h3>Деталі замовлення #{selectedOrder.id}</h3>
                  <div className="detail-row">
                    <span className="label">Час:</span>
                    <span>{formatTime(selectedOrder.created_at)}</span>
                  </div>
                  <div className="detail-row">
                    <span className="label">Телефон:</span>
                    <span>{selectedOrder.phone}</span>
                  </div>
                  {selectedOrder.delivery_address && (
                    <div className="detail-row">
                      <span className="label">Адреса:</span>
                      <span>{selectedOrder.delivery_address}</span>
                    </div>
                  )}

                  <h4>Страви</h4>
                  <ul className="items-list">
                    {selectedOrder.items.map((item) => (
                      <li key={item.id} className="item-row">
                        <div className="item-name">{item.name}</div>
                        <div className="item-meta">
                          <span className="qty">{item.quantity}x</span>
                          {item.notes && <span className="notes">{item.notes}</span>}
                        </div>
                      </li>
                    ))}
                  </ul>

                  <button className="btn-primary" onClick={() => markPickedUp(selectedOrder.id)}>
                    ✅ Підтвердити видачу
                  </button>
                </div>
              ) : (
                <div className="empty-details">
                  <h3>Оберіть замовлення</h3>
                  <p>Натисніть на карточку замовлення, щоб побачити деталі</p>
                </div>
              )}
            </aside>
          </div>
        )}
      </main>
    </div>
  );
}