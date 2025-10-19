import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Product Recommender 🤖</h1>
        <nav className="main-nav">
          <Link to="/">Home</Link>
          <Link to="/analytics">Analytics</Link>
        </nav>
      </header>
      
      {/* This Outlet renders the correct page (Home or Analytics) */}
      <Outlet />
    </div>
  );
}

export default App;