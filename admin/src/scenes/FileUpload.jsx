import { useState } from "react";
import { Box } from "@mui/material";
import { tokens } from "../theme";
import Header from "../components/Header";
import UploaderBox from "../components/uploader/UploaderBox";
import TableBox from "../components/table/TableBox";

const FileUpload = () => {
    const colors = tokens();

    const [files, setFiles] = useState([]);
    const [refreshKey, setRefreshKey] = useState(0);
    
    const handleFileUploadSuccess = () => {
        setRefreshKey(prev => prev + 1); 
    };
  
    return (
      <Box mt="30px" mx="30px">
        {/* HEADER */}
        <Header title="FILE UPLOAD"/>

        {/* GRID & COMPONENTS */}
        <Box
            display="grid"
            gridTemplateColumns="repeat(12, 1fr)"
            gridAutoRows="auto"
            gap="20px"
        >
            {/* ROW 1 FILE UPLOADER */}
            <Box
            gridColumn="span 12"
            backgroundColor={colors.white}
            display="flex"
            alignItems="center"
            justifyContent="center"
            borderRadius="12px"
            border={`2px solid ${colors.gray[200]}`}
            >
                <UploaderBox onFileUploaded={handleFileUploadSuccess}/>
            </Box>
            
            {/* ROW 2 TABLE OF FILES */}
            <Box
            gridColumn="span 12"
            backgroundColor={colors.white}
            display="flex"
            alignItems="center"
            justifyContent="center"
            borderRadius="12px"
            border={`2px solid ${colors.gray[200]}`}
            >
                <TableBox files={files} setFiles={setFiles} refreshKey={refreshKey}/>
            </Box>
        </Box>
    </Box>
    );
}

export default FileUpload;