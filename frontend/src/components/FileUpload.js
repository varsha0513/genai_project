import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

function FileUpload({ onFileUpload, loading }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'text/csv') {
      setSelectedFile(file);
    } else {
      alert('Please select a valid CSV file');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedFile) {
      onFileUpload(selectedFile);
      setSelectedFile(null);
    }
  };

  return (
    <div className="file-upload-container">
      <h4 className="mb-4">📁 Upload CSV Dataset</h4>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Select CSV File</Form.Label>
          <Form.Control
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={loading}
          />
          <Form.Text className="text-muted">
            Maximum file size: 100MB
          </Form.Text>
        </Form.Group>

        <Button
          variant="primary"
          type="submit"
          disabled={!selectedFile || loading}
          className="w-100"
        >
          {loading ? (
            <>
              <Spinner
                as="span"
                animation="border"
                size="sm"
                role="status"
                aria-hidden="true"
                className="me-2"
              />
              Uploading...
            </>
          ) : (
            '📤 Upload'
          )}
        </Button>
      </Form>
    </div>
  );
}

export default FileUpload;
