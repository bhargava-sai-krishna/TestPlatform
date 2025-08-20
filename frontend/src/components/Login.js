import React, { useState } from "react";
import { apiRequest } from "../utils/api";

function Login({ onLogin, switchToRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await apiRequest("/api/auth/login", "POST", { email, password });
      if (res.error) {
        setError(res.error);
      } else {
        onLogin(res.user, res.access_token);
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="form-container">
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
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
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account?{" "}
        <button className="link" onClick={switchToRegister}>
          Register
        </button>
      </p>
    </div>
  );
}

export default Login;
