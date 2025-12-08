import { useEffect } from 'react';
import { useFormWithServerErrors } from '../hooks/useFormWithServerErrors'; 
import apiClient from '../api';
import { toast } from 'react-toastify';
import { useQueryClient } from '@tanstack/react-query';
import { useUser } from '../hooks/useUser';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './forms.css';

const API_ENDPOINT = '/auth/me/'; 

const ROLE_DISPLAY_NAMES = {
  KITCHEN_STAFF: 'Кухар',
  COURIER: 'Кур\'єр',
  MANAGER: 'Менеджер',
};

function UserProfile() {
  const queryClient = useQueryClient();
  const { data: user, isLoading } = useUser();

  const { 
    register, 
    reset, 
    wrapSubmit, 
    handleServerErrors, 
    formatError,
    formState: { errors, isDirty } 
  } = useFormWithServerErrors({
    defaultValues: {
      first_name: '',
      last_name: '',
      email: '',
      password: ''
    }
  });

  useEffect(() => {
    if (user) {
      reset({
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
        password: '' 
      });
    }
  }, [user, reset]);

  const onSubmit = async (data) => {
    try {
      const payload = {
        first_name: data.first_name,
        last_name: data.last_name,
        email: data.email
      };

      if (data.password) {
        payload.password = data.password;
      }

      await apiClient.patch(API_ENDPOINT, payload);
      
      toast.success("Профіль оновлено успішно!");
      queryClient.invalidateQueries(['user']);
      
      reset({ ...data, password: '' });
      
    } 
    catch (error) {
      handleServerErrors(error);
    }
  };

  if (isLoading) return <div className="container" style={{padding: '4rem'}}>Завантаження...</div>;

  return (
    <div>
      <Header/>
      <div className="base-form" style={{ padding: '2rem', width: "50%", minWidth: "400px", margin: "auto" }}>
        <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Мій Профіль</h2>
        
        <form onSubmit={wrapSubmit(onSubmit)} className="form-grid" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        
          <div className="form-group">
            <label htmlFor="role">Роль (незмінна)</label>
            <input 
              id="role"
              type="text" 
              disabled
              value={ROLE_DISPLAY_NAMES[user?.role] || user?.role || ''}
            />
          </div>

          <div className="form-group">
            <label htmlFor="first_name">Ім'я</label>
            <input
              id="first_name"
              type="text"
              {...register('first_name', { required: "Ім'я обов'язкове" })}
            />
            {errors.first_name && <span className="error-message">{formatError(errors.first_name.message)}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="last_name">Прізвище</label>
            <input
              id="last_name"
              type="text"
              {...register('last_name', { required: "Прізвище обов'язкове" })}
            />
            {errors.last_name && <span className="error-message">{formatError(errors.last_name.message)}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              {...register('email', { 
                required: "Email обов'язковий",
              })}
            />
            {errors.email && <span className="error-message">{formatError(errors.email.message)}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password">Новий пароль (необов'язково)</label>
            <input
              id="password"
              type="password"
              placeholder="Залиште пустим, щоб не змінювати"
              {...register('password', { 
                minLength: { value: 12, message: "Мінімум 8 символів" }
              })}
            />
            {errors.password && <span className="error-message">{formatError(errors.password.message)}</span>}
          </div>

          <button 
            type="submit" 
            className="admin-button" 
            style={{ marginTop: '1rem', alignSelf: 'center', width: '100%' }}
            disabled={!isDirty} 
          >
            Зберегти зміни
          </button>
        </form>
      </div>
      <Footer/>
    </div>
  );
}

export default UserProfile;