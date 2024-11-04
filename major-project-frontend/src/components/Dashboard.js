import React from 'react'
import { useLocation } from "react-router-dom";
import FileUploadForm from './FileUploadForm'
import FileCheckForm from './FileCheckForm'
import LogGenerator from './LogGenerator'

function Dashboard() {
  const location = useLocation();
  const { user } = location.state || {};  // Retrieve `user` from state

    console.log("USER DASHBOARD", user)
    console.log("USER DASHBOARD", user.userID)
    console.log("USER DASHBOARD", user.username)

    return (
    <>
        <h1>Hello, {user.username}</h1>
        <FileUploadForm userID={user.userID} />
        <FileCheckForm userID={user.userID} />
        <LogGenerator userID={user.userID} username={user.username} />
    </>
  )
}

export default Dashboard