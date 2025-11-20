import React, { createContext, useContext, useState, useEffect } from 'react';

const MetricsContext = createContext();

export const useMetrics = () => {
  const context = useContext(MetricsContext);
  if (!context) {
    throw new Error('useMetrics must be used within a MetricsProvider');
  }
  return context;
};

export const MetricsProvider = ({ children }) => {
  const [metrics, setMetrics] = useState({
    prescriptions: 0,
    interactions: 0,
    peopleSaved: 0,
    medications: 0
  });

  // Load metrics from localStorage on mount with real scan history data
  useEffect(() => {
    // Clear any old cached static data
    localStorage.removeItem('prescriptions');
    localStorage.removeItem('interactions');
    localStorage.removeItem('peopleSaved');
    localStorage.removeItem('users');
    
    refreshMetrics();
  }, []);

  // Listen for storage changes to update metrics when scan history changes
  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === 'scan_history') {
        refreshMetrics();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  // Function to refresh metrics from scan history (called when history changes)
  const refreshMetrics = () => {
    const savedHistory = localStorage.getItem('scan_history');
    let realMetrics = {
      prescriptions: 0,
      interactions: 0,
      peopleSaved: 0,
      medications: 0
    };
    
    if (savedHistory) {
      try {
        const history = JSON.parse(savedHistory);
        realMetrics = {
          prescriptions: history.length,
          medications: history.reduce((total, scan) => total + (scan.medications?.length || 0), 0),
          interactions: history.reduce((total, scan) => total + (scan.interactions?.length || 0), 0),
          peopleSaved: Math.max(1, Math.floor(history.length / 5))
        };
      } catch (error) {
        console.error('Error parsing scan history:', error);
      }
    }
    
    setMetrics(realMetrics);
  };

  const incrementPrescriptions = () => {
    // This is now handled automatically by refreshMetrics when scan history updates
    refreshMetrics();
  };

  const incrementInteractions = (count = 1) => {
    // This is now handled automatically by refreshMetrics when scan history updates
    refreshMetrics();
  };

  const incrementPeopleSaved = () => {
    // This is now handled automatically by refreshMetrics when scan history updates
    refreshMetrics();
  };

  const incrementUsers = () => {
    // This is now handled automatically by refreshMetrics when scan history updates
    refreshMetrics();
  };

  const value = {
    metrics,
    refreshMetrics,
    incrementPrescriptions,
    incrementInteractions,
    incrementPeopleSaved,
    incrementUsers
  };

  return (
    <MetricsContext.Provider value={value}>
      {children}
    </MetricsContext.Provider>
  );
};
