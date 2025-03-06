import React, { useState, useRef } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faLink, faTimesCircle } from '@fortawesome/free-solid-svg-icons';
import ReactMarkdown from 'react-markdown';
import "./Chatbot.css";

const Chatbot = ({ messages, onSendMessage, setIsChatModified }) => {
  const QUERY_SERVICE = "http://localhost:8000/chat/query/";
  const [inputText, setInputText] = useState("");
  const [attachedFile, setAttachedFile] = useState(null);
  const textareaRef = useRef(null);

  // Function to auto-resize the textarea
  const autoResizeTextarea = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';  
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; 
    }
  };

  const handleDeleteFile = () => { 
    setAttachedFile(null);
  };

  const formatChatHistory = (messages) => {
    return messages
      .map((msg) => `${msg.sender}:${msg.text}`) 
      .join("\n\n");
  };

  const handleSendMessage = async () => {
    if (inputText.trim() === "") return;

    const newMessage = { text: inputText, sender: "Human" }; 
    onSendMessage(newMessage);
    
    setInputText(""); 
    setAttachedFile(null);

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";  
    }

    try {
      const chatHistoryString = formatChatHistory([...messages, newMessage]);
      console.log("Formatted History:", chatHistoryString); 

      //link for api endpoint
      const response = await fetch(QUERY_SERVICE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          user_query: inputText,
          chat_history: chatHistoryString,
        }),
      });

      const data = await response.json();
      const botMessage = { sender: 'AI', text: data.answer };
      
      onSendMessage(botMessage);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { 
        sender: 'AI', 
        text: "Something went wrong"
      };
      onSendMessage(errorMessage);
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
          {messages.map((msg, index) => {
            console.log(msg.text); // Debug the string
            const result = msg.text.trim() ;
            return (
              <div key={index} className={`message ${msg.sender}`}>
                <ReactMarkdown
                  components={{

                    // Modify `p` to reduce padding
                    p(props) {
                      const { node, ...rest } = props;
                      return <p style={{ margin: '0' }} {...rest} />;
                    }
                  }}
                >
                  {result}
                </ReactMarkdown>

              </div>
            );
          })}
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
          <span>Attached file: {attachedFile.name}</span>
          <FontAwesomeIcon
            icon={faTimesCircle}
            className="delete-icon"
            onClick={handleDeleteFile}
          />
        </div>
      )}
    </div>
  );
};

export default Chatbot;