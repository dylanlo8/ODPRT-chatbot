import axios from "axios";

const API_BASE_URL = "http://0.0.0.0:8000"; 


export const uploadFile = async (files) => {
  try {    
    const formData = new FormData();

    console.log(formData)

    // Construct Payload for File Upload
    formData.append("files", files);
    
    // Ingest the files into VectorDB
    const ingestResponse = await axios.post(
      `${API_BASE_URL}/ingestion/ingest-files/`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" }
      }
    );

    const bucketResponse = await axios.post(
      `${API_BASE_URL}/buckets/upload/`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" }
      }
    );

    return { ingest: ingestResponse.data , bucket : bucketResponse };
  } catch (error) {
    console.error("Error uploading or ingesting files:", error);
    throw error;
  }
};

export const fetchFiles = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/buckets/fetch-files`);
    return response.data;
  } catch (error) {
    console.error("Error fetching files:", error);
    throw error;
  }
};

export const deleteFile = async (fileNames) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/buckets/delete`, {
      data: { file_names: fileNames }, 
    });

    return response.data; 
  } catch (error) {
    console.error("Error deleting file:", error);
    throw error;
  }
};
