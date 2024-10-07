import React, { useState } from 'react'

function FileCheckForm() {
    const [file, setFile] = useState(null);

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

        const formData = new FormData();
        formData.append('file', file);
        formData.append('user_id', 1);

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
                alert(result.error);
            }
        } catch (error) {
            console.error('Error checking file:', error);
        }
    };

    return (
        <>
            <div>
                <h1>Check a File</h1>
                <input type="file" onChange={handleFileChange} />
                <br />
                <button onClick={handleFileCheck}>Check File</button>
                <p id="formCheckMessage" style={{display: "none"}}>File check in progress</p>
            </div>
        </>
    );
}

export default FileCheckForm;