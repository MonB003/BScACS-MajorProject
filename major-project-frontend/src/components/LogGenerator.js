import React from 'react'

function LogGenerator() {
    // Handle log file generation
    const handleLogGeneration = async () => {
        // Send the request to the backend
        try {
            const URL = process.env.REACT_APP_BACKEND_LOCAL_URL;
            const response = await fetch(`${URL}/generate-log-file`);

            if (!response.ok) {
                alert('Error: The log file could not be generated.');
            }

            // Store response as a Blob (Binary Large Object) for the PDF
            const blobResult = await response.blob();

            // Create a PDF link to download
            const logFileURL = window.URL.createObjectURL(blobResult);
            const a = document.createElement('a');
            a.href = logFileURL;
            a.download = 'log_file.pdf'; // PDF file name
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
            <div>
                <h1>Logs</h1>
                <button onClick={handleLogGeneration}>Get Log File</button>
            </div>
        </>
    );
}

export default LogGenerator;