import { tokens } from "../../theme";
import { useState } from "react";
import { Box, Snackbar, Alert } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

const Uploader = () => {
    const colors = tokens();
    const [notification, setNotification] = useState({ message: "", type: "" });

    const handleFileChange = ({ target: { files } }) => {
        if (files.length > 0) {
        const selectedFile = files[0];
        const allowedTypes = ["image/png", "image/jpeg", "image/jpg", "application/pdf"];

        if (!allowedTypes.includes(selectedFile.type)) {
            setNotification({ message: "Error: Invalid file type. Please upload a PDF, PNG, JPG, or JPEG file.", type: "error" });
            return;
        }

        setNotification({ message: "File successfully uploaded!", type: "success" });
        }
    };

    return (
        <Box textAlign="center" sx={{ cursor: "pointer" }}>
        <form onClick={() => document.querySelector(".input-field").click()}>
            <input
            type="file"
            accept=".pdf, .png, .jpg, .jpeg"
            className="input-field"
            hidden
            onChange={handleFileChange}
            />
            <CloudUploadIcon sx={{ fontSize: 50, color: colors.indigo[500] }} />
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
