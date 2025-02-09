import React, { useState } from "react";

const Chatbot = () => {
    const [userInput, setUserInput] = useState("");
    const [response, setResponse] = useState("");

    const handleInputChange = (event) => {
        setUserInput(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (userInput.trim() !== "") {
            // Call the backend API to get the chatbot response
            const res = await fetch(`/api/chatbot/?user_input=${encodeURIComponent(userInput)}`);
            const data = await res.json();
            setResponse(data.response);
        }
    };

    return (
        <div>
            <h1>Chat with Us</h1>
            <div>
                <textarea
                    value={userInput}
                    onChange={handleInputChange}
                    placeholder="Ask me about insurance costs..."
                />
            </div>
            <button onClick={handleSubmit}>Ask</button>
            <div>
                <h3>Response:</h3>
                <p>{response}</p>
            </div>
        </div>
    );
};

export default Chatbot;
