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
        setError(null); // Reset any previous errors

        if (userInput.trim() !== "") {
            try {
                const res = await fetch(`/api/chatbot/?user_input=${encodeURIComponent(userInput)}`);
                if (!res.ok) {
                    throw new Error(`HTTP error! Status: ${res.status}`);
                }
                const data = await res.json();
                console.log("API Response:", data); // Debugging: log API response
                setResponse(data.response);
            } catch (err) {
                console.error("Error fetching chatbot response:", err);
                setError("Failed to fetch the chatbot response. Please try again.");
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
