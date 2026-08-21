import React from 'react';
import { Cpu, FileCode } from 'lucide-react';

const TechStackCard = ({ technologies }) => {
  if (!technologies || technologies.length === 0) {
    return (
      <div className="glass-card">
        <div className="card-header-title">
          <Cpu color="#06b6d4" size={22} />
          <span>Technology Stack</span>
        </div>
        <p className="summary-text" style={{ color: 'var(--text-dim)' }}>
          No specific framework configuration files detected in root paths.
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card">
      <div className="card-header-title">
        <Cpu color="#06b6d4" size={22} />
        <span>Technology Stack & Frameworks</span>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginLeft: 'auto' }}>
          {technologies.length} detected
        </span>
      </div>

      <div className="tech-grid">
        {technologies.map((tech, idx) => (
          <div key={idx} className="tech-badge-card">
            <div className="tech-name">{tech.name}</div>
            <div className="tech-cat">{tech.category}</div>
            <div className="tech-source">
              <FileCode size={12} style={{ display: 'inline', marginRight: '4px' }} />
              {tech.source_file}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TechStackCard;
