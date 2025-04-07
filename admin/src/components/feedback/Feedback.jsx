import React from 'react';
import './Feedback.css';

const Feedback = ({ feedbacks, dates }) => {
  const maxChars = 70; // Set your character limit here

  return (
      <ol className="feedback-list">
        {feedbacks.map((text, index) => {
          const truncated = text.length > maxChars ? text.slice(0, maxChars) + '...' : text;

          return (
            <li key={index} className="feedback-item">
              <span className="feedback-text" title={text}>
                "{truncated}" - {dates[index]}
              </span>
            </li>
          );
        })}
      </ol>

  );
};

export default Feedback;