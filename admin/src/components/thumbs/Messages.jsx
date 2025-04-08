import { Box, Typography } from '@mui/material';
import { tokens } from "../../theme";

const Messages = ({ msgInput }) => {
  const colors = tokens();

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
              lineHeight: 1,
              display: "flex",
              alignItems: "center",
              gap: "4px",
              maxWidth: "250px",
            }}
          >
            <span style={{ flexShrink: 0 }}>&ldquo;</span>
            <span
              title={msg}
              style={{
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
                flexShrink: 1,
              }}
            >
              {msg}
            </span>
            <span style={{ flexShrink: 0 }}>&rdquo;</span>
          </Typography>
        ))}
      </Box>
    </Box>
  );
};

export default Messages;