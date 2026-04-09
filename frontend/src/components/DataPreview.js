import React from 'react';
import Table from 'react-bootstrap/Table';

function DataPreview({ data }) {
  if (!data || data.length === 0) {
    return <div>No data to display</div>;
  }

  const columns = Object.keys(data[0]);

  return (
    <div className="data-preview-container">
      <h4 className="mb-3">Dataset Preview (First 5 Rows)</h4>
      <div className="table-responsive">
        <Table striped bordered hover>
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx}>
                {columns.map((col) => (
                  <td key={`${idx}-${col}`}>
                    {row[col] !== null ? String(row[col]).substring(0, 50) : 'N/A'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </div>
  );
}

export default DataPreview;
