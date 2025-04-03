import { Box, Typography } from "@mui/material";
import { tokens } from "../theme";

const StatBox = ({ stats = [] }) => {
  const colors = tokens();

  return (
    <Box width="100%" >
      <Box display="flex"
        justifyContent="space-between"
        flexWrap="wrap">
        {stats.map(({ title, figure }, index) => (
          <Box key={index}>
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
              sx={{ color: colors.text, mt: "5px" }}
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