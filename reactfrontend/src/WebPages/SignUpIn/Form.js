import React, { useState, useEffect } from 'react';
import bgImg from "../../assets/Food.jpg"; // Assuming you want to reuse the background image
import siteIcon from "../../assets/FDA.png"; // Assuming you want to reuse the site icon

export default function Form(props) {
  const [isSignup, setIsSignup] = useState(false); // Toggle between login and signup
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState(''); // New field for signup
  const [phoneNum, setPhoneNum] = useState(''); // New field for signup

  useEffect(() => {
    document.body.classList.add('blaze-page');
    return () => document.body.classList.remove('blaze-page');
  }, []);

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: email, password }),
    });
    const data = await response.json();
    if (data.success) {
        // Check if logged in user is an Admin or Subscriber and handle accordingly
        if (data.name === "Admin") {
          alert('Admin login successful!');
          // Handle admin-specific success scenario, e.g., redirect to an admin dashboard
          props.onLoginSuccess('Admin');
        } else if (data.name === "Subscriber") {
          alert('Subscriber login successful!');
          // Handle subscriber-specific success scenario, e.g., redirect to a subscriber page
          props.onLoginSuccess(email);
        }
      } else {
        alert('Login failed: ' + data.message);
      }
    };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, password, phonenum: phoneNum, email }),
    });
    const data = await response.json();
    if (response.ok) {
      alert('Signup successful!');
      // Potentially auto-login the user or redirect to the login page
    } else {
      alert('Signup failed: ' + data.error);
    }
  };

  return (
    <section>
      <div className="register">
        <div className="col-1">
          <img src={siteIcon} alt="site-icon" className="blaze-icon"/>
          <h2>{isSignup ? 'Sign Up' : 'Sign In'}</h2>
          <form id='form' className="flex flex-col" onSubmit={isSignup ? handleSignupSubmit : handleLoginSubmit}>
            {isSignup && (
              <>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Name"
                  required
                  className="input-field"
                />
                <input
                  type="text"
                  value={phoneNum}
                  onChange={(e) => setPhoneNum(e.target.value)}
                  placeholder="Phone Number"
                  required
                  className="input-field"
                />
              </>
            )}
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              required
              className="input-field"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
              className="input-field"
            />
            <button type='submit' className='btn'>{isSignup ? 'Sign up' : 'Log in'}</button>
          </form>
          <button onClick={() => setIsSignup(!isSignup)} className='btn-toggle'>
            {isSignup ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
          </button>
        </div>
        <div className="col-2">
          <img src={bgImg} alt="background" />
        </div>
      </div>
    </section>
  );
}
