import React, { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight, faLink, faTimesCircle, faThumbsUp, faThumbsDown } from '@fortawesome/free-solid-svg-icons';
import ReactMarkdown from 'react-markdown';
import { v4 as uuidv4 } from 'uuid'; // Import uuid for generating message IDs
import "./Chatbot.css";

const API_SERVICE = "http://localhost:8000";

const Chatbot = ({ messages, currentChatId, userUUID, onSendMessage, onNewConversationCreated, onUpdateMessageFeedback}) => {  const QUERY_SERVICE = `${API_SERVICE}/chat/query/`;
  const DOCUMENT_PARSER_SERVICE = `${API_SERVICE}/document-parser/process-upload/`;
  const [inputText, setInputText] = useState("");
  const [attachedFiles, setAttachedFiles] = useState([]); 
  const [uploadedContent, setUploadedContent] = useState("");
  const [loading, setLoading] = useState(false);

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
    console.log('Sending message:', inputText);
    if (inputText.trim() === "" && attachedFiles.length === 0) return;

    const humanMessage = {
        text: inputText,
        sender: "user",
        files: attachedFiles.map((file) => file.name),
    };

    let conversationId = currentChatId;

    // If no conversation exists, create one and wait for ChatPage to update state
    if (!conversationId) {
        conversationId = uuidv4();
        const newConversation = await createConversation(userUUID, conversationId, inputText);

        if (newConversation) {
            onNewConversationCreated(newConversation[0]);
            await new Promise((resolve) => setTimeout(resolve, 100)); // Wait for state update
        }
    }

    console.log("Using conversation ID:", conversationId);

    // Insert the user message into the database
    const insertedMessage = await insertMessage(conversationId, humanMessage.sender, humanMessage.text);
    if (insertedMessage) {
        onSendMessage(insertedMessage);
    }

    setInputText("");
    setAttachedFiles([]);
    setLoading(true);

    try {
        const chatHistoryString = formatChatHistory([...messages, humanMessage]);

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
        const botMessage = {
            sender: 'bot',
            text: data.answer,
        };

        const insertedBotMessage = await insertMessage(conversationId, botMessage.sender, botMessage.text);
        if (insertedBotMessage) {
            onSendMessage(insertedBotMessage);
        }
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = {
            sender: 'bot',
            text: "Something went wrong",
        };
        const insertedErrorMessage = await insertMessage(conversationId, errorMessage.sender, errorMessage.text);
        if (insertedErrorMessage) {
            onSendMessage(insertedErrorMessage);
        }
    } finally {
        setLoading(false);
    }
};

  const insertMessage = async (conversationId, sender, text) => {
    try {
      // Insert message into the database
      const response = await fetch(`${API_SERVICE}/messages/insert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          sender: sender,
          text: text,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        return data.data;
      } else {
        console.error('Error inserting message:', data);
        return null;
      }
    } catch (error) {
      console.error('Failed to insert message:', error);
      return null;
    }
  };

  const createConversation = async (userId, conversationId, conversationTitle) => {
    try {
      const response = await fetch(`${API_SERVICE}/conversations/insert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          user_id: userId,
          conversation_title: conversationTitle,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        return data.data;
      } else {
        console.error('Error creating conversation:', data);
        return null;
      }
    } catch (error) {
      console.error('Failed to create conversation:', error);
      return null;
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

  const handleFileChange = async (e) => {
    const uploadedFiles = Array.from(e.target.files);

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

      const extractedContents = await Promise.all(
        validFiles.map(file => uploadAndExtractFile(file))
      );
      setUploadedContent(extractedContents.join(" "));
    }
  };

  const handleFeedback = async (message, feedback) => {
    console.log('Feedback:', feedback, "for message:", message.text);
    
    onUpdateMessageFeedback(message.message_id, feedback);

    try {
      const response = await fetch(`${API_SERVICE}/messages/${message.message_id}/useful?is_useful=${feedback}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        }
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
          {messages.flatMap(innerArray => innerArray).map((msg, index) => {
            return (
              <div key={index} className={`message-container ${msg.sender}`}>
                {msg.sender === "user" && msg.files && msg.files.length > 0 && (
                  <div className="attached-files-message">
                    <strong>Attached Files:</strong>
                    <ul>
                      {msg.files.map((file, fileIndex) => (
                        <li key={fileIndex}>{file}</li>
                      ))}
                    </ul>
                  </div>
                )}
                <div className={`message ${msg.sender}`}>
                  <ReactMarkdown
                    components={{
                      p(props) {
                        const { node, ...rest } = props;
                        return <p style={{ margin: '0' }} {...rest} />;
                      }
                    }}
                  >
                    {msg.text}
                  </ReactMarkdown>
                </div>

                {msg.sender === 'bot' && (
                  <div className="feedback-buttons">
                    <button
                      className={`feedback-button ${msg.is_useful === true ? 'liked' : ''}`} 
                      onClick={() => handleFeedback(msg, true)}
                      title="Like"
                    >
                      <FontAwesomeIcon icon={faThumbsUp} />
                    </button>
                    <button
                      className={`feedback-button ${msg.is_useful === false ? 'disliked' : ''}`} 
                      onClick={() => handleFeedback(msg, false)}
                      title="Dislike"
                    >
                      <FontAwesomeIcon icon={faThumbsDown} />
                    </button>
                  </div>
                )}
              </div>
            );
          })}

          {loading && <div className="loading-dots">...</div>}
        </div>
      )}
      
      <div className="input-container">
        <FontAwesomeIcon 
          icon={faLink} 
          className="link-icon" 
          onClick={() => document.getElementById("fileInput").click()}
        />
        <input
          type="file"
          id="fileInput"
          style={{ display: "none" }}
          onChange={handleFileChange}
          multiple 
          accept=".docx,.pdf" 
        />

        <div
          className="input-box"
          contentEditable
          placeholder={messages.length === 0 ? "Type your message..." : ""}
          onInput={(e) => setInputText(e.target.textContent)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSendMessage();
            }
          }}
          spellCheck="false"
          data-gramm="false"
          data-gramm_editor="false"
          role="textbox"
          aria-placeholder={messages.length === 0 ? "Type your message..." : ""}
        ></div>

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
