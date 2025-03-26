import { Box, Typography } from "@mui/material";
import { tokens } from "../theme";

const StatBox = ({ title, figure }) => {
  const colors = tokens();

  return (
    <Box width="100%" 
    m="0 30px"
    >
      {/* TITLE */}
      <Box display="flex" justifyContent="space-between">
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ color: colors.text }}
          >
            {title}
          </Typography>
      </Box>

      {/* FIGURE */}
      <Box display="flex" justifyContent="space-between" mt="2px">
        <Box my="15px">
          <Typography variant="h3" 
          fontWeight="bold"
          sx={{ color: colors.text }}>
            {figure}
          </Typography>
        </Box>
      </Box>

    </Box>
  );
};

export default StatBox;