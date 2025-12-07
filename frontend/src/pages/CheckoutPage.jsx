import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import Header from '../components/Header';
import { useCart } from '../context/CartContext';
import { useFormWithServerErrors } from '../hooks/useFormWithServerErrors';
import apiClient from '../api';
import './CheckoutPage.css';
import './forms.css';

export default function CheckoutPage() {
    const { cartItems, clearCart, cartTotal } = useCart();
    const navigate = useNavigate();
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { register, wrapSubmit, handleServerErrors, watch, formState: { errors } } = useFormWithServerErrors({
        defaultValues: {
            phone: '',
            delivery_address: '',
            self_pickup: false,
            payment_method: 'cash',
        }
    });

    const selfPickup = watch('self_pickup');

    if (cartItems.length === 0) {
        navigate('/cart');
        return null;
    }

    const onSubmit = async (data) => {
        setIsSubmitting(true);
        const payload = {
            items_input: cartItems.map(item => ({
                dish_id: item.id,
                quantity: item.quantity
            })),
            phone: data.phone,
            payment_method: data.payment_method,
            self_pickup: data.self_pickup,
            delivery_address: data.self_pickup ? '' : data.delivery_address,
        };

        try {
            const response = await apiClient.post('/menu/orders/', payload);
            toast.success('Замовлення успішно оформлено!');
            clearCart();
            navigate('/order-confirmation', { state: { orderId: response.data.id } });
        } catch (error) {
            handleServerErrors(error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="page-wrapper">
            <Header />
            <main className="container checkout-container">
                <h1 className="page-title">Checkout</h1>

                <div className="checkout-content">
                    <div className="order-summary-side">
                        <h3>Your Order</h3>
                        <ul>
                            {cartItems.map(item => (
                                <li key={item.id} className="summary-item">
                                    <span>{item.name} x{item.quantity}</span>
                                    <span>{(item.price * item.quantity).toFixed(2)} ₴</span>
                                </li>
                            ))}
                        </ul>
                        <div className="total-line">
                            <strong>Total:</strong>
                            <strong>{cartTotal.toFixed(2)} ₴</strong>
                        </div>
                    </div>

                    <form onSubmit={wrapSubmit(onSubmit)} className="checkout-form base-form">
                        <div className="form-group">
                            <label>Phone Number</label>
                            <input
                                type="tel"
                                placeholder="+380..."
                                {...register('phone', {
                                    required: 'Phone is required',
                                    pattern: {
                                        value: /^\+?\d{9,15}$/,
                                        message: "Invalid phone format"
                                    }
                                })}
                                className={errors.phone ? 'error' : ''}
                            />
                            {errors.phone && <span className="error-msg">{errors.phone.message}</span>}
                        </div>

                        <div className="form-group checkbox-group">
                            <label>
                                <input
                                    type="checkbox"
                                    {...register('self_pickup')}
                                />
                                I will pick up the order myself
                            </label>
                        </div>

                        {!selfPickup && (
                            <div className="form-group">
                                <label>Delivery Address</label>
                                <textarea
                                    {...register('delivery_address', {
                                        required: !selfPickup ? 'Address is required for delivery' : false
                                    })}
                                    placeholder="City, Street, House, Apt..."
                                    rows="3"
                                    className={errors.delivery_address ? 'error' : ''}
                                />
                                {errors.delivery_address && <span className="error-msg">{errors.delivery_address.message}</span>}
                            </div>
                        )}

                        <div className="form-group hidden">
                            {/* Hidden for now as only cash is supported/default */}
                            <input type="hidden" {...register('payment_method')} value="cash" />
                        </div>

                        <button
                            type="submit"
                            className="btn-submit"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Placing Order...' : 'Place Order'}
                        </button>
                    </form>
                </div>
            </main>
        </div>
    );
}
