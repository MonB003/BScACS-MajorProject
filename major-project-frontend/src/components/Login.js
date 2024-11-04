import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;
      const response = await fetch(`${URL}/login`, {
          method: 'POST',
          body: formData,
      });

      const result = await response.json();
      console.log("RESULT", result)
      if (response.ok) {
        const userJSON = {
          userID: result.user_id,
          username: result.username
        };
        navigate("/toolkit", { state: { user: userJSON } });  // Pass the user in the state and redirect to dashboard
      } else {
        console.error("Error with login:", result.error);
        const formLoginMessage = document.getElementById('formLoginMessage');
        formLoginMessage.innerHTML = result.error;
        formLoginMessage.style.display = "block";
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div id="page">
        <>
          <h1>Login</h1>
          <form id="loginForm" onSubmit={handleLogin}>
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
            <button type="submit">Login</button>
          </form>
          <p id="formLoginMessage" style={{display: "none"}}></p>

          <br />

          <div id="signupDiv">
            <button onClick={() => navigate("/signup")}>Signup</button>
          </div>
        </>
    </div>
  );
}

export default Login;
