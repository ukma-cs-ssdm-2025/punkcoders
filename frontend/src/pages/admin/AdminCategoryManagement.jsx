import { useState, useEffect } from 'react';
import { useFormWithServerErrors } from '../../hooks/useFormWithServerErrors';
import apiClient from '../../api';
import { toast } from 'react-toastify';

const defaultFormState = {
  name: '',
};

function AdminCategoryManagement() {
  const [categories, setCategories] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const { 
    register,         
    reset,            
    setValue,         
    clearErrors,
    wrapSubmit,
    handleServerErrors,
    formatError,
    formState: { errors } 
  } = useFormWithServerErrors({
    defaultValues: defaultFormState
  });

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
      handleServerErrors(error)
    }
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
      
      <form className="base-form" onSubmit={wrapSubmit(onSubmit)}>
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
            {errors.name && <span className="error-message">{formatError(errors.name.message)}</span>}
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