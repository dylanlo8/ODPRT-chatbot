import { Box, Typography } from '@mui/material';
import { tokens } from "../../theme";

const Messages = ({ msgInput = [] }) => {
  const colors = tokens();

  return (
    <Box display="flex">
      {/* Messages */}
      <Box>
        {msgInput.map((msg, index) => (
            <Typography
            key={index}
            variant="body1"
            title={msg} 
            sx={{
                color: colors.text,
                fontSize: "12px",
                lineHeight: 1,
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
                maxWidth: "250px", 
            }}>
            "{msg}..."
            </Typography> ))}
        </Box>
    </Box>
  );
};

export default Messages;