import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LoginPage.css'; 

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Спроба входу з даними:', email, password);

    if (email === "manager@clickeat.com" && password === "12345") {
      
      const fakeToken = "my-super-secret-manager-token-12345";
      
      localStorage.setItem('managerAuthToken', fakeToken);
      
      alert('Вхід успішний! Токен збережено в localStorage.');
      
      navigate('/admin/menu'); 

    } else {
      alert('Неправильний email або пароль (спробуйте manager@clickeat.com / 12345)');
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
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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