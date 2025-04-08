import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";
import Thumbs from "./Thumbs"; 
import Messages from "./Messages";

const ThumbsBox = ({upFigure, downFigure, upMessages, downMessages}) => {
  const colors = tokens();

  return (
    <Box width="100%">
      <Box display="flex" flexDirection="column" ml="30px">
        <Typography
          variant="h6"
          fontWeight="600"
          sx={{ color: colors.text }}
        >
          Thumbs Up/Down
        </Typography>

        <Box display="flex" gap={10}>
          {/* THUMBS UP */}
          <Box>
            <Box display="flex" alignItems="center" mb={0.5}>
              <Thumbs figure={upFigure} isThumbsUp={true} />
            </Box>
            <Messages msgInput={upMessages}/>
            {/* <Box minHeight="36px" >
              <Messages msgInput={upMessages}/>
            </Box> */}
            
          </Box>

          {/* THUMBS DOWN*/}
          <Box>
            <Box display="flex" alignItems="center" mb={0.5}>
              <Thumbs figure={downFigure} isThumbsUp={false} />
            </Box>
            <Messages msgInput={downMessages}/>
            {/* <Box minHeight="36px" >
              <Messages msgInput={downMessages}/>
            </Box>             */}

          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default ThumbsBox;
