import React from 'react';
import Alert from 'react-bootstrap/Alert';
import Card from 'react-bootstrap/Card';

function VisualizationDisplay({ data }) {
  if (!data) {
    return <div>No visualization to display</div>;
  }

  const API_BASE_URL = 'http://localhost:8000';
  const chartPath = data.chart_path ? `${API_BASE_URL}/${data.chart_path}` : null;

  return (
    <div className="visualization-container">
      <div className="mb-4">
        <h4>📊 {data.chart_type?.toUpperCase() || 'Visualization'}</h4>
        <Alert variant="info">
          <strong>Chart Type:</strong> {data.chart_type || 'Unknown'}
          {data.x_column && <div><strong>X-axis:</strong> {data.x_column}</div>}
          {data.y_column && <div><strong>Y-axis:</strong> {data.y_column}</div>}
        </Alert>
      </div>

      {chartPath && (
        <Card className="mb-4">
          <Card.Body>
            <iframe
              title="chart"
              src={chartPath}
              style={{
                width: '100%',
                height: '600px',
                border: 'none',
                borderRadius: '8px'
              }}
            />
          </Card.Body>
        </Card>
      )}

      {data.insight && (
        <Card className="insight-card">
          <Card.Header className="bg-primary text-white">
            <h5 className="mb-0">💡 AI Insights</h5>
          </Card.Header>
          <Card.Body>
            <p style={{ whiteSpace: 'pre-wrap' }}>{data.insight}</p>
          </Card.Body>
        </Card>
      )}
    </div>
  );
}

export default VisualizationDisplay;
