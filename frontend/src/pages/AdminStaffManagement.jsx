import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import apiClient from '../api';
import { toast } from 'react-toastify';

const defaultFormState = {
  username: '',
  password: '',
  role: 'cook',
};

const ROLE_DISPLAY_NAMES = {
  cook: 'Кухар',
  courier: 'Кур\'єр',
  manager: 'Менеджер',
};

function AdminStaffManagement() {
  const [staffList, setStaffList] = useState([]);
  
  const { 
    register,
    handleSubmit,
    reset,
    setError,
    formState: { errors }
  } = useForm({
    defaultValues: defaultFormState
  });

  useEffect(() => {
    fetchStaff();
  }, []);

  
    const fetchStaff = async () => {
    try {
        const response = await apiClient.get('/users/staff/'); 
        setStaffList(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
        toast.error("Не вдалося завантажити список персоналу.");
        console.error('Error fetching staff:', error);
    }
    };


  
  const onSubmit = async (data) => {
    try {
      await apiClient.post('/users/staff/', data);
      toast.success(`Акаунт для '${data.username}' (роль: ${data.role}) успішно створено!`);
      reset(defaultFormState); 
      fetchStaff();
      
    } catch (error) {
    if (error.response && error.response.data) {
        const serverErrors = error.response.data;
        for (const [field, message] of Object.entries(serverErrors)) {
        setError(field, { type: 'server', message: message[0] });
        }
    } else {
        toast.error("Сталася неочікувана помилка при створенні акаунта.");
        console.error('Submission error:', error);
    }
    }


  
  const handleDelete = async (id, username) => {
    if (globalThis.confirm(`Ви впевнені, що хочете видалити акаунт '${username}'?`)) {
      try {
        await apiClient.delete(`/users/staff/${id}/`);
        toast.success("Акаунт видалено.");
        fetchStaff();
      } catch (error) {
        if (error.response?.status === 404) {
          toast.error(`Цього акаунту вже не існує.`)
        }
        toast.error("Не вдалося видалити акаунт.");
        console.error('Error deleting staff:', error);
      }
    }
  };

  return (
    <div>
      <h2>Керування персоналом</h2>
      
      <form className="admin-form" onSubmit={handleSubmit(onSubmit)}>
        <h3>Створити новий акаунт</h3>
        <div className="form-grid">
          
          <div className="form-group">
            <label htmlFor="username">Ім'я користувача (Логін)</label>
            <input
              type="text"
              id="username"
              {...register('username', { required: 'Логін є обов\'язковим' })}
            />
            {errors.username && <span className="error-message">{errors.username.message}</span>}
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              {...register('password', { required: 'Пароль є обов\'язковим' })}
            />
            {errors.password && <span className="error-message">{errors.password.message}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="role">Роль</label>
            <select
              id="role"
              {...register('role', { required: 'Роль є обов\'язковою' })}
            >
              <option value="cook">Кухар</option>
              <option value="courier">Кур'єр</option>
            </select>
            {errors.role && <span className="error-message">{errors.role.message}</span>}
          </div>

        </div>
        
        <div className="actions" style={{ marginTop: '1rem' }}>
          <button type="submit" className="admin-button">
            Створити акаунт
          </button>
        </div>
      </form>
      
      <h3>Наявний персонал</h3>
      <table className="admin-table">
        <thead>
          <tr>
            <th>Ім'я користувача</th>
            <th>Роль</th>
            <th>Дії</th>
          </tr>
        </thead>
        <tbody>
          {staffList.map(user => (
            <tr key={user.id}>
              <td>{user.username}</td>
              <td>{ROLE_DISPLAY_NAMES[user.role] || user.role}</td>
              <td className="actions">
                <button 
                  className="admin-button admin-button-secondary" 
                  onClick={() => handleDelete(user.id, user.username)}
                >
                  Видалити
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminStaffManagement;