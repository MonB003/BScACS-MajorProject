import React, { useState, useEffect } from 'react'

function FileUploadForm() {
    const [file, setFile] = useState(null);

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
        console.log("File to send:", file);

        const formData = new FormData();
        formData.append('file', file);

        // Send the file to the backend
        try {
            const response = await fetch('http://localhost:5000/upload-file', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            console.log("RESPONSE", result)
            if (response.ok) {
                alert(result.message);
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
                <input type="file" onChange={handleFileChange} />
                <br />
                <button onClick={handleFileUpload}>Upload File</button>
            </div>
        </>
    );
}

export default FileUploadForm;