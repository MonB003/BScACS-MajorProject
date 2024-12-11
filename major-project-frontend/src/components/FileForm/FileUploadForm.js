import React, { useState } from 'react'

function FileUploadForm({ userID, onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const MAX_FILE_SIZE = 1000000;

    // Handle file change
    const handleFileChange = (event) => {
        // Set the selected file
        setFile(event.target.files[0]);
    };

    // Handle file upload
    const handleFileUpload = async () => {
        if (!file) {
            alert("Error: Please select a file.");
            return;
        }

        const formMessage = document.getElementById('formMessage')
        formMessage.style.display = "block";

        // Convert local date and time into readable format
        const lastModified = new Date(file.lastModified);
        const readableDate = new Intl.DateTimeFormat('en-CA', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
            hour12: false // Ensures 24-hour format
        }).format(lastModified);
    
        console.log("File to send:", file);
        console.log("Type:", file.type);
        console.log("Size:", file.size);
        console.log("Last modified date:", readableDate);

        if (file.size > MAX_FILE_SIZE) {
            let errorMessage = "Error: File size is too large. Max file size to upload: " + MAX_FILE_SIZE;
            alert(errorMessage);
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('size', file.size);
        formData.append('lastModifiedDate', readableDate);
        formData.append('user_id', userID);

        // Send the file to the backend
        try {
            const URL = process.env.REACT_APP_BACKEND_HOSTED_URL;
            const response = await fetch(`${URL}/upload-file`, {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            formMessage.style.display = "none";

            console.log("Response", result)
            if (response.ok) {
                alert(result.message);
                if (onUploadSuccess) {
                    onUploadSuccess(); // Callback to refresh files displayed in UserFiles component
                }
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <>
            <div>
                <h1>File Upload</h1>
                <input data-testid="fileInput" type="file" onChange={handleFileChange} required={true} />
                <br />
                <button onClick={handleFileUpload}>Upload File</button>
                <p id="formMessage" style={{ display: "none" }}>File upload in progress</p>
            </div>
        </>
    );
}

export default FileUploadForm;