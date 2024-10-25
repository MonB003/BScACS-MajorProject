import React from 'react'
import FileUploadForm from './FileUploadForm'
import FileCheckForm from './FileCheckForm'
import LogGenerator from './LogGenerator'

function Dashboard({ user }) {
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