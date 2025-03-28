import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";

import Table from "./Table";

const TableBox = ({ files, setFiles, refreshKey }) => {
  const colors = tokens();

  return (
    <Box width="100%">
 
        <Box ml="30px" mt="30px">
          {/* TITLE */}
            <Box display="flex" justifyContent="space-between">
            <Typography
                variant="h5"
                fontWeight="600"
                sx={{ color: colors.text }}
            >
                Uploaded Files
            </Typography>
        </Box>
        </Box>

        {/* TABLE */}
        <Box height="50vh">
            <Table files={files} setFiles={setFiles} refreshKey={refreshKey} />
        </Box>

    </Box>
  );
};
export default TableBox;