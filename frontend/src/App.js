import React, { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import Profile from "./components/Profile";
import Exam from "./components/Exam"; // ✅ import exam

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [view, setView] = useState("login"); // login | register | profile | exam

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
            <Login
              onLogin={handleLogin}
              switchToRegister={() => setView("register")}
            />
          )}
          {view === "register" && (
            <Register
              onRegister={handleLogin}
              switchToLogin={() => setView("login")}
            />
          )}
        </>
      ) : (
        <>
          {view === "profile" && (
            <>
              <Profile user={user} token={token} />
              <button onClick={handleLogout}>Logout</button>
              <button onClick={() => setView("exam")}>Take Test</button>
            </>
          )}

          {view === "exam" && (
            <Exam
              user={user}
              token={token}
              onExit={() => setView("profile")}   // ✅ use onExit instead of onSubmit
            />
          )}
        </>
      )}
    </div>
  );
}

export default App;
