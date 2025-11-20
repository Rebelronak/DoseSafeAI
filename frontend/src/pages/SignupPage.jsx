import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useMetrics } from '../contexts/MetricsContext';
import { Shield, Eye, EyeOff, Mail, Lock, User, UserPlus, CheckCircle, AlertCircle } from 'lucide-react';

const SignupPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPasswords, setShowPasswords] = useState({
    password: false,
    confirmPassword: false
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { register } = useAuth();
  const { incrementUsers } = useMetrics();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const togglePasswordVisibility = (field) => {
    setShowPasswords(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // Validation
      if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
        setError('Please fill in all fields');
        return;
      }

      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match');
        return;
      }

      if (formData.password.length < 6) {
        setError('Password must be at least 6 characters long');
        return;
      }

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Register user
      register({
        name: formData.name,
        email: formData.email,
        password: formData.password
      });

      // Increment user count
      incrementUsers();
      
      navigate('/home');
    } catch (err) {
      setError('Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 via-primary-500 to-orange-500 flex items-center justify-center px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="floating-pill absolute top-20 left-20 w-16 h-32 bg-white/20 rounded-full"></div>
        <div className="floating-pill absolute top-40 right-32 w-20 h-20 bg-white/15 rounded-full" style={{ animationDelay: '1s' }}></div>
        <div className="floating-pill absolute bottom-32 left-32 w-12 h-24 bg-white/25 rounded-full" style={{ animationDelay: '2s' }}></div>
        <div className="floating-pill absolute bottom-20 right-20 w-24 h-24 bg-white/20 rounded-full" style={{ animationDelay: '0.5s' }}></div>
        <div className="floating-pill absolute top-1/2 left-1/4 w-8 h-16 bg-white/10 rounded-full" style={{ animationDelay: '1.5s' }}></div>
        <div className="floating-pill absolute top-3/4 right-1/3 w-14 h-28 bg-white/15 rounded-full" style={{ animationDelay: '3s' }}></div>
      </div>

      <div className="max-w-md w-full space-y-8 relative z-10">
        {/* Header */}
        <div className="text-center animate-slide-down">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-white rounded-2xl flex items-center justify-center shadow-2xl transform hover:scale-105 transition-transform duration-300">
              <UserPlus className="w-10 h-10 text-primary-500" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">Join DoseSafe AI</h1>
          <p className="text-xl text-orange-100 max-w-sm mx-auto">Create your account and start protecting your medication safety today</p>
        </div>

        {/* Signup Form */}
        <div className="bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl p-8 animate-slide-up">
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center gap-2 animate-shake">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-1">
              <label className="block text-sm font-semibold text-gray-900">
                Full Name
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 text-gray-900 placeholder-gray-500"
                  placeholder="Enter your full name"
                  required
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-semibold text-gray-900">
                Email Address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 text-gray-900 placeholder-gray-500"
                  placeholder="Enter your email address"
                  required
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-semibold text-gray-900">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type={showPasswords.password ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full pl-12 pr-12 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 text-gray-900 placeholder-gray-500"
                  placeholder="Create a secure password"
                  required
                />
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility('password')}
                  className="absolute inset-y-0 right-0 pr-4 flex items-center hover:text-gray-600 transition-colors duration-200"
                >
                  {showPasswords.password ? (
                    <EyeOff className="h-5 w-5 text-gray-400" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {formData.password && (
                <div className="text-xs text-gray-600 mt-1">
                  Password strength: {formData.password.length >= 8 ? 'Strong' : formData.password.length >= 6 ? 'Medium' : 'Weak'}
                </div>
              )}
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-semibold text-gray-900">
                Confirm Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type={showPasswords.confirmPassword ? 'text' : 'password'}
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className="w-full pl-12 pr-12 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 text-gray-900 placeholder-gray-500"
                  placeholder="Confirm your password"
                  required
                />
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility('confirmPassword')}
                  className="absolute inset-y-0 right-0 pr-4 flex items-center hover:text-gray-600 transition-colors duration-200"
                >
                  {showPasswords.confirmPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {formData.confirmPassword && (
                <div className="flex items-center gap-1 text-xs mt-1">
                  {formData.password === formData.confirmPassword ? (
                    <>
                      <CheckCircle className="w-3 h-3 text-green-500" />
                      <span className="text-green-600">Passwords match</span>
                    </>
                  ) : (
                    <>
                      <AlertCircle className="w-3 h-3 text-red-500" />
                      <span className="text-red-600">Passwords don't match</span>
                    </>
                  )}
                </div>
              )}
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-primary hover:shadow-lg text-white font-semibold py-3 px-4 rounded-xl transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Creating Account...</span>
                </>
              ) : (
                <>
                  <UserPlus className="w-5 h-5" />
                  <span>Create Account</span>
                </>
              )}
            </button>
          </form>

          {/* Terms */}
          <div className="mt-6 text-center">
            <p className="text-xs text-gray-600 leading-relaxed">
              By creating an account, you agree to our{' '}
              <Link to="/terms" className="text-primary-600 hover:text-primary-500 font-medium underline transition-colors duration-200">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link to="/privacy" className="text-primary-600 hover:text-primary-500 font-medium underline transition-colors duration-200">
                Privacy Policy
              </Link>
            </p>
          </div>

          {/* Footer Links */}
          <div className="mt-8 text-center space-y-3">
            <p className="text-sm text-gray-700">
              Already have an account?{' '}
              <Link 
                to="/login" 
                className="font-semibold text-primary-600 hover:text-primary-500 transition-colors duration-200"
              >
                Sign in here
              </Link>
            </p>
            <p className="text-sm">
              <Link 
                to="/about" 
                className="text-gray-500 hover:text-gray-700 transition-colors duration-200"
              >
                Learn more about DoseSafe AI
              </Link>
            </p>
          </div>
        </div>

        {/* Security Badge */}
        <div className="text-center animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full">
            <Shield className="w-4 h-4 text-white" />
            <span className="text-sm text-white font-medium">256-bit SSL Encryption</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
