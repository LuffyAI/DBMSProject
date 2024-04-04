import React, { useState } from 'react';
import LoginPage from './WebPages/SignUpIn/LoginPage';
import AccountPage from './WebPages/Dashboard/AccountPage'; 

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState('');

  const handleLoginSuccess = (name) => {
    setIsLoggedIn(true);
    setUserName(name); 
  };

  return (
    <div className="App">
      {!isLoggedIn ? <LoginPage onLoginSuccess={handleLoginSuccess} /> : <AccountPage userName={userName} />}
    </div>
  );
}

export default App;