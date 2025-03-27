import { useState, useEffect } from "react";
import { Box, IconButton, Menu, MenuItem, ListItemIcon, Typography, CircularProgress, Snackbar, Alert } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { fetchFiles, deleteFile, downloadFile } from "../../api/FileUploadApi";
import { tokens } from "../../theme";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import DownloadIcon from '@mui/icons-material/Download';
import DeleteIcon from '@mui/icons-material/Delete';

const Table = ({ files, setFiles }) => {
  const colors = tokens();
  const [loading, setLoading ] = useState(true);
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedRow, setSelectedRow] = useState(null);
  const [notification, setNotification] = useState({ message: "", type: "" });


  useEffect(() => {
    const loadFiles = async () => {
      try {
        const data = await fetchFiles();
        
        const modifiedData = data.map(file => ({
          id : file.id,
          file_name : file.name,
          file_size: `${(file.metadata.size / 1024).toFixed(2)} KB`, 
          upload_date: new Date(file.created_at).toLocaleString() 
        }));

        setFiles(modifiedData);
      } catch (error) {
        console.error("Error fetching files", error);
      } finally {
        setLoading(false);
      }
    };
    loadFiles();
  }, [ setFiles ]);

  const handleMenuOpen = (event, rowId) => {
    setAnchorEl(event.currentTarget);
    setSelectedRow(rowId);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedRow(null);
  };

  const handleActionClick = async (action) => {
    const selectedFile = files.find((file) => file.id === selectedRow);
    if (!selectedFile) return;

    if (action === "Download") {
      try {
        const fileData = await downloadFile(selectedFile.file_name);
        const url = window.URL.createObjectURL(new Blob([fileData]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", selectedFile.file_name);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error("Error downloading file:", error);
      }
    }

    if (action === "Delete") {
      try {
        await deleteFile([selectedFile.file_name]);
        setFiles(files.filter((file) => file.file_name !== selectedFile.file_name));
        setNotification({ message: "File successfully deleted!", type: "success" });
      } catch (error) {
        console.error("Delete failed:", error);
        setNotification({ message: "Delete failed. Please try again.", type: "error" });
      }
    }

    handleMenuClose();
  };

  const columns = [
    { field: "file_name", headerName: "File Name", flex: 1 },
    { field: "file_size", headerName: "File Size", flex: 1 },
    { field: "upload_date", headerName: "Upload Date", flex: 1 },
    {
      field: "actions",
      headerName: "Actions",
      flex: 1,
      renderCell: (params) => (
        <>
          <IconButton onClick={(event) => handleMenuOpen(event, params.row.id)}>
            <MoreHorizIcon />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl) && selectedRow === params.row.id}
            onClose={handleMenuClose}
            PaperProps={{ elevation: 3, sx: { minWidth: 150, borderRadius: "8px", p: 1 } }}
          >
            <MenuItem onClick={() => handleActionClick("Download")}>
              <ListItemIcon>
                <DownloadIcon fontSize="small" />
              </ListItemIcon>
              <Typography variant="inherit">Download</Typography>
            </MenuItem>
            <MenuItem onClick={() => handleActionClick("Delete")} sx={{ color: "red" }}>
              <ListItemIcon>
                <DeleteIcon fontSize="small" sx={{ color: "red" }} />
              </ListItemIcon>
              <Typography variant="inherit">Delete</Typography>
            </MenuItem>
          </Menu>
        </>
      ),
      sortable: false,
      filterable: false,
    },
  ];

  return (
    
    <Box mx="40px" my="30px">
      <Box height="50vh"
      sx={{
        "& .MuiDataGrid-root": { border: "none" },
        "& .MuiDataGrid-cell": { borderBottom: "none" },
        "& .MuiDataGrid-columnHeaders": { backgroundColor: colors.text, borderBottom: "none" },
        "& .MuiDataGrid-virtualScroller": { backgroundColor: colors.white },
        "& .MuiDataGrid-footerContainer": { borderTop: "none", backgroundColor: colors.white },
        "& .MuiCheckbox-root": { color: `${colors.white} !important` },
        "& .MuiDataGrid-toolbarContainer .MuiButton-text": { color: `${colors.white} !important` },
      }}>
        {loading ? (
          <CircularProgress />
        ) : (
        <DataGrid
        rows={files}
        columns={columns}
        components={{ Toolbar: GridToolbar }}
        pageSizeOptions={[10, 25, 100]}/>
        ) }
      </Box>

      {/* NOTIFICATION SNACKBAR */}
      <Snackbar
          open={Boolean(notification.message)}
          autoHideDuration={3000}
          onClose={() => setNotification({ message: "", type: "" })}
          anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
          <Alert onClose={() => setNotification({ message: "", type: "" })} severity={notification.type} sx={{ width: "100%" }}>
              {notification.message}
          </Alert>
      </Snackbar>
    </Box>
  );
};

export default Table;
