import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';  // Import your CSS for global styles
import App from './App';  // Main app component
import reportWebVitals from './reportWebVitals';  // Performance measurement (optional)

// Create the root for the app
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component into the root element in the DOM
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Optional: Log performance metrics
reportWebVitals(console.log);
