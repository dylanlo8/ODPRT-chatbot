import { Box, Typography } from "@mui/material";
import { tokens } from "../../theme";

import Uploader from "./Uploader"; 

const UploaderBox = ({ onFileUploaded }) => {
    const colors = tokens();

  return (
    <Box width="100%" display="flex" justifyContent="center" alignItems="center">
        
        <Box height="200px" display="flex" justifyContent="center" alignItems="center">
            <Box display="flex" flexDirection="column" alignItems="center">
                {/* FILE UPLOADER */}
                <Uploader onUploadSuccess={ onFileUploaded } />
                
                {/* UPLOAD CAPTION */}
                <Box display="flex" gap={0.5} alignItems="center">
                    <Typography variant="h5" fontWeight="600" sx={{ color: colors.text }}>
                        Click here
                    </Typography>
                    <Typography variant="h5" fontWeight="400" sx={{ color: colors.text }}>
                        to upload your file (.pdf, .png, .jpg, .jpeg)
                    </Typography>
                </Box>
            
            </Box>  
        </Box>
    </Box>
  );
};

export default UploaderBox;
