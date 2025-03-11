import React, { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import Chatbot from "./Chatbot/Chatbot";
import ChatHistory from "./ChatHistory/ChatHistory";
import FeedbackForm from "./FeedbackForm/FeedbackForm";
import "./ChatPage.css";

// Generate or retrieve userUUID from localStorage
const getUserUUID = () => {
  let userUUID = localStorage.getItem("userUUID");
  if (!userUUID) {
    userUUID = uuidv4();
    localStorage.setItem("userUUID", userUUID);
  }
  return userUUID;
};

const sendToBackend = async (userId, chatHistory) => {
  try {
    const response = await fetch('/api/saveUserData', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userId,
        chatHistory,
      }),
    });

    const data = await response.json();
    if (response.ok) {
      console.log('Data saved successfully:', data);
    } else {
      console.error('Error saving data:', data);
    }
  } catch (error) {
    console.error('Failed to send data to the backend:', error);
  }
};

const ChatPage = () => {
  const userUUID = getUserUUID();
  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [showChatHistory, setShowChatHistory] = useState(true);

  // Function to handle chat history updates
  const updateChatHistory = (newChatHistory) => {
    setChatHistory(newChatHistory);
    // Optionally, you can send the updated chat history to the backend here
    sendToBackend(userUUID, newChatHistory);
  };

  const handleSendMessage = (message) => {
    setMessages((prevMessages) => {
      const updatedMessages = [...prevMessages, message];
      if (currentChatId) {
        const updatedHistory = chatHistory.map(chat =>
          chat.id === currentChatId ? { ...chat, messages: updatedMessages } : chat
        );
        updateChatHistory(updatedHistory);
      }
      return updatedMessages;
    });
  };

  const handleNewChat = () => {
    setMessages([]);
    setCurrentChatId(null);
  };

  const handleLoadChat = (chatId) => {
    const selectedChat = chatHistory.find((chat) => chat.id === chatId);
    if (selectedChat) {
      setMessages(selectedChat.messages);
      setCurrentChatId(selectedChat.id);
    }
  };

  const handleDeleteChat = (chatId) => {
    const updatedHistory = chatHistory.filter((chat) => chat.id !== chatId);
    updateChatHistory(updatedHistory);
    setMessages([]);
    setCurrentChatId(null);
  };

  useEffect(() => {
    if (messages.length > 0) {
      const chatIndex = chatHistory.length;
      const chatId = currentChatId || `${userUUID}-${chatIndex}`;
      const existingChat = chatHistory.find(chat => chat.id === chatId);

      if (existingChat) {
        const updatedHistory = chatHistory.map(chat =>
          chat.id === chatId ? { ...chat, messages } : chat
        );
        updateChatHistory(updatedHistory);
      } else {
        const newChat = {
          id: chatId,
          messages,
          date: new Date().toISOString(),
        };
        const updatedHistory = [newChat, ...chatHistory].slice(0, 10);
        updateChatHistory(updatedHistory);
      }

      if (!currentChatId) {
        setCurrentChatId(chatId);
      }
    }
  }, [messages]);

  const toggleChatHistory = () => {
    setShowChatHistory(prev => !prev);
  };

  return (
    <div className="chat-page">
      <button onClick={toggleChatHistory} className="menu-button">☰</button>
      {showChatHistory && (
        <ChatHistory chatHistory={chatHistory} onNewChat={handleNewChat} onLoadChat={handleLoadChat} onDeleteChat={handleDeleteChat} />
      )}
      <Chatbot messages={messages} onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatPage;