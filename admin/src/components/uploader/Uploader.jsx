import { useState } from "react";
import { Box, Snackbar, Alert, CircularProgress } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { uploadFile } from "../../api/FileUploadApi"; 
import { tokens } from "../../theme";

const Uploader = ({ onUploadSuccess }) => {
    const colors = tokens();
    const [notification, setNotification] = useState({ message: "", type: "" });
    const [uploading, setUploading] = useState(false); 

    const handleFileChange = async ({ target: { files } }) => {
        if (files.length === 0) return;
        
        const selectedFile = files[0];
        const allowedTypes = ["image/png", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];

        if (!allowedTypes.includes(selectedFile.type)) {
            setNotification({ message: "Error: Invalid file type. Please upload a PDF or DOCX file.", type: "error" });
            return;
        }

        setUploading(true); 

        try {
            const response = await uploadFile(selectedFile);
            setNotification({ message: "File successfully uploaded!", type: "success" });
            console.log("Uploaded file:", response); 

            if (onUploadSuccess) onUploadSuccess();
        } catch (error) {
            setNotification({ message: "Upload failed. Please try again.", type: "error" });
            console.error("Upload error:", error);
        } finally {
            setUploading(false); 
        }
    };

    return (
        <Box textAlign="center" sx={{ cursor: "pointer", position: "relative" }}>
            <form onClick={() => document.querySelector(".input-field").click()}>
                <input
                    type="file"
                    accept=".pdf, .docx"
                    className="input-field"
                    hidden
                    onChange={handleFileChange}
                />
                {uploading ? (
                    <CircularProgress size={50} sx={{ color: colors.indigo[500] }} /> 
                ) : (
                    <CloudUploadIcon sx={{ fontSize: 50, color: colors.indigo[500] }} />
                )}
            </form>

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

export default Uploader;
