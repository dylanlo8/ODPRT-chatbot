import { Box, Typography } from '@mui/material';
import { tokens } from "../../theme";
import { useState } from 'react';

const Feedback = ({ feedbacks, dates }) => {
  const colors = tokens();
  const [tooltip, setTooltip] = useState(null); // custom tooltip state

  return (
    <Box>
      <Box>
        {feedbacks.map((fdbk, index) => (
          <Typography
            key={index}
            variant="body2"
            sx={{
              color: colors.text,
              fontSize: "12px",
              lineHeight: 1.4,
              display: "flex",
              alignItems: "flex-start",
              gap: "4px",
              maxWidth: "550px",
            }}
          >
            {index + 1}.{" "}
            <span style={{ flexShrink: 0 }}>&ldquo;</span>
            <span
              onMouseEnter={(e) => {
                const rect = e.currentTarget.getBoundingClientRect();
                setTooltip({
                  text: fdbk,
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
              {fdbk}
            </span>
            <span style={{ flexShrink: 0 }}>&rdquo;</span>
            {dates?.[index] && (
              <span
                style={{
                  flexShrink: 0,
                  whiteSpace: "nowrap",
                  marginLeft: "4px",
                }}
              >
                - {dates[index]}
              </span>
            )}
          </Typography>
        ))}
      </Box>

      {/* Custom tooltip */}
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

export default Feedback;
