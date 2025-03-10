import React, { useState, useEffect } from "react";
import Chatbot from "./Chatbot/Chatbot";
import ChatHistory from "./ChatHistory/ChatHistory";
import FeedbackForm from "./FeedbackForm/FeedbackForm";
import "./ChatPage.css";

const getCookie = (name) => {
  return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
};

const setCookie = (name, value, days) => {
  const expires = new Date();
  expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
  document.cookie = `${name}=${value}; path=/; expires=${expires.toUTCString()}`;
};

const getUserId = () => {
  let userId = getCookie("userId");
  if (!userId) {
    userId = `user-${Date.now()}-${Math.random().toString(36).substring(2, 15)}`;
    setCookie("userId", userId, 365);
  }
  return userId;
};

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
  const [idleTimer, setIdleTimer] = useState(null);

  useEffect(() => {
    const resetIdleTimer = () => {
      if (idleTimer) clearTimeout(idleTimer);
      setIdleTimer(setTimeout(() => setShowFeedback(true), 30000)); // 5 minutes
    };

    resetIdleTimer();
    window.addEventListener("mousemove", resetIdleTimer);
    window.addEventListener("keydown", resetIdleTimer);
    window.addEventListener("click", resetIdleTimer);
    window.addEventListener("scroll", resetIdleTimer);

    return () => {
      if (idleTimer) clearTimeout(idleTimer);
      window.removeEventListener("mousemove", resetIdleTimer);
      window.removeEventListener("keydown", resetIdleTimer);
      window.removeEventListener("click", resetIdleTimer);
      window.removeEventListener("scroll", resetIdleTimer);
    };
  }, []);

  useEffect(() => {
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
    localStorage.setItem("currentChatId", JSON.stringify(currentChatId));
    localStorage.setItem("showChatHistory", JSON.stringify(showChatHistory));
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

  const handleFeedbackClose = () => setShowFeedback(false);

  return (
    <div className="chat-page">
      <button onClick={toggleChatHistory} className="menu-button">☰</button>
      {showChatHistory && (
        <ChatHistory chatHistory={chatHistory} onNewChat={handleNewChat} onLoadChat={handleLoadChat} onDeleteChat={handleDeleteChat} />
      )}
      <Chatbot messages={messages} onSendMessage={handleSendMessage} />
      {showFeedback && <FeedbackForm onClose={handleFeedbackClose} />}
    </div>
  );
};

export default ChatPage;
