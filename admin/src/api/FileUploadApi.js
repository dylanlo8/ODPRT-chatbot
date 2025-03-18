import axios from "axios";

const API_BASE_URL = ""; 

export const uploadFile = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file); 

    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    return response.data; 
  } catch (error) {
    console.error("Error uploading file:", error);
    throw error;
  }
};

export const fetchFiles = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/files`);
    return response.data;
  } catch (error) {
    console.error("Error fetching files:", error);
    throw error;
  }
};

export const deleteFile = async (fileNames) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/delete`, {
      data: { file_names: fileNames }, 
    });

    return response.data; 
  } catch (error) {
    console.error("Error deleting file:", error);
    throw error;
  }
};