import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { MetricsProvider } from './contexts/MetricsContext';

// Components
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import SplashScreen from './pages/SplashScreen';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import HomePage from './pages/HomePage';
import ScanPage from './pages/ScanPage';
import ResultsPage from './pages/ResultsPage';
import ChatbotPage from './pages/ChatbotPage';
import PreviousScansPage from './pages/PreviousScansPage';
import AboutPage from './pages/AboutPage';

function App() {
  return (
    <AuthProvider>
      <MetricsProvider>
        <Router>
          <div className="min-h-screen bg-gray-50">
            <Routes>
              {/* Public Routes */}
              <Route path="/splash" element={<SplashScreen />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/about" element={<AboutPage />} />
              
              {/* Protected Routes with Layout */}
              <Route path="/home" element={<ProtectedRoute><Layout><HomePage /></Layout></ProtectedRoute>} />
              <Route path="/scan" element={<ProtectedRoute><Layout><ScanPage /></Layout></ProtectedRoute>} />
              <Route path="/results" element={<ProtectedRoute><Layout><ResultsPage /></Layout></ProtectedRoute>} />
              <Route path="/chatbot" element={<ProtectedRoute><Layout><ChatbotPage /></Layout></ProtectedRoute>} />
              <Route path="/history" element={<ProtectedRoute><Layout><PreviousScansPage /></Layout></ProtectedRoute>} />
              
              {/* Default redirects */}
              <Route path="/" element={<Navigate to="/splash" replace />} />
              <Route path="*" element={<Navigate to="/splash" replace />} />
            </Routes>
          </div>
        </Router>
      </MetricsProvider>
    </AuthProvider>
  );
}

export default App;
