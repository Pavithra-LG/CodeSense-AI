import React, { useState } from 'react';
import { Search, ArrowRight, Github } from 'lucide-react';

const SAMPLES = [
  { label: 'FastAPI', url: 'https://github.com/fastapi/fastapi' },
  { label: 'Flask', url: 'https://github.com/pallets/flask' },
  { label: 'React', url: 'https://github.com/facebook/react' },
  { label: 'Express', url: 'https://github.com/expressjs/express' },
];

const UrlForm = ({ onSubmit, isLoading }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      onSubmit(url.trim());
    }
  };

  const handleChipClick = (sampleUrl) => {
    setUrl(sampleUrl);
    onSubmit(sampleUrl);
  };

  return (
    <div className="url-form-wrapper">
      <form onSubmit={handleSubmit}>
        <div className="url-input-container">
          <div className="url-input-wrapper">
            <Github size={20} className="url-icon" />
            <input
              type="text"
              className="url-input"
              placeholder="Paste GitHub URL (e.g. https://github.com/owner/repo or owner/repo)"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={isLoading}
              required
            />
          </div>
          <button type="submit" className="btn-analyze" disabled={isLoading || !url.trim()}>
            {isLoading ? 'Analyzing...' : 'Analyze Repo'}
            {!isLoading && <ArrowRight size={18} />}
          </button>
        </div>
      </form>

      <div className="sample-chips">
        <span className="sample-label">Try popular repos:</span>
        {SAMPLES.map((sample) => (
          <button
            key={sample.label}
            className="chip-btn"
            onClick={() => handleChipClick(sample.url)}
            disabled={isLoading}
          >
            {sample.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default UrlForm;
