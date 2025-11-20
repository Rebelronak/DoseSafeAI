import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Shield, Eye, EyeOff, Mail, Lock } from 'lucide-react';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic validation
    const newErrors = {};
    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // Demo login - accepts any email/password
    const success = login(email, password);
    if (success) {
      navigate('/home');
    } else {
      setErrors({ general: 'Invalid credentials' });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        {/* WHITE CARD BOX - rounded-2xl shadow-xl */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          
          {/* Shield Icon - primary colors */}
          <div className="flex justify-center mb-6">
            <div className="p-3 bg-primary-100 rounded-full">
              <Shield className="h-8 w-8 text-primary-600" />
            </div>
          </div>

          {/* Welcome Back - 32px bold gray */}
          <h1 className="text-3xl font-bold text-gray-900 text-center mb-2">
            Welcome Back
          </h1>
          
          {/* Sign in to your DoseSafe account - 16px gray-600 */}
          <p className="text-gray-600 text-center mb-8">
            Sign in to your DoseSafe account
          </p>

          {errors.general && (
            <div className="mb-4 p-3 bg-danger-50 border border-danger-200 rounded-lg text-danger-800 text-sm">
              {errors.general}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Input - gray border, focus:primary */}
            <div>
              <label className="label">Email Address</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className={`input pl-10 ${errors.email ? 'border-danger-300 focus:ring-danger-500 focus:border-danger-500' : 'border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-primary-500'}`}
                  placeholder="Enter your email"
                />
              </div>
              {errors.email && (
                <p className="mt-1 text-sm text-danger-600">{errors.email}</p>
              )}
            </div>

            {/* Password Input with eye toggle */}
            <div>
              <label className="label">Password</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={`input pl-10 pr-10 ${errors.password ? 'border-danger-300 focus:ring-danger-500 focus:border-danger-500' : 'border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-primary-500'}`}
                  placeholder="Enter your password"
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-danger-600">{errors.password}</p>
              )}
            </div>

            {/* SIGN IN BTN - primary-600 bg, white text */}
            <button
              type="submit"
              className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              Sign In
            </button>
          </form>

          {/* Don't have an account? Create Account - primary-600 link */}
          <p className="mt-6 text-center text-gray-600">
            Don't have an account?{' '}
            <button
              onClick={() => navigate('/signup')}
              className="text-primary-600 hover:text-primary-700 font-medium underline"
            >
              Create Account
            </button>
          </p>

          {/* OR divider */}
          <div className="mt-8 flex items-center">
            <div className="flex-grow border-t border-gray-300"></div>
            <span className="mx-4 text-gray-500 text-sm">OR</span>
            <div className="flex-grow border-t border-gray-300"></div>
          </div>

          {/* Create New Account Button - more prominent */}
          <button
            onClick={() => navigate('/signup')}
            className="mt-6 w-full bg-white border-2 border-primary-600 text-primary-600 hover:bg-primary-50 font-semibold py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            Create New Account
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
