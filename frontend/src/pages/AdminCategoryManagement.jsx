import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form'; // 1. Import useForm
import apiClient from '../api'; // Your API client
import { toast } from 'react-toastify';

// This is just for resetting the form, react-hook-form handles the state
const defaultFormState = {
  name: '',
};

function AdminCategoryManagement() {
  // --- State for the LIST of categories ---
  const [categories, setCategories] = useState([]);
  const [editingId, setEditingId] = useState(null);

  // --- 2. Initialize react-hook-form ---
  const { 
    register,         // Connects inputs to the form
    handleSubmit,     // Wraps your submit function
    reset,            // Clears the form
    setValue,         // Sets a field's value (for editing)
    setError,         // Sets server-side errors
    formState: { errors } // Contains all validation errors
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
      toast.error("Не вдалося завантажити категорії."); 
      console.error('Error fetching categories:', error);
    }
  };

  // --- 3. Create the real submit handler ---
  // This function receives the 'data' object from react-hook-form
  const onSubmit = async (data) => {
    try {
      if (editingId) {
        // UPDATE (PATCH)
        await apiClient.patch(`/menu/categories/${editingId}/`, data);
      } else {
        // CREATE (POST)
        await apiClient.post('/menu/categories/', data);
      }
      
      // Success: Clear the form and reload the list
      clearForm();
      fetchCategories();
      toast.success(`Категорія успішно ${editingId ? 'оновлена' : 'додана'}.`);
    } catch (error) {
      // --- 4. Handle Django's "you filled it out wrong" errors ---
      if (error.response?.status === 400) {
        const serverErrors = error.response.data; // e.g., { name: ["This name is already taken."] }
        
        // Loop over the errors from Django and set them in the form
        for (const [field, message] of Object.entries(serverErrors)) {
          setError(field, {
            type: 'server',
            message: message[0] // Show the first error message
          });
        }
      } 
      else if (error.response?.status === 404) {
        toast.error(`Цю категорію не можна відредагувати, бо її не існує.`)
      }
      else {
        toast.error("Сталася непередбачена помилка.");
        console.error('An unexpected error occurred:', error);
      }
    }
  };

  // --- CRUD Helper Functions ---
  const handleEdit = (item) => {
    // 5. Populate the form fields using setValue
    setValue('name', item.name);
    setEditingId(item.id);
  };

  const handleDelete = async (id) => {
    if (globalThis.confirm('Ви впевнені, що хочете видалити цю категорію?')) {
      try {
        await apiClient.delete(`/menu/categories/${id}/`);
        fetchCategories(); // Reload the list after deleting
        toast.success("Категорію успішно видалено.");
      } catch (error) {
        if (error.response?.status === 404) {
          toast.error(`Цієї категорії вже не існує.`)
        }
        else {
          toast.error("Не вдалося видалити категорію.");
          console.error('Error deleting category:', error);
        }
      }
    }
  };

  const clearForm = () => {
    // 6. Reset the form state and our editingId state
    reset(defaultFormState);
    setEditingId(null);
  };
  
  return (
    <div>
      <h2>Керування категоріями</h2>
      
      {/* 7. Use handleSubmit(onSubmit) to wrap the form */}
      <form className="admin-form" onSubmit={handleSubmit(onSubmit)}>
        <h3>{editingId ? 'Редагувати категорію' : 'Додати нову категорію'}</h3>
        <div className="form-grid">
          
          <div className="form-group">
            <label htmlFor="name">Назва категорії</label>
            <input
              type="text"
              id="name"
              // 8. "Register" the input (replaces value, name, and onChange)
              {...register('name', { 
                required: 'Назва не може бути порожньою' 
              })}
            />
            {/* 9. Automatically show validation errors */}
            {errors.name && <span className="error-message">{errors.name.message}</span>}
          </div>
          
          {/* The emoji field is removed, as requested */ }

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
            {/* Emoji column is removed */}
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