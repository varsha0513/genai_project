import React from 'react';
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';
import Alert from 'react-bootstrap/Alert';

function StatisticsDisplay({ data }) {
  if (!data) {
    return <div>No data to display</div>;
  }

  const renderValue = (value) => {
    if (typeof value === 'object') {
      return <pre>{JSON.stringify(value, null, 2)}</pre>;
    }
    return String(value);
  };

  return (
    <div className="statistics-container">
      {data.message && (
        <Alert variant="info" className="mb-4">
          {data.message}
        </Alert>
      )}

      {data.data && (
        <Card className="mb-4">
          <Card.Header className="bg-primary text-white">
            <h5 className="mb-0">📈 Statistical Results</h5>
          </Card.Header>
          <Card.Body>
            {typeof data.data === 'object' && (
              <>
                {typeof data.data === 'string' ? (
                  <p>{data.data}</p>
                ) : Object.entries(data.data).length > 5 ? (
                  <div style={{ overflowX: 'auto' }}>
                    <pre>{JSON.stringify(data.data, null, 2)}</pre>
                  </div>
                ) : (
                  <Table striped bordered>
                    <tbody>
                      {Object.entries(data.data).map(([key, value]) => (
                        <tr key={key}>
                          <td className="fw-bold">{key}</td>
                          <td>{renderValue(value)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                )}
              </>
            )}
          </Card.Body>
        </Card>
      )}

      {data.response && (
        <Card>
          <Card.Header className="bg-success text-white">
            <h5 className="mb-0">✨ Analysis</h5>
          </Card.Header>
          <Card.Body>
            <p style={{ whiteSpace: 'pre-wrap' }}>{data.response}</p>
          </Card.Body>
        </Card>
      )}
    </div>
  );
}

export default StatisticsDisplay;
