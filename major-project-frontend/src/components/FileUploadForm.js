import { useState } from 'react';

function FileUploadForm() {
    const [file, setFile] = useState(null);

    // Handle file change
    const handleFileChange = (event) => {
        // Set the selected file
        setFile(event.target.files[0]); 
    };

    // Handle file upload
    const handleFileUpload = () => {
        if (!file) {
            alert("Error: Please select a file.");
            return;
        }
        /** Todo: Send the file to the backend */
        console.log("File to upload:", file);
    };

    return (
        <div>
            <h1>File Upload</h1>
            <input type="file" onChange={handleFileChange} />
            <br />
            <button onClick={handleFileUpload}>Upload File</button>
        </div>
    );
}

export default FileUploadForm;