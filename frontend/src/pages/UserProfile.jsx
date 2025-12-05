import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import apiClient from '../api'; 
import { toast } from 'react-toastify';
import { useQueryClient } from '@tanstack/react-query';
import { useUser } from '../hooks/useUser';
import Header from '../components/Header';
import Footer from '../components/Footer';

const KNOWN_FIELDS = ['first_name', 'last_name', 'email', 'password'];

function UserProfile() {
  const queryClient = useQueryClient();
  
  // 1. Use the hook instead of manual fetching
  const { data: user, isLoading } = useUser();

  const { 
    register, 
    handleSubmit, 
    reset, 
    setError,
    clearErrors,
    formState: { errors, isDirty } 
  } = useForm({
    defaultValues: {
      first_name: '',
      last_name: '',
      email: '',
      role: '',
      password: ''
    }
  });

  const API_ENDPOINT = '/auth/me/'; 

  // 2. Sync the hook data with the Form
  // When 'user' loads (or updates), we reset the form to match.
  useEffect(() => {
    if (user) {
      reset({
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
        role: user.role,
        password: '' // Explicitly keep password empty
      });
    }
  }, [user, reset]);

  const handleSubmitWrapper = (e) => {
    clearErrors();
    handleSubmit(onSubmit, onError)(e);
  };

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
      
      // 3. Invalidate 'user' so the Header (and this form) updates immediately
      queryClient.invalidateQueries(['user']);
      
      // Reset isDirty to false with the new data
      reset({ ...data, password: '' });
      
    } 
    catch (error) {
      console.error("API Submission Error:", error);

      if (error.response?.data) {
      const serverData = error.response.data;
      let hasFieldErrors = false;

      if (Array.isArray(serverData.errors)) {
        serverData.errors.forEach((err) => {
        const fieldName = err.attr;
        const message = err.detail;

        if (fieldName && KNOWN_FIELDS.includes(fieldName)) {
          setError(fieldName, { type: 'server', message: message });
          hasFieldErrors = true;
        } 
        else {
          const msg = fieldName ? `${fieldName}: ${message}` : message;
            toast.error(msg);
            console.error(`Unmapped Error [${fieldName}]:`, message);
          }
        });
      } 
      else if (typeof serverData === 'object') {
        Object.keys(serverData).forEach((key) => {
          const msg = Array.isArray(serverData[key]) ? serverData[key][0] : serverData[key];
          
          if (KNOWN_FIELDS.includes(key)) {
            setError(key, { type: 'server', message: msg });
            hasFieldErrors = true;
          } else if (key === 'detail') {
            toast.error(serverData.detail);
          }
        });
      }

      if (hasFieldErrors) {
        toast.error("Перевірте дані форми (помилки підсвічено).");
      } 
      else if (!hasFieldErrors && !serverData.errors) {
        const msg = "Сталася невідома помилка валідації.";
        toast.error(msg);
        console.error(msg, serverData);
      }

      } 
      else {
        const msg = "Сталася помилка сервера або проблема з мережею.";
        toast.error(msg);
        console.error(msg, error);
      }
    }
  };

  const onError = (errors, e) => {
    console.log("Client-side validation blocked submission:", errors);
    toast.error("Форма містить помилки. Виправте їх перед відправкою.");
  };

  const formatTextWithLineBreaks = (text) => {
    if (!text) return null;
    return text.split('\\' + 'n').map((line, index) => (
      <span key={index}>
      {line}
      {index < text.split('\\' + 'n').length - 1 && <br />} 
      </span>
    ));
  };

  if (isLoading) return <div className="container" style={{padding: '4rem'}}>Завантаження...</div>;

  return (
    <div>
      <Header/>
      <div className="base-form" style={{ padding: '2rem', width: "50%", "min-width": "400px", margin: "auto" }}>
        <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Мій Профіль</h2>
        
        <form onSubmit={handleSubmitWrapper} className="form-grid" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        
          <div className="form-group">
            <label>Роль (незмінна)</label>
            <input 
            type="text" 
            disabled 
            {...register('role')} 
            style={{ background: '#f0f0f0', cursor: 'not-allowed' }}
            />
          </div>

          <div className="form-group">
            <label htmlFor="first_name">Ім'я</label>
            <input
            id="first_name"
            type="text"
            {...register('first_name', { required: "Ім'я обов'язкове" })}
            />
            {errors.first_name && <span className="error-message">{formatTextWithLineBreaks(errors.first_name.message)}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="last_name">Прізвище</label>
            <input
            id="last_name"
            type="text"
            {...register('last_name', { required: "Прізвище обов'язкове" })}
            />
            {errors.last_name && <span className="error-message">{formatTextWithLineBreaks(errors.last_name.message)}</span>}
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
            {errors.email && <span className="error-message">{formatTextWithLineBreaks(errors.email.message)}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password">Новий пароль (необов'язково)</label>
            <input
            id="password"
            type="password"
            placeholder="Залиште пустим, щоб не змінювати"
            {...register('password', { 
              minLength: { value: 8, message: "Мінімум 8 символів" }
            })}
            />
            {errors.password && <span className="error-message">{formatTextWithLineBreaks(errors.password.message)}</span>}
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