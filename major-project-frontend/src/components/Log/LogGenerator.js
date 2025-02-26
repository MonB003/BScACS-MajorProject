import React from 'react'
import "./LogGenerator.css"

function LogGenerator({ userID, username }) {
    // Handle log file generation
    const handleLogGeneration = async () => {
        const formData = new FormData();
        formData.append('user_id', userID);
        formData.append('username', username);

        // Send the request to the backend
        try {
            const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;
            const response = await fetch(`${URL}/generate-log-file`,{
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                alert('Error: The log file could not be generated.');
            }

            // Store response as a Blob (Binary Large Object) for the PDF
            const blobResult = await response.blob();

            // Create a PDF link to download
            const logFileURL = window.URL.createObjectURL(blobResult);
            const a = document.createElement('a');
            a.href = logFileURL;
            a.download = username + '_log_file.pdf'; // PDF file name
            // Put file on the page to download, then remove it after
            document.body.appendChild(a);
            a.click();
            a.remove();
            
        } catch (error) {
            console.error('Error generating the log file:', error);
        }
    };

    return (
        <>
            <div id='logContainer' className='dashboardDiv'>
                <h1>Logs</h1>
                <button onClick={handleLogGeneration}>Get Log File</button>
            </div>
        </>
    );
}

export default LogGenerator;