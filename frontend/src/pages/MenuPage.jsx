import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from '@tanstack/react-query';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import apiClient from '../api';
import Header from '../Common.jsx';
import './MenuPage.css';

// --- React Query Client ---
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: false,
      retry: (failureCount, error) => {
        if (error.response?.status === 404) return false;
        return failureCount < 3;
      },
    },
  },
});

// --- API Fetching Functions ---

const fetchCategories = async () => {
  console.log('Fetching categories from /categories/');
  try {
    const response = await apiClient.get('/categories/');
    console.log('Categories fetched:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
    toast.error('Could not load food categories.');
    throw error;
  }
};

const fetchDishesByCategory = async (id) => {
  let url = `/dishes/` + (id ? `?category_id=${id}` : '');
  console.log('Fetching dishes from URL:', url);
  try {
    const response = await apiClient.get(url);
    console.log(`Dishes fetched for category ${id}:`, response.data);
    return response.data;
  } catch (error) {
    console.error(`Error fetching dishes for category ${id}:`, error);
    toast.error(`Could not load dishes for this category.`);
    throw error;
  }
};

/**
 * Fetches the full details for a single dish by its ID.
 * Corresponds to: GET /dishes/:id/
 */
const fetchDishDetails = async (dishId) => {
  console.log(`Fetching dish details from /dishes/${dishId}/`);
  if (!dishId) return null;
  try {
    const response = await apiClient.get(`/dishes/${dishId}/`);
    console.log(`Dish details fetched for ID ${dishId}:`, response.data);
    return response.data;
  } catch (error) {
    console.error(`Error fetching dish details for ID ${dishId}:`, error);
    toast.error('Could not load dish details.');
    throw error;
  }
};

// --- Main App Component ---
export default function MenuPage() {
  return (
    <QueryClientProvider client={queryClient}>
      <Header />
      <MainContent />
    </QueryClientProvider>
  );
}

// --- Page Components ---

/**
 * Main Menu Page Component
 * This renders the <main> and <section> wrappers from your HomePage.jsx
 */
function MainContent() {
  const { categorySlug } = useParams();
  const navigate = useNavigate();

  const { data: categories, isLoading: categoriesLoading } = useQuery({
    queryKey: ['categories'],
    queryFn: fetchCategories,
  });

  const currentCategory = React.useMemo(() => {
    if (!categories) return null;

    if (categorySlug) {
      return categories.find((c) => c.slug === categorySlug);
    }
    
    return categories[0] || null;
  }, [categories, categorySlug]);

  const selectedCategoryID = currentCategory ? currentCategory.id : null;

  React.useEffect(() => {
    if (categories && categories.length > 0 && !categorySlug) {
      navigate(`/menu/${categories[0].slug}`, { replace: true });
    }
  }, [categories, categorySlug, navigate]);

  const handleSelectCategory = (newSlug) => {
    navigate(`/menu/${newSlug}`);
  };

  return (
    <main>
      <section className="menu-section">
        <p className="section-subtitle">OUR SELECTION</p>
        <h2 className="section-title">A Menu That Will Always<br />Capture Your Heart</h2>

        <CategoryTabs
          // --- UPDATED PROPS ---
          categories={categories}
          isLoading={categoriesLoading}
          selectedCategoryID={selectedCategoryID}
          onSelectCategory={handleSelectCategory} // Pass the new handler
        />

        <DishList selectedCategoryID={selectedCategoryID} />
      </section>
    </main>
  );
}

/**
 * Displays the category tabs using your .tab-pill class
 */
function CategoryTabs({
  categories,
  isLoading,
  selectedCategoryID,
  onSelectCategory,
}) {
  // --- REMOVED: useQuery for categories (moved to MainContent) ---
  // --- REMOVED: useEffect for default selection (moved to MainContent) ---

  if (isLoading) {
    return (
      <div className="category-tabs">
        {[...Array(3)].map((_, i) => (
          <button key={i} className="tab-pill" disabled style={{ opacity: 0.5 }}>
            Loading...
          </button>
        ))}
      </div>
    );
  }

  // We can just check the passed-in prop
  if (!categories || categories.length === 0) {
    return (
      <div className="category-tabs">
        <p>No categories found.</p>
      </div>
    );
  }

  return (
    <div className="category-tabs">
      {categories.map((category) => (
        <button
          key={category.id}
          // --- KEY CHANGE: Call with the SLUG, not the ID ---
          onClick={() => onSelectCategory(category.slug)}
          className={`tab-pill ${
            selectedCategoryID === category.id ? 'active' : ''
          }`}
        >
          {category.name}
        </button>
      ))}
    </div>
  );
}

/**
 * Displays the list of dishes using your .menu-cards and .card classes
 */
function DishList({ selectedCategoryID }) {
  const [viewingDishId, setViewingDishId] = useState(null);

  const {
    data: dishes,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ['dishes', selectedCategoryID],
    queryFn: () => fetchDishesByCategory(selectedCategoryID),
    enabled: !!selectedCategoryID,
  });

  if (!selectedCategoryID) {
    return (
      <div style={{ padding: '2rem 0', color: '#555' }}>
        <p>Please select a category above to see the available dishes.</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="menu-cards">
        {/* Skeleton loaders matching the .card structure */}
        {[...Array(3)].map((_, i) => (
          <div key={i} className="card" style={{ opacity: 0.5, pointerEvents: 'none' }}>
            <div style={{ height: '200px', background: '#eee' }} />
            <div className="card-content" style={{ filter: 'blur(4px)' }}>
              <h3 className="product-title">Loading...</h3>
              <p className="product-price">...₴</p>
              <button className="tab-pill">read more</button>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <div className="menu-cards">
        <p style={{ color: 'red' }}>We couldn't load the dishes for this category. Please try again.</p>
      </div>
    );
  }

  if (!dishes || dishes.length === 0) {
    return (
      <div className="menu-cards">
        <p>There are currently no dishes available in this category.</p>
      </div>
    );
  }

  return (
    <>
      <div className="menu-cards">
        {dishes.map((dish) => (
          <DishCard
            key={dish.id}
            dish={dish}
            onShowDetails={() => setViewingDishId(dish.id)}
          />
        ))}
      </div>

      {/* The modal will appear on top when viewingDishId is set */}
      <DishDetailModal
        dishId={viewingDishId}
        onClose={() => setViewingDishId(null)}
      />
    </>
  );
}

/**
 * Displays a single dish card using your .card structure
 */
function DishCard({ dish, onShowDetails }) {
  const handleAddToCart = (e) => {
    e.stopPropagation(); // Prevent modal from opening
    toast.success(`${dish.name} added to cart! (Not really)`);
  };

  const handleShowDetails = (e) => {
    e.stopPropagation();
    onShowDetails();
  };

  // Fallback image handler
  const handleImageError = (e) => {
    e.target.src = `https://placehold.co/600x400/E5E7EB/333?text=${encodeURIComponent(dish.name)}`;
    e.target.onerror = null;
  };

  return (
    <div className="card" style={{ cursor: 'pointer' }} onClick={handleShowDetails}>
      {/* Assuming /content/ paths are available */}
      <img src="/content/heart.png" className="fav-icon" alt="favorite" />
      <img
        src={dish.photo_url || `https://placehold.co/600x400/E5E7EB/333?text=${encodeURIComponent(dish.name)}`}
        alt={dish.name}
        className="card-img"
        onError={handleImageError}
      />
      
      {!dish.is_available && (
        <div style={{
          position: 'absolute', top: 0, left: 0, width: '100%', height: '200px',
          background: 'rgba(0,0,0,0.5)', color: 'white', display: 'flex',
          alignItems: 'center', justifyContent: 'center', fontWeight: 'bold'
        }}>
          Unavailable
        </div>
      )}
        
      <div className="card-content">
        <h3 className="product-title">{dish.name}</h3>
        <p className="product-price">{dish.price}₴</p>
        
        <div className="card-actions">
          <button 
            className="read-btn"
            onClick={handleAddToCart}
            disabled={!dish.is_available}
          >
            Add to Cart
          </button>
          <button 
            className="tab-pill"
            onClick={handleShowDetails}
          >
            Read more
          </button>
        </div>
      </div>
    </div>
  );
}

/**
 * Modal to display full dish details.
 * This uses the custom styles from the <CustomStyles> component.
 */
function DishDetailModal({ dishId, onClose }) {
  const {
    data: dish,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ['dish', dishId],
    queryFn: () => fetchDishDetails(dishId),
    enabled: !!dishId,
  });

  const handleImageError = (e) => {
    e.target.src = `https://placehold.co/400x400/E5E7EB/333?text=${encodeURIComponent(dish?.name || 'Loading...')}`;
    e.target.onerror = null;
  };

  if (!dishId) return null;

  const handleAddToCart = () => {
    // TODO: Implement Add to Cart logic
    toast.success(`${dish.name} added to cart! (Not really)`);
    onClose(); // Close modal after adding
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{dish ? dish.name : 'Loading...'}</h2>
          <button onClick={onClose} className="modal-close-btn">&times;</button>
        </div>
        
        <div className="modal-body">
          {isLoading && <p>Loading details...</p>}
          {isError && <p style={{ color: 'red' }}>Could not load dish details.</p>}
          {dish && (
            <>
              <img
                src={dish.photo_url || `https://placehold.co/400x400/E5E7EB/333?text=${encodeURIComponent(dish.name)}`}
                alt={dish.name}
                onError={handleImageError}
              />
              <p className="modal-price">{dish.price}₴</p>
              <p>{dish.description}</p>
              
              {dish.ingredients && dish.ingredients.length > 0 && (
                <div className="modal-ingredients">
                  <h4>Ingredients</h4>
                  <ul>
                    {dish.ingredients.map((ing) => (
                      <li key={ing.ingredient_id}>
                        {ing.name}
                        {ing.is_base_ingredient && (
                          <span style={{ color: '#888', fontSize: '0.8em' }}> (Base)</span>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}
        </div>
        
        <div className="modal-footer">
          <button onClick={onClose} className="read-btn">
            Close
          </button>
          <button
            onClick={handleAddToCart}
            disabled={!dish?.is_available || isLoading}
            className="cart-btn-modal"
          >
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
}

