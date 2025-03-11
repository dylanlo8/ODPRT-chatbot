import { useState } from "react";
import { Box, IconButton, Menu, MenuItem, ListItemIcon, Typography, Dialog } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockUploadedFiles } from "../../data/mockData";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import VisibilityIcon from '@mui/icons-material/Visibility';
import DownloadIcon from '@mui/icons-material/Download';
import DeleteIcon from '@mui/icons-material/Delete';
import DocViewer, { DocViewerRenderers } from "@cyntler/react-doc-viewer";

const Table = () => {
  const colors = tokens();
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedRow, setSelectedRow] = useState(null);
  const [previewFile, setPreviewFile] = useState(null); 

  const handleMenuOpen = (event, rowId) => {
    setAnchorEl(event.currentTarget);
    setSelectedRow(rowId);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedRow(null);
  };

  const handleActionClick = (action) => {
    const selectedFile = mockUploadedFiles.find((file) => file.id === selectedRow);
    if (!selectedFile) return;

    if (action === "Preview") {
      const filePath = `/files/${selectedFile.file_name}`; 
      setPreviewFile([{ uri: filePath }]); 
    }

    if (action === "Download") {
      const filePath = `/files/${selectedFile.file_name}`;
      const link = document.createElement("a");
      link.href = filePath;
      link.download = selectedFile.file_name; 
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    console.log(`Performing ${action} on row ${selectedRow}`);
    handleMenuClose();
  };

  const handleClosePreview = () => {
    setPreviewFile(null); 
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
            <MenuItem onClick={() => handleActionClick("Preview")}>
              <ListItemIcon>
                <VisibilityIcon fontSize="small" />
              </ListItemIcon>
              <Typography variant="inherit">Preview</Typography>
            </MenuItem>
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
        <DataGrid
          rows={mockUploadedFiles}
          columns={columns}
          components={{ Toolbar: GridToolbar }}
          pageSizeOptions={[10, 25, 100]}
        />
      </Box>

      <Dialog open={Boolean(previewFile)} onClose={handleClosePreview} maxWidth="lg" fullWidth>
        <Box p={2}>
          <Typography variant="h6">File Preview</Typography>
          {previewFile && (
            <DocViewer
              documents={previewFile}
              pluginRenderers={DocViewerRenderers}
              style={{ height: "600px", marginTop: "10px" }}
            />
          )}
        </Box>
      </Dialog>
    </Box>
  );
};

export default Table;
