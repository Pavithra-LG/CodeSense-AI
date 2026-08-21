import React, { useState } from 'react';
import { ExternalLink, RefreshCcw, Sparkles, Cpu, Code2, FolderTree, BarChart3, LayoutGrid } from 'lucide-react';
import SummaryCard from '../components/SummaryCard';
import TechStackCard from '../components/TechStackCard';
import LanguagesCard from '../components/LanguagesCard';
import StatsCard from '../components/StatsCard';
import FolderTreeCard from '../components/FolderTreeCard';
import { useNavigate } from 'react-router-dom';

const DashboardPage = ({ data, onReset }) => {
  const [activeTab, setActiveTab] = useState('all');
  const navigate = useNavigate();

  if (!data) {
    navigate('/');
    return null;
  }

  const { owner, repo_name, url, stats, languages, technologies, summary, folder_structure, readme_content } = data;

  return (
    <div>
      {/* Dashboard Header */}
      <div className="dashboard-header">
        <div className="repo-title-wrapper">
          <div className="repo-badge-icon">
            <Code2 size={26} />
          </div>
          <div>
            <h1 className="repo-name">{owner} / {repo_name}</h1>
            <a href={url} target="_blank" rel="noopener noreferrer" className="repo-url-link">
              {url} <ExternalLink size={14} />
            </a>
          </div>
        </div>

        <button onClick={onReset} className="btn-secondary">
          <RefreshCcw size={16} />
          Analyze Another Repo
        </button>
      </div>

      {/* Overview Metric Stats */}
      <StatsCard stats={stats} />

      {/* Tabs */}
      <div className="dashboard-tabs">
        <button
          className={`tab-btn ${activeTab === 'all' ? 'active' : ''}`}
          onClick={() => setActiveTab('all')}
        >
          <LayoutGrid size={16} /> All Insights
        </button>
        <button
          className={`tab-btn ${activeTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveTab('summary')}
        >
          <Sparkles size={16} /> AI Summary
        </button>
        <button
          className={`tab-btn ${activeTab === 'tech' ? 'active' : ''}`}
          onClick={() => setActiveTab('tech')}
        >
          <Cpu size={16} /> Tech Stack & Languages
        </button>
        <button
          className={`tab-btn ${activeTab === 'explorer' ? 'active' : ''}`}
          onClick={() => setActiveTab('explorer')}
        >
          <FolderTree size={16} /> Files & README
        </button>
      </div>

      {/* Tab Contents */}
      {activeTab === 'all' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <SummaryCard summary={summary} />
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '2rem' }}>
            <TechStackCard technologies={technologies} />
            <LanguagesCard languages={languages} />
          </div>
          <FolderTreeCard folderStructure={folder_structure} readmeContent={readme_content} />
        </div>
      )}

      {activeTab === 'summary' && (
        <SummaryCard summary={summary} />
      )}

      {activeTab === 'tech' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <TechStackCard technologies={technologies} />
          <LanguagesCard languages={languages} />
        </div>
      )}

      {activeTab === 'explorer' && (
        <FolderTreeCard folderStructure={folder_structure} readmeContent={readme_content} />
      )}
    </div>
  );
};

export default DashboardPage;
