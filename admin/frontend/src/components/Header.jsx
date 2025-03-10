import { Typography, Box, useTheme } from "@mui/material";
import { tokens } from "../theme";

const Header = ({ title, subtitle }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Box mb="10px">
      <Typography
        variant="h2"
        color={colors.text}
        fontWeight="bold"
      >
        {title}
      </Typography>
    </Box>
  );
};

export default Header;