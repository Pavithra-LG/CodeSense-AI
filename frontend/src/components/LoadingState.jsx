import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, GitBranch, FileCode2, Cpu, Sparkles } from 'lucide-react';

const STEPS = [
  { label: 'Validating GitHub URL & Access Permissions', icon: GitBranch },
  { label: 'Cloning Repository to Storage', icon: GitBranch },
  { label: 'Parsing Source Code Files & Directories', icon: FileCode2 },
  { label: 'Detecting Frameworks & Language Distribution', icon: Cpu },
  { label: 'Generating AI Architecture & Developer Insights', icon: Sparkles },
];

const LoadingState = () => {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 3500);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="loading-container glass-card">
      <div className="spinner-glow" />
      
      <h3 className="loading-title">Analyzing Repository</h3>
      <p className="loading-subtitle">
        Cloning codebase, calculating metrics, and fetching AI architecture summary...
      </p>

      <div className="progress-steps">
        {STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isCompleted = idx < activeStep;
          const isActive = idx === activeStep;

          return (
            <div
              key={idx}
              className={`step-item ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}`}
            >
              {isCompleted ? (
                <CheckCircle2 className="step-icon" color="#34d399" />
              ) : isActive ? (
                <Loader2 className="step-icon animate-spin" color="#6366f1" />
              ) : (
                <Icon className="step-icon" color="#6b7280" />
              )}
              <span>{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default LoadingState;
