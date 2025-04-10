import { Button } from "@mui/material";
import { tokens } from "../../theme";
import FileDownloadIcon from "@mui/icons-material/FileDownload";
import { exportDashboardDataToExcel } from "./Export"; 


const ExportButton = () => {
  const colors = tokens();

  return (
    <Button
      variant="contained"
      startIcon={<FileDownloadIcon />}
      onClick={exportDashboardDataToExcel}
      sx={{
        backgroundColor: colors.indigo[500],
        color: colors.white,
        boxShadow: "none",
        textTransform: "none",
        fontSize: "14px",
        '&:hover': {
          backgroundColor: colors.indigo[600],
          boxShadow: "none",
        },
      }}
    >
      Export as Excel
    </Button>
  );
};

export default ExportButton;

