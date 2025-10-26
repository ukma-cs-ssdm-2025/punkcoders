import React, { useState, useEffect } from 'react';
import apiClient from '../api';

// const initialMenuItems = [
//   { 
//     id: 1, 
//     name: 'Піца "Маргарита"', 
//     description: 'Класична піца з томатним соусом, моцарелою та базиліком.',
//     price: 150.00,
//     category: 'pizza',
//     photoUrl: 'content/margarita-pizza.png',
//     isAvailable: true 
//   },
//   { 
//     id: 2, 
//     name: 'Піца "Пепероні"', 
//     description: 'Піца з гострою ковбаскою пепероні.',
//     price: 180.00,
//     category: 'pizza',
//     photoUrl: 'content/sausage-pizza.png',
//     isAvailable: true 
//   },
//   { 
//     id: 3, 
//     name: 'Кока-Кола', 
//     description: '0.5л, холодна.',
//     price: 30.00,
//     category: 'drinks',
//     photoUrl: 'content/coke.png',
//     isAvailable: false 
//   },
// ];


const defaultFormState = {
  id: null,
  name: '',
  description: '',
  price: '',
  category: '1',
  isAvailable: true
};

function AdminMenuManagement() {

  useEffect(() => {
    fetchDishes();
  }, []);

  const [menuItems, setMenuItems] = useState([]);
  const [formData, setFormData] = useState(defaultFormState);
  const [editingId, setEditingId] = useState(null);
  const [photoFile, setPhotoFile] = useState(null);

  const fetchDishes = async () => {
    try {
      const response = await apiClient.get('/dishes/');
      setMenuItems(response.data);
    } catch (error) {
      console.error('Error fetching dishes:', error);
    }
  }

  const createDish = async (dish) => {
    try {
      const response = await apiClient.post('/dishes/', dish);
      setMenuItems(prevItems => [response.data, ...prevItems]);
    } catch (error) {
      console.error('Error creating dish:', error);
    }
  }

  const updateDish = async (id, updatedDish) => {
    try {
      const response = await apiClient.patch(`/dishes/${id}/`, updatedDish);
      setMenuItems(prevItems => 
        prevItems.map(item => 
          item.id === id ? response.data : item
        )
      );
    } catch (error) {
      console.error('Error updating dish:', error);
    }
  }

  const deleteDish = async (id) => {
    try {
      await apiClient.delete(`/dishes/${id}/`);
      setMenuItems(prevItems => prevItems.filter(item => item.id !== id));
    } catch (error) {
      console.error('Error deleting dish:', error);
    }
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value
    }));
  };


  const handleSubmit = (e) => {
    e.preventDefault();

    const dishData = new FormData();

    // 2. Add all the text/number/boolean fields from state
    dishData.append('name', formData.name);
    dishData.append('description', formData.description);
    dishData.append('price', formData.price);
    dishData.append('isAvailable', formData.isAvailable);
    
    // CRITICAL: Send 'category_id' as expected by your serializer
    dishData.append('category_id', formData.category);

    // 3. Add the file *only if* one was selected
    if (photoFile) {
      dishData.append('photo', photoFile);
    }

    if (editingId) {
      updateDish(editingId, dishData);//, price: parseFloat(formData.price) });
      // setMenuItems(prevItems => 
      //   prevItems.map(item => 
      //     item.id === editingId ? { ...formData, id: editingId, price: parseFloat(formData.price) } : item
      //   )
      // );
    } else {
      createDish(dishData);
      // setMenuItems(prevItems => [newItem, ...prevItems]);
    }
    

    clearForm();
  };


  const handleEdit = (item) => {
    setEditingId(item.id);
    setFormData(item);
  };


  const handleDelete = (id) => {
    if (window.confirm('Ви впевнені, що хочете видалити цю страву?')) {
      deleteDish(id);
      // setMenuItems(prevItems => prevItems.filter(item => item.id !== id));
    }
  };

  const clearForm = () => {
    setFormData(defaultFormState);
    setEditingId(null);
  };
  
  return (
    <div>
      <h2>Керування меню</h2>
      
      <form className="admin-form" onSubmit={handleSubmit}>
        <h3>{editingId ? 'Редагувати страву' : 'Додати нову страву'}</h3>
        <div className="form-grid">
          
          <div className="form-group form-group-full">
            <label htmlFor="name">Назва страви</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group form-group-full">
            <label htmlFor="description">Опис</label>
            <textarea
              id="description"
              name="description"
              rows="3"
              value={formData.description}
              onChange={handleInputChange}
            ></textarea>
          </div>
          
          <div className="form-group">
            <label htmlFor="price">Ціна (грн)</label>
            <input
              type="number"
              id="price"
              name="price"
              step="0.01"
              value={formData.price}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="category">Категорія</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
            >
              <option value="pizza">🍕 Піца</option>
              <option value="drinks">🥤 Напої</option>
              <option value="sauces">🧂 Соуси</option>
            </select>
          </div>

          <div className="form-group form-group-full">
            <label htmlFor="photo">Фото (необов'язково)</label>
            <input
              type="file"
              id="photo"
              name="photo"
              accept="image/*"
              onChange={(e) => setPhotoFile(e.target.files[0] || null)}
            />
          </div>
          
          <div className="form-group form-group-checkbox form-group-full">
            <input
              type="checkbox"
              id="isAvailable"
              name="isAvailable"
              checked={formData.isAvailable}
              onChange={handleInputChange}
            />
            <label htmlFor="isAvailable">Тимчасово недоступна</label>
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
      

      <h3>Наявні страви </h3>
      <table className="admin-table">
        <thead>
          <tr>
            <th>Назва</th>
            <th>Ціна</th>
            <th>Категорія</th>
            <th>Статус</th>
            <th>Дії</th>
          </tr>
        </thead>
        <tbody>
          {menuItems.map(item => (
            <tr key={item.id} className={!item.isAvailable ? 'status-unavailable' : ''}>
              <td>{item.name}</td>
              <td>{item.price.toFixed(2)} грн</td>
              <td>{item.category}</td>
              <td>{item.isAvailable ? 'Доступна' : 'Недоступна'}</td>
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