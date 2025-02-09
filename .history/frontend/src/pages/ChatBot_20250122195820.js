import React, { useState } from "react";

const Chatbot = () => {
    const [userInput, setUserInput] = useState("");
    const [response, setResponse] = useState("");
    const [error, setError] = useState(null);

    const handleInputChange = (event) => {
        setUserInput(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null); // Clear previous errors
    
        if (userInput.trim() !== "") {
            try {
                const response = await fetch("http://127.0.0.1:8000/api/chatbot/?user_input=" + encodeURIComponent(userInput), {
                    method: "GET",
                });
    
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
    
                const data = await response.json();
                console.log("API Response:", data); // Log response for debugging
                setResponse(data.response);
            } catch (err) {
                console.error("Error fetching chatbot response:", err);
                setError(`Failed to fetch the chatbot response. Error: ${err.message}`);
            }
        }
    };
    

    return (
        <div>
            <h1>Chat with Us</h1>
            <textarea
                value={userInput}
                onChange={handleInputChange}
                placeholder="Ask me about insurance costs..."
            />
            <button onClick={handleSubmit}>Ask</button>
            <div>
                {error && <p style={{ color: "red" }}>{error}</p>}
                <h3>Response:</h3>
                <p>{response}</p>
            </div>
        </div>
    );
};

export default Chatbot;
