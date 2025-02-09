// src/components/Chatbot.js
import React, { useState } from "react";
import axios from "axios";

const Chatbot = () => {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleUserInput = async () => {
    try {
      const response = await axios.get(`/api/chatbot/?user_input=${userInput}`);
      const botResponse = response.data.response;

      // Update chat history with user input and bot response
      setMessages([
        ...messages,
        { text: userInput, sender: "user" },
        { text: botResponse, sender: "bot" }
      ]);
      setUserInput(""); // Clear input field
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
    }
  };

  return (
    <div>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={msg.sender}>
            {msg.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Ask me something"
      />
      <button onClick={handleUserInput}>Send</button>
    </div>
  );
};

export default Chatbot;
