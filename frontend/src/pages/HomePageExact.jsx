import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useMetrics } from '../contexts/MetricsContext';
import { 
  Scan, 
  MessageCircle, 
  History, 
  Shield, 
  Heart, 
  Users, 
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Star
} from 'lucide-react';

const HomePage = () => {
  const { user } = useAuth();
  const { metrics } = useMetrics();
  const navigate = useNavigate();
  const [isNewUser, setIsNewUser] = useState(false);

  useEffect(() => {
    // Check if user is new (created in last 24 hours)
    if (user?.createdAt) {
      const createdDate = new Date(user.createdAt);
      const now = new Date();
      const daysSinceCreation = (now - createdDate) / (1000 * 60 * 60 * 24);
      setIsNewUser(daysSinceCreation < 1);
    }
  }, [user]);

  const quickActions = [
    {
      title: 'Scan Prescription',
      description: 'Upload or manually enter medication details',
      icon: Scan,
      color: 'primary',
      path: '/scan',
      delay: '0s'
    },
    {
      title: 'AI Assistant',
      description: 'Ask questions about medications and interactions',
      icon: MessageCircle,
      color: 'success',
      path: '/chatbot',
      delay: '0.1s'
    },
    {
      title: 'Previous Scans',
      description: 'View your medication history and past results',
      icon: History,
      color: 'secondary',
      path: '/history',
      delay: '0.2s'
    }
  ];

  const getColorClasses = (color) => {
    const colors = {
      primary: 'bg-primary-100 text-primary-700 hover:bg-primary-200',
      success: 'bg-success-100 text-success-700 hover:bg-success-200',
      secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200',
      danger: 'bg-danger-100 text-danger-700 hover:bg-danger-200'
    };
    return colors[color] || colors.primary;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="p-4 bg-white/10 rounded-full backdrop-blur-sm">
                <Shield className="h-16 w-16" />
              </div>
            </div>
            <h1 className="text-4xl md:text-6xl font-bold mb-4">
              Welcome back, {user?.name || 'User'}!
            </h1>
            
            {/* Tagline */}
            <div className="mb-6">
              <p className="text-2xl font-semibold text-primary-100 animate-text-glow">
                💡 "Scan Smart. Prescribe Safe. Live Healthy."
              </p>
            </div>
            
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              Your AI-powered prescription safety companion
            </p>
            
            {isNewUser && (
              <div className="inline-flex items-center px-4 py-2 bg-success-500 text-white rounded-full text-sm font-medium mb-6">
                <Star className="h-4 w-4 mr-2" />
                New User - Welcome to DoseSafe!
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {quickActions.map((action, index) => {
            const Icon = action.icon;
            return (
              <div
                key={action.title}
                className="card p-8 text-center group hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:-translate-y-1"
                style={{ animationDelay: action.delay }}
                onClick={() => navigate(action.path)}
              >
                <div className={`inline-flex p-4 rounded-full mb-4 transition-colors duration-300 ${getColorClasses(action.color)}`}>
                  <Icon className="h-8 w-8" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {action.title}
                </h3>
                <p className="text-gray-600 mb-4">
                  {action.description}
                </p>
                <div className="text-sm font-medium text-primary-600 group-hover:text-primary-700">
                  Get Started →
                </div>
              </div>
            );
          })}
        </div>

        {/* Stats Section */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 mb-12">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Your Safety Impact</h2>
            <p className="text-gray-600">See how DoseSafe is helping keep you and others safe</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600 mb-2">
                {metrics?.scansCompleted || 0}
              </div>
              <div className="text-gray-600">Scans Completed</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-success-600 mb-2">
                {metrics?.safetyChecks || 0}
              </div>
              <div className="text-gray-600">Safety Checks</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-danger-600 mb-2">
                {metrics?.warningsIssued || 0}
              </div>
              <div className="text-gray-600">Warnings Issued</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">
                {metrics?.livesProtected || 0}
              </div>
              <div className="text-gray-600">Lives Protected</div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Recent Activity</h2>
            <button 
              onClick={() => navigate('/history')}
              className="text-primary-600 hover:text-primary-700 font-medium text-sm"
            >
              View All →
            </button>
          </div>
          
          <div className="space-y-4">
            {[
              {
                icon: CheckCircle,
                title: 'Prescription Scan Completed',
                description: 'No interactions found - All medications are safe',
                time: '2 hours ago',
                status: 'success'
              },
              {
                icon: AlertTriangle,
                title: 'Drug Interaction Warning',
                description: 'Potential interaction detected between medications',
                time: '1 day ago',
                status: 'warning'
              },
              {
                icon: MessageCircle,
                title: 'AI Assistant Consultation',
                description: 'Asked about medication timing and dosage',
                time: '3 days ago',
                status: 'info'
              }
            ].map((activity, index) => {
              const Icon = activity.icon;
              const statusColors = {
                success: 'text-success-600 bg-success-100',
                warning: 'text-warning-600 bg-warning-100',
                info: 'text-blue-600 bg-blue-100'
              };
              
              return (
                <div key={index} className="flex items-start space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className={`p-2 rounded-full ${statusColors[activity.status]}`}>
                    <Icon className="h-4 w-4" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{activity.title}</h4>
                    <p className="text-sm text-gray-600">{activity.description}</p>
                  </div>
                  <div className="text-xs text-gray-500 flex items-center">
                    <Clock className="h-3 w-3 mr-1" />
                    {activity.time}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
