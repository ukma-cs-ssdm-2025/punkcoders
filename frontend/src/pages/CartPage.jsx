import { Link } from 'react-router-dom';
import Header from '../components/Header';
import { useCart } from '../context/CartContext';
import './CartPage.css';

export default function CartPage() {
    const { cartItems, removeFromCart, updateQuantity, cartTotal, clearCart } = useCart();

    if (cartItems.length === 0) {
        return (
            <div className="page-wrapper">
                <Header />
                <main className="container cart-empty">
                    <h2>Your Cart is Empty</h2>
                    <p>Looks like you haven't added any dishes yet.</p>
                    <Link to="/menu" className="btn-primary">Go to Menu</Link>
                </main>
            </div>
        );
    }

    return (
        <div className="page-wrapper">
            <Header />
            <main className="container cart-container">
                <h1 className="page-title">Your Cart</h1>

                <div className="cart-content">
                    <div className="cart-items">
                        {cartItems.map((item) => (
                            <div key={item.id} className="cart-item">
                                <div className="cart-item-image">
                                    <img
                                        src={item.photo_url || `https://placehold.co/100x100/E5E7EB/333?text=${encodeURIComponent(item.name)}`}
                                        alt={item.name}
                                    />
                                </div>
                                <div className="cart-item-details">
                                    <h3>{item.name}</h3>
                                    <p className="item-price">{item.price} ₴</p>
                                </div>
                                <div className="cart-item-actions">
                                    <div className="quantity-controls">
                                        <button
                                            onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                            disabled={item.quantity <= 1}
                                            className="btn-quantity"
                                        >
                                            -
                                        </button>
                                        <span>{item.quantity}</span>
                                        <button onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                            className="btn-quantity">
                                            +
                                        </button>
                                    </div>
                                    <button
                                        className="btn-remove"
                                        onClick={() => removeFromCart(item.id)}
                                    >
                                        Remove
                                    </button>
                                </div>
                                <div className="cart-item-total">
                                    {(item.price * item.quantity).toFixed(2)} ₴
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="cart-summary">
                        <h3>Summary</h3>
                        <div className="summary-row">
                            <span>Total:</span>
                            <span className="summary-total">{cartTotal.toFixed(2)} ₴</span>
                        </div>
                        <div className="summary-actions">
                            <Link to="/checkout" className="btn-checkout">Proceed to Checkout</Link>
                            <button onClick={clearCart} className="btn-clear">Clear Cart</button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
