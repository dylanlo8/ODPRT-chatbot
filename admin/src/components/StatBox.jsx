import { Box, Typography } from "@mui/material";
import { tokens } from "../theme";

const StatBox = ({ stats = [] }) => {
  const colors = tokens();

  return (
    <Box width="100%" >
      <Box display="flex"
        flexWrap="wrap"
        ml="30px">
        {stats.map(({ title, figure }, index) => (
          <Box key={index} sx={{ mr: 10 }}>
            <Typography
              variant="h6"
              fontWeight="600"
              sx={{ color: colors.text }}
            >
              {title}
            </Typography>
            <Typography
              variant="h3"
              fontWeight="bold"
              sx={{ color: colors.text }}
            >
              {figure}
            </Typography>
          </Box>
        ))}
      </Box>
    </Box>
  );
};

export default StatBox;