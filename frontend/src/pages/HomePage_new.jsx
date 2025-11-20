import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useMetrics } from '../contexts/MetricsContext';
import { 
  Scan, 
  MessageCircle, 
  History, 
  Shield, 
  Clock, 
  Users, 
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
      title: '📸 Scan Prescription',
      description: 'Upload or photograph your prescription for instant analysis',
      icon: Scan,
      gradient: 'from-primary-500 to-primary-600',
      path: '/scan',
      delay: '0s'
    },
    {
      title: '💬 AI Assistant', 
      description: 'Get instant answers about medications and interactions',
      icon: MessageCircle,
      gradient: 'from-blue-500 to-blue-600',
      path: '/chatbot',
      delay: '0.1s'
    },
    {
      title: '📊 Scan History',
      description: 'View and manage your previous prescription scans',
      icon: History,
      gradient: 'from-purple-500 to-purple-600',
      path: '/history',
      delay: '0.2s'
    }
  ];

  const benefits = [
    {
      icon: Shield,
      title: '🛡️ Advanced Safety Checks',
      description: 'AI-powered analysis detects dangerous drug interactions before they happen'
    },
    {
      icon: Clock,
      title: '⚡ Instant Results',
      description: 'Get comprehensive medication analysis in seconds, not hours'
    },
    {
      icon: Users,
      title: '👥 Expert-Backed',
      description: 'Developed by medical professionals and validated by clinical research'
    },
    {
      icon: Star,
      title: '🏆 99.7% Accuracy',
      description: 'Industry-leading precision in drug interaction detection and analysis'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section with Gradient Background */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="lg:grid lg:grid-cols-2 lg:gap-8 items-center">
            <div className="mb-8 lg:mb-0">
              {isNewUser ? (
                <h1 className="text-5xl font-bold mb-4">
                  ✨ Welcome to DoseSafe AI, {user?.name}!
                </h1>
              ) : (
                <h1 className="text-5xl font-bold mb-4">
                  Welcome back, {user?.name}!
                </h1>
              )}
              <p className="text-xl text-primary-100 mb-8 leading-relaxed">
                Your smart prescription management journey starts here. Let's keep you 
                safe with AI-powered medication analysis.
              </p>
              <div className="flex gap-4">
                <button
                  onClick={() => navigate('/scan')}
                  className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
                >
                  Scan Now
                </button>
                <button
                  onClick={() => navigate('/about')}
                  className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-600 transition-colors"
                >
                  Learn More →
                </button>
              </div>
            </div>
            
            {/* Stats Preview with Glass Effect */}
            <div className="lg:ml-8">
              <div className="glass-card p-6 rounded-xl">
                <h3 className="text-lg font-semibold mb-4 text-white">DoseSafe AI Impact</h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">💊</span>
                    <span className="text-white">2.5M+ Prescriptions Analyzed</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">⚠️</span>
                    <span className="text-white">150K+ Drug Interactions Detected</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Quick Action Cards - 3-column grid */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Get Started</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              return (
                <div
                  key={action.title}
                  className="animate-slide-up opacity-0"
                  style={{ 
                    animation: `slideUp 0.6s ease-out ${action.delay} forwards` 
                  }}
                >
                  <button
                    onClick={() => navigate(action.path)}
                    className={`w-full p-8 bg-gradient-to-br ${action.gradient} rounded-2xl text-white shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 text-left group`}
                  >
                    <div className="mb-6">
                      <Icon className="w-8 h-8 text-white group-hover:scale-110 transition-transform duration-300" />
                    </div>
                    <h3 className="text-xl font-semibold mb-3">
                      {action.title}
                    </h3>
                    <p className="text-white/90 leading-relaxed">
                      {action.description}
                    </p>
                    <div className="mt-4">
                      <span className="inline-block bg-white/20 px-4 py-2 rounded-lg text-sm font-medium">
                        Get started
                      </span>
                    </div>
                  </button>
                </div>
              );
            })}
          </div>
        </div>

        {/* Benefits Section */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Choose DoseSafe AI?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Advanced AI technology meets medical expertise to provide unparalleled medication safety
            </p>
          </div>
          <div className="grid md:grid-cols-4 gap-6">
            {benefits.map((benefit, index) => {
              const Icon = benefit.icon;
              return (
                <div key={benefit.title} className="text-center p-6 bg-white rounded-xl shadow-sm border border-gray-200">
                  <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-primary-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    {benefit.title}
                  </h3>
                  <p className="text-gray-600">
                    {benefit.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Impact Statistics */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">DoseSafe AI Impact</h2>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">💊</span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">2.5M+</div>
              <div className="text-gray-600">Prescriptions Analyzed</div>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-danger-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">⚠️</span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">150K+</div>
              <div className="text-gray-600">Drug Interactions Detected</div>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🛡️</span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">500K+</div>
              <div className="text-gray-600">Users Protected</div>
            </div>
          </div>
        </div>

        {/* Safety Disclaimer */}
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-6">
          <div className="flex items-start gap-4">
            <div className="w-6 h-6 bg-amber-200 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
              <span className="text-amber-700 text-sm">⚠️</span>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-amber-700 mb-2">Safety First</h3>
              <p className="text-amber-700 leading-relaxed">
                Always consult with your healthcare provider before making any changes to your medication regimen. 
                DoseSafe AI is a powerful tool to help identify potential interactions, but it's not a replacement 
                for professional medical advice.
              </p>
              <div className="mt-4 flex gap-4">
                <button
                  onClick={() => navigate('/chatbot')}
                  className="bg-amber-200 text-amber-700 px-4 py-2 rounded-lg font-medium hover:bg-amber-300 transition-colors"
                >
                  Ask our AI assistant
                </button>
                <button
                  onClick={() => navigate('/about')}
                  className="text-amber-700 px-4 py-2 rounded-lg font-medium hover:bg-amber-100 transition-colors"
                >
                  Learn about our team
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
