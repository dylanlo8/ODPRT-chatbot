import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";

import PieChart from "./PieChart";

const PieBox = ({ title, figure, data }) => {
  const colors = tokens();

  return (
    <Box width="100%">
 
        <Box ml="30px">
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
        </Box>

        {/* PIE CHART */}
        <Box height="200px" >
            <PieChart data={data}/>
        </Box>

    </Box>
  );
};

export default PieBox;