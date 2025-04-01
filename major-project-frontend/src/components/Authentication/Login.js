import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Authentication.css"
import recordTestTime from "../Utilities/TestTime";

function Login() {
  const TEST_MODE = process.env.REACT_APP_TEST_MODE === "true";
  console.log("TEST MODE", TEST_MODE)
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;

  // Redirect to dashboard if already logged in
  useEffect(() => {
    const accessToken = sessionStorage.getItem('accessToken');
    if (accessToken) {
      navigate("/toolkit");
    }
  }, [navigate]);

  // const recordTestTime = async (methodName, timeTaken) => {
  //   try {
  //     const timePrecision = 4;
  //     const timeSeconds = (timeTaken / 1000).toFixed(timePrecision);

  //     const response = await fetch(`${URL}/record-time`, {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({ methodName, totalTime: parseFloat(timeSeconds) }),
  //     });
  //     console.log("Response status:", response.status);  // Debugging line
  //     if (response.ok) {
  //       console.log("Successfully logged time!");
  //     } else {
  //       console.error("Failed to log time:", await response.json());
  //     }
  //   } catch (error) {
  //     console.error("Error logging method execution time:", error);
  //   }
  // };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      let startTime = null, endTime = null;
      if (TEST_MODE) {
        startTime = performance.now();
      }
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      // const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;
      const response = await fetch(`${URL}/login`, {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      console.log("RESULT", result)
      if (TEST_MODE) {
        endTime = performance.now();
        let totalTime = endTime - startTime;
        // console.log("TIME", totalTime)

        await recordTestTime("handleLogin", totalTime);

        // const timeResult = await recordTestTime("handleLogin", totalTime);
        // console.log("TIME RESULT", timeResult)
      }
      if (response.ok) {
        // Store token in memory (or use a secure cookie)
        sessionStorage.setItem('userID', result.user_id);
        sessionStorage.setItem('username', result.username);
        sessionStorage.setItem('accessToken', result.access_token);
        navigate("/toolkit");  // Redirect to dashboard
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
      <h1>Secure MoniTor Toolkit</h1>
      <div id="formContainer">
        <h2>Login</h2>
        <form id="submissionForm" onSubmit={handleLogin}>
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
        <p id="formLoginMessage" className="message" style={{ display: "none" }}></p>

        <br />

        <div id="redirectDiv">
          <button onClick={() => navigate("/signup")}>Signup</button>
        </div>
      </div>
    </div>
  );
}

export default Login;
