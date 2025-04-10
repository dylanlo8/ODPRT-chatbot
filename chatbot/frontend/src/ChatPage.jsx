/**
 * ChatPage component serves as the main interface for the chatbot application.
 * It manages user interactions, chat history, feedback, and communication with the backend API.
 */

import React, { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { FaComment } from "react-icons/fa";
import Chatbot from "./Chatbot/Chatbot";
import ChatHistory from "./ChatHistory/ChatHistory";
import FeedbackForm from "./FeedbackForm/FeedbackForm";
import "./ChatPage.css";

/**
 * Base URL for the backend API service.
 */
const API_SERVICE = "http://localhost:8000";

// Add this flag to track UUID creation
let isCreatingUser = false;

/**
 * Retrieves or generates a unique user identifier (UUID) stored in localStorage.
 * 
 * @returns {string} The user's UUID.
 */
const getUserUUID = async () => {
  let userUUID = localStorage.getItem("userUUID");

  // If UUID exists in localStorage, verify it in the database
  if (userUUID) {
    try {
      const response = await fetch(`${API_SERVICE}/users/${userUUID}`);
      const data = await response.json();
      
      if (data.exists) {
        return userUUID; // User exists, return the existing UUID
      }
      // User doesn't exist in database, will create a new one below
    } catch (error) {
      console.error("Error checking user UUID:", error);
      // Continue to create a new UUID on error
    }
  }

  // Create a new UUID if:
  // 1. No UUID in localStorage, OR
  // 2. UUID in localStorage but not in database
  userUUID = uuidv4();
  try {
    const createResponse = await fetch(`${API_SERVICE}/users/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        uuid: userUUID,
        faculty: "default_faculty", // Replace with actual faculty if available
      }),
    });

    if (createResponse.ok) {
      localStorage.setItem("userUUID", userUUID);
      return userUUID;
    } else {
      console.error("Failed to create user:", await createResponse.json());
      return null;
    }
  } catch (error) {
    console.error("Error creating user UUID:", error);
    return null;
  }
};

/**
 * Fetches the list of user conversations from the backend.
 * 
 * @param {string} userId - The unique identifier of the user.
 * @returns {Promise<Array>} A promise resolving to an array of user conversations.
 */
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

/**
 * Fetches the messages of a specific conversation from the backend.
 * 
 * @param {string} conversationId - The unique identifier of the conversation.
 * @returns {Promise<Array>} A promise resolving to an array of messages.
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

/**
 * Deletes a specific conversation from the backend.
 * 
 * @param {string} conversationId - The unique identifier of the conversation.
 * @returns {Promise<Object|null>} A promise resolving to the deleted conversation data or null if an error occurs.
 */
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

/**
 * Generates a topic for a chat based on its messages using the backend topic model.
 * 
 * @param {string} chatId - The unique identifier of the chat.
 * @param {Array} messages - An array of chat messages.
 * @returns {Promise<string|null>} A promise resolving to the generated topic or null if an error occurs.
 */
const generateChatTopic = async (chatId, messages) => {
  try {
    // Get topic mapping
    const response = await fetch(`${API_SERVICE}/topic-model/map-topics/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ "qa_pairs" : messages.map((msg) => msg.text) })
    });

    const data = await response.json();

    if (response.ok) {
      console.log("Generated topic:", data.topic);
      return data.topic;
    } else {
      console.error("Error generating chat topic:", data);
      return null;
    }
  } catch (error) {
    console.error("Failed to generate chat topic:", error);
    return null;
  }
};

/**
 * Updates the topic of a specific conversation in the backend.
 * 
 * @param {string} conversationId - The unique identifier of the conversation.
 * @param {string} topic - The new topic to be updated.
 */
const updateTopic = async (conversationId, topic) => {
  try {
    const response = await fetch(`${API_SERVICE}/conversations/${conversationId}/topic?topic=${topic}`, {
      method: "PUT",
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error updating chat topic:", errorData);
    } else {
      console.log("Chat topic updated successfully");
    }
  } catch (error) {
    console.error("Failed to update chat topic:", error);
  }
};

/**
 * Main ChatPage component that renders the chatbot interface, chat history, and feedback form.
 */
const ChatPage = () => {
  const [userUUID, setUserUUID] = useState(null); // State to store the UUID
  const [showRegistration, setShowRegistration] = useState(false);
  const [faculty, setFaculty] = useState("default_faculty");

  useEffect(() => {
    const checkExistingUser = async () => {
      const storedUUID = localStorage.getItem("userUUID");
      
      if (storedUUID) {
        try {
          const response = await fetch(`${API_SERVICE}/users/${storedUUID}`);
          const data = await response.json();
          
          if (data.exists) {
            setUserUUID(storedUUID);
            return;
          }
        } catch (error) {
          console.error("Error checking stored UUID:", error);
        }
      }
      
      // No valid UUID found, show registration form
      setShowRegistration(true);
    };
    
    checkExistingUser();
  }, []);

  // Handle form submission to create new user
  const handleRegistration = async (e) => {
    e.preventDefault();
    
    if (isCreatingUser) return; // Prevent duplicate submissions
    isCreatingUser = true;
    
    try {
      const newUUID = uuidv4();
      const createResponse = await fetch(`${API_SERVICE}/users/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          uuid: newUUID,
          faculty: faculty,
        }),
      });

      if (createResponse.ok) {
        localStorage.setItem("userUUID", newUUID);
        setUserUUID(newUUID);
        setShowRegistration(false);
      } else {
        console.error("Failed to create user:", await createResponse.json());
        alert("Failed to create user. Please try again.");
      }
    } catch (error) {
      console.error("Error creating user:", error);
      alert("An error occurred during registration. Please try again.");
    } finally {
      isCreatingUser = false;
    }
  };

  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [showChatHistory, setShowChatHistory] = useState(true);
  const [showFeedback, setShowFeedback] = useState(false);
  const [idleTimer, setIdleTimer] = useState(null);
  const [topicTimer, setTopicTimer] = useState(null);

  /**
   * Resets the timer for generating a chat topic. If the timer is already running, it clears it first.
   */
  const resetTopicTimer = () => {
    if (topicTimer) {
      clearTimeout(topicTimer);
    }
  
    setTopicTimer(
      setTimeout(async () => {
        if (currentChatId && messages.length > 0) {
          const topic = await generateChatTopic(currentChatId, messages);
          //testing
          console.log("Generated topic:", topic);
          await updateTopic(currentChatId, topic)
        }
      }, 60000) 
    );
  };
  
  useEffect(() => {
    resetTopicTimer();
    return () => {
      if (topicTimer) clearTimeout(topicTimer);
    };
  }, [messages])

  useEffect(() => {
    if (userUUID) {
      const loadUserConversations = async () => {
        const conversations = await fetchUserConversations(userUUID);
        setChatHistory(conversations);
      };
      loadUserConversations();
    }
  }, [userUUID]); // Dependency array ensures this runs when userUUID changes

  useEffect(() => {
    console.log("messages ", messages)
  }, [messages])

  /**
   * Handles the creation of a new chat by resetting the current chat ID and messages.
   */
  const handleNewChat = async () => {
    setCurrentChatId(null); 
    setMessages([]); 
  };

  /**
   * Loads a specific chat by fetching its messages and setting them in the state.
   * 
   * @param {string} chatId - The unique identifier of the chat to load.
   */
  const handleLoadChat = async (chatId) => {
    setCurrentChatId(chatId); 
    const messages = await fetchConversationMessages(chatId);
    setMessages(messages);
  };

  /**
   * Updates the feedback for a specific message in the chat.
   * 
   * @param {string} messageId - The unique identifier of the message.
   * @param {boolean} feedback - The feedback value (true for useful, false for not useful).
   */
  const handleUpdateMessageFeedback = (messageId, feedback) => {
    setMessages((prevMessages) => {
      const updatedMessages = prevMessages.map((msg) =>
        msg.message_id === messageId ? { ...msg, is_useful: feedback } : msg
      );
      return updatedMessages; // Return the updated flat array
    });
  };
  

  /**
   * Deletes a specific chat and updates the chat history and messages state.
   * 
   * @param {string} chatId - The unique identifier of the chat to delete.
   */
  const handleDeleteChat = async (chatId) => {
    await deleteConversation(chatId);
    setChatHistory((prevHistory) =>
      prevHistory.filter((chat) => chat.conversation_id !== chatId)
    );
    setMessages([]);
    setCurrentChatId(null);
  };

  /**
   * Toggles the visibility of the chat history panel.
   */
  const toggleChatHistory = () => {
    setShowChatHistory((prev) => !prev);
  };

  /**
   * Toggles the visibility of the feedback form and resets the idle timer.
   */
  const toggleFeedbackForm = () => {
    setShowFeedback((prev) => !prev);
    resetIdleTimer(); 
  };

  /**
   * Handles the cancellation of the feedback form and resets the idle timer.
   */
  const handleFeedbackCancel = () => {
    setShowFeedback(false); 
    resetIdleTimer(); 
  };
  
  /**
   * Resets the idle timer. If the timer is already running, it clears it first.
   */
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

  /**
   * Handles the creation of a new conversation by updating the chat history and resetting messages.
   * 
   * @param {Object} newChat - The new chat object containing conversation details.
   */
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

  /**
   * Sends an email escalation for a specific chat by communicating with the backend.
   * 
   * @param {string} chatHistory - The chat history to include in the email.
   * @param {string} chatId - The unique identifier of the chat.
   * @returns {Promise<Object|null>} A promise resolving to the email data or null if an error occurs.
   */
  const sendEmail = async (chatHistory, chatId) => {
    try {
        const response = await fetch(`${API_SERVICE}/chat/email-escalation/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chat_history: chatHistory }),
        });
        
        const intervention = await fetch(`${API_SERVICE}/conversations/${chatId}/intervention/`, {
          method: 'PUT',
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to send email:', error);
        alert('Failed to send email. Please try again.');
    }
}

  /**
   * Exports a specific chat by sending its messages via email.
   * 
   * @param {string} chatId - The unique identifier of the chat to export.
   */
  const handleExportChat = async (chatId) => {
    try {
        // Fetch the conversation messages for the given chatId
        const messages = await fetchConversationMessages(chatId);

        if (!messages || messages.length === 0) {
            alert('No messages found for this chat.');
            return;
        }

        // Convert the messages to a string format for sending via email
        const chatHistory = messages.map(message => {
          return `Sender: ${message.sender}\nMessage: ${message.text}`;
        }).join('\n\n');
        
        // Send the email with the chat history
        const emailData = await sendEmail(chatHistory, chatId);

        if (emailData) {
            const subject = encodeURIComponent(emailData.email_subject);
            const body = encodeURIComponent(emailData.email_body);
            const recipients = emailData.email_recipients.join(",");

            const mailtoLink = `mailto:${recipients}?subject=${subject}&body=${body}`;
            window.location.href = mailtoLink;
        }
    } catch (error) {
        console.error('Failed to export chat:', error);
        alert('Failed to export chat. Please try again.');
    }
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
  
  if (showRegistration) {
    return (
      <div className="registration-container">
        <h2>Welcome to ODPRT Chatbot</h2>
        <form onSubmit={handleRegistration}>
          <div className="form-group">
            <label htmlFor="faculty">Select your faculty:</label>
            <select 
              id="faculty" 
              value={faculty} 
              onChange={(e) => setFaculty(e.target.value)}
              required
            >
              <option value="default_faculty">Select Faculty</option>
              <option value="science">Faculty of Science</option>
              <option value="arts">Faculty of Arts</option>
              <option value="engineering">Faculty of Engineering</option>
              {/* Add more options as needed */}
            </select>
          </div>
          <button type="submit" className="submit-button">
            Start Chatting
          </button>
        </form>
      </div>
    );
  }

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
      <div className="feedback-container">
      {messages.length > 0 && (
        <button className="feedback-button" onClick={toggleFeedbackForm}>
          <span className="feedback-icon">
            <FaComment size={18} />
          </span>
          <span className="feedback-label">Send Feedback</span>
        </button>



      )}
      </div>

      <Chatbot
        messages={messages}
        currentChatId={currentChatId}
        userUUID={userUUID}
        onSendMessage={(message) => setMessages((prev) => [...prev, ...[].concat(message)])}
        onNewConversationCreated={handleNewConversationCreated}
        onUpdateMessageFeedback={handleUpdateMessageFeedback}
      />
      
      {showFeedback && <FeedbackForm conversationId = {currentChatId} onClose={handleFeedbackCancel} />}
    </div>
  );
};

export default ChatPage;
