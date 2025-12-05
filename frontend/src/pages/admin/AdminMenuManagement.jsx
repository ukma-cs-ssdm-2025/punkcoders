import { useState, useEffect } from 'react';
import apiClient from '../../api';
import { toast } from 'react-toastify'; 
import { useFormWithServerErrors } from '../../hooks/useFormWithServerErrors';

const defaultFormState = {
  name: '',
  description: '',
  price: '',
  category: '', 
  is_available: true,
  photo: null,
};

function AdminMenuManagement() {
  const [menuItems, setMenuItems] = useState([]);
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
    fetchDishes();
    fetchCategories();
  }, []); 

  const fetchDishes = async () => {
    try {
      const response = await apiClient.get('/menu/dishes/');
      setMenuItems(response.data);
    } 
    catch (error) {
      const msg = "Не вдалося завантажити страви.";
      toast.error(msg);
      console.error(msg, error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await apiClient.get('/menu/categories/');
      setCategories(response.data);
      if (response.data.length > 0) {
        setValue('category', response.data[0].id);
      }
    } 
    catch (error) {
      const msg = "Не вдалося завантажити категорії.";
      toast.error(msg);
      console.error(msg, error);
    }
  };

  const onSubmit = async (data) => {
    const dishData = new FormData();
    dishData.append('name', data.name);
    dishData.append('description', data.description);
    dishData.append('price', data.price);
    dishData.append('is_available', data.is_available);
    dishData.append('category_id', data.category); 

    if (data.photo?.length > 0) {
      dishData.append('photo', data.photo[0]);
    }

    try {
      if (editingId) {
        await apiClient.patch(`/menu/dishes/${editingId}/`, dishData);
        toast.success("Страву успішно оновлено!");
      } else {
        await apiClient.post('/menu/dishes/', dishData);
        toast.success("Страву успішно створено!");
      }
      
      clearForm();
      fetchDishes();

    } 
    catch (error) {
      handleServerErrors(error);
    }
  };

  // --- Helper Functions (Edit, Delete, Clear) ---
  const handleEdit = (item) => {
    setEditingId(item.id);
    clearErrors();
    
    reset({
      name: item.name,
      description: item.description,
      price: item.price,
      is_available: item.is_available,
      category: item.category.id, 
      photo: null, 
    });
  };

  const handleDelete = async (id) => {
    if (globalThis.confirm('Ви впевнені, що хочете видалити цю страву?')) {
      try {
        await apiClient.delete(`/menu/dishes/${id}/`);
        toast.success("Страву видалено.");
        fetchDishes(); 
      } catch (error) {
        if (error.response?.status === 404) {
          toast.error(`Цієї страви вже не існує.`)
        }
        else {
          const msg = "Не вдалося видалити страву.";
          toast.error(msg);
          console.error(msg, error);
        }
      }
    }
  };

  const handleAvailabilityToggle = async (dishId, newAvailability) => {
    const originalMenuItems = [...menuItems];
    const dishData = new FormData();
    dishData.append('is_available', newAvailability);

    setMenuItems(prevItems =>
      prevItems.map(item =>
        item.id === dishId ? { ...item, is_available: newAvailability } : item
      )
    );

    try {
      await apiClient.patch(`/menu/dishes/${dishId}/`, dishData);
    } 
    catch (error) {
      if (error.response?.status === 404) {
        toast.error(`Цій страві не можна змінити доступність, бо її не існує.`)
      }
      else {
        const msg = "Не вдалось змінити доступність. Спробуйте ще раз.";
        toast.error(msg);
        console.error(msg, error);
      }
      setMenuItems(originalMenuItems);
    }
  };

  const clearForm = () => {
    reset(defaultFormState); 
    setEditingId(null);
    // can be returned if requested, but i found it annoying af
    // if (categories.length > 0) {
    //   setValue('category', categories[0].id);
    // }
    clearErrors();
  };
  
  return (
    <div>
      <h2>Керування меню</h2>
      
      <form className="base-form" onSubmit={wrapSubmit(onSubmit)}>
        <h3>{editingId ? 'Редагувати страву' : 'Додати нову страву'}</h3>
        <div className="form-grid">
          
          <div className="form-group form-group-full">
            <label htmlFor="name">Назва страви</label>
            <input
              type="text"
              id="name"
              {...register('name', { required: 'Назва страви є обов\'язковою' })}
            />
            {errors.name && <span className="error-message">{formatError(errors.name.message)}</span>}
          </div>
          
          <div className="form-group form-group-full">
            <label htmlFor="description">Опис</label>
            <textarea
              id="description"
              rows="3"
              {...register('description', { required: 'Опис є обов\'язковим' })}
            ></textarea>
            {errors.description && <span className="error-message">{formatError(errors.description.message)}</span>}
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
                min: { 
                value: 0,
                message: 'Ціна не може бути від\'ємною'
              }
              })}
            />
            {errors.price && <span className="error-message">{formatError(errors.price.message)}</span>}
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
            {errors.category && <span className="error-message">{formatError(errors.category.message)}</span>}
          </div>

          <div className="form-group form-group-full">
            <label htmlFor="photo">Фото (необов'язково)</label>
            <input
              type="file"
              id="photo"
              accept="image/*"
              {...register('photo')}
            />
            {errors.photo && <span className="error-message">{formatError(errors.photo.message)}</span>}
          </div>
          
          <div className="form-group form-group-checkbox form-group-full">
            <input
              type="checkbox"
              id="is_available"
              {...register('is_available')}
            />
            <label htmlFor="is_available">Доступна</label> 
            {errors.is_available && <span className="error-message">{formatError(errors.is_available.message)}</span>}
          </div>

        </div>
        
        <div className="actions" style={{ marginTop: '1rem' }}>
          <button type="submit" className="admin-button">
            {editingId ? 'Зберегти зміни' : 'Додати страву'}
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
      
      {/* The table remains the same */}
      <h3>Наявні страви </h3>
      <table className="admin-table">
        <thead>
           <tr>
              <th>Назва</th>
              <th>Ціна</th>
              <th>Категорія</th>
              <th>Перемкнути</th>
              <th>Доступність</th>
              <th>Дії</th>
          </tr>
        </thead>
        <tbody>
          {menuItems.map(item => (
            <tr key={item.id} className={item.is_available ? '' : 'status-unavailable'}>
              <td>{item.name}</td>
              <td>{Number.parseFloat(item.price).toFixed(2)} грн</td>
              <td>{item.category.name}</td>
              <td>
                <input
                  type="checkbox"
                  checked={item.is_available}
                  onChange={(e) =>
                    handleAvailabilityToggle(item.id, e.target.checked)
                  }
                  style={{ cursor: 'pointer', transform: 'scale(1.2)' }}
                />
              </td>
              <td>{item.is_available ? 'Доступна' : 'Недоступна'}</td>
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

export default AdminMenuManagement;