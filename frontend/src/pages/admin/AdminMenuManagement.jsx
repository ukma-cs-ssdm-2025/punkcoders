import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form'; 
import apiClient from '../../api';
import { toast } from 'react-toastify'; 

const defaultFormState = {
  name: '',
  description: '',
  price: '',
  category: '', 
  is_available: true,
  photo: null,
};

// const KNOWN_FIELDS = ['name', 'description', 'price', 'category', 'is_available', 'photo'];
const KNOWN_FIELDS = Object.keys(defaultFormState);

function AdminMenuManagement() {
  const [menuItems, setMenuItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const { 
    register, handleSubmit, reset, setValue, setError, clearErrors,
    formState: { errors } 
  } = useForm({
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

  const handleSubmitWrapper = (e) => {
    clearErrors();
    handleSubmit(onSubmit, onError)(e);
  }

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

      } else {
        const msg = "Сталася неочікувана помилка. Спробуйте ще раз.";
        toast.error(msg);
        console.error(msg, error);
      }
    }
  };

  const onError = (errors, e) => {
    console.log("Client-side validation blocked submission:", errors);
    toast.error("Форма містить помилки. Виправте їх перед відправкою.");
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
      
      <form className="admin-form" onSubmit={handleSubmitWrapper}>
        <h3>{editingId ? 'Редагувати страву' : 'Додати нову страву'}</h3>
        <div className="form-grid">
          
          <div className="form-group form-group-full">
            <label htmlFor="name">Назва страви</label>
            <input
              type="text"
              id="name"
              {...register('name', { required: 'Назва страви є обов\'язковою' })}
            />
            {errors.name && <span className="error-message">{errors.name.message}</span>}
          </div>
          
          <div className="form-group form-group-full">
            <label htmlFor="description">Опис</label>
            <textarea
              id="description"
              rows="3"
              {...register('description', { required: 'Опис є обов\'язковим' })}
            ></textarea>
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
                min: { 
                value: 0,
                message: 'Ціна не може бути від\'ємною'
              }
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
            {errors.category && <span className="error-message">{errors.category.message}</span>}
          </div>

          <div className="form-group form-group-full">
            <label htmlFor="photo">Фото (необов'язково)</label>
            <input
              type="file"
              id="photo"
              accept="image/*"
              {...register('photo')}
            />
            {errors.photo && <span className="error-message">{errors.photo.message}</span>}
          </div>
          
          <div className="form-group form-group-checkbox form-group-full">
            <input
              type="checkbox"
              id="is_available"
              {...register('is_available')}
            />
            <label htmlFor="is_available">Доступна</label> 
            {errors.is_available && <span className="error-message">{errors.is_available.message}</span>}
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
              <th>Перемкнути доступність</th>
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