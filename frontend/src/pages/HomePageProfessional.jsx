import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  Scan, 
  Shield, 
  MessageCircle,
  History,
  CheckCircle,
  Users,
  TrendingUp,
  Star,
  Heart,
  Brain,
  AlertTriangle,
  Sparkles,
  ArrowRight,
  FileText,
  Clock,
  Award
} from 'lucide-react';

const HomePage = () => {
  const { user } = useAuth();
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
      color: 'gradient-orange',
      textColor: 'text-white',
      path: '/scan',
      delay: '0s'
    },
    {
      title: 'AI Assistant',
      description: 'Ask questions about medications and interactions',
      icon: MessageCircle,
      color: 'gradient-blue',
      textColor: 'text-white',
      path: '/chatbot',
      delay: '0.1s'
    },
    {
      title: 'Previous Scans',
      description: 'View your medication history and past results',
      icon: History,
      color: 'gradient-purple',
      textColor: 'text-white',
      path: '/history',
      delay: '0.2s'
    }
  ];

  const stats = [
    {
      icon: Shield,
      value: '12',
      label: 'Scans Completed',
      color: 'text-primary-600',
      bgColor: 'bg-primary-100'
    },
    {
      icon: CheckCircle,
      value: '8',
      label: 'Safety Checks',
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      icon: AlertTriangle,
      value: '2',
      label: 'Warnings Issued',
      color: 'text-amber-600',
      bgColor: 'bg-amber-100'
    },
    {
      icon: Users,
      value: '5',
      label: 'Lives Protected',
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    }
  ];

  const recentActivity = [
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
  ];

  const benefits = [
    {
      icon: Shield,
      title: 'Safety First',
      description: 'Advanced AI algorithms detect dangerous drug interactions',
      color: 'primary'
    },
    {
      icon: TrendingUp,
      title: 'Lightning Fast',
      description: 'Get comprehensive analysis results in seconds',
      color: 'blue'
    },
    {
      icon: Award,
      title: 'Expert Backed',
      description: 'Validated by healthcare professionals and pharmacists',
      color: 'green'
    },
    {
      icon: Star,
      title: '99.7% Accuracy',
      description: 'Industry-leading precision in drug interaction detection',
      color: 'purple'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-orange-50">
      {/* Hero Section */}
      <div className="gradient-hero text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left Side - Welcome Content */}
            <div className="text-center lg:text-left">
              <div className="flex justify-center lg:justify-start mb-6">
                <div className="relative">
                  <div className="p-4 bg-white/20 rounded-full backdrop-blur-sm animate-pulse-slow">
                    <Shield className="h-16 w-16" />
                  </div>
                  <Sparkles className="h-6 w-6 text-yellow-300 absolute -top-2 -right-2 animate-bounce-slow" />
                </div>
              </div>
              
              {isNewUser && (
                <div className="inline-flex items-center px-4 py-2 bg-green-500 text-white rounded-full text-sm font-medium mb-6 animate-fade-in">
                  <Star className="h-4 w-4 mr-2" />
                  New User - Welcome to DoseSafe!
                </div>
              )}
              
              <h1 className="text-4xl md:text-6xl font-bold mb-4 animate-fade-in">
                Welcome back, {user?.name || 'User'}!
              </h1>
              <p className="text-xl md:text-2xl mb-8 text-white/90 animate-fade-in" style={{ animationDelay: '0.2s' }}>
                Your AI-powered prescription safety companion
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start animate-fade-in" style={{ animationDelay: '0.4s' }}>
                <button
                  onClick={() => navigate('/scan')}
                  className="btn-gradient hover-lift flex items-center justify-center gap-2"
                >
                  <Scan className="h-5 w-5" />
                  Scan Now
                </button>
                <button
                  onClick={() => navigate('/about')}
                  className="btn-outline-gradient flex items-center justify-center gap-2"
                >
                  Learn More
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
            
            {/* Right Side - Stats Preview */}
            <div className="flex justify-center">
              <div className="glass-card rounded-2xl p-8 animate-slide-up">
                <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Your Safety Impact</h3>
                <div className="grid grid-cols-2 gap-6">
                  {stats.map((stat, index) => {
                    const Icon = stat.icon;
                    return (
                      <div key={stat.label} className="text-center animate-fade-in" style={{ animationDelay: `${0.6 + index * 0.1}s` }}>
                        <div className={`inline-flex p-3 rounded-full ${stat.bgColor} mb-3`}>
                          <Icon className={`h-6 w-6 ${stat.color}`} />
                        </div>
                        <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                        <div className="text-sm text-gray-600">{stat.label}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
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
                className="card-interactive hover-lift cursor-pointer animate-fade-in"
                style={{ animationDelay: action.delay }}
                onClick={() => navigate(action.path)}
              >
                <div className="text-center">
                  <div className={`inline-flex p-6 rounded-2xl mb-6 ${action.color} shadow-glow`}>
                    <Icon className={`h-10 w-10 ${action.textColor}`} />
                  </div>
                  <h3 className="text-2xl font-semibold text-gray-900 mb-3">
                    {action.title}
                  </h3>
                  <p className="text-gray-600 mb-6 leading-relaxed">
                    {action.description}
                  </p>
                  <div className="text-primary-600 font-semibold hover:text-primary-700 transition-colors flex items-center justify-center gap-2">
                    Get Started <ArrowRight className="h-4 w-4" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Benefits Section */}
        <div className="bg-white rounded-3xl shadow-xl p-8 md:p-12 mb-12 border border-gray-100">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Choose DoseSafe AI?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Advanced technology meets healthcare expertise to keep you and your loved ones safe
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => {
              const Icon = benefit.icon;
              const colorClasses = {
                primary: 'bg-primary-100 text-primary-600',
                blue: 'bg-blue-100 text-blue-600',
                green: 'bg-green-100 text-green-600',
                purple: 'bg-purple-100 text-purple-600'
              };
              
              return (
                <div
                  key={benefit.title}
                  className="text-center group animate-fade-in"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className={`inline-flex p-4 rounded-2xl mb-4 ${colorClasses[benefit.color]} group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="h-8 w-8" />
                  </div>
                  <h4 className="text-xl font-semibold text-gray-900 mb-2">{benefit.title}</h4>
                  <p className="text-gray-600 leading-relaxed">{benefit.description}</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Statistics Panel */}
        <div className="bg-white rounded-3xl shadow-xl p-8 md:p-12 mb-12 border border-gray-100">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">DoseSafe AI Impact</h2>
            <p className="text-xl text-gray-600">See how we're making healthcare safer every day</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-5xl font-bold text-gradient-primary mb-2">2.5M+</div>
              <div className="text-lg text-gray-600 font-medium">Prescriptions Analyzed</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-gradient-blue mb-2">150K+</div>
              <div className="text-lg text-gray-600 font-medium">Interactions Detected</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-green-600 mb-2">500K+</div>
              <div className="text-lg text-gray-600 font-medium">Users Protected</div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-3xl shadow-xl p-8 md:p-12 border border-gray-100">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Recent Activity</h2>
            <button 
              onClick={() => navigate('/history')}
              className="text-primary-600 hover:text-primary-700 font-semibold flex items-center gap-2 transition-colors"
            >
              View All <ArrowRight className="h-4 w-4" />
            </button>
          </div>
          
          <div className="space-y-6">
            {recentActivity.map((activity, index) => {
              const Icon = activity.icon;
              const statusStyles = {
                success: 'text-green-600 bg-green-100',
                warning: 'text-amber-600 bg-amber-100',
                info: 'text-blue-600 bg-blue-100'
              };
              
              return (
                <div key={index} className="flex items-start space-x-4 p-6 rounded-2xl hover:bg-gray-50 transition-colors card-hover">
                  <div className={`p-3 rounded-full ${statusStyles[activity.status]}`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 text-lg">{activity.title}</h4>
                    <p className="text-gray-600 mt-1">{activity.description}</p>
                  </div>
                  <div className="text-sm text-gray-500 flex items-center">
                    <Clock className="h-4 w-4 mr-1" />
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
