import React, { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';

const CartContext = createContext();

export const useCart = () => {
    const context = useContext(CartContext);
    if (!context) {
        throw new Error('useCart must be used within a CartProvider');
    }
    return context;
};

export const CartProvider = ({ children }) => {
    const [cartItems, setCartItems] = useState(() => {
        try {
            const storedCart = localStorage.getItem('cartItems');
            return storedCart ? JSON.parse(storedCart) : [];
        } catch (error) {
            console.error("Failed to load cart from localStorage", error);
            return [];
        }
    });

    useEffect(() => {
        try {
            localStorage.setItem('cartItems', JSON.stringify(cartItems));
        } catch (error) {
            console.error("Failed to save cart to localStorage", error);
        }
    }, [cartItems]);

    // 1. We wrap this in useCallback. 
    // We use (prevItems) so we don't depend on the outer cartItems variable.
    const addToCart = useCallback((dish, quantity = 1) => {
        setCartItems((prevItems) => {
            const existingItem = prevItems.find((item) => item.id === dish.id);
            if (existingItem) {
                return prevItems.map((item) =>
                    item.id === dish.id
                        ? { ...item, quantity: item.quantity + quantity }
                        : item
                );
            }
            return [...prevItems, { ...dish, quantity }];
        });
    }, []);

    // 2. Wrapped in useCallback
    const removeFromCart = useCallback((dishId) => {
        setCartItems((prevItems) => prevItems.filter((item) => item.id !== dishId));
    }, []);

    // 3. Wrapped in useCallback
    const updateQuantity = useCallback((dishId, newQuantity) => {
        if (newQuantity < 1) return;
        setCartItems((prevItems) =>
            prevItems.map((item) =>
                item.id === dishId ? { ...item, quantity: newQuantity } : item
            )
        );
    }, []);

    // 4. Wrapped in useCallback. THIS IS THE CRITICAL FIX FOR YOUR BUG.
    const clearCart = useCallback(() => {
        setCartItems([]);
    }, []);

    // These are just calculations, they re-run when cartItems changes. This is fine.
    const cartTotal = cartItems.reduce(
        (total, item) => total + item.price * item.quantity,
        0
    );

    const cartCount = cartItems.reduce((count, item) => count + item.quantity, 0);

    // 5. We bundle everything into a stable object
    const value = useMemo(() => ({
        cartItems,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        cartTotal,
        cartCount,
    }), [cartItems, addToCart, removeFromCart, updateQuantity, clearCart, cartTotal, cartCount]);

    return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

CartProvider.propTypes = {
    children: PropTypes.node.isRequired,
};