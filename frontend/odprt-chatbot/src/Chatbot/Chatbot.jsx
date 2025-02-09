import React, { useState, useRef } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faLink } from '@fortawesome/free-solid-svg-icons';
import "./Chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [attachedFile, setAttachedFile] = useState(null);
  const textareaRef = useRef(null);

  const autoResizeTextarea = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';  
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; 
    }
  };

  const handleSendMessage = async () => {
    if (inputText.trim() === "") return;

    const newMessage = { text: inputText, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setInputText(""); 
    setAttachedFile(null);

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";  
    }

    try {
      /*
      const response = await fetch('', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
      });

      const data = await response.json();
      const botMessage = { sender: 'chatbot', text: data.message };
      */

      const botMessage = { sender: 'chatbot', text: "Bot received the message." };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { sender: 'chatbot', text: 'Something went wrong.' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();  
    }
  };

  const handleInputChange = (e) => {
    setInputText(e.target.value);
    autoResizeTextarea();
  };

  const handleFileChange = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setAttachedFile(uploadedFile);
    }
  };

  const handleLinkClick = () => {
    document.getElementById("fileInput").click();
  };

  return (
    <div className="chat-container">
      {messages.length === 0 ? (
        <h2 className="placeholder">Ask NUS ODPRT anything!</h2>
      ) : (
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>
      )}
      <div className="input-container">
        <FontAwesomeIcon 
          icon={faLink} 
          className="link-icon" 
          onClick={handleLinkClick}
        />
        <input
          type="file"
          id="fileInput"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
        <textarea
          ref={textareaRef}
          placeholder={messages.length === 0 ? "Type your message..." : ""}
          value={inputText}
          onChange={handleInputChange}
          onKeyDown={handleKeyPress}
          spellCheck="false"
          data-gramm="false"
          data-gramm_editor="false"
        />
        <FontAwesomeIcon 
          icon={faPaperPlane} 
          className="send-icon" 
          onClick={handleSendMessage}
        />
      </div>
      {attachedFile && (
        <div className="file-info">
          Attached file: {attachedFile.name}
        </div>
      )}
    </div>
  );
};

export default Chatbot;
