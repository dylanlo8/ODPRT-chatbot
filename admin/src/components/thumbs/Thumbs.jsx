import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';

const Thumbs = ({ Figure, isThumbsUp }) => { // replace with figure, and isUp/ isDown
    const colors = tokens();
  
    return (
      <Box width="100%">
        <Box display="flex" alignItems="center" gap={1}>
            {isThumbsUp ? (<ThumbUpIcon sx={{ fontSize: 20, color: colors.green[500] }} />) : (<ThumbDownIcon sx={{ fontSize: 20, color: colors.red[500] }} />)}
            <Typography
              variant="h3"
              fontWeight="bold"
              sx={{ color: colors.text }}
            >
              {Figure}
            </Typography>
        </Box>
      </Box>
    );
  };
  
  export default Thumbs;