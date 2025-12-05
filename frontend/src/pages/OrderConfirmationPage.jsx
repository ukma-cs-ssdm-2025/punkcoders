import React, { useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import Header from '../components/Header';
import { useCart } from '../context/CartContext';
import './CheckoutPage.css'; // Reuse styles

export default function OrderConfirmationPage() {
    const location = useLocation();
    const orderId = location.state?.orderId;
    const { clearCart } = useCart();

    useEffect(() => {
        if (orderId) {
            clearCart();
        }
    }, [orderId, clearCart]);

    return (
        <div className="page-wrapper">
            <Header />
            <main className="container checkout-container" style={{ textAlign: 'center' }}>
                <img src="/content/heart.png" alt="Success" style={{ width: '80px', marginBottom: '1rem' }} />
                <h1 className="page-title">Thank You!</h1>
                <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>
                    Your order has been placed successfully.
                </p>

                {orderId ? (
                    <div style={{ background: '#e6fffa', padding: '2rem', borderRadius: '12px', display: 'inline-block', marginBottom: '2rem' }}>
                        <h2 style={{ margin: 0, color: '#006666' }}>Order #{orderId}</h2>
                        <p>Save this number to track your order.</p>
                    </div>
                ) : (
                    <p>We've received your order.</p>
                )}

                <div>
                    <Link to="/menu" className="btn-primary">Back to Menu</Link>
                </div>
            </main>
        </div>
    );
}
