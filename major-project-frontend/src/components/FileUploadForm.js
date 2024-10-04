import React, { useState } from 'react'

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

        const formMessage = document.getElementById('formMessage')
        formMessage.style.display = "block";

        console.log("File to send:", file);
        console.log("TYPE:", file.type);
        console.log("SIZE:", file.size);
        console.log("LAST MODIFIED:", file.lastModified);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('user_id', 1);

        // Send the file to the backend
        try {
            const URL = process.env.REACT_APP_BACKEND_HOSTED_URL;
            const response = await fetch(`${URL}/upload-file`, {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            formMessage.style.display = "none";

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
                <p id="formMessage" style={{display: "none"}}>File upload in progress</p>
            </div>
        </>
    );
}

export default FileUploadForm;