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
    const [orderCompleted, setOrderCompleted] = useState(false);

    const { register, wrapSubmit, handleServerErrors, watch, formState: { errors } } = useFormWithServerErrors({
        defaultValues: {
            phone: '',
            delivery_address: '',
            self_pickup: false,
            payment_method: 'cash',
        }
    });

    const selfPickup = watch('self_pickup');

    if (cartItems.length === 0 && !orderCompleted) {
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
            setOrderCompleted(true);
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
                <h1 className="page-title">Оформлення замовлення</h1>

                <div className="checkout-content">
                    <div className="order-summary-side">
                        <h3>Твоє замовлення</h3>
                        <ul>
                            {cartItems.map(item => (
                                <li key={item.id} className="summary-item">
                                    <span>{item.name} x{item.quantity}</span>
                                    <span>{(item.price * item.quantity).toFixed(2)} ₴</span>
                                </li>
                            ))}
                        </ul>
                        <div className="total-line">
                            <strong>Разом:</strong>
                            <strong>{cartTotal.toFixed(2)} ₴</strong>
                        </div>
                    </div>

                    <form onSubmit={wrapSubmit(onSubmit)} className="checkout-form base-form">
                        <div className="form-group">
                            <label htmlFor='phone'>Номер телефону</label>
                            <input
                                type="tel"
                                name="phone"
                                placeholder="+380..."
                                {...register('phone', {
                                    required: 'Номер телефону є обовʼязковим',
                                    pattern: {
                                        value: /^\+?\d{9,15}$/,
                                        message: "Некоректний формат номера"
                                    }
                                })}
                                className={errors.phone ? 'error' : ''}
                            />
                            {errors.phone && <span className="error-msg">{errors.phone.message}</span>}
                        </div>

                        <div className="form-group checkbox-group">
                            <label htmlFor='self_pickup'>
                                <input
                                    name="self_pickup"
                                    type="checkbox"
                                    {...register('self_pickup')}
                                />
                                Я заберу замовлення самостійно
                            </label>
                        </div>

                        {!selfPickup && (
                            <div className="form-group">
                                <label htmlFor='delivery_address'>Адреса доставки</label>
                                <textarea
                                    name="delivery_address"
                                    {...register('delivery_address', {
                                        required: !selfPickup ? 'Адреса обовʼязкова для доставки' : false
                                    })}
                                    placeholder="Місто, вулиця, будинок, квартира..."
                                    rows="3"
                                    className={errors.delivery_address ? 'error' : ''}
                                />
                                {errors.delivery_address && <span className="error-msg">{errors.delivery_address.message}</span>}
                            </div>
                        )}

                        <div className="form-group hidden">
                            {/* Приховано, зараз підтримується тільки оплата готівкою */}
                            <input type="hidden" {...register('payment_method')} value="cash" />
                        </div>

                        <button
                            type="submit"
                            className="btn-submit"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Оформлюємо замовлення…' : 'Підтвердити замовлення'}
                        </button>
                    </form>
                </div>
            </main>
        </div>
    );
}
