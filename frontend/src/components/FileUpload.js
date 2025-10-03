import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, CheckCircle, AlertCircle, Trash2 } from 'lucide-react';
import { useSettings } from '../context/SettingsContext';
import { uploadFiles, clearDatabase } from '../services/api';

const FileUpload = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isClearing, setIsClearing] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const { settings } = useSettings();

  const onDrop = useCallback((acceptedFiles) => {
    const pdfFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    setUploadedFiles(prev => [...prev, ...pdfFiles]);
    setUploadStatus(null); // Clear previous status
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true
  });

  const removeFile = (index) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (uploadedFiles.length === 0) return;

    setIsUploading(true);
    setUploadStatus(null);

    try {
      const formData = new FormData();
      uploadedFiles.forEach(file => {
        formData.append('files', file);
      });
      
      // Add settings to the request
      formData.append('settings', JSON.stringify(settings));

      const response = await uploadFiles(formData);
      setUploadStatus({ 
        type: 'success', 
        message: `${response.message} (Stored in: ${response.persist_directory})` 
      });
      setUploadedFiles([]);
    } catch (error) {
      const errorMessage = error.response?.data?.detail 
        || error.message 
        || 'Upload failed. Make sure the backend is running.';
      setUploadStatus({ 
        type: 'error', 
        message: errorMessage
      });
    } finally {
      setIsUploading(false);
    }
  };

  const handleClearDatabase = async () => {
    if (!window.confirm('Are you sure you want to clear the entire knowledge base? This action cannot be undone.')) {
      return;
    }

    setIsClearing(true);
    setUploadStatus(null);

    try {
      const response = await clearDatabase();
      setUploadStatus({ 
        type: 'success', 
        message: response.message + (response.cleared_directories ? 
          ` (Cleared: ${response.cleared_directories.join(', ')})` : '')
      });
    } catch (error) {
      const errorMessage = error.response?.data?.detail 
        || error.message 
        || 'Failed to clear database';
      setUploadStatus({ 
        type: 'error', 
        message: errorMessage
      });
    } finally {
      setIsClearing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Upload PDFs
        </h3>
        <p className="text-sm text-gray-600">
          Drag and drop your PDF files here, or click to browse. Files will be processed and added to your knowledge base.
        </p>
      </div>

      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-primary-500 bg-primary-50' 
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }
        `}
      >
        <input {...getInputProps()} />
        <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
        {isDragActive ? (
          <p className="text-lg text-primary-600 font-medium">Drop the files here...</p>
        ) : (
          <>
            <p className="text-lg text-gray-700 font-medium mb-2">
              Drag & drop PDF files here
            </p>
            <p className="text-sm text-gray-500">
              or click to select files from your computer
            </p>
          </>
        )}
      </div>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium text-gray-700">
            Files ready to upload ({uploadedFiles.length})
          </h4>
          <div className="space-y-2">
            {uploadedFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200"
              >
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{file.name}</p>
                    <p className="text-xs text-gray-500">
                      {(file.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="text-gray-400 hover:text-red-500 transition-colors"
                  aria-label="Remove file"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex space-x-4">
        <button
          onClick={handleUpload}
          disabled={uploadedFiles.length === 0 || isUploading}
          className="flex-1 bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
        >
          {isUploading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Uploading...</span>
            </>
          ) : (
            <>
              <Upload className="h-5 w-5" />
              <span>Upload Files</span>
            </>
          )}
        </button>

        <button
          onClick={handleClearDatabase}
          disabled={isClearing || isUploading}
          className="bg-red-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isClearing ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Clearing...</span>
            </>
          ) : (
            <>
              <Trash2 className="h-5 w-5" />
              <span>Clear DB</span>
            </>
          )}
        </button>
      </div>

      {/* Status Messages */}
      {uploadStatus && (
        <div
          className={`p-4 rounded-lg flex items-start space-x-3 ${
            uploadStatus.type === 'success'
              ? 'bg-green-50 border border-green-200'
              : 'bg-red-50 border border-red-200'
          }`}
        >
          {uploadStatus.type === 'success' ? (
            <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
          ) : (
            <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
          )}
          <div className="flex-1">
            <p
              className={`text-sm font-medium ${
                uploadStatus.type === 'success' ? 'text-green-800' : 'text-red-800'
              }`}
            >
              {uploadStatus.type === 'success' ? 'Success!' : 'Error'}
            </p>
            <p
              className={`text-sm mt-1 ${
                uploadStatus.type === 'success' ? 'text-green-700' : 'text-red-700'
              }`}
            >
              {uploadStatus.message}
            </p>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Note:</strong> Uploaded files will be processed and stored in the vector database. 
          You can then ask questions about the content in the "Ask Questions" tab.
        </p>
      </div>
    </div>
  );
};

export default FileUpload;