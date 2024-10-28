import React, { useState } from 'react'

function FileUploadForm({ userID }) {
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
        console.log("Type:", file.type);
        console.log("Size:", file.size);
        // console.log("Last modified:", file.lastModified);
        console.log("Last modified date:", file.lastModifiedDate);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('size', file.size);
        // formData.append('lastModified', file.lastModified);
        formData.append('lastModifiedDate', file.lastModifiedDate);

        formData.append('user_id', userID);


        // Send the file to the backend
        try {
            const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;
            const response = await fetch(`${URL}/upload-file`, {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            formMessage.style.display = "none";

            console.log("Response", result)
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
                <input type="file" onChange={handleFileChange} required={true} />
                <br />
                <button onClick={handleFileUpload}>Upload File</button>
                <p id="formMessage" style={{display: "none"}}>File upload in progress</p>
            </div>
        </>
    );
}

export default FileUploadForm;