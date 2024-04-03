import React, { useState, useEffect } from 'react';
import bgImg from "../assets/Food.jpg"; // Assuming you want to reuse the background image
import siteIcon from "../assets/FDA.png"; // Assuming you want to reuse the site icon

export default function Form(props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    document.body.classList.add('blaze-page');
    return () => document.body.classList.remove('blaze-page');
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (data.success) {
      alert('Login successful!');
      props.onLoginSuccess(data.name); // Assuming the response includes the user's name
    } else {
      alert('Login failed: ' + data.message);
    }
  };

  return (
    <section>
      <div className="register">
        <div className="col-1">
          <img src={siteIcon} alt="site-icon" className="blaze-icon"/>
          <h2>Sign In</h2>
          <form id='form' className="flex flex-col" onSubmit={handleSubmit}>
            <input
              type="text"
              value={username}
              className="input-field" // Assuming you have styling for input fields
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              required
            />
            <input
              type="password"
              value={password}
              className="input-field" // Assuming you have styling for input fields
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
            />
            <button type='submit' className='btn'>Log in</button>
          </form>
        </div>
        <div className="col-2">
          <img src={bgImg} alt="background" />
        </div>
      </div>
    </section>
  );
}


