import React, { useState } from 'react'

function FileCheckForm({ userID }) {
    const [file, setFile] = useState(null);
    const MAX_FILE_SIZE = 1000000;

    // Handle file change
    const handleFileChange = (event) => {
        // Set the selected file
        setFile(event.target.files[0]);
    };

    // Handle file checking
    const handleFileCheck = async () => {
        if (!file) {
            alert("Error: Please select a file.");
            return;
        }
        console.log("File to send:", file);

        const formCheckMessage = document.getElementById('formCheckMessage')
        formCheckMessage.style.display = "block";

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

        if (file.size > MAX_FILE_SIZE) {
            let errorMessage = "Error: File size is too large. Max file size to upload: " + MAX_FILE_SIZE;
            alert(errorMessage);
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('user_id', userID);
        formData.append('size', file.size);
        formData.append('lastModifiedDate', readableDate);

        // Send the file to the backend
        try {
            const URL = process.env.REACT_APP_BACKEND_HOSTED_URL;
            const response = await fetch(`${URL}/check-file`, {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            formCheckMessage.style.display = "none";

            console.log("Response", result)
            if (response.ok) {
                alert(result.message);
            } else {
                let alertMessage = ""
                alertMessage += result.error + "\n"
                alertMessage += result.log_message
                alert(alertMessage);
            }
        } catch (error) {
            console.error('Error checking file:', error);
        }
    };

    return (
        <>
            <div>
                <h1>Check a File</h1>
                <input type="file" onChange={handleFileChange} required={true} />
                <br />
                <button onClick={handleFileCheck}>Check File</button>
                <p id="formCheckMessage" style={{ display: "none" }}>File check in progress</p>
            </div>
        </>
    );
}

export default FileCheckForm;