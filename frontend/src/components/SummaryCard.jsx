import React from 'react';
import { Sparkles, Layers, Cpu, FolderGit2, CheckCircle2, UserCheck } from 'lucide-react';

const SummaryCard = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="glass-card">
      <div className="card-header-title">
        <Sparkles color="#a855f7" size={22} />
        <span>AI Architectural Analysis</span>
        {!summary.is_ai_generated && (
          <span style={{ fontSize: '0.75rem', background: 'rgba(245, 158, 11, 0.15)', color: '#fbbf24', border: '1px solid rgba(245, 158, 11, 0.3)', padding: '0.2rem 0.6rem', borderRadius: '12px', marginLeft: 'auto' }}>
            Algorithmic Mode
          </span>
        )}
      </div>

      {/* Purpose */}
      <div className="summary-block">
        <h4 className="summary-subtitle">
          <Layers size={17} /> Project Purpose
        </h4>
        <p className="summary-text">{summary.project_purpose}</p>
      </div>

      {/* Architecture */}
      <div className="summary-block">
        <h4 className="summary-subtitle">
          <Layers size={17} /> Architecture Overview
        </h4>
        <p className="summary-text">{summary.architecture_overview}</p>
      </div>

      {/* Developer Quickstart Summary */}
      <div className="summary-block">
        <h4 className="summary-subtitle">
          <UserCheck size={17} /> Developer Onboarding Summary
        </h4>
        <p className="summary-text">{summary.developer_summary}</p>
      </div>

      {/* Technology Explanations */}
      {summary.technology_explanation && summary.technology_explanation.length > 0 && (
        <div className="summary-block">
          <h4 className="summary-subtitle">
            <Cpu size={17} /> Technology Breakdown
          </h4>
          <ul className="summary-list">
            {summary.technology_explanation.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Folder Structure Explanations */}
      {summary.folder_explanation && summary.folder_explanation.length > 0 && (
        <div className="summary-block">
          <h4 className="summary-subtitle">
            <FolderGit2 size={17} /> Directory Structure Insights
          </h4>
          <ul className="summary-list">
            {summary.folder_explanation.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Main Features */}
      {summary.main_features && summary.main_features.length > 0 && (
        <div className="summary-block">
          <h4 className="summary-subtitle">
            <CheckCircle2 size={17} /> Key Highlights & Features
          </h4>
          <ul className="summary-list">
            {summary.main_features.map((feat, idx) => (
              <li key={idx}>{feat}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SummaryCard;
