import { Box, Typography } from "@mui/material";
import { tokens } from "../theme";

const StatBox = ({ title, figure, arrow, percentage, isIncreasing}) => {
  const colors = tokens();

  return (
    <Box width="100%" 
    m="0 30px"
    >
      {/* TITLE */}
      <Box display="flex" justifyContent="space-between">
          <Typography
            variant="h4"
            fontWeight="600"
            sx={{ color: colors.text }}
          >
            {title}
          </Typography>
      </Box>

      {/* FIGURE */}
      <Box display="flex" justifyContent="space-between" mt="2px">
        <Box my="10px">
          <Typography variant="h2" 
          fontWeight="bold"
          sx={{ color: colors.text }}>
            {figure}
          </Typography>
        </Box>
      </Box>

      {/* PERCENTAGE */}
      <Box display="flex" justifyContent="centre" mt="2px">
      {arrow}
        <Typography
            variant="h5"
            sx={{ color: isIncreasing ? colors.green[500] : colors.red[500] }}
          >
          {percentage}
        </Typography>
      </Box>


    </Box>
  );
};

export default StatBox;