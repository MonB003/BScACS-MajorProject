import React from 'react'
import { useLocation, useNavigate } from "react-router-dom";
import FileCheckForm from '../FileForm/FileCheckForm'
import LogGenerator from '../Log/LogGenerator'
import UserFiles from './UserFiles';

function Dashboard() {
  const location = useLocation();
  const { user } = location.state || {};  // Retrieve user data from state
  const navigate = useNavigate();

    return (
    <>
        <h1>Hello, {user.username}</h1>
        <UserFiles userID={user.userID} username={user.username} />
        <FileCheckForm userID={user.userID} />
        <LogGenerator userID={user.userID} username={user.username} />
        <br />
        <div id="logoutDiv">
        <button onClick={() => navigate("/")}>Logout</button>
      </div>
    </>
  )
}

export default Dashboard