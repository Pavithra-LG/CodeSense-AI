import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 180000, // 3 minutes timeout for git clones and AI responses
});

export const analyzeRepository = async (githubUrl) => {
  try {
    const response = await api.post('/upload/github', { url: githubUrl });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail);
    } else if (error.request) {
      throw new Error('Backend server is unreachable. Please check if the FastAPI server is running on http://localhost:8000.');
    } else {
      throw new Error(error.message || 'An unknown error occurred during repository analysis.');
    }
  }
};

export const getRepositoryInfo = async (repoSlug) => {
  const params = repoSlug ? { repo: repoSlug } : {};
  const response = await api.get('/repository/info', { params });
  return response.data;
};

export const getRepositorySummary = async (repoSlug) => {
  const params = repoSlug ? { repo: repoSlug } : {};
  const response = await api.get('/repository/summary', { params });
  return response.data;
};

export const getRepositoryTechStack = async (repoSlug) => {
  const params = repoSlug ? { repo: repoSlug } : {};
  const response = await api.get('/repository/techstack', { params });
  return response.data;
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'offline' };
  }
};

export default api;
