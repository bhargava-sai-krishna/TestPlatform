// src/App.js
import React, { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import Profile from "./components/Profile";

function App() {
  const [user, setUser] = useState(null); // store logged in user
  const [token, setToken] = useState(null); // store access token
  const [view, setView] = useState("login"); // "login" | "register" | "profile"

  const handleLogin = (userData, accessToken) => {
    setUser(userData);
    setToken(accessToken);
    setView("profile");
  };

  const handleLogout = () => {
    setUser(null);
    setToken(null);
    setView("login");
  };

  return (
    <div className="App">
      <h1>LeadMasters AI</h1>

      {!user ? (
        <>
          {view === "login" && (
            <Login onLogin={handleLogin} switchToRegister={() => setView("register")} />
          )}
          {view === "register" && (
            <Register onRegister={handleLogin} switchToLogin={() => setView("login")} />
          )}
        </>
      ) : (
        <>
          <Profile user={user} token={token} />
          <button onClick={handleLogout}>Logout</button>
          <button onClick={() => alert("TODO: Navigate to Test UI")}>Take Test</button>
        </>
      )}
    </div>
  );
}

export default App;
