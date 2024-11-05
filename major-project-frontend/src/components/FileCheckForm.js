import React, { useState } from 'react'

function FileCheckForm({ userID }) {
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

        // const lastModified = new Date(file.lastModified);
        // const readableDate = lastModified.toLocaleString(); // Converts local date and time
        // console.log("Last modified date and time:", readableDate);

        const lastModified = new Date(file.lastModified);
        // Format example: Mon Nov 04 2024 13:10:35 GMT-0800 (Pacific Standard Time)
        const options = {
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZoneName: 'short',
        };
        const readableDate = lastModified.toLocaleString('en-CA', options);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('user_id', userID);
        formData.append('size', file.size);
        formData.append('lastModifiedDate', readableDate);

        // Send the file to the backend
        try {
            const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;
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