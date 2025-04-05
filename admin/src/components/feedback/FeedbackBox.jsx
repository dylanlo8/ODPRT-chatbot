import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";

import Feedback from "./Feedback";

const FeedbackBox = ({ feedbacks, dates }) => {
  const colors = tokens();

  return (
    <Box width="100%">
 
        <Box ml="30px">
          {/* TITLE */}
            <Box display="flex" justifyContent="space-between">
            <Typography
                variant="h5"
                fontWeight="600"
                sx={{ color: colors.text }}
            >
                Most Recent Feedbacks
            </Typography>
        </Box>
        
        {/* FEEDBACK */}
        <Box>
          <Feedback feedbacks={feedbacks} dates={dates}></Feedback>
        </Box>
        </Box>
    </Box>
  );
};

export default FeedbackBox;