import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard/Dashboard";
import Signup from "./components/Authentication/Signup";
import Login from "./components/Authentication/Login";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="*" element={<Login />} />
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/toolkit" element={<Dashboard />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;