import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import './index.css';
import App from './App';
import HomePage from './pages/HomePage';
import AnalyticsPage from './pages/AnalyticsPage';

// This defines our routes
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />, // App is now the main layout
    children: [
      {
        path: "/", // The default page
        element: <HomePage />,
      },
      {
        path: "analytics", // The new analytics page
        element: <AnalyticsPage />,
      },
    ],
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);