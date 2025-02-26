import React, { useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import FileCheckForm from '../FileForm/FileCheckForm'
import LogGenerator from '../Log/LogGenerator'
import UserFiles from './UserFiles';
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();
  const accessToken = sessionStorage.getItem('accessToken');
  const userID = sessionStorage.getItem('userID');
  const username = sessionStorage.getItem('username');
  // console.log("TOKEN: ", accessToken)

  // Redirect to login if no token is present
  useEffect(() => {
    if (!accessToken || !userID) {
      navigate("/");
    }
  }, [accessToken, userID, navigate]);

  if (!accessToken || !userID) {
    return null; // Render nothing while redirecting
  }

  return (
    <>
      <div id="logoutDiv">
        <button onClick={() => {
          sessionStorage.clear(); // Clear data
          navigate("/")
        }}>Logout</button>
      </div>
      <h1>Hello, {username}</h1>
      <div id="dashboardContainer">
        <UserFiles userID={userID} username={username} />
        <FileCheckForm userID={userID} />
        <LogGenerator userID={userID} username={username} />
      </div>
    </>
  )
}

export default Dashboard