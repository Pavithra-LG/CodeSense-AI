import React from 'react';
import UrlForm from '../components/UrlForm';
import LoadingState from '../components/LoadingState';
import ErrorAlert from '../components/ErrorAlert';
import { Cpu, GitBranch, Sparkles, Zap } from 'lucide-react';

const HomePage = ({ onAnalyze, isLoading, error, setError }) => {
  return (
    <div>
      <div className="hero-section">
        <h1 className="hero-title">
          Understand any GitHub codebase in <span className="gradient-text">seconds</span>
        </h1>
        <p className="hero-subtitle">
          CodeSense AI clones public GitHub repositories, analyzes source code structure, detects framework tech stacks, and generates developer-friendly architectural summaries.
        </p>

        {error && <ErrorAlert message={error} onRetry={() => setError(null)} />}

        {isLoading ? (
          <LoadingState />
        ) : (
          <UrlForm onSubmit={onAnalyze} isLoading={isLoading} />
        )}
      </div>

      {/* Feature Highlights Grid */}
      {!isLoading && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem', marginTop: '4rem' }}>
          <div className="glass-card" style={{ textAlign: 'center', padding: '2rem 1.5rem' }}>
            <div style={{ width: '50px', height: '50px', borderRadius: '14px', background: 'rgba(99, 102, 241, 0.15)', color: '#6366f1', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.2rem auto' }}>
              <GitBranch size={26} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '0.5rem', color: '#fff' }}>Git Clone Engine</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              Automatic shallow cloning of public repositories powered by GitPython for high-speed analysis.
            </p>
          </div>

          <div className="glass-card" style={{ textAlign: 'center', padding: '2rem 1.5rem' }}>
            <div style={{ width: '50px', height: '50px', borderRadius: '14px', background: 'rgba(6, 182, 212, 0.15)', color: '#06b6d4', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.2rem auto' }}>
              <Cpu size={26} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '0.5rem', color: '#fff' }}>Tech Detector</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              Scans package manifests, Dockerfiles, and build configurations to extract frameworks and language percentages.
            </p>
          </div>

          <div className="glass-card" style={{ textAlign: 'center', padding: '2rem 1.5rem' }}>
            <div style={{ width: '50px', height: '50px', borderRadius: '14px', background: 'rgba(168, 85, 247, 0.15)', color: '#a855f7', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.2rem auto' }}>
              <Sparkles size={26} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '0.5rem', color: '#fff' }}>AI Architecture Insights</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              OpenAI integration summarizes project purpose, key features, and developer onboarding instructions.
            </p>
          </div>

          <div className="glass-card" style={{ textAlign: 'center', padding: '2rem 1.5rem' }}>
            <div style={{ width: '50px', height: '50px', borderRadius: '14px', background: 'rgba(236, 72, 153, 0.15)', color: '#ec4899', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.2rem auto' }}>
              <Zap size={26} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '0.5rem', color: '#fff' }}>Interactive Explorer</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              Explore tree folder structures, README previews, and statistics in a clean glassmorphic dashboard.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;
