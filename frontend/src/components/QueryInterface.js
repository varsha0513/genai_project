import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

function QueryInterface({ onQuery, loading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onQuery(query);
      setQuery('');
    }
  };

  const quickQueries = [
    'What is the summary of this data?',
    'Show me minimum values',
    'Show me maximum values',
    'Generate a histogram',
    'Remove missing values'
  ];

  return (
    <div className="query-interface-container">
      <h4 className="mb-4">🔍 Natural Language Query</h4>
      
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Enter your query:</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="E.g., 'Show me a histogram of age', 'What is the average salary?', 'Remove missing values'"
            disabled={loading}
          />
        </Form.Group>

        <Button
          variant="primary"
          type="submit"
          disabled={!query.trim() || loading}
          className="w-100 mb-3"
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
              Processing...
            </>
          ) : (
            '✨ Analyze'
          )}
        </Button>
      </Form>

      <div className="quick-queries mt-4">
        <h6>Quick Queries:</h6>
        <div>
          {quickQueries.map((q, idx) => (
            <Button
              key={idx}
              variant="outline-secondary"
              size="sm"
              className="me-2 mb-2"
              onClick={() => onQuery(q)}
              disabled={loading}
            >
              {q}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default QueryInterface;
