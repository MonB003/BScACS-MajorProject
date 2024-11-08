import React from 'react'
import { useLocation, useNavigate } from "react-router-dom";

import FileUploadForm from '../FileForm/FileUploadForm'
import FileCheckForm from '../FileForm/FileCheckForm'
import LogGenerator from '../Log/LogGenerator'

function Dashboard() {
  const location = useLocation();
  const { user } = location.state || {};  // Retrieve user data from state
  const navigate = useNavigate();

    return (
    <>
        <h1>Hello, {user.username}</h1>
        <FileUploadForm userID={user.userID} />
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