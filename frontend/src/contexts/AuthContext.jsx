import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load user from localStorage on mount
  useEffect(() => {
    const savedUser = localStorage.getItem('dosesafe_user');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (error) {
        console.error('Error parsing saved user:', error);
        localStorage.removeItem('dosesafe_user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = (userData) => {
    setUser(userData);
    localStorage.setItem('dosesafe_user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('dosesafe_user');
    // Also clear any scan data
    localStorage.removeItem('latest_scan_result');
  };

  const register = (userData) => {
    // In a real app, this would make an API call
    const newUser = {
      id: Date.now().toString(),
      email: userData.email,
      name: userData.name,
      createdAt: new Date().toISOString()
    };
    
    // Save to users list
    const existingUsers = JSON.parse(localStorage.getItem('dosesafe_users') || '[]');
    existingUsers.push(newUser);
    localStorage.setItem('dosesafe_users', JSON.stringify(existingUsers));
    
    // Auto login after registration
    login(newUser);
    
    return newUser;
  };

  const value = {
    user,
    isLoading,
    login,
    logout,
    register,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
