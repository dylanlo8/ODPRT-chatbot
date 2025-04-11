import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";

import BarChart from "./BarChart";

const BarBox = ({ title, data, keys, index, showLegend, pieTitle, hover, topicBreakdown }) => {
  const colors = tokens();

  return (
    <Box width="100%" sx={{ overflow: "visible" }} >
 
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

        {/* BAR CHART */}
        <Box height="190px" >
            <BarChart 
            data={data} 
            keys={keys}
            pieTitle={pieTitle}
            index={index}
            showLegend={showLegend} 
            hover={hover}
            topicBreakdown={topicBreakdown}/>
        </Box>

    </Box>
  );
};

export default BarBox;