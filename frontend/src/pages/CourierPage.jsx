import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import apiClient from '../api';
import './CourierPage.css';

export default function CourierPage() {
    const [activeTab, setActiveTab] = useState('ready'); // 'ready' | 'my'
    const [readyOrders, setReadyOrders] = useState([]);
    const [myOrders, setMyOrders] = useState([]);
    const [selectedOrder, setSelectedOrder] = useState(null);
    const [loading, setLoading] = useState(true);

    // Fetch orders based on active tab
    const fetchOrders = async () => {
        setLoading(true);
        try {
            if (activeTab === 'ready') {
                const response = await apiClient.get('/menu/courier/ready/');
                setReadyOrders(response.data);
            } else {
                const response = await apiClient.get('/menu/courier/my/');
                setMyOrders(response.data);
            }
        } catch (error) {
            console.error('Error fetching orders:', error);
            toast.error('Не вдалося завантажити замовлення');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchOrders();
        // Poll for updates every 30 seconds
        const interval = setInterval(fetchOrders, 30000);
        return () => clearInterval(interval);
    }, [activeTab]);

    // Fetch order details (with phone number)
    const fetchOrderDetails = async (orderId) => {
        try {
            const response = await apiClient.get(`/menu/courier/${orderId}/details/`);
            setSelectedOrder(response.data);
        } catch (error) {
            console.error('Error fetching order details:', error);
            toast.error('Не вдалося завантажити деталі замовлення');
        }
    };

    // Assign order to self
    const handleAssign = async (orderId) => {
        try {
            await apiClient.post(`/menu/courier/${orderId}/assign/`);
            toast.success('Замовлення взято на доставку!');
            // Refresh both lists
            const readyRes = await apiClient.get('/menu/courier/ready/');
            const myRes = await apiClient.get('/menu/courier/my/');
            setReadyOrders(readyRes.data);
            setMyOrders(myRes.data);
            setActiveTab('my');
        } catch (error) {
            console.error('Error assigning order:', error);
            const msg = error.response?.data?.detail || 'Не вдалося взяти замовлення';
            toast.error(msg);
        }
    };

    // Complete delivery
    const handleComplete = async (orderId) => {
        try {
            await apiClient.post(`/menu/courier/${orderId}/complete/`);
            toast.success('Замовлення доставлено!');
            setSelectedOrder(null);
            // Refresh my orders
            const response = await apiClient.get('/menu/courier/my/');
            setMyOrders(response.data);
        } catch (error) {
            console.error('Error completing order:', error);
            const msg = error.response?.data?.detail || 'Не вдалося завершити замовлення';
            toast.error(msg);
        }
    };

    // Unassign order
    const handleUnassign = async (orderId) => {
        try {
            await apiClient.post(`/menu/courier/${orderId}/unassign/`);
            toast.success('Замовлення повернуто в список');
            setSelectedOrder(null);
            // Refresh both lists
            const readyRes = await apiClient.get('/menu/courier/ready/');
            const myRes = await apiClient.get('/menu/courier/my/');
            setReadyOrders(readyRes.data);
            setMyOrders(myRes.data);
        } catch (error) {
            console.error('Error unassigning order:', error);
            const msg = error.response?.data?.detail || 'Не вдалося повернути замовлення';
            toast.error(msg);
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleTimeString('uk-UA', {
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="courier-dashboard">
            <header className="courier-header">
                <div className="container header-flex">
                    <div className="logo-area">
                        <img src="/content/logo-clock.png" alt="Logo" width="40" />
                        <h2>Доставка</h2>
                    </div>
                    <div className="courier-stats">
                        <span className="stat-badge ready">Готові: {readyOrders.length}</span>
                        <span className="stat-badge my">Мої: {myOrders.length}</span>
                        <Link to="/" className="exit-btn">Вихід</Link>
                    </div>
                </div>
            </header>

            <nav className="courier-tabs">
                <button
                    className={`tab-btn ${activeTab === 'ready' ? 'active' : ''}`}
                    onClick={() => { setActiveTab('ready'); setSelectedOrder(null); }}
                >
                    🍽️ Готові до доставки
                </button>
                <button
                    className={`tab-btn ${activeTab === 'my' ? 'active' : ''}`}
                    onClick={() => { setActiveTab('my'); setSelectedOrder(null); }}
                >
                    🚗 Мої доставки
                </button>
            </nav>

            <main className="container courier-content">
                {loading ? (
                    <div className="loading-state">Завантаження...</div>
                ) : (
                    <div className="courier-layout">
                        {/* Orders List */}
                        <div className="orders-list">
                            {activeTab === 'ready' ? (
                                readyOrders.length === 0 ? (
                                    <div className="empty-state">
                                        <div className="pulsing-circle"></div>
                                        <h3>Немає готових замовлень</h3>
                                        <p>Очікуємо замовлення з кухні...</p>
                                    </div>
                                ) : (
                                    readyOrders.map(order => (
                                        <div
                                            key={order.id}
                                            className={`order-card ${selectedOrder?.id === order.id ? 'selected' : ''}`}
                                            onClick={() => fetchOrderDetails(order.id)}
                                        >
                                            <div className="order-card-header">
                                                <span className="order-id">#{order.id}</span>
                                                <span className="order-time">{formatDate(order.created_at)}</span>
                                            </div>
                                            <div className="order-address">{order.delivery_address}</div>
                                            <div className="order-card-footer">
                                                <span className="order-total">{order.total_amount} ₴</span>
                                                <span className={`payment-badge ${order.payment_method}`}>
                                                    {order.payment_method === 'cash' ? '💵 Готівка' : '💳 Картка'}
                                                </span>
                                            </div>
                                            <button
                                                className="btn-assign"
                                                onClick={(e) => { e.stopPropagation(); handleAssign(order.id); }}
                                            >
                                                Взяти замовлення
                                            </button>
                                        </div>
                                    ))
                                )
                            ) : (
                                myOrders.length === 0 ? (
                                    <div className="empty-state">
                                        <h3>У вас немає активних доставок</h3>
                                        <p>Візьміть замовлення зі списку готових</p>
                                    </div>
                                ) : (
                                    myOrders.map(order => (
                                        <div
                                            key={order.id}
                                            className={`order-card my-order ${selectedOrder?.id === order.id ? 'selected' : ''}`}
                                            onClick={() => fetchOrderDetails(order.id)}
                                        >
                                            <div className="order-card-header">
                                                <span className="order-id">#{order.id}</span>
                                                <span className="order-time">{formatDate(order.created_at)}</span>
                                            </div>
                                            <div className="order-address">{order.delivery_address}</div>
                                            <div className="order-card-footer">
                                                <span className="order-total">{order.total_amount} ₴</span>
                                                <span className={`payment-badge ${order.payment_method}`}>
                                                    {order.payment_method === 'cash' ? '💵 Готівка' : '💳 Картка'}
                                                </span>
                                            </div>
                                        </div>
                                    ))
                                )
                            )}
                        </div>

                        {/* Order Details Panel */}
                        {selectedOrder && (
                            <div className="order-details-panel">
                                <div className="panel-header">
                                    <h3>Замовлення #{selectedOrder.id}</h3>
                                    <button className="close-btn" onClick={() => setSelectedOrder(null)}>✕</button>
                                </div>

                                <div className="panel-section">
                                    <h4>📍 Адреса доставки</h4>
                                    <p className="address-text">{selectedOrder.delivery_address}</p>
                                </div>

                                <div className="panel-section">
                                    <h4>📞 Телефон клієнта</h4>
                                    <a href={`tel:${selectedOrder.phone}`} className="phone-link">
                                        {selectedOrder.phone}
                                    </a>
                                </div>

                                <div className="panel-section">
                                    <h4>🍽️ Замовлення</h4>
                                    <ul className="items-list">
                                        {selectedOrder.items?.map(item => (
                                            <li key={item.id}>
                                                <span>{item.quantity}x {item.name}</span>
                                                <span>{item.line_total} ₴</span>
                                            </li>
                                        ))}
                                    </ul>
                                    <div className="total-line">
                                        <strong>Всього:</strong>
                                        <strong>{selectedOrder.total_amount} ₴</strong>
                                    </div>
                                </div>

                                <div className="panel-section">
                                    <h4>💰 Оплата</h4>
                                    <p className={`payment-info ${selectedOrder.payment_method}`}>
                                        {selectedOrder.payment_method === 'cash'
                                            ? '💵 Готівка при отриманні'
                                            : '💳 Оплачено карткою'}
                                    </p>
                                </div>

                                <div className="panel-actions">
                                    {activeTab === 'ready' ? (
                                        <button
                                            className="btn-primary"
                                            onClick={() => handleAssign(selectedOrder.id)}
                                        >
                                            🚗 Взяти на доставку
                                        </button>
                                    ) : (
                                        <>
                                            <button
                                                className="btn-primary btn-complete"
                                                onClick={() => handleComplete(selectedOrder.id)}
                                            >
                                                ✅ Доставлено
                                            </button>
                                            <button
                                                className="btn-secondary"
                                                onClick={() => handleUnassign(selectedOrder.id)}
                                            >
                                                ↩️ Повернути
                                            </button>
                                        </>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </main>
        </div>
    );
}
