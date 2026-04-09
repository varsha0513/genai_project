import React, { useState } from 'react';
import {
  InputGroup,
  Form,
  Button,
  Alert,
  Spinner
} from 'react-bootstrap';
import './ChatInterface.css';

function ChatInterface({
  messages,
  onSendMessage,
  onFileUpload,
  onDownload,
  loading,
  datasetInfo,
  messagesEndRef,
  inputValue,
  setInputValue
}) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type === 'text/csv' || file.name.endsWith('.csv')) {
        setSelectedFile(file);
      } else {
        alert('Please select a CSV file');
      }
    }
  };

  const handleFileUploadClick = () => {
    if (selectedFile) {
      onFileUpload(selectedFile);
      setSelectedFile(null);
      const fileInput = document.getElementById('fileInput');
      if (fileInput) fileInput.value = '';
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const suggestedQueries = [
    'What are the statistics for this dataset?',
    'Remove missing values',
    'Show unique values',
    'Count total rows',
    'Remove duplicates'
  ];

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="header-content">
          <h1>🤖 Data Analytics AI Assistant</h1>
          <p>Your intelligent partner for data analysis and insights</p>
        </div>
        {datasetInfo && (
          <div className="header-actions">
            <Button
              variant="success"
              size="sm"
              onClick={onDownload}
              disabled={loading}
            >
              📥 Download Dataset
            </Button>
          </div>
        )}
      </div>

      {/* Chat Messages Area */}
      <div className="chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.type} ${message.isError ? 'error' : ''}`}
          >
            <div className="message-avatar">
              {message.type === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              <div className="message-text">
                {message.content.split('\n').map((line, idx) => (
                  <div key={idx}>
                    {line.includes('**') ? (
                      line.split(/\*\*/).map((part, i) =>
                        i % 2 === 0 ? (
                          <span key={i}>{part}</span>
                        ) : (
                          <strong key={i}>{part}</strong>
                        )
                      )
                    ) : (
                      line
                    )}
                  </div>
                ))}
              </div>
              
              {/* Display Chart Image if available */}
              {message.chartPath && (
                <div className="message-chart">
                  <img 
                    src={`http://localhost:8000/chart/${message.chartPath.split('\\').pop()}`}
                    alt="Data Visualization"
                    className="chart-image"
                    onError={(e) => {
                      console.error('Failed to load chart:', e);
                      e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Ctext x="50" y="150" font-size="16"%3EChart image loading failed%3C/text%3E%3C/svg%3E';
                    }}
                  />
                </div>
              )}
              
              {message.data && (
                <div className="message-data">
                  <pre>{JSON.stringify(message.data, null, 2)}</pre>
                </div>
              )}
            </div>
            <span className="message-time">
              {message.timestamp.toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit'
              })}
            </span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Queries (shown when no dataset is uploaded) */}
      {!datasetInfo && messages.length === 1 && (
        <div className="suggested-queries">
          <p className="section-title">📌 Quick Start: Upload a CSV file to begin</p>
        </div>
      )}

      {/* Suggested Queries (shown when dataset is uploaded) */}
      {datasetInfo && (
        <div className="suggested-queries">
          <p className="section-title">💡 Suggested Queries:</p>
          <div className="query-buttons">
            {suggestedQueries.map((query, idx) => (
              <Button
                key={idx}
                variant="outline-primary"
                size="sm"
                onClick={() => onSendMessage(query)}
                disabled={loading}
                className="suggested-btn"
              >
                {query}
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="chat-input-area">
        {!datasetInfo ? (
          // File Upload Section
          <div className="file-upload-section">
            <h5>📤 Upload CSV Dataset</h5>
            <InputGroup className="mb-3">
              <Form.Control
                id="fileInput"
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                disabled={loading}
              />
              <Button
                variant="primary"
                onClick={handleFileUploadClick}
                disabled={!selectedFile || loading}
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
                  'Upload'
                )}
              </Button>
            </InputGroup>
            {selectedFile && (
              <Alert variant="info" className="mb-0">
                Selected file: <strong>{selectedFile.name}</strong>
              </Alert>
            )}
          </div>
        ) : (
          // Message Input Section
          <form onSubmit={handleSendMessage} className="message-input-form">
            <InputGroup>
              <Form.Control
                placeholder="Ask me anything... (e.g., 'remove missing values and give total count')"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                disabled={loading}
                className="chat-input"
              />
              <Button
                variant="primary"
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || loading}
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
                  </>
                ) : (
                  '📤'
                )}
              </Button>
            </InputGroup>
          </form>
        )}
      </div>

      {/* Footer Info */}
      <div className="chat-footer">
        <p>
          💡 <strong>Tips:</strong> Be specific with your requests. Ask me to
          clean, analyze, visualize, or download your data.
        </p>
      </div>
    </div>
  );
}

export default ChatInterface;
