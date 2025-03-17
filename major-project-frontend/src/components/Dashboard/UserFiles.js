import React, { useState, useEffect } from 'react'
import FileUploadForm from '../FileForm/FileUploadForm';
import './UserFiles.css'

function UserFiles({ userID, username, showModal }) {
    // Store user's files
    const [files, setFiles] = useState(null);

    // Handle retrieving a user's files
    const handleUserFiles = async () => {
        const formData = new FormData();
        formData.append('user_id', userID);

        // Send user ID to the backend to get the user's files
        try {
            const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;
            const response = await fetch(`${URL}/get-user-files`, {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            console.log("Response", result)
            if (response.ok) {
                setFiles(result.files);
            } else {
                console.error('Error getting files:', result.message);
            }

        } catch (error) {
            console.error('Error getting files:', error);
        }
    };

    // Initial fetch of files
    useEffect(() => {
        handleUserFiles();
    }, []);

    // Function to pass to FileUploadForm, which updates files displayed after each upload
    const refreshFiles = () => {
        handleUserFiles();
    };

    return (
        <>
            <FileUploadForm userID={userID} onUploadSuccess={refreshFiles} showModal={showModal} />
            <div id='userFilesContainer' className='dashboardDiv'>
                <h1>{username}'s Files</h1>
                <div id="fileList">
                    {
                        // Loop through files state object and display each file's info
                        files ? (
                            files.map((file, index) => (
                                <div key={index} className='fileItem'>
                                    <h3 className='userFilename'>{file.filename}</h3>
                                    <ul>
                                        <li>File Path: {file.file_path}</li>
                                        <li>File Type: {file.content_type}</li>
                                        <li>Size: {file.size}</li>
                                        <li>Last Modified: {file.last_modified_date}</li>
                                        <li>Date Uploaded: {file.date}</li>
                                    </ul>
                                </div>
                            ))
                        ) : (
                            <p>There are no files.</p>
                        )}
                </div>
            </div>
        </>
    );
}

export default UserFiles