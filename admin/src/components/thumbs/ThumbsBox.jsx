import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";
import Thumbs from "./Thumbs"; 
import Messages from "./Messages";

const ThumbsBox = () => {
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
              <Thumbs Figure={"XX"} isThumbsUp={true} />
            </Box>
            <Messages
              msgInput={[
                "The Office of the Deputy President (Research & Technology) oversees NUS’s research strategy, innovation ecosystem, and global research partnerships.",
                "Yes, ODPRT works closely with NUS Enterprise and the Industry Liaison Office to support research translation, innovation, and spin-off formation.",
                "Yes! ODPRT administers several internal research grant schemes. You can explore open calls via the Research Portal or reach out to your department’s grant administrator for assistance.",
              ]}
            />
          </Box>

          {/* THUMBS DOWN*/}
          <Box>
            <Box display="flex" alignItems="center" mb={0.5}>
              <Thumbs Figure={"XX"} isThumbsUp={false} />
            </Box>
            <Messages
              msgInput={[
                "Sorry to hear that! ODPRT typically responds within 7–10 working days. Would you like me to flag this for follow-up?",
                'To use the IEP Contracting Hub, access it via CDPRT (hosted on Pactly). As a PI, researcher, or faculty-admin, you can submit agreement requests, upload drafts, and download NUS standard templates. The Hub lets you track requests from submission to execution and view or download executed agreements. For help or to set up an account, contact the IEP team through the Hub.',
                "I am sorry, but I am unable to provide a response to your query at the moment"
              ]}
            />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default ThumbsBox;
