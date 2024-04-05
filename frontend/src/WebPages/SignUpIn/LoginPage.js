import React from "react";
import "./SignUpForm.css";
import Form from './Form.js'

const LoginPage = ({ onLoginSuccess }) => { // Accept onLoginSuccess prop here
    return (
      <div className="SignUpForm">
        <Form onLoginSuccess={onLoginSuccess}></Form> {/* Pass it to Form */}
      </div>
    );
  };

export default LoginPage;