import React, { useState, useEffect } from 'react';
import bgImg from "../../assets/Food.jpg"; // Background image
import siteIcon from "../../assets/FDA.png"; // Site icon
import { useNavigate } from 'react-router-dom'; 

export default function Form(props) {
  const [isSignup, setIsSignup] = useState(false); // Toggle between login and signup
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState(''); // New field for signup
  const [phoneNum, setPhoneNum] = useState(''); // New field for signup
  const navigate = useNavigate()
  

  useEffect(() => {
    document.body.classList.add('blaze-page');
    return () => document.body.classList.remove('blaze-page');
  }, []);

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (data.success) {
          localStorage.setItem('token', data.Token); // Save the token
          localStorage.setItem('userName', data.email);
          localStorage.setItem('ID', data.ID);
          alert(`${data.role} login successful!`);
          props.onLoginSuccess(); // Notify the parent component about the login success
          if (data.role === 'Admin') {
            console.log("hello hello");
            navigate('/admin');
          } else {
            navigate('/subscriber');
          } 
      } else {
          alert('Login failed: ' + data.message);
      }
    }
    catch (error) {
      console.error('Error logging in:', error);
      alert('Login failed. Please try again.');
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
      setIsSignup(false); // Switch back to login form on successful signup
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
