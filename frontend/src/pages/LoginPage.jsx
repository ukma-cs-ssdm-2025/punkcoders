import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LoginPage.css'; 
import axios from 'axios';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Надсилаємо дані на сервер:', username, password);

    try {
      // 1. Надсилаємо POST-запит на ваш Django ендпоінт
      // TODO: use apiClient
      const response = await axios.post('http://localhost:8000/api/token/', {
        // Ми припускаємо, що ваш Django налаштований на вхід по 'email'.
        // Якщо він очікує 'username', змініть 'email' на 'username'.
        username: username, 
        password: password
      });

      // 2. Якщо запит успішний (код 200), Django поверне токени
      console.log('Сервер відповів:', response.data);
      
      // 3. Зберігаємо ОБИДВА токени у localStorage
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);

      // 4. Повідомляємо користувача та перенаправляємо його
      alert('Вхід успішний! Токени збережено.');
      navigate('/admin/menu'); 

    } catch (error) {
      // 5. Якщо сервер повернув помилку (400, 401, 500)
      console.error('Помилка входу:', error.response ? error.response.data : error.message);
      alert('Неправильний username або пароль. Спробуйте ще раз.');
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        
        <div className="login-logo">
          <img src="/content/Shopicons_Light_Stars.png" alt="Star-Logo" />
          <h5>ClickEat</h5>
        </div>
        
        <h2>Вхід для менеджерів</h2>
        
        <div className="form-group">
          <label htmlFor="username">username</label>
          <input
            type="username"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Пароль</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        
        <button type="submit" className="login-button">
          Увійти
        </button>
        
        <div className="login-links">
          <Link to="/">Повернутись на головну</Link>
        </div>
        
      </form>
    </div>
  );
}

export default LoginPage;