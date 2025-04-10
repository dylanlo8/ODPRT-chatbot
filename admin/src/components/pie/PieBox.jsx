import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";

import PieChart from "./PieChart";

const PieBox = ({ title, data }) => {
  const colors = tokens();

  return (
    <Box width="100%">
 
        <Box justifyContent={"center"}>
          {/* TITLE */}
          <Box display="flex" justifyContent="center" mb="10px">
            <Typography
            variant="h6"
            fontWeight="600"
            sx={{ color: colors.text }}
            >
                {title}
                </Typography>
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