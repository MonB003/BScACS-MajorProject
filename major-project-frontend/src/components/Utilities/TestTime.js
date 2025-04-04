const recordTestTime = async (methodName, timeTaken) => {
    try {
        const timePrecision = 4;
        const timeSeconds = (timeTaken / 1000).toFixed(timePrecision);

        const response = await fetch(`${process.env.REACT_APP_BACKEND_LOCAL_URL}/record-time`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ methodName, totalTime: parseFloat(timeSeconds) }),
        });

        if (response.ok) {
            console.log("Successfully logged time");
        } else {
            console.error("Failed to log time:", await response.json());
        }
    } catch (error) {
        console.error("Error logging method execution time:", error);
    }
};

// Export the function so it can be imported and used in other files
export default recordTestTime;  