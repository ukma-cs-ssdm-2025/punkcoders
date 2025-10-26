import React, { useState } from 'react';

const initialMenuItems = [
  { 
    id: 1, 
    name: 'Піца "Маргарита"', 
    description: 'Класична піца з томатним соусом, моцарелою та базиліком.',
    price: 150.00,
    category: 'pizza',
    photoUrl: 'content/margarita-pizza.png',
    isAvailable: true 
  },
  { 
    id: 2, 
    name: 'Піца "Пепероні"', 
    description: 'Піца з гострою ковбаскою пепероні.',
    price: 180.00,
    category: 'pizza',
    photoUrl: 'content/sausage-pizza.png',
    isAvailable: true 
  },
  { 
    id: 3, 
    name: 'Кока-Кола', 
    description: '0.5л, холодна.',
    price: 30.00,
    category: 'drinks',
    photoUrl: 'content/coke.png',
    isAvailable: false 
  },
];


const defaultFormState = {
  id: null,
  name: '',
  description: '',
  price: '',
  category: 'pizza',
  photoUrl: '',
  isAvailable: true
};

function AdminMenuManagement() {

  const [menuItems, setMenuItems] = useState(initialMenuItems);
  
  const [formData, setFormData] = useState(defaultFormState);
  
  const [editingId, setEditingId] = useState(null);


  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value
    }));
  };


  const handleSubmit = (e) => {
    e.preventDefault();

    if (editingId) {
      setMenuItems(prevItems => 
        prevItems.map(item => 
          item.id === editingId ? { ...formData, id: editingId, price: parseFloat(formData.price) } : item
        )
      );
    } else {
      const newItem = {
        ...formData,
        id: Date.now(),
        price: parseFloat(formData.price)
      };
      setMenuItems(prevItems => [newItem, ...prevItems]);
    }
    

    clearForm();
  };


  const handleEdit = (item) => {
    setEditingId(item.id);
    setFormData(item);
  };


  const handleDelete = (id) => {
    if (window.confirm('Ви впевнені, що хочете видалити цю страву?')) {
      setMenuItems(prevItems => prevItems.filter(item => item.id !== id));
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
            <label htmlFor="photoUrl">URL фото</label>
            <input
              type="text"
              id="photoUrl"
              name="photoUrl"
              value={formData.photoUrl}
              onChange={handleInputChange}
              required
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