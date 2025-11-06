import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LoginPage.css'; 
import { API_URL } from '../api';
import { toast } from 'react-toastify';
import axios from 'axios';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // use axios to avoid the api-token-checking interceptors
      // while we're trying to set the tokens in question
      // (and the baseURL override is neater this way)
      const response = await axios.post(API_URL + 'token/', {
        email: email, 
        password: password
      });
      
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);

      toast.success('Вхід успішний!');
      navigate('/admin/menu'); 

    } catch (error) {
      const status = error?.response?.status;

      if (status === 401) {
        toast.error('Неправильний email або пароль. Спробуйте ще раз.');
      } else {
        console.error('Помилка входу:', error?.response ? error.response.data : error.message);
        toast.error('Не вдалося увійти. Спробуйте ще раз.');
      }
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
          <label htmlFor="email">email</label>
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