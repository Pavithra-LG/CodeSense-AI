import React from 'react';
import { Files, Folder, HardDrive, FileCheck, FileCode } from 'lucide-react';

const StatsCard = ({ stats }) => {
  if (!stats) return null;

  const largestFile = stats.largest_files && stats.largest_files.length > 0
    ? stats.largest_files[0]
    : null;

  return (
    <div className="stats-grid">
      <div className="glass-card stat-card">
        <div className="stat-icon-wrapper" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#6366f1' }}>
          <Files size={24} />
        </div>
        <div>
          <div className="stat-val">{stats.total_files.toLocaleString()}</div>
          <div className="stat-lbl">Total Files</div>
        </div>
      </div>

      <div className="glass-card stat-card">
        <div className="stat-icon-wrapper" style={{ background: 'rgba(6, 182, 212, 0.15)', color: '#06b6d4' }}>
          <Folder size={24} />
        </div>
        <div>
          <div className="stat-val">{stats.total_folders.toLocaleString()}</div>
          <div className="stat-lbl">Total Folders</div>
        </div>
      </div>

      <div className="glass-card stat-card">
        <div className="stat-icon-wrapper" style={{ background: 'rgba(168, 85, 247, 0.15)', color: '#a855f7' }}>
          <HardDrive size={24} />
        </div>
        <div>
          <div className="stat-val">{stats.total_size_formatted}</div>
          <div className="stat-lbl">Repo Size</div>
        </div>
      </div>

      <div className="glass-card stat-card">
        <div className="stat-icon-wrapper" style={{ background: stats.readme_available ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)', color: stats.readme_available ? '#10b981' : '#ef4444' }}>
          <FileCheck size={24} />
        </div>
        <div>
          <div className="stat-val">{stats.readme_available ? 'Available' : 'Missing'}</div>
          <div className="stat-lbl">README File</div>
        </div>
      </div>

      {largestFile && (
        <div className="glass-card stat-card" style={{ gridColumn: 'span 2' }}>
          <div className="stat-icon-wrapper" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#f59e0b' }}>
            <FileCode size={24} />
          </div>
          <div style={{ overflow: 'hidden' }}>
            <div className="stat-val" style={{ fontSize: '1.1rem', wordBreak: 'break-all' }}>{largestFile.path}</div>
            <div className="stat-lbl">Largest File ({largestFile.size_formatted})</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StatsCard;
