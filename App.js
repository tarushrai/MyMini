import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // Function to send user input to the backend
  const sendMessage = async () => {
    if (input.trim() === '') return;
    
    const userMessage = { message: input, user_id: '12345' };  // Example user_id
    
    // Add user message to the messages list
    setMessages([...messages, { sender: 'user', text: input }]);
    
    try {
      // Send user message to the backend
      const response = await axios.post('http://localhost:5000/chat', userMessage);
      const botResponse = response.data.response;
      
      // Add bot response to the messages list
      setMessages([...messages, { sender: 'user', text: input }, { sender: 'bot', text: botResponse }]);
      
    } catch (error) {
      console.error("Error communicating with chatbot", error);
    }

    // Clear the input field
    setInput('');
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input 
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
