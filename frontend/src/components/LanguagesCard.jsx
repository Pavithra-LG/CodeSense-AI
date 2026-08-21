import React from 'react';
import { Code2 } from 'lucide-react';

const LanguagesCard = ({ languages }) => {
  if (!languages || languages.length === 0) return null;

  return (
    <div className="glass-card">
      <div className="card-header-title">
        <Code2 color="#3b82f6" size={22} />
        <span>Programming Languages</span>
      </div>

      <div className="languages-container">
        {/* Multi-color Progress Bar */}
        <div className="lang-bar-wrapper">
          {languages.map((lang, idx) => (
            <div
              key={idx}
              className="lang-bar-segment"
              style={{
                width: `${lang.percentage}%`,
                backgroundColor: lang.color,
              }}
              title={`${lang.language}: ${lang.percentage}%`}
            />
          ))}
        </div>

        {/* Legend Grid */}
        <div className="lang-list">
          {languages.map((lang, idx) => (
            <div key={idx} className="lang-item">
              <div className="lang-dot" style={{ backgroundColor: lang.color }} />
              <span className="lang-name">{lang.language}</span>
              <span className="lang-pct">{lang.percentage}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LanguagesCard;
