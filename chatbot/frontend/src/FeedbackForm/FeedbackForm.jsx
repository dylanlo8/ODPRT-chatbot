import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSmile, faFrown, faMeh, faGrinStars, faAngry } from '@fortawesome/free-solid-svg-icons';
import "./FeedbackForm.css";

const API_SERVICE = "http://localhost:8000";

const FeedbackForm = ({ conversationId, onClose }) => {
  const [feedback, setFeedback] = useState("");
  const [selectedEmoji, setSelectedEmoji] = useState(null);

  const emojis = [
    { icon: faAngry, label: "Angry" },
    { icon: faFrown, label: "Unhappy" },
    { icon: faMeh, label: "Neutral" },
    { icon: faSmile, label: "Happy" },
    { icon: faGrinStars, label: "Very Happy" },
  ];

  const handleEmojiClick = (index, label) => {
    setSelectedEmoji(index);
    console.log(`Selected Emoji: ${label}`);
  };
  
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(`Feedback Submitted: ${feedback}`);
    console.log(`Selected Emoji: ${selectedEmoji !== null ? emojis[selectedEmoji].label : "None"}`);
    
    const feedbackData = {};

    if (selectedEmoji !== null) {
      feedbackData.rating = emojis[selectedEmoji].label;
    }
  
    if (feedback !== null) {
      feedbackData.text = feedback;
    }

    try {
      const response = await fetch(`${API_SERVICE}/conversations/${conversationId}/feedback`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(feedbackData),
      });

      if (response.ok) {
        console.log("Feedback submitted successfully!");
        onClose();  // Close form after submission
      } else {
        console.error("Error submitting feedback");
      }
    } catch (error) {
      console.error("Failed to submit feedback:", error);
    }
    onClose();
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); 
      handleSubmit();
    }
  };

  return (
    <div className="feedback-overlay">
      <div className="feedback-modal">
        <button className="close-button" onClick={onClose}>✖</button>
        <h3>How was your experience?</h3>
        <div className="emoji-container">
          {emojis.map((emoji, index) => (
            <FontAwesomeIcon
              key={index}
              icon={emoji.icon}
              size="2x"
              className={`emoji ${selectedEmoji === index ? "selected" : ""}`}
              onClick={() => handleEmojiClick(index, emoji.label)}
              title={emoji.label}
            />
          ))}
        </div>
        <textarea
          placeholder="Leave your feedback..."
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          onKeyDown={handleKeyPress} 
        />
        <button className="submit-button" onClick={handleSubmit}>Submit</button>
      </div>
    </div>
  );
};

export default FeedbackForm;
