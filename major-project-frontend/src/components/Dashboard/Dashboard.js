import React from 'react'
import { useEffect } from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import FileCheckForm from '../FileForm/FileCheckForm'
import LogGenerator from '../Log/LogGenerator'
import UserFiles from './UserFiles';

function Dashboard() {
  // const location = useLocation();
  // const { user } = location.state || {};  // Retrieve user data from state
  // // console.log("TOKEN: ", user.accessToken)

  const navigate = useNavigate();
  const accessToken = sessionStorage.getItem('accessToken');
  const userID = sessionStorage.getItem('userID');
  const username = sessionStorage.getItem('username');
  console.log("TOKEN: ", accessToken)

  // Redirect to login if no token is present
  useEffect(() => {
    if (!accessToken || !userID) {
      navigate("/");
    }
  }, [accessToken, userID, navigate]);

  if (!accessToken || !userID) {
    return null; // Render nothing while redirecting
  }

  const user = {
    "userID": userID,
    "username": username
  }

  return (
    <>
      <h1>Hello, {user.username}</h1>
      <UserFiles userID={user.userID} username={user.username} />
      <FileCheckForm userID={user.userID} />
      <LogGenerator userID={user.userID} username={user.username} />
      <br />
      <div id="logoutDiv">
        <button onClick={() => {
          sessionStorage.clear(); // Clear data
          navigate("/")
        }}>Logout</button>
      </div>
    </>
  )
}

export default Dashboard