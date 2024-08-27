// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RegistrationPage from "./RegistrationPage";
import { useAuth } from "./AuthContext";

function App() {
  const { user } = useAuth() || {}; // Safeguard in case useAuth returns undefined

  return (
    <Router>
      <Routes>
        <Route path="/" element={<RegistrationPage />} />
        
  
      </Routes>
    </Router>
  );
}

export default App;



