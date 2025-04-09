import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEnvelope, faPlus, faTrash, faSpinner  } from "@fortawesome/free-solid-svg-icons";
import "./ChatHistory.css";

const ChatHistory = ({ chatHistory, onNewChat, onLoadChat, onDeleteChat, onExportChat }) => {
  const [exportingChatId, setExportingChatId] = useState(null);

  const handleExport = async (conversationId) => {
    setExportingChatId(conversationId);
    try {
      await onExportChat(conversationId);
    } finally {
      setExportingChatId(null);
    }
  };


  // Group chats by created_at date
  const groupedChats = chatHistory.reduce((acc, chat) => {
    const chatDate = new Date(chat.created_at).toDateString();
    if (!acc[chatDate]) {
      acc[chatDate] = [];
    }
    acc[chatDate].push(chat);
    return acc;
  }, {});

  return (
    <div className="chat-history">
      {/* Header Section */}
      <div className="chat-header">
        <h2 className="chat-history-title">Chat History</h2>
        <FontAwesomeIcon className="new-chat-btn" icon={faPlus} onClick={onNewChat} />
      </div>

      {/* Chat List */}
      {Object.keys(groupedChats).length > 0 ? (
        <ul>
          {Object.entries(groupedChats).map(([date, chats], index) => {
            const today = new Date().toDateString();
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);

            let formattedDate =
              date === today
                ? "Today"
                : date === yesterday.toDateString()
                ? "Yesterday"
                : new Date(date).toLocaleDateString();

            return (
              <li key={index}>
                <div className="chat-date">{formattedDate}</div>
                <ul className="chat-group">
                  {chats.map((chat) => (
                    <li key={chat.conversation_id} className="chat-item">
                      <div className = "chat-title" onClick={() => onLoadChat(chat.conversation_id)}>
                        {chat.conversation_title}
                      </div>
                      <FontAwesomeIcon 
                        className="email-btn"
                        icon={exportingChatId === chat.conversation_id ? faSpinner : faEnvelope}
                        spin={exportingChatId === chat.conversation_id}
                        title="Email Correspondent"
                        onClick={() => handleExport(chat.conversation_id)}
                      />
                      <FontAwesomeIcon
                        className="delete-btn"
                        icon={faTrash}
                        title="Delete Chat"
                        onClick={() => onDeleteChat(chat.conversation_id)}
                      />
                    </li>
                  ))}
                </ul>
              </li>
            );
          })}
        </ul>
      ) : (
        <p>No chat history available.</p>
      )}
    </div>
  );
};

export default ChatHistory;
