import { useState } from "react";
import { Box, Snackbar, Alert, CircularProgress } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { uploadFile } from "../../api/FileUploadApi"; 
import { tokens } from "../../theme";

const Uploader = ({ onFileUploaded }) => {
    const colors = tokens();
    const [notification, setNotification] = useState({ message: "", type: "" });
    const [uploading, setUploading] = useState(false); 

    const handleFileChange = async ({ target: { files } }) => {
        if (files.length === 0) return;
        
        const selectedFile = files[0];
        const allowedTypes = ["image/png", "image/jpeg", "image/jpg", "application/pdf"];

        if (!allowedTypes.includes(selectedFile.type)) {
            setNotification({ message: "Error: Invalid file type. Please upload a PDF, PNG, JPG, or JPEG file.", type: "error" });
            return;
        }

        setUploading(true); 

        try {
            const response = await uploadFile(selectedFile);

            const newFile = {
                id: response.id,
                file_name: response.name,
                file_size: `${(response.metadata.size / 1024).toFixed(2)} KB`,
                upload_date: new Date(response.created_at).toLocaleString(),
                file_url: response.file_url 
            };

            onFileUploaded?.(newFile); 
            setNotification({ message: "File successfully uploaded!", type: "success" });
            console.log("Uploaded file:", response); 
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
                    accept=".pdf, .png, .jpg, .jpeg"
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
