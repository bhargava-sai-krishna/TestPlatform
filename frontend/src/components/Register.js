import React, { useState } from "react";
import { apiRequest } from "../utils/api";

function Register({ onRegister, switchToLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await apiRequest("/api/auth/register", "POST", {
        email,
        password,
        full_name: fullName,
      });
      if (res.error) {
        setError(res.error);
      } else {
        onRegister(res.user, res.access_token);
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="form-container">
      <h2>Register</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Register</button>
      </form>
      <p>
        Already have an account?{" "}
        <button className="link" onClick={switchToLogin}>
          Login
        </button>
      </p>
    </div>
  );
}

export default Register;
