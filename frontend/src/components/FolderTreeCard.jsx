import React, { useState } from 'react';
import { Folder, FileText, ChevronRight, ChevronDown, FolderTree, BookOpen } from 'lucide-react';

const TreeNode = ({ node }) => {
  const [isOpen, setIsOpen] = useState(false);
  const isDir = node.type === 'directory';

  if (!isDir) {
    return (
      <div className="tree-item" style={{ paddingLeft: '1.2rem' }}>
        <FileText size={15} className="tree-icon-file" />
        <span>{node.name}</span>
      </div>
    );
  }

  return (
    <div className="tree-node">
      <div className="tree-item" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? <ChevronDown size={15} /> : <ChevronRight size={15} />}
        <Folder size={15} className="tree-icon-folder" />
        <span style={{ fontWeight: 600, color: '#fff' }}>{node.name}</span>
      </div>

      {isOpen && node.children && (
        <div style={{ borderLeft: '1px solid rgba(255, 255, 255, 0.08)', marginLeft: '0.8rem' }}>
          {node.children.map((child, idx) => (
            <TreeNode key={idx} node={child} />
          ))}
        </div>
      )}
    </div>
  );
};

const FolderTreeCard = ({ folderStructure, readmeContent }) => {
  const [activeSubTab, setActiveSubTab] = useState('tree');

  return (
    <div className="glass-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem', flexWrap: 'wrap', gap: '0.8rem' }}>
        <div className="card-header-title" style={{ marginBottom: 0 }}>
          <FolderTree color="#a855f7" size={22} />
          <span>Codebase Explorer & Docs</span>
        </div>

        <div style={{ display: 'flex', gap: '0.4rem', background: 'rgba(15, 23, 42, 0.6)', padding: '0.3rem', borderRadius: '8px' }}>
          <button
            className={`chip-btn ${activeSubTab === 'tree' ? 'active' : ''}`}
            onClick={() => setActiveSubTab('tree')}
            style={{ background: activeSubTab === 'tree' ? 'rgba(99, 102, 241, 0.2)' : 'transparent', color: activeSubTab === 'tree' ? '#fff' : 'var(--text-muted)' }}
          >
            <FolderTree size={14} style={{ display: 'inline', marginRight: '4px' }} />
            Directory Tree
          </button>
          <button
            className={`chip-btn ${activeSubTab === 'readme' ? 'active' : ''}`}
            onClick={() => setActiveSubTab('readme')}
            style={{ background: activeSubTab === 'readme' ? 'rgba(99, 102, 241, 0.2)' : 'transparent', color: activeSubTab === 'readme' ? '#fff' : 'var(--text-muted)' }}
          >
            <BookOpen size={14} style={{ display: 'inline', marginRight: '4px' }} />
            README Preview
          </button>
        </div>
      </div>

      {activeSubTab === 'tree' ? (
        <div className="tree-container">
          {folderStructure ? (
            <TreeNode node={folderStructure} />
          ) : (
            <p style={{ color: 'var(--text-dim)' }}>No folder structure available.</p>
          )}
        </div>
      ) : (
        <div className="readme-box">
          {readmeContent ? (
            readmeContent
          ) : (
            <p style={{ color: 'var(--text-dim)', textAlign: 'center', padding: '2rem' }}>
              No README file found in root directory of this repository.
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default FolderTreeCard;
