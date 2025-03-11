import React, { useState, useRef } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight, faLink, faTimesCircle, faThumbsUp, faThumbsDown } from '@fortawesome/free-solid-svg-icons';
import ReactMarkdown from 'react-markdown';
import "./Chatbot.css";

const Chatbot = ({ messages, onSendMessage, setIsChatModified }) => {
  const QUERY_SERVICE = "http://localhost:8000/chat/query/";
  const DOCUMENT_PARSER_SERVICE = "http://localhost:8000/document-parser/process-upload/";
  const [inputText, setInputText] = useState("");
  const [attachedFiles, setAttachedFiles] = useState([]); 
  const [uploadedContent, setUploadedContent] = useState("");
  const textareaRef = useRef(null);

  const autoResizeTextarea = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';  
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; 
    }
  };

  const handleDeleteFile = (index) => { 
    const updatedFiles = attachedFiles.filter((_, i) => i !== index);
    setAttachedFiles(updatedFiles);
    if (updatedFiles.length === 0) {
      setUploadedContent("");
    }
  };

  const formatChatHistory = (messages) => {
    return messages
      .map((msg) => `${msg.sender}:${msg.text}`) 
      .join("\n\n");
  };

  const handleSendMessage = async () => {
    if (inputText.trim() === "" && attachedFiles.length === 0) return;
  
    // Create a new message object with file information
    const newMessage = { 
      text: inputText, 
      sender: "Human", 
      files: attachedFiles.map(file => file.name) // Include file names
    }; 
  
    onSendMessage(newMessage);
    
    setInputText(""); 
    setAttachedFiles([]);
  
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";  
    }
  
    try {
      const chatHistoryString = formatChatHistory([...messages, newMessage]);
      console.log("Formatted History:", chatHistoryString); 
  
      const response = await fetch(QUERY_SERVICE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          user_query: inputText,
          chat_history: chatHistoryString,
          uploaded_content: uploadedContent,
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

  const uploadAndExtractFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(DOCUMENT_PARSER_SERVICE, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    return data.text_chunks.join(" ");
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

  const handleFileChange = async (e) => {
    const uploadedFiles = Array.from(e.target.files);

    // Check if the total number of files exceeds 3
    if (uploadedFiles.length + attachedFiles.length > 3) {
      alert("You can only upload a maximum of 3 files.");
      return;
    }

    const validFiles = uploadedFiles.filter(file => 
      file.type === "application/pdf" || 
      file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    );

    if (validFiles.length !== uploadedFiles.length) {
      alert("Only .docx and .pdf files are allowed.");
    }

    if (validFiles.length > 0) {
      setAttachedFiles([...attachedFiles, ...validFiles]);

      // Extract content from all files
      const extractedContents = await Promise.all(
        validFiles.map(file => uploadAndExtractFile(file))
      );
      setUploadedContent(extractedContents.join(" "));
    }
  };

  const handleLinkClick = () => {
    document.getElementById("fileInput").click();
  };

  const handleFeedback = async (message, feedback) => {
    console.log('Feedback:', feedback, "for message:", message.text);
    try {
      const response = await fetch(FEEDBACK_SERVICE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.text,
          feedback: feedback,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send feedback');
      }

      console.log('Feedback sent successfully');
    } catch (error) {
      console.error('Error sending feedback:', error);
    }
  };

  return (
    <div className="chat-container">
      {messages.length === 0 ? (
        <h2 className="placeholder">Ask NUS ODPRT anything!</h2>
      ) : (
        <div className="chat-box">
  {messages.map((msg, index) => {
    const result = msg.text;
    return (
      <div key={index} className={`message-container ${msg.sender}`}>
        {/* Display attached files outside the message container for human messages */}
        {msg.sender === "Human" && msg.files && msg.files.length > 0 && (
          <div className="attached-files-message">
            <strong>Attached Files:</strong>
            <ul>
              {msg.files.map((file, fileIndex) => (
                <li key={fileIndex}>{file}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Display the message text inside the message container */}
        <div className={`message ${msg.sender}`}>
          <ReactMarkdown
            components={{
              p(props) {
                const { node, ...rest } = props;
                return <p style={{ margin: '0' }} {...rest} />;
              }
            }}
          >
            {result}
          </ReactMarkdown>
          
        </div>
        {msg.sender === 'AI' && (
            <div className="feedback-buttons">
              <button className="feedback-button" 
                onClick={() => handleFeedback(msg, 'like')}
                title="Like"
              >
                <FontAwesomeIcon icon={faThumbsUp} />
              </button>
              <button className="feedback-button" 
                onClick={() => handleFeedback(msg, 'dislike')}
                title="Dislike"
              >
                <FontAwesomeIcon icon={faThumbsDown} />
              </button>
            </div>
          )}
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
          multiple 
          accept=".docx,.pdf" 
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
          icon={faArrowRight} 
          className="send-icon" 
          onClick={handleSendMessage}
        />
      </div>
      <div className="attached-files">
          {attachedFiles.map((file, index) => (
            <div key={index} className="file-item">
              <span>{file.name}</span>
              <FontAwesomeIcon 
                icon={faTimesCircle} 
                className="delete-icon" 
                onClick={() => handleDeleteFile(index)}
              />
            </div>
          ))}
        </div>
    </div>
  );
};

export default Chatbot;