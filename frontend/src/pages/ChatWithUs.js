import React, { useState } from "react";
import axios from "axios";
import "./ChatWithUs.css";

function Chatbot() {
    const [userInput, setUserInput] = useState("");
    const [chat, setChat] = useState([]);

    const handleSend = async () => {
        if (!userInput.trim()) return;

        // Update chat with user input
        setChat([...chat, { sender: "User", message: userInput }]);

        try {
            // Log user input
            console.log("User Input:", userInput);

            // Call Django API
            const res = await axios.post("http://127.0.0.1:8000/api/chatbot-response/", {
                query: userInput,
            });

            // Log the API response
            console.log("API Response:", res.data);

            // Update chat with chatbot's response
            if (res.data.response) {
                setChat([
                    ...chat,
                    { sender: "User", message: userInput },
                    { sender: "Chatbot", message: res.data.response },
                ]);
            } else {
                setChat([
                    ...chat,
                    { sender: "Chatbot", message: "Sorry, I did not get that." },
                ]);
            }

        } catch (error) {
            console.error("Error occurred:", error);
            setChat([
                ...chat,
                { sender: "Chatbot", message: "Error occurred. Please try again." },
            ]);
        }

        setUserInput(""); // Clear input field after sending
    };

    return (
        <div className="chatbot-container">
            <div className="chat-display">
                {chat.map((message, index) => (
                    <div key={index} className={`chat-message ${message.sender}`}>
                        <p>{message.message}</p>
                    </div>
                ))}
            </div>
            <div className="chat-input">
                <input
                    type="text"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    placeholder="Type your message..."
                />
                <button onClick={handleSend}>Send</button>
            </div>
        </div>
    );
}

export default Chatbot;
