import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

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
        const userJSON = {
          userID: result.user_id,
          username: result.username
        };
        navigate("/toolkit", { state: { user: userJSON } });  // Pass the user in the state and redirect to dashboard
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
      <h1>Signup</h1>
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
        <button type="submit">Signup</button>
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
