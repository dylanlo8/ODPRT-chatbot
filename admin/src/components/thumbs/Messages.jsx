import { Box, Typography } from '@mui/material';
import { tokens } from "../../theme";
import { useState } from 'react';

const Messages = ({ msgInput }) => {
  const colors = tokens();
  const [tooltip, setTooltip] = useState(null);

  return (
    <Box display="flex">
      {/* Messages */}
      <Box>
        {msgInput.map((msg, index) => (
          <Typography
            key={index}
            variant="body1"
            sx={{
              color: colors.text,
              fontSize: "12px",
              lineHeight: 1.4,
              display: "flex",
              alignItems: "flex-start",
              gap: "4px",
              maxWidth: "250px",
            }}
          >
            <span style={{ flexShrink: 0 }}>&ldquo;</span>
            <span
              onMouseEnter={(e) => {
                const rect = e.currentTarget.getBoundingClientRect();
                setTooltip({
                  text: msg,
                  x: rect.left + rect.width / 2,
                  y: rect.top,
                });
              }}
              onMouseLeave={() => setTooltip(null)}
              style={{
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
                flexShrink: 1,
                cursor: "default",
              }}
            >
              {msg}
            </span>
            <span style={{ flexShrink: 0 }}>&rdquo;</span>
          </Typography>
        ))}
      </Box>

      {/* TOOLTIP */}
      {tooltip && (
        <Box
        sx={{
          position: "fixed",
          left: tooltip.x,
          top: tooltip.y - 30,
          backgroundColor: colors.white,
          color: colors.text,
          padding: "6px 10px",
          borderRadius: "6px",
          fontSize: "12px",
          boxShadow: "0 2px 10px rgba(0,0,0,0.2)",
          zIndex: 9999,
          pointerEvents: "none",

          whiteSpace: "pre-wrap",      
          maxWidth: "350px",
          overflowWrap: "break-word",
          fontFamily: "inherit",   
        }}
      >
        {tooltip.text}
      </Box>
      )}
    </Box>
  );
};

export default Messages;
