import React, { useState } from 'react';
import "./FileForm.css";
import recordTestTime from "../Utilities/TestTime";

function FileForm({ userID, onUploadSuccess = null, showModal, backendPath }) {
    const TEST_MODE = process.env.REACT_APP_TEST_MODE === "true";
    const [file, setFile] = useState(null);
    const [filePath, setFilePath] = useState("");
    const MAX_FILE_SIZE = 1000000;

    // Handle file input change
    const handleFileChange = (event) => {
        // Set the selected file
        setFile(event.target.files[0]);
    };
    const handleFilePathChange = (event) => {
        setFilePath(event.target.value);
    };

    // Handle file upload
    const handleFileUpload = async () => {
        if (!file) {
            showModal("Error", "Error: Please select a file.");
            return;
        }
        if (!filePath) {
            showModal("Error", "Error: Please enter a file path.");
            return;
        }

        let startTime = null, endTime = null;
        if (TEST_MODE) {
            startTime = performance.now();
        }

        const formMessage = document.getElementById('formMessage');
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
        console.log("File path:", filePath);
        console.log("Type:", file.type);
        console.log("Size:", file.size);
        console.log("Last modified date:", readableDate);

        if (file.size > MAX_FILE_SIZE) {
            let errorMessage = "Error: File size is too large. Max file size to upload: " + MAX_FILE_SIZE;
            showModal("Error", errorMessage);
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('size', file.size);
        formData.append('lastModifiedDate', readableDate);
        formData.append('filePath', filePath);
        formData.append('user_id', userID);

        // Send the file to the backend
        try {
            const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;
            const response = await fetch(`${URL}/${backendPath}`, {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            formMessage.style.display = "none";

            console.log("Response", result)
            if (TEST_MODE) {
                // Send time to the backend to record 
                endTime = performance.now();
                let totalTime = endTime - startTime;
                let methodName = backendPath === 'upload-file' ? 'handleFileUpload' : 'handleFileCheck';
                await recordTestTime(methodName, totalTime);
            }
            if (response.ok) {
                showModal("Success", result.message);
                if (onUploadSuccess) {
                    onUploadSuccess(); // Callback to refresh files displayed in UserFiles component
                }
            } else {
                let alertMessage = ""
                alertMessage += result.error + "\n"
                if (result.log_message != undefined) {
                    alertMessage += result.log_message
                }
                // Check if file check content log was created (for supported file types)
                if (result.log_file != "" && result.log_file != undefined) {
                    alertMessage += "\n" + result.log_file
                }
                showModal("Error", alertMessage);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <div class='fileForm dashboardDiv'>
            <h1>{backendPath === 'upload-file' ? 'File Upload' : 'Check a File'}</h1>
            <input data-testid="fileInput" type="file" onChange={handleFileChange} required={true} />
            <br />
            <input type="text" value={filePath} onChange={handleFilePathChange} required={true} placeholder='File path' />
            <br />
            <button onClick={handleFileUpload}>{backendPath === 'upload-file' ? 'Upload File' : 'Check File'}</button>
            <p id="formMessage" style={{ display: "none" }}>{backendPath === 'upload-file' ? 'File upload in progress' : 'File check in progress'}</p>
        </div>
    );
}

export default FileForm;