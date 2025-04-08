import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";

import Feedback from "./Feedback";

const FeedbackBox = ({ figure, feedbacks, dates }) => {
  const colors = tokens();

  return (
    <Box width="100%">
 
        <Box ml="30px">
          {/* TITLE */}
            <Box display="flex">
              <Box>
                <Typography
                  variant="h6"
                  fontWeight="600"
                  sx={{ color: colors.text }}
              >
                Feedbacks
                </Typography>

                {/* FIGURE */}
                <Box display="box" alignItems="center" mb={0.5}>
                  <Typography
                    variant="h3"
                    fontWeight="bold"
                    sx={{ color: colors.text }}
                  >
                    {figure}
                  </Typography>
                </Box>
                <Feedback feedbacks={feedbacks} dates={dates} />
                {/* <Box minHeight="36px" >
                  <Feedback feedbacks={feedbacks} dates={dates} />
                </Box> */}
              </Box>
            </Box>
        </Box>
    </Box>
  );
};

export default FeedbackBox;