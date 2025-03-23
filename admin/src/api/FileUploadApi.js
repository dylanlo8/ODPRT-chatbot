import axios from "axios";

const API_BASE_URL = "http://0.0.0.0:8000"; 


export const uploadFile = async (files) => {
  try {    
    const formData = new FormData();

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

    // Upload File into Bucket
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
    // Delete file from Bucket
    const bucketResponse = await axios.delete(`${API_BASE_URL}/buckets/delete`, {
      data: { 
        file_names: fileNames 
      }, 
    });

    // Delete file from VectorDB
    // Specify field as doc_source
    const vectorResponse = await axios.delete(`${API_BASE_URL}/vector-db/delete-data/?field=doc_source`, {
      data: fileNames
    });

    return { bucket_response : bucketResponse.data, vector_response : vectorResponse.data }
  } catch (error) {
    console.error("Error deleting file:", error);
    throw error;
  }
};

export const downloadFile = async (filePath) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/buckets/download-file`, {
      params: { file_path: filePath },
      responseType: 'blob', // Important to handle binary data
    });
    return response.data;
  } catch (error) {
    console.error("Error downloading file:", error);
    throw error;
  }
};