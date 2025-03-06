import React, { useState, useEffect } from "react";
import Chatbot from "./Chatbot/Chatbot";
import ChatHistory from "./ChatHistory/ChatHistory";
import FeedbackForm from "./FeedbackForm/FeedbackForm";
import "./ChatPage.css";

// Function to get a cookie value by name
const getCookie = (name) => {
  return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
};

// Function to set a cookie with a specified name, value, and expiration time in days
const setCookie = (name, value, days) => {
  const expires = new Date();
  expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
  document.cookie = `${name}=${value}; path=/; expires=${expires.toUTCString()}`;
};

// Function to get or create a unique user ID and store it in a cookie
const getUserId = () => {
  let userId = getCookie("userId");
  if (!userId) {
    userId = `user-${Date.now()}-${Math.random().toString(36).substring(2, 15)}`;
    setCookie("userId", userId, 365);
  }
  return userId;
};

// Function to send user data to the backend (database)
const sendToBackend = async (userId, chatHistory, preferences) => {
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
  const userId = getUserId();
  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState(() => JSON.parse(localStorage.getItem("chatHistory")) || []);
  const [currentChatId, setCurrentChatId] = useState(() => JSON.parse(localStorage.getItem("currentChatId")) || null);
  const [showChatHistory, setShowChatHistory] = useState(() => JSON.parse(localStorage.getItem("showChatHistory")) ?? true);
  const [showFeedback, setShowFeedback] = useState(false);

  // Effect to send user data to the backend when the userId is detected or updated
  useEffect(() => {
    if (userId) {
      const preferences = { showChatHistory }; // Add more preferences if needed
      sendToBackend(userId, chatHistory, preferences); // Send to backend when user data changes

      if (chatHistory.length > 0 && currentChatId) {
        const savedChat = chatHistory.find(chat => chat.id === currentChatId);
        if (savedChat) {
          setMessages(savedChat.messages);
        }
      }
    }
  }, [userId, chatHistory, showChatHistory]); // Trigger when userId, chatHistory, or showChatHistory change

  // Effect to save data to local storage and send updated data to the backend
  useEffect(() => {
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
    localStorage.setItem("currentChatId", JSON.stringify(currentChatId));
    localStorage.setItem("showChatHistory", JSON.stringify(showChatHistory));

    sendToBackend(userId, chatHistory, { showChatHistory }); // Send updated data to backend

  }, [chatHistory, currentChatId, showChatHistory]);

  const handleSendMessage = (message) => {
    setMessages((prevMessages) => {
      const updatedMessages = [...prevMessages, message];
      if (currentChatId) {
        setChatHistory(prevHistory => prevHistory.map(chat =>
          chat.id === currentChatId ? { ...chat, messages: updatedMessages } : chat
        ));
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
    setChatHistory(updatedHistory);
    setMessages([]);
    setCurrentChatId(null);
  };

  useEffect(() => {
    if (messages.length > 0) {
      const chatIndex = chatHistory.length;
      const chatId = currentChatId || `${userId}-${chatIndex}`;
      const existingChat = chatHistory.find(chat => chat.id === chatId);

      if (existingChat) {
        setChatHistory(prevHistory =>
          prevHistory.map(chat =>
            chat.id === chatId ? { ...chat, messages } : chat
          )
        );
      } else {
        const newChat = {
          id: chatId,
          messages,
          date: new Date().toISOString(),
        };
        setChatHistory(prevHistory => [newChat, ...prevHistory].slice(0, 10));
      }

      if (!currentChatId) {
        setCurrentChatId(chatId);
      }
    }
  }, [messages]);

  const toggleChatHistory = () => {
    setShowChatHistory(prev => {
      const newState = !prev;
      localStorage.setItem("showChatHistory", JSON.stringify(newState));
      return newState;
    });
  };

  const handleFeedbackSubmit = () => setShowFeedback(false);
  const handleFeedbackClose = () => setShowFeedback(false);

  return (
    <div className="chat-page">
      <button onClick={toggleChatHistory} className="menu-button">☰</button>
      {showChatHistory && (
        <ChatHistory chatHistory={chatHistory} onNewChat={handleNewChat} onLoadChat={handleLoadChat} onDeleteChat={handleDeleteChat} />
      )}
      <Chatbot messages={messages} onSendMessage={handleSendMessage} />
      {showFeedback && <FeedbackForm onSubmit={handleFeedbackSubmit} onClose={handleFeedbackClose} />}
    </div>
  );
};

export default ChatPage;
