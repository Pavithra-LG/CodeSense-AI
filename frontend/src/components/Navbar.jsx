import React from 'react';
import { Code2, Github, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();

  return (
    <header className="navbar">
      <div className="nav-brand" onClick={() => navigate('/')}>
        <div className="nav-logo-icon">
          <Code2 size={22} color="#ffffff" />
        </div>
        <span>CodeSense <span className="gradient-text">AI</span></span>
      </div>

      <div className="nav-links">
        <div className="nav-badge">
          <Sparkles size={13} style={{ display: 'inline', marginRight: '4px' }} />
          v1.0 MVP
        </div>
        <a 
          href="https://github.com" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="btn-github-link"
        >
          <Github size={18} />
          GitHub
        </a>
      </div>
    </header>
  );
};

export default Navbar;
