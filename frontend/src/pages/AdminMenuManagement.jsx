import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form'; // 1. Import the hook
import apiClient from '../api';
import { toast } from 'react-toastify'; // For general error messages

// Default values for the form
const defaultFormState = {
  name: '',
  description: '',
  price: '',
  category: '', 
  is_available: true,
  photo: null,
};

function AdminMenuManagement() {
  // --- STATE ---
  // We only keep state for data that *isn't* in the form
  const [menuItems, setMenuItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [editingId, setEditingId] = useState(null);

  // --- 2. Initialize react-hook-form ---
  const { 
    register,         // Connects inputs
    handleSubmit,     // Wraps our submit function
    reset,            // Clears the form
    setValue,         // Sets form values for "Edit"
    setError,         // Sets server-side errors
    formState: { errors } // Object containing validation errors
  } = useForm({
    defaultValues: defaultFormState
  });

  // --- 3. Data Fetching (on component load) ---
  useEffect(() => {
    fetchDishes();
    fetchCategories();
  }, []); // Empty array means "run once on load"

  const fetchDishes = async () => {
    try {
      const response = await apiClient.get('/dishes/');
      setMenuItems(response.data);
    } catch (error) {
      toast.error("Не вдалося завантажити страви.");
      console.error('Error fetching dishes:', error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await apiClient.get('/categories/');
      setCategories(response.data);
      // Set default category in the form *after* they load
      if (response.data.length > 0) {
        setValue('category', response.data[0].id);
      }
    } catch (error) {
      toast.error("Не вдалося завантажити категорії.");
      console.error('Error fetching categories:', error);
    }
  };

  // --- 4. Form Submit Logic (Create/Update) ---
  // This function is called by react-hook-form's handleSubmit
  // It receives the form data *only* if client-side validation passes
  const onSubmit = async (data) => {
    // 1. Build the FormData object for file upload
    const dishData = new FormData();
    dishData.append('name', data.name);
    dishData.append('description', data.description);
    dishData.append('price', data.price);
    dishData.append('is_available', data.is_available);
    dishData.append('category_id', data.category); // Your API wants category_id

    // 2. Handle the optional file upload
    if (data.photo && data.photo.length > 0) {
      dishData.append('photo', data.photo[0]); // data.photo is a FileList
    }

    try {
      // 3. Call the correct API endpoint
      if (editingId) {
        // UPDATE (PATCH)
        await apiClient.patch(`/dishes/${editingId}/`, dishData);
        toast.success("Страву успішно оновлено!");
      } else {
        // CREATE (POST)
        await apiClient.post('/dishes/', dishData);
        toast.success("Страву успішно створено!");
      }
      
      // 4. Success: Clear form and reload the table
      clearForm();
      fetchDishes();

    } catch (error) {
      // 5. Handle errors from the server
      if (error.response?.status === 400) {
        // This is a validation error (e.g., "name already exists")
        const serverErrors = error.response.data;
        for (const [field, message] of Object.entries(serverErrors)) {
          // Show the error message under the correct form field
          setError(field, { type: 'server', message: message[0] });
        }
      } else {
        // This is a network error or 500 server error
        toast.error("Сталася неочікувана помилка. Спробуйте ще раз.");
        console.error('Submission error:', error);
      }
    }
  };

  // --- 5. Helper Functions (Edit, Delete, Clear) ---
  const handleEdit = (item) => {
    setEditingId(item.id);
    
    // Use reset() to populate the form with the item's data
    // This is the correct way to fix your old bug
    reset({
      name: item.name,
      description: item.description,
      price: item.price,
      is_available: item.is_available,
      category: item.category.id, // Set the category ID for the dropdown
      photo: null, // Clear file input on edit
    });
  };

  const handleDelete = async (id) => {
    if (globalThis.confirm('Ви впевнені, що хочете видалити цю страву?')) {
      try {
        await apiClient.delete(`/dishes/${id}/`);
        toast.success("Страву видалено.");
        fetchDishes(); // Reload the list
      } catch (error) {
        toast.error("Не вдалося видалити страву.");
        console.error('Error deleting dish:', error);
      }
    }
  };

  const clearForm = () => {
    reset(defaultFormState); // Resets all fields to their defaults
    setEditingId(null);
    // Re-set default category after clear
    if (categories.length > 0) {
      setValue('category', categories[0].id);
    }
  };
  
  return (
    <div>
      <h2>Керування меню</h2>
      
      {/* 6. Connect the form to react-hook-form */}
      <form className="admin-form" onSubmit={handleSubmit(onSubmit)}>
        <h3>{editingId ? 'Редагувати страву' : 'Додати нову страву'}</h3>
        <div className="form-grid">
          
          <div className="form-group form-group-full">
            <label htmlFor="name">Назва страви</label>
            <input
              type="text"
              id="name"
              // 7. "Register" the input. This replaces 'value' and 'onChange'.
              {...register('name', { required: 'Назва страви є обов\'язковою' })}
            />
            {/* Show error message if this field fails validation */}
            {errors.name && <span className="error-message">{errors.name.message}</span>}
          </div>
          
          <div className="form-group form-group-full">
            <label htmlFor="description">Опис</label>
            <textarea
              id="description"
              rows="3"
              // 1. Add the validation rule here
              {...register('description', { required: 'Опис є обов\'язковим' })}
            ></textarea>
            
            {/* 2. Add this line to show the error */}
            {errors.description && <span className="error-message">{errors.description.message}</span>}
          </div>
          
          <div className="form-group">
            <label htmlFor="price">Ціна (грн)</label>
            <input
              type="number"
              id="price"
              step="0.01"
              {...register('price', { 
                required: 'Ціна є обов\'язковою',
                valueAsNumber: true,
              })}
            />
            {errors.price && <span className="error-message">{errors.price.message}</span>}
          </div>
          
          <div className="form-group">
            <label htmlFor="category">Категорія</label>
            <select
              id="category"
              {...register('category', { required: 'Категорія є обов\'язковою' })}
            >
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>
                  {cat.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group form-group-full">
            <label htmlFor="photo">Фото (необов'язково)</label>
            <input
              type="file"
              id="photo"
              accept="image/*"
              {...register('photo')}
            />
          </div>
          
          <div className="form-group form-group-checkbox form-group-full">
            <input
              type="checkbox"
              id="is_available"
              {...register('is_available')}
            />
            <label htmlFor="is_available">Доступна</label> 
            {/* Changed logic: unchecked = "Недоступна" */}
          </div>

        </div>
        
        <div className="actions" style={{ marginTop: '1rem' }}>
          <button type="submit" className="admin-button">
            {editingId ? 'Зберегти зміни' : 'Додати страву'}
          </button>
          {editingId && (
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={clearForm}
            >
              Скасувати редагування
            </button>
          )}
        </div>
      </form>
      
      {/* The table remains the same */}
      <h3>Наявні страви </h3>
      <table className="admin-table">
        {/* ... (thead) ... */}
        <tbody>
          {menuItems.map(item => (
            <tr key={item.id} className={item.is_available ? '' : 'status-unavailable'}>
              <td>{item.name}</td>
              <td>{Number.parseFloat(item.price).toFixed(2)} грн</td>
              <td>{item.category.name}</td>
              <td>{item.is_available ? 'Доступна' : 'Недоступна'}</td>
              <td className="actions">
                <button className="admin-button" onClick={() => handleEdit(item)}>
                  Редагувати
                </button>
                <button className="btn btn-secondary" onClick={() => handleDelete(item.id)}>
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

export default AdminMenuManagement;