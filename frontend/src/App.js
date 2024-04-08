import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './WebPages/SignUpIn/LoginPage';
import SubscriberPage from './WebPages/Dashboard/AccountPage'; 
import AdminPage from './WebPages/Dashboard/AdminPage'; // Import the AdminPage component
import axios from 'axios';


const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check auth on initial load
    checkAuth();
  }, []);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true); // This updates the state to reflect the user is logged in
  };
  const signOut = () => {
    localStorage.removeItem('token'); // Remove the token from local storage
    localStorage.removeItem('username'); // Remove the token from local storage
    localStorage.removeItem('ID'); // Remove the token from local storage
    setIsLoggedIn(false); // Update state to reflect that the user is no longer logged in
  };

  const checkAuth = async () => {
    try {
      const response = await axios.get('http://localhost:5000/protected', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}` // Assuming the token is stored in localStorage
        }
      });
      if (response.status === 200) {
        setIsLoggedIn(true);
      }
    } catch (error) {
      console.error('You are not logged in.', error);
      setIsLoggedIn(false);
    } finally {
      setLoading(false); // Ensure we stop showing a loading state
    }
  };

  if (loading) {
    return <div>Loading...</div>; // Or any other loading state representation
  }

  return (
    <Router>
      <div>
        <nav>
          {/* Navigation links can be placed here */}
          {isLoggedIn && (
            <button onClick={signOut}>Sign Out</button>
          )}
        </nav>
        <Routes>
          <Route path="/" element={!isLoggedIn ? <Login onLoginSuccess={handleLoginSuccess} /> : <Navigate replace to="/subscriber" />} />
          <Route path="/subscriber" element={isLoggedIn ? <SubscriberPage /> : <Navigate replace to="/" />} />
          <Route path="/admin" element={isLoggedIn ? <AdminPage /> : <Navigate replace to="/" />} /> {/* Add route for the AdminPage */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
