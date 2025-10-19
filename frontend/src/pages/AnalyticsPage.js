import React from 'react';
import '../App.css'; // We can reuse the same CSS

function AnalyticsPage() {
  return (
    <div className="page-content">
      <div className="analytics-container">
        <h2>Product Analytics</h2>
        <p>This page shows insights from our product database.</p>
        
        <div className="plot-card">
          <h3>Product Price Distribution (Log Scale)</h3>
          {/* This path works because we moved the folder to 'public' */}
          <img src="/analytics_plots/price_distribution.png" alt="Price Distribution" />
        </div>
        
        <div className="plot-card">
          <h3>Top 10 Product Brands</h3>
          <img src="/analytics_plots/top_10_brands.png" alt="Top 10 Brands" />
        </div>
        
        <div className="plot-card">
          <h3>Top 10 Product Categories</h3>
          <img src="/analytics_plots/top_10_categories.png" alt="Top 10 Categories" />
        </div>
      </div>
    </div>
  );
}

export default AnalyticsPage;