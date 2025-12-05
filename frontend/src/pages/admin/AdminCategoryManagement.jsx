import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form'; 
import apiClient from '../../api';
import { toast } from 'react-toastify';

const defaultFormState = {
  name: '',
};

const KNOWN_FIELDS = Object.keys(defaultFormState);

function AdminCategoryManagement() {
  const [categories, setCategories] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const { 
    register,         
    handleSubmit,     
    reset,            
    setValue,         
    setError,         
    clearErrors,
    formState: { errors } 
  } = useForm({
    defaultValues: defaultFormState
  });

  // --- Data Fetching (GET) ---
  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await apiClient.get('/menu/categories/');
      setCategories(response.data);
    } catch (error) {
      const msg = "Не вдалося завантажити категорії.";
      toast.error(msg); 
      console.error(msg, error);
    }
  };

  const handleSubmitWrapper = (e) => {
    clearErrors();
    handleSubmit(onSubmit, onError)(e);
  }

  const onSubmit = async (data) => {
    try {
      if (editingId) {
        await apiClient.patch(`/menu/categories/${editingId}/`, data);
      } else {
        await apiClient.post('/menu/categories/', data);
      }
      
      clearForm();
      fetchCategories();
      toast.success(`Категорія успішно ${editingId ? 'оновлена' : 'додана'}.`);
    } 
    catch (error) {
      console.error("API Submission Error:", error);

      if (error.response?.data) {
        const serverData = error.response.data;
        let hasFieldErrors = false;

        // CHECK 1: Handle standardized errors (attr/detail)
        if (Array.isArray(serverData.errors)) {
          serverData.errors.forEach((err) => {
            const fieldName = err.attr;
            const message = err.detail;

            if (fieldName && KNOWN_FIELDS.includes(fieldName)) {
              setError(fieldName, { type: 'server', message: message });
              hasFieldErrors = true;
            } else {
              const msg = fieldName ? `${fieldName}: ${message}` : message;
              toast.error(msg);
              console.error(`Unmapped Error [${fieldName}]:`, message);
            }
          });
        } 
        // CHECK 2: Fallback for standard DRF keys
        else if (typeof serverData === 'object') {
            Object.keys(serverData).forEach((key) => {
                const msg = Array.isArray(serverData[key]) ? serverData[key][0] : serverData[key];
                
                if (KNOWN_FIELDS.includes(key)) {
                    setError(key, { type: 'server', message: msg });
                    hasFieldErrors = true;
                } 
                else if (key === 'detail') {
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

  const handleEdit = (item) => {
    setValue('name', item.name);
    setEditingId(item.id);
    clearErrors();
  };

  const handleDelete = async (id) => {
    if (globalThis.confirm('Ви впевнені, що хочете видалити цю категорію?')) {
      try {
        await apiClient.delete(`/menu/categories/${id}/`);
        fetchCategories(); 
        toast.success("Категорію успішно видалено.");
      } catch (error) {
        if (error.response?.status === 404) {
          toast.error(`Цієї категорії вже не існує.`)
        }
        else {
          const msg = "Не вдалося видалити категорію.";
          toast.error(msg);
          console.error(msg, error);
        }
      }
    }
  };

  const clearForm = () => {
    reset(defaultFormState);
    setEditingId(null);
    clearErrors();
  };
  
  return (
    <div>
      <h2>Керування категоріями</h2>
      
      <form className="base-form" onSubmit={handleSubmitWrapper}>
        <h3>{editingId ? 'Редагувати категорію' : 'Додати нову категорію'}</h3>
        <div className="form-grid">
          
          <div className="form-group">
            <label htmlFor="name">Назва категорії</label>
            <input
              type="text"
              id="name"
              {...register('name', { 
                required: 'Назва не може бути порожньою' 
              })}
            />
            {errors.name && <span className="error-message">{errors.name.message}</span>}
          </div>
        </div>
        
        <div className="actions" style={{ marginTop: '1rem' }}>
          <button type="submit" className="admin-button">
            {editingId ? 'Зберегти зміни' : 'Додати категорію'}
          </button>
          {editingId && (
            <button 
              type="button" 
              className="admin-button admin-button-secondary" 
              onClick={clearForm}
            >
              Скасувати редагування
            </button>
          )}
        </div>
      </form>
      
      <h3>Наявні категорії</h3>
      <table className="admin-table">
        <thead>
          <tr>
            <th>Назва</th>
            <th>Дії</th>
          </tr>
        </thead>
        <tbody>
          {categories.map(item => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td className="actions">
                <button className="admin-button" onClick={() => handleEdit(item)}>
                  Редагувати
                </button>
                <button className="admin-button admin-button-secondary" onClick={() => handleDelete(item.id)}>
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

export default AdminCategoryManagement;