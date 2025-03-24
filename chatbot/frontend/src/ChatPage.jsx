import React, { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import Chatbot from "./Chatbot/Chatbot";
import ChatHistory from "./ChatHistory/ChatHistory";
import FeedbackForm from "./FeedbackForm/FeedbackForm";
import "./ChatPage.css";

const API_SERVICE = "http://localhost:8000";

const getUserUUID = () => {
  let userUUID = localStorage.getItem("userUUID");
  if (!userUUID) {
    userUUID = uuidv4();
    localStorage.setItem("userUUID", userUUID);
  }
  return userUUID;
};

/*
const fetchUserConversations = async (userId) => {
  try {
    const response = await fetch(`${API_SERVICE}/users/${userId}/conversations`);
    const data = await response.json();
    if (response.ok) {
      return data.data;
    } else {
      console.error('Error fetching user conversations:', data);
      return [];
    }
  } catch (error) {
    console.error('Failed to fetch user conversations:', error);
    return [];
  }
};
*/

const fetchConversationMessages = async (conversationId) => {
  try {
    const response = await fetch(`${API_SERVICE}/conversations/${conversationId}/messages`);
    const data = await response.json();
    if (response.ok) {
      return data.data;
    } else {
      console.error('Error fetching conversation messages:', data);
      return [];
    }
  } catch (error) {
    console.error('Failed to fetch conversation messages:', error);
    return [];
  }
};

const deleteConversation = async (conversationId) => {
  try {
    const response = await fetch(`${API_SERVICE}/conversations/${conversationId}`, {
      method: 'DELETE',
    });
    const data = await response.json();
    if (response.ok) {
      return data.data;
    } else {
      console.error('Error deleting conversation:', data);
      return null;
    }
  } catch (error) {
    console.error('Failed to delete conversation:', error);
    return null;
  }
};

const ChatPage = () => {
  const userUUID = getUserUUID();
  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [showChatHistory, setShowChatHistory] = useState(true);
  const [showFeedback, setShowFeedback] = useState(false);
  const [idleTimer, setIdleTimer] = useState(null);

  useEffect(() => {
    const loadUserConversations = async () => {
    const conversations = await fetchUserConversations(userUUID);
      setChatHistory(conversations);
    };
    loadUserConversations();
  }, [userUUID]);

  useEffect(() => {
    console.log("messages ", messages)
  }, [messages])

  const handleNewChat = async () => {
    setCurrentChatId(null); 
    setMessages([]); 
  };

  const handleLoadChat = async (chatId) => {
    setCurrentChatId(chatId); 
    const messages = await fetchConversationMessages(chatId);
    setMessages(messages);
  };

  const handleUpdateMessageFeedback = (messageId, feedback) => {
    setMessages((prevMessages) => {
      const updatedMessages = prevMessages.map(innerArray =>
        innerArray.map(msg =>
          msg.message_id === messageId ? { ...msg, is_useful: feedback } : msg
        )
      );
      return [...updatedMessages]; 
    });
  };
  

  const handleDeleteChat = async (chatId) => {
    await deleteConversation(chatId);
    setChatHistory((prevHistory) =>
      prevHistory.filter((chat) => chat.conversation_id !== chatId)
    );
    setMessages([]);
    setCurrentChatId(null);
  };

  const toggleChatHistory = () => {
    setShowChatHistory((prev) => !prev);
  };

  const handleFeedbackCancel = () => {
    setShowFeedback(false); 
    resetIdleTimer(); 
  };
  
  const resetIdleTimer = () => {
    if (idleTimer) {
      clearTimeout(idleTimer); 
    }
    setIdleTimer(
      setTimeout(() => {
        setShowFeedback(true); 
      }, 300000) 
    );
  };
  useEffect(() => {
    console.log("Updated chatHistory", chatHistory);
  }, [chatHistory]);

  const handleNewConversationCreated = (newChat) => {
    console.log("creating new chat ", newChat);
    setCurrentChatId(newChat.conversation_id);
    console.log("Before", chatHistory)
    setChatHistory((prev) => [
      {
        ...newChat, 
      },
      ...prev,
    ]);    

    setMessages([]); 
    console.log("After", chatHistory)

  };

  const sendEmail = async (conversationId) => {
    try {
      const response = await fetch(`${API_SERVICE}/conversations/${conversationId}/send-email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
  
      if (!response.ok) {
        throw new Error("Failed to send email");
      }
  
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error sending email:", error);
    }
  };
  
  const handleExportChat = async (chatId) => {
    const emailData = await sendEmail(chatId);
    if (emailData) {
      const subject = encodeURIComponent(emailData.subject);
      const body = encodeURIComponent(emailData.body);
      const recipients = emailData.recipients.join(",");
  
      const mailtoLink = `mailto:${recipients}?subject=${subject}&body=${body}`;
      window.location.href = mailtoLink; 
  };
};
  
  
  
  
  useEffect(() => {
    resetIdleTimer();
    window.addEventListener("mousemove", resetIdleTimer);
    window.addEventListener("keydown", resetIdleTimer);
    window.addEventListener("click", resetIdleTimer);
    window.addEventListener("scroll", resetIdleTimer);
  
    return () => {
      if (idleTimer) clearTimeout(idleTimer); // Cleanup the timer
      window.removeEventListener("mousemove", resetIdleTimer);
      window.removeEventListener("keydown", resetIdleTimer);
      window.removeEventListener("click", resetIdleTimer);
      window.removeEventListener("scroll", resetIdleTimer);
    };
  }, [showFeedback]);
  

  return (
    <div className="chat-page">
      <button onClick={toggleChatHistory} className="menu-button">
        ☰
      </button>
      {showChatHistory && (
        <ChatHistory
          chatHistory={chatHistory}
          onNewChat={handleNewChat}
          onLoadChat={handleLoadChat}
          onDeleteChat={handleDeleteChat}
          onExportChat={handleExportChat}
        />
      )}
      <Chatbot
        messages={messages}
        currentChatId={currentChatId}
        userUUID={userUUID}
        onSendMessage={(message) => setMessages((prev) => [...prev, message])}
        onNewConversationCreated={handleNewConversationCreated}
        onUpdateMessageFeedback={handleUpdateMessageFeedback}
      />
      {showFeedback && <FeedbackForm conversationId = {currentChatId} onClose={handleFeedbackCancel} />}
    </div>
  );
};

export default ChatPage;