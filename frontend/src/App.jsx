import React, { useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import { analyzeRepository } from './services/api';
import './App.css';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  const handleAnalyze = async (githubUrl) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await analyzeRepository(githubUrl);
      setAnalysisData(data);
      setIsLoading(false);
      navigate('/dashboard');
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'Failed to analyze repository. Please check the URL and try again.');
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setAnalysisData(null);
    setError(null);
    navigate('/');
  };

  return (
    <div className="app-container">
      <Navbar />

      <main className="main-content">
        <Routes>
          <Route
            path="/"
            element={
              <HomePage
                onAnalyze={handleAnalyze}
                isLoading={isLoading}
                error={error}
                setError={setError}
              />
            }
          />
          <Route
            path="/dashboard"
            element={
              <DashboardPage
                data={analysisData}
                onReset={handleReset}
              />
            }
          />
        </Routes>
      </main>

      <footer className="footer">
        CodeSense AI – AI-Powered GitHub Repository Analysis Assistant &copy; {new Date().getFullYear()}
      </footer>
    </div>
  );
}

export default App;
