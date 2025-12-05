import { useState, useEffect } from 'react';
import apiClient from '../../api';
import { toast } from 'react-toastify';
import { useFormWithServerErrors } from '../../hooks/useFormWithServerErrors';

const ROLE_OPTIONS = [
  { value: 'KITCHEN_STAFF', label: 'Кухар' },
  { value: 'COURIER', label: 'Кур\'єр' },
  { value: 'MANAGER', label: 'Менеджер' },
];

const ROLE_DISPLAY_NAMES = {
  KITCHEN_STAFF: 'Кухар',
  COURIER: 'Кур\'єр',
  MANAGER: 'Менеджер',
};

const defaultValues = {
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  role: 'KITCHEN_STAFF',
}


function AdminStaffManagement() {
  const [staffList, setStaffList] = useState([]);
  const [editingId, setEditingId] = useState(null);
  
  const { 
    register,
    reset,
    clearErrors,
    wrapSubmit,
    handleServerErrors,
    formatError,
    formState: { errors } 
  } = useFormWithServerErrors({
    defaultValues: defaultValues
  });

  useEffect(() => { fetchStaff(); }, []);

  const fetchStaff = async () => {
      try {
        const response = await apiClient.get('/auth/users/'); 
        setStaffList(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
        toast.error("Не вдалося завантажити список персоналу.");
        console.error("error fetching staff: ", error);
    }
  };

  const onSubmit = async (data) => {
    try {
      if (editingId) {
        await apiClient.patch(`/auth/users/${editingId}/`, { role: data.role });
        toast.success(`Роль користувача оновлено!`);
      } else {
        await apiClient.post('/auth/users/', data);
        toast.success(`Акаунт створено!`);
      }
      clearForm();
      fetchStaff();
    } catch (error) {
      handleServerErrors(error);
    }
  }

  const handleEdit = (user) => {
    setEditingId(user.id);
    clearErrors();
    reset({
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      role: user.role,
      password: '', // Password not needed/allowed for edit
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id, email) => {
      if (globalThis.confirm(`Ви впевнені, що хочете видалити/деактивувати акаунт '${email}'?`)) {
      try {
        await apiClient.delete(`/auth/users/${id}/`);
        toast.success("Акаунт видалено або деактивовано.");
        fetchStaff();
      } catch (error) {
        toast.error("Не вдалося видалити акаунт.");
        console.error("error deleting user: ", error);
      }
    }
  };

  const clearForm = () => {
    reset({ first_name: '', last_name: '', email: '', password: '', role: 'KITCHEN_STAFF' });
    setEditingId(null);
    clearErrors();
  };

  return (
    <div>
      <h2>Керування персоналом</h2>
      
      <form className="base-form" onSubmit={wrapSubmit(onSubmit)}>
        <h3>{editingId ? 'Редагувати роль' : 'Створити новий акаунт'}</h3>
        <div className="form-grid">
          
          <div className="form-group">
            <label htmlFor='first_name'>Ім'я</label>
            <input
              id="first_name"
              type="text"
              disabled={!!editingId} // LOCK INPUT IF EDITING
              style={editingId ? { backgroundColor: '#e9ecef', cursor: 'not-allowed' } : {}}
              {...register('first_name', { required: 'Ім\'я є обов\'язковим' })}
            />
             {errors.first_name && <span className="error-message">{formatError(errors.first_name.message)}</span>}
          </div>

          <div className="form-group">
            <label htmlFor='last_name'>Прізвище</label>
            <input
              id="last_name"
              type="text"
              disabled={!!editingId} // LOCK INPUT IF EDITING
              style={editingId ? { backgroundColor: '#e9ecef', cursor: 'not-allowed' } : {}}
              {...register('last_name', { required: 'Прізвище є обов\'язковим' })}
            />
             {errors.last_name && <span className="error-message">{formatError(errors.last_name.message)}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id='email'
              type="email"
              disabled={!!editingId} // LOCK INPUT IF EDITING
              style={editingId ? { backgroundColor: '#e9ecef', cursor: 'not-allowed' } : {}}
              {...register('email', { 
                required: 'Email є обов\'язковим',
              })}
            />
            {errors.email && <span className="error-message">{formatError(errors.email.message)}</span>}
          </div>
          
          {/* HIDE PASSWORD FIELD COMPLETELY WHEN EDITING */}
          {!editingId && (
            <div className="form-group">
              <label htmlFor='password'>Пароль</label>
              <input
                id="password"
                type="password"
                {...register('password', { 
                  required: 'Пароль є обов\'язковим',
                  minLength: { value: 12, message: 'Мінімум 12 символів' }
                })}
              />
              {errors.password && <span className="error-message">{formatError(errors.password.message)}</span>}
            </div>
          )}

          <div className="form-group form-group-full">
            <label htmlFor='role'>Роль</label>
            <select 
              id="role"
              {...register('role', { required: true })}>
              {ROLE_OPTIONS.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

        </div>
        
        <div className="actions" style={{ marginTop: '1rem' }}>
          <button type="submit" className="admin-button">
            {editingId ? 'Оновити роль' : 'Створити акаунт'}
          </button>
          {editingId && (
            <button type="button" className="admin-button admin-button-secondary" onClick={clearForm}>
              Скасувати
            </button>
          )}
        </div>
      </form>
      
       <h3>Наявний персонал</h3>
      <table className="admin-table">
        <thead>
          <tr>
            <th>ПІБ</th>
            <th>Email</th>
            <th>Роль</th>
            <th>Статус</th>
            <th>Дії</th>
          </tr>
        </thead>
        <tbody>
          {staffList.map(user => (
            <tr key={user.id} style={{ opacity: user.is_active ? 1 : 0.6 }}>
              <td>{user.first_name} {user.last_name}</td>
              <td>{user.email}</td>
              <td>{ROLE_DISPLAY_NAMES[user.role] || user.role}</td>
              <td>
                <span style={{ 
                    padding: '4px 8px', 
                    borderRadius: '4px', 
                    background: user.is_active ? '#e6fffa' : '#fff5f5',
                    color: user.is_active ? '#008060' : '#c53030',
                    fontSize: '0.85rem'
                  }}>
                  {user.is_active ? 'Активний' : 'Вимкнений'}
                </span>
              </td>
              <td className="actions">
                <button 
                  className="admin-button" 
                  onClick={() => handleEdit(user)}
                  disabled={!user.is_active} 
                >
                  Ред.
                </button>
                <button 
                  className="admin-button admin-button-secondary" 
                  onClick={() => handleDelete(user.id, user.email)}
                >
                  {user.is_active ? 'Видалити' : 'Х'}
                </button>
              </td>
            </tr>
          ))}
          {staffList.length === 0 && (
            <tr>
              <td colSpan="5" style={{textAlign: 'center', padding: '2rem'}}>Список персоналу порожній</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default AdminStaffManagement;