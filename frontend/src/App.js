import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import ChatInterface from './components/ChatInterface';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const API_BASE_URL = 'http://localhost:5001';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'Welcome to Data Analytics AI Assistant! 👋\n\nI can help you with:\n• Data cleaning (remove missing values, duplicates)\n• Statistical analysis (min, max, average, count, etc.)\n• Data visualization (charts, graphs)\n• Data insights and trends\n\nPlease upload a CSV file to get started.',
      timestamp: new Date()
    }
  ]);
  const [datasetInfo, setDatasetInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle file upload
  const handleFileUpload = async (file) => {
    setLoading(true);
    
    // Add user message about file upload
    const userMsg = {
      id: messages.length + 1,
      type: 'user',
      content: `📁 Uploading file: ${file.name}`,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setDatasetInfo(response.data);

      // Get dataset info
      const infoResponse = await axios.get(`${API_BASE_URL}/info`);
      
      const assistantMsg = {
        id: messages.length + 2,
        type: 'assistant',
        content: `✅ Dataset loaded successfully!\n\n📊 **Dataset Overview:**\n• **Rows:** ${response.data.rows}\n• **Columns:** ${response.data.columns.length}\n• **Column Names:** ${response.data.columns.join(', ')}\n\n📈 **Data Types:**\n• **Numeric:** ${infoResponse.data.numeric_columns.join(', ') || 'None'}\n• **Categorical:** ${infoResponse.data.categorical_columns.join(', ') || 'None'}\n\n💡 **What would you like me to do?**\nTry asking me to:\n• Clean the data (remove missing values, duplicates)\n• Analyze statistics (min, max, average, total)\n• Create visualizations\n• Or any other data operation`,
        timestamp: new Date(),
        data: infoResponse.data
      };
      
      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      const errorMsg = {
        id: messages.length + 2,
        type: 'assistant',
        content: `❌ Error uploading file: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  // Handle user query
  const handleSendMessage = async (userQuery) => {
    if (!userQuery.trim()) return;
    if (!datasetInfo) {
      const msg = {
        id: messages.length + 1,
        type: 'assistant',
        content: '⚠️ Please upload a dataset first!',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, msg]);
      return;
    }

    setLoading(true);
    setInputValue('');

    // Add user message
    const userMsg = {
      id: messages.length + 1,
      type: 'user',
      content: userQuery,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, {
        query: userQuery,
        session_id: null
      });

      let assistantContent = '';
      let resultData = null;
      let chartPath = null;

      if (response.data.status === 'success') {
        const { operation, message, data, results, additional_data, rows_before, rows_after, rows_removed, chart_path, operations, statistics } = response.data;

        // Handle compound operations (multiple cleaning + stats)
        if (response.data.operations && Array.isArray(response.data.operations)) {
          assistantContent = response.data.message || '✅ Data processing complete!';
          if (statistics) {
            resultData = statistics;
          }
        }
        // Handle visualization
        else if (response.data.chart_path) {
          chartPath = response.data.chart_path;
          assistantContent = `📊 **${response.data.message}**\n\n✨ Visualization created successfully!${response.data.insight ? '\n\n💡 **AI Insight:** ' + response.data.insight : ''}`;
          resultData = {
            chart_type: response.data.chart_type,
            x_column: response.data.x_column,
            y_column: response.data.y_column
          };
        }
        // Handle cleaning operations with single rows_before
        else if (response.data.rows_before !== undefined) {
          // Cleaning operation
          assistantContent = `✅ **${message}**\n\n📊 **Cleaning Summary:**\n• **Rows before:** ${rows_before}\n• **Rows after:** ${rows_after}\n• **Rows removed:** ${rows_removed}`;
          
          if (additional_data) {
            assistantContent += `\n\n📈 **Additional Information:**\n• **Total remaining rows:** ${additional_data.total_rows}\n• **Total columns:** ${additional_data.total_columns}`;
          }
          
          assistantContent += '\n\n✅ Your dataset has been cleaned and updated. You can download it anytime!';
        } else if (operation === 'count' || operation === 'unique') {
          assistantContent = `📊 **${operation === 'count' ? 'Count Analysis' : 'Unique Values Analysis'}**\n\n`;
          
          if (data) {
            Object.entries(data).forEach(([key, value]) => {
              if (typeof value === 'object' && !Array.isArray(value)) {
                assistantContent += `\n**${key}:**\n`;
                Object.entries(value).forEach(([k, v]) => {
                  assistantContent += `  • ${k}: ${Array.isArray(v) ? v.slice(0, 5).join(', ') : v}\n`;
                });
              } else if (!Array.isArray(value)) {
                assistantContent += `• **${key}:** ${value}\n`;
              }
            });
          }
          resultData = data;
        } else if (data && typeof data === 'object') {
          assistantContent = `📈 **Analysis Complete**\n\n`;
          
          if (data.summary) {
            assistantContent += '**Statistical Summary:**\n';
            Object.entries(data.summary).forEach(([col, stats]) => {
              assistantContent += `\n**${col}:**\n`;
              Object.entries(stats).forEach(([stat, value]) => {
                assistantContent += `  • ${stat}: ${typeof value === 'number' ? value.toFixed(2) : value}\n`;
              });
            });
          } else if (results && typeof results === 'object') {
            assistantContent += '**Analysis Results:**\n';
            Object.entries(results).forEach(([key, value]) => {
              assistantContent += `• **${key}:** ${typeof value === 'number' ? value.toFixed(2) : value}\n`;
            });
          } else {
            Object.entries(data).forEach(([key, value]) => {
              assistantContent += `• **${key}:** ${value}\n`;
            });
          }
          resultData = data;
        } else {
          assistantContent = `✅ ${message}`;
        }
      } else {
        assistantContent = `❌ **Analysis Error**\n\n${response.data.error || 'Unknown error occurred'}`;
      }

      const assistantMsg = {
        id: messages.length + 2,
        type: 'assistant',
        content: assistantContent,
        timestamp: new Date(),
        chartPath: chartPath,
        data: resultData,
        isError: response.data.status !== 'success'
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      const errorMsg = {
        id: messages.length + 2,
        type: 'assistant',
        content: `❌ Error processing query: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  // Handle download
  const handleDownload = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/download`, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'processed_dataset.xlsx');
      document.body.appendChild(link);
      link.click();
      if (link.parentElement) {
        link.parentElement.removeChild(link);
      }

      const downloadMsg = {
        id: messages.length + 1,
        type: 'assistant',
        content: '✅ Dataset downloaded successfully! File: processed_dataset.xlsx',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, downloadMsg]);
    } catch (error) {
      const errorMsg = {
        id: messages.length + 1,
        type: 'assistant',
        content: `❌ Download failed: ${error.message}`,
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container fluid className="chat-app">
      <Row className="h-100">
        <Col md={12} className="p-0">
          <ChatInterface
            messages={messages}
            onSendMessage={handleSendMessage}
            onFileUpload={handleFileUpload}
            onDownload={handleDownload}
            loading={loading}
            datasetInfo={datasetInfo}
            messagesEndRef={messagesEndRef}
            inputValue={inputValue}
            setInputValue={setInputValue}
          />
        </Col>
      </Row>
    </Container>
  );
}

export default App;
