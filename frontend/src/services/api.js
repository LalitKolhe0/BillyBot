import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('No response from server');
    } else {
      // Error setting up request
      console.error('Request setup error:', error.message);
    }
    return Promise.reject(error);
  }
);

/**
 * Check API health status
 */
export const getHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend server is not responding. Make sure it\'s running on port 8000.');
  }
};

/**
 * Get current system status
 */
export const getStatus = async () => {
  const response = await api.get('/status');
  return response.data;
};

/**
 * Upload PDF files with settings
 */
export const uploadFiles = async (formData) => {
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 60000, // 60 second timeout for large files
  });
  return response.data;
};

/**
 * Ask a question to the chatbot
 */
export const askQuestion = async (question, settings) => {
  const response = await api.post('/ask', {
    question,
    settings,
  });
  return response.data;
};

/**
 * Clear the vector database
 */
export const clearDatabase = async () => {
  const response = await api.delete('/clear-database');
  return response.data;
};

/**
 * Register a new user
 */
export const registerUser = async (email, password) => {
  const response = await api.post('/register', { email, password });
  return response.data;
};

export const loginUser = async (email, password) => {
  const response = await api.post('/login', { email, password });
  return response.data;
}

export default api;