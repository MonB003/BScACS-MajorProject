import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  // Redirect to dashboard if already logged in
  useEffect(() => {
    const accessToken = sessionStorage.getItem('accessToken');
    if (accessToken) {
      navigate("/toolkit");
    }
  }, [navigate]);

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;
      const response = await fetch(`${URL}/signup`, {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      console.log("RESULT", result)
      if (response.ok) {
        // const userJSON = {
        //   userID: result.user_id,
        //   username: result.username,
        //   accessToken: result.access_token
        // };
        // Store token in memory (or use a secure cookie)
        sessionStorage.setItem('userID', result.user_id);
        sessionStorage.setItem('username', result.username);
        sessionStorage.setItem('accessToken', result.access_token);
        navigate("/toolkit");  // Redirect to dashboard
      } else {
        console.error("Error with signup:", result.error);
        const formSignupMessage = document.getElementById('formSignupMessage');
        formSignupMessage.innerHTML = result.error;
        formSignupMessage.style.display = "block";
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div id="page">
      <h1>Secure MoniTor Toolkit</h1>
      <h2>Sign Up</h2>
      <form id="signupForm" onSubmit={handleSignup}>
        <input
          type="text"
          placeholder="Username"
          required={true}
          onChange={(e) => setUsername(e.target.value)}
        />
        <br />
        <input
          type="password"
          placeholder="Password"
          required={true}
          onChange={(e) => setPassword(e.target.value)}
        />
        <br />
        <button type="submit">Sign Up</button>
      </form>
      <p id="formSignupMessage" style={{ display: "none" }}></p>

      <br />

      <div>
        <button onClick={() => navigate("/")}>Back to Login</button>
      </div>
    </div>
  );
}

export default Signup;
