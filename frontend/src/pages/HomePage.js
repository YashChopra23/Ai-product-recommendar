import React, { useState } from 'react';
import axios from 'axios';
// We've moved the CSS, so we go up one directory
import '../App.css'; 

function HomePage() {
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendQuery = async () => {
    setLoading(true);
    setError(null);
    setProducts([]);
    
    try {
      const response = await axios.post('https://my-product-backend.onrender.com/recommend', {
        query: query
      });
      setProducts(response.data.products);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      setError("Failed to get recommendations. Please try again.");
    }
    setLoading(false);
  };

  return (
    // We just wrap this in a 'page-content' div
    <div className="page-content">
      <div className="chat-container">
        <div className="input-area">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="What are you looking for?"
          />
          <button onClick={sendQuery} disabled={loading}>
            {loading ? 'Thinking...' : 'Send'}
          </button>
        </div>
        
        {error && <p className="error">{error}</p>}
        
        <div className="results-area">
          {products.map((product) => (
            <div key={product.id} className="product-card">
              <img src={product.image} alt={product.title} />
              <div className="product-info">
                <h3>{product.title}</h3>
                <p className="price">${product.price.toFixed(2)}</p>
                <p className="description">{product.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HomePage;