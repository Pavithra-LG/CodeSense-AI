import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

const ErrorAlert = ({ message, onRetry }) => {
  if (!message) return null;

  return (
    <div className="error-banner">
      <AlertTriangle className="error-icon" size={24} />
      <div style={{ flex: 1 }}>
        <div className="error-title">Analysis Failed</div>
        <p style={{ fontSize: '0.9rem', lineHeight: '1.5' }}>{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="btn-secondary"
          style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}
        >
          <RefreshCw size={14} /> Retry
        </button>
      )}
    </div>
  );
};

export default ErrorAlert;
