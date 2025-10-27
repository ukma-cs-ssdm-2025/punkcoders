import React, { useState } from 'react';

const initialCategories = [
  { 
    id: 1, 
    name: 'Піца',
    emoji: '🍕'
  },
  { 
    id: 2, 
    name: 'Напої',
    emoji: '🥤'
  },
  { 
    id: 3, 
    name: 'Соуси',
    emoji: '🧂'
  },
];

const defaultFormState = {
  id: null,
  name: '',
  emoji: '🍕'
};

function AdminCategoryManagement() {

  const [categories, setCategories] = useState(initialCategories);
  
  const [formData, setFormData] = useState(defaultFormState);
  
  const [editingId, setEditingId] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (editingId) {
      setCategories(prevItems => 
        prevItems.map(item => 
          item.id === editingId ? { ...formData, id: editingId } : item
        )
      );
    } else {
      const newItem = {
        ...formData,
        id: Date.now()
      };
      setCategories(prevItems => [newItem, ...prevItems]);
    }
    
    clearForm();
  };

  const handleEdit = (item) => {
    setEditingId(item.id);
    setFormData(item);
  };

  const handleDelete = (id) => {
    if (window.confirm('Ви впевнені, що хочете видалити цю категорію?')) {
      setCategories(prevItems => prevItems.filter(item => item.id !== id));
    }
  };

  const clearForm = () => {
    setFormData(defaultFormState);
    setEditingId(null);
  };
  
  return (
    <div>
      <h2>Керування категоріями</h2>
      
      <form className="admin-form" onSubmit={handleSubmit}>
        <h3>{editingId ? 'Редагувати категорію' : 'Додати нову категорію'}</h3>
        <div className="form-grid">
          
          <div className="form-group">
            <label htmlFor="name">Назва категорії</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="emoji">Емоджі</label>
            <input
              type="text"
              id="emoji"
              name="emoji"
              value={formData.emoji}
              onChange={handleInputChange}
              placeholder="🍕"
              maxLength="2"
            />
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
            <th>Емоджі</th>
            <th>Назва</th>
            <th>Дії</th>
          </tr>
        </thead>
        <tbody>
          {categories.map(item => (
            <tr key={item.id}>
              <td style={{ fontSize: '1.5rem' }}>{item.emoji}</td>
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