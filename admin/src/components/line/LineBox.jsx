import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";

import LineChart from "./LineChart";

const BarBox = ({ title, data, showLegend}) => {
  const colors = tokens();

  return (
    <Box width="100%">
 
        <Box ml="30px">
          {/* TITLE */}
            <Box display="flex" justifyContent="space-between">
                <Typography
                    variant="h6"
                    fontWeight="600"
                    sx={{ color: colors.text }}
                >
                    {title}
                </Typography>
            </Box>
        </Box>

        {/* LINE CHART */}
        <Box height="190px" >
            <LineChart 
            data={data} 
            showLegend={showLegend}/>
        </Box>

    </Box>
  );
};

export default BarBox;