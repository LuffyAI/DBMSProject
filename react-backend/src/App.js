import React, { useState } from 'react';
import LoginPage from './SignUpIn/LoginPage';
import AccountPage from './Dashboard/AccountPage'; // Make sure this component is created

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState('');

  const handleLoginSuccess = (name) => {
    setIsLoggedIn(true);
    setUserName(name); // Store the user's name
  };

  return (
    <div className="App">
      {!isLoggedIn ? <LoginPage onLoginSuccess={handleLoginSuccess} /> : <AccountPage userName={userName} />}
    </div>
  );
}

export default App;
