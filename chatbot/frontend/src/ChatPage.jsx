import React, { useState, useEffect } from "react";
import Chatbot from "./Chatbot/Chatbot";
import ChatHistory from "./ChatHistory/ChatHistory";
import FeedbackForm from "./FeedbackForm/FeedbackForm";
import "./ChatPage.css";

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState(() => JSON.parse(localStorage.getItem("chatHistory")) || []);
  const [isChatModified, setIsChatModified] = useState(false);
  const [currentChatId, setCurrentChatId] = useState(() => JSON.parse(localStorage.getItem("currentChatId")) || null);
  const [showChatHistory, setShowChatHistory] = useState(() => JSON.parse(localStorage.getItem("showChatHistory")) ?? true);
  const [showFeedback, setShowFeedback] = useState(false);

  let inactivityTimer;
  const resetTimer = () => {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => setShowFeedback(true), 300000);
  };

  useEffect(() => {
    if (chatHistory.length > 0 && currentChatId) {
      const savedChat = chatHistory.find(chat => chat.id === currentChatId);
      if (savedChat) {
        setMessages(savedChat.messages);
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
    localStorage.setItem("currentChatId", JSON.stringify(currentChatId));
    localStorage.setItem("showChatHistory", JSON.stringify(showChatHistory));
  }, [chatHistory, currentChatId, showChatHistory]);

  useEffect(() => {
    if (messages.length > 0) {
      const chatId = currentChatId || messages[0].text; 
      const existingChat = chatHistory.find(chat => chat.id === chatId);

      if (existingChat) {
        // Update the existing chat
        setChatHistory(prevHistory =>
          prevHistory.map(chat =>
            chat.id === chatId ? { ...chat, messages } : chat
          )
        );
      } else {
        // Create a new chat and add it to chatHistory
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

  useEffect(() => {
    window.addEventListener('mousemove', resetTimer);
    window.addEventListener('keydown', resetTimer);
    window.addEventListener('scroll', resetTimer);
    resetTimer();
    return () => {
      window.removeEventListener('mousemove', resetTimer);
      window.removeEventListener('keydown', resetTimer);
      window.removeEventListener('scroll', resetTimer);
    };
  }, []);

  const handleSendMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
    resetTimer();
  };

  const handleNewChat = () => {
    if (messages.length > 0) {
      const chatId = messages[0].text;
      if (!chatHistory.some(chat => chat.id === chatId)) {
        const newChat = {
          id: chatId,
          messages,
          date: new Date().toISOString(),
        };
        setChatHistory(prevHistory => [newChat, ...prevHistory].slice(0, 10)); // Keep only the last 10 chats
      }
    }

    setMessages([]);
    setIsChatModified(false);
    setCurrentChatId(null);
  };

  const handleLoadChat = (chatId) => {
    const selectedChat = chatHistory.find((chat) => chat.id === chatId);
    if (selectedChat) {
      setMessages(selectedChat.messages);
      setCurrentChatId(selectedChat.id);
    }
    setIsChatModified(false);
  };

  const handleDeleteChat = (chatId) => {
    const updatedHistory = chatHistory.filter((chat) => chat.id !== chatId);
    setChatHistory(updatedHistory);
    setMessages([]);
    setIsChatModified(false);
    setCurrentChatId(null);
  };

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
      <Chatbot messages={messages} onSendMessage={handleSendMessage} setIsChatModified={setIsChatModified} />
      {showFeedback && <FeedbackForm onSubmit={handleFeedbackSubmit} onClose={handleFeedbackClose} />}
    </div>
  );
};

export default ChatPage;