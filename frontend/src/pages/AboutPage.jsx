import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMetrics } from '../contexts/MetricsContext';
import { 
  Shield,
  Heart,
  Brain,
  Users,
  CheckCircle,
  Upload,
  Search,
  AlertTriangle,
  Github,
  Linkedin,
  Mail,
  Globe,
  Award,
  TrendingUp,
  Clock,
  Star,
  ArrowLeft,
  Camera,
  BarChart3,
  Target,
  Zap,
  ArrowRight
} from 'lucide-react';

const AboutPage = () => {
  const navigate = useNavigate();
  const { metrics } = useMetrics();

  // Navigation handler
  const handleNavigation = (path) => {
    navigate(path);
  };

  // Stats data with real usage metrics from scan history
  const stats = [
    {
      icon: Shield,
      number: metrics.prescriptions,
      label: 'Total Scans',
      color: 'primary'
    },
    {
      icon: Users,
      number: metrics.peopleSaved,
      label: 'Users Helped',
      color: 'green'
    },
    {
      icon: AlertTriangle,
      number: metrics.interactions,
      label: 'Interactions Found',
      color: 'yellow'
    },
    {
      icon: Target,
      number: metrics.medications,
      label: 'Medications Analyzed',
      color: 'blue'
    }
  ];

  // How it works steps - exactly matching your specifications
  const howItWorks = [
    {
      step: 1,
      title: 'Scan or Enter',
      description: 'Upload photo or enter manually',
      icon: Camera,
      color: 'primary'
    },
    {
      step: 2,
      title: 'AI Analysis',
      description: 'AI processes your data',
      icon: Brain,
      color: 'blue'
    },
    {
      step: 3,
      title: 'Results',
      description: 'Get comprehensive report',
      icon: BarChart3,
      color: 'green'
    }
  ];

  // Team data with only CEO
  const team = [
    {
      name: 'Ronak Kanani',
      role: 'Visionary CEO & Founder',
      description: 'Healthcare entrepreneur with passion for patient safety and AI innovation. Leading the mission to revolutionize prescription safety through intelligent technology.',
      links: { linkedin: '#', email: 'ronak@dosesafe.ai' },
      hasImage: true,
      imageUrl: '/images/ronak-kanani.jpg'
    }
  ];

  // Values data - exactly matching your specifications
  const values = [
    {
      icon: Shield,
      title: 'Safety First',
      description: 'Patient safety is our top priority'
    },
    {
      icon: Users,
      title: 'Accessibility',
      description: 'Healthcare technology should be accessible'
    },
    {
      icon: Award,
      title: 'Excellence',
      description: 'We strive for excellence in everything'
    }
  ];

  // Features data
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Analysis',
      description: 'Advanced machine learning algorithms analyze drug interactions with 99.7% accuracy'
    },
    {
      icon: Shield,
      title: 'Real-time Safety Checks',
      description: 'Instant analysis of drug combinations for immediate safety assessment'
    },
    {
      icon: Upload,
      title: 'Easy Upload System',
      description: 'Simple photo upload or manual entry for prescription analysis'
    },
    {
      icon: BarChart3,
      title: 'Comprehensive Reports',
      description: 'Detailed clinical summaries with clear risk assessments and recommendations'
    },
    {
      icon: Clock,
      title: 'Instant Results',
      description: 'Get complete medication safety analysis in seconds, not hours'
    },
    {
      icon: Star,
      title: 'Clinical Excellence',
      description: 'Developed by medical professionals and validated by clinical research'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <div className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-4">
              <button
                onClick={() => handleNavigation('/home')}
                className="flex items-center gap-2 text-primary-600 hover:text-primary-700 font-semibold transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
                Back to Home
              </button>
            </div>
            <div className="flex items-center gap-6">
              <button
                onClick={() => handleNavigation('/home')}
                className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
              >
                Home
              </button>
              <button
                onClick={() => handleNavigation('/scan')}
                className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
              >
                Scan
              </button>
              <button
                onClick={() => handleNavigation('/chatbot')}
                className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
              >
                AI Assistant
              </button>
              <button
                onClick={() => handleNavigation('/home')}
                className="bg-gradient-to-r from-primary-500 to-primary-600 text-white px-4 py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-300"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <div className="bg-gradient-to-br from-primary-600 via-primary-500 to-orange-500 relative overflow-hidden">
        {/* Animated Background Pattern */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="floating-pill absolute top-20 left-20 w-16 h-32 bg-white/20 rounded-full"></div>
          <div className="floating-pill absolute top-40 right-32 w-20 h-20 bg-white/15 rounded-full" style={{ animationDelay: '1s' }}></div>
          <div className="floating-pill absolute bottom-32 left-32 w-12 h-24 bg-white/25 rounded-full" style={{ animationDelay: '2s' }}></div>
          <div className="floating-pill absolute bottom-20 right-20 w-24 h-24 bg-white/20 rounded-full" style={{ animationDelay: '0.5s' }}></div>
          <div className="floating-pill absolute top-1/2 left-1/4 w-8 h-16 bg-white/10 rounded-full" style={{ animationDelay: '1.5s' }}></div>
          <div className="floating-pill absolute top-3/4 right-1/3 w-14 h-28 bg-white/15 rounded-full" style={{ animationDelay: '3s' }}></div>
        </div>

        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center animate-slide-down">
            {/* Logo and Icons - Smaller */}
            <div className="flex items-center justify-center gap-4 mb-8">
              <div className="animate-bounce" style={{ animationDelay: '0s' }}>
                <div className="w-16 h-16 bg-white rounded-xl flex items-center justify-center shadow-xl">
                  <Shield className="w-8 h-8 text-primary-500" />
                </div>
              </div>
              <div className="animate-bounce" style={{ animationDelay: '0.2s' }}>
                <div className="w-16 h-16 bg-white rounded-xl flex items-center justify-center shadow-xl">
                  <Heart className="w-8 h-8 text-red-500" />
                </div>
              </div>
              <div className="animate-bounce" style={{ animationDelay: '0.4s' }}>
                <div className="w-16 h-16 bg-white rounded-xl flex items-center justify-center shadow-xl">
                  <Brain className="w-8 h-8 text-green-500" />
                </div>
              </div>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Revolutionizing Prescription Safety<br />
              <span className="text-orange-200">Through AI</span>
            </h1>
            <p className="text-lg md:text-xl text-orange-100 max-w-3xl mx-auto mb-8 leading-relaxed">
              DoseSafe AI is a smart prescription safety platform built by Ronak Kanani to reduce the risk of harmful drug interactions using AI. Advanced machine learning technology combines with comprehensive drug databases to provide real-time medication safety analysis and protect patients from dangerous drug interactions.
            </p>

            {/* Stats Grid - More Compact */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-2xl mx-auto">
              {stats.map((stat, index) => {
                const Icon = stat.icon;
                return (
                  <div 
                    key={stat.label}
                    className="text-center animate-slide-up"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div className="w-10 h-10 bg-white/20 backdrop-blur-sm rounded-lg flex items-center justify-center mx-auto mb-2">
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    <p className="text-xl md:text-2xl font-bold text-white mb-1">{stat.number}</p>
                    <p className="text-orange-100 font-medium text-xs">{stat.label}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="bg-white py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20 animate-slide-down">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-8">How DoseSafe AI Works</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our simple three-step process makes medication safety analysis accessible to everyone
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            {howItWorks.map((step, index) => {
              const Icon = step.icon;
              return (
                <div 
                  key={step.step}
                  className="text-center relative animate-slide-up"
                  style={{ animationDelay: `${index * 0.2}s` }}
                >
                  {/* Step connector line */}
                  {index < howItWorks.length - 1 && (
                    <div className="hidden md:block absolute top-12 left-1/2 w-full h-1 bg-gradient-to-r from-primary-300 to-primary-500 z-0" style={{ transform: 'translateX(25%)' }}></div>
                  )}
                  
                  <div className="relative z-10">
                    <div className="w-24 h-24 bg-gradient-to-br from-primary-500 to-primary-600 rounded-3xl flex items-center justify-center mx-auto mb-8 relative shadow-2xl">
                      <Icon className="w-12 h-12 text-white" />
                      <div className="absolute -top-3 -right-3 w-12 h-12 bg-white text-primary-600 rounded-2xl flex items-center justify-center text-xl font-bold shadow-lg">
                        {step.step}
                      </div>
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-6">{step.title}</h3>
                    <p className="text-gray-600 text-lg leading-relaxed">{step.description}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">Advanced Features</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Powered by cutting-edge AI technology and comprehensive medical databases
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div 
                key={feature.title}
                className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 hover:shadow-lg transition-all duration-300 animate-fade-in"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mb-6">
                  <Icon className="w-6 h-6 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Values Section with Better Alignment */}
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">Our Values</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              The principles that guide everything we do at DoseSafe AI
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-start justify-center max-w-4xl mx-auto">
            {values.map((value, index) => {
              const Icon = value.icon;
              return (
                <div 
                  key={value.title}
                  className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8 text-center hover:shadow-xl transition-all duration-300 animate-fade-in h-full flex flex-col"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl shadow-lg flex items-center justify-center mx-auto mb-6">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">{value.title}</h3>
                  <p className="text-gray-600 leading-relaxed flex-grow">{value.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Team Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">Meet Our Team</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Healthcare professionals and technology experts working together to improve medication safety
          </p>
        </div>

        {/* Special CEO Section for Ronak Kanani */}
        <div className="mb-16 bg-gradient-to-br from-primary-50 to-orange-50 rounded-3xl p-8 border-2 border-primary-200">
          <div className="lg:grid lg:grid-cols-2 lg:gap-12 items-center">
            {/* Left Side - CEO Info */}
            <div className="mb-8 lg:mb-0">
              <div className="flex items-center gap-3 mb-4">
                <div className="bg-gradient-to-r from-yellow-400 to-yellow-500 text-yellow-900 text-sm font-bold px-3 py-1 rounded-full shadow-lg">
                  CEO & FOUNDER
                </div>
                <div className="animate-pulse">
                  <span className="text-2xl">👑</span>
                </div>
              </div>
              
              <h3 className="text-4xl font-bold text-gray-900 mb-2 animate-slide-up">Ronak Kanani</h3>
              <p className="text-xl text-primary-600 font-semibold mb-6 animate-slide-up" style={{animationDelay: '0.1s'}}>Visionary CEO & Founder</p>
              
              <div className="prose prose-lg max-w-none animate-fade-in" style={{animationDelay: '0.2s'}}>
                <p className="text-gray-700 leading-relaxed mb-6">
                  Healthcare entrepreneur with passion for patient safety and AI innovation. Leading the mission to revolutionize prescription safety through intelligent technology.
                </p>
                <p className="text-gray-600 leading-relaxed mb-6">
                  With a vision to make healthcare safer through AI, Ronak founded DoseSafe AI to protect patients from dangerous drug interactions and improve medication management worldwide.
                </p>
              </div>

              <div className="flex items-center gap-4 animate-slide-up" style={{animationDelay: '0.3s'}}>
                <a href="#" className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center hover:bg-blue-200 transition-all duration-300 hover:scale-110">
                  <Linkedin className="w-5 h-5 text-blue-600" />
                </a>
                <a href="mailto:ronak@dosesafe.ai" className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center hover:bg-green-200 transition-all duration-300 hover:scale-110">
                  <Mail className="w-5 h-5 text-green-600" />
                </a>
                <a href="#" className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200 transition-all duration-300 hover:scale-110">
                  <Globe className="w-5 h-5 text-gray-600" />
                </a>
              </div>
            </div>

            {/* Right Side - Animated Profile Image */}
            <div className="flex justify-center lg:justify-end">
              <div className="relative animate-float">
                {/* Large Circular Image - READY FOR YOUR PHOTO */}
                <div className="w-80 h-80 rounded-full border-8 border-yellow-400 shadow-2xl overflow-hidden bg-gradient-to-br from-yellow-100 to-orange-100 relative group hover:scale-105 transition-all duration-500">
                  
                  {/* Your Image Will Show Here Automatically */}
                  <img 
                    src="/images/ronak-ceo.jpg" 
                    alt="Ronak Kanani - CEO & Founder"
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    onError={(e) => {
                      // If image not found, show initials
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                  
                  {/* Fallback - Shows initials if image not found */}
                  <div className="w-full h-full bg-gradient-to-br from-yellow-500 via-orange-500 to-red-500 flex items-center justify-center text-white font-bold text-8xl shadow-inner" style={{display: 'none'}}>
                    RK
                  </div>
                  
                  {/* Animated Ring Effect */}
                  <div className="absolute inset-0 rounded-full border-4 border-yellow-400 animate-ping opacity-30"></div>
                  <div className="absolute inset-0 rounded-full border-2 border-orange-400 animate-pulse"></div>
                </div>

                {/* Floating Elements Around Image */}
                <div className="absolute -top-4 -right-4 w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center animate-bounce shadow-lg">
                  <span className="text-2xl">⭐</span>
                </div>
                <div className="absolute -bottom-4 -left-4 w-12 h-12 bg-orange-400 rounded-full flex items-center justify-center animate-pulse shadow-lg">
                  <span className="text-xl">🚀</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Add Team Member CTA */}
        <div className="text-center mt-16">
          <p className="text-gray-600 mb-6">Want to join our mission to improve medication safety?</p>
          <button className="bg-gradient-to-r from-primary-500 to-primary-600 text-white font-semibold px-8 py-3 rounded-xl hover:shadow-lg transition-all duration-300 transform hover:scale-105">
            View Open Positions
          </button>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-br from-primary-600 to-orange-600 py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Enhance Your Medication Safety?
          </h2>
          <p className="text-xl text-orange-100 mb-8 max-w-2xl mx-auto">
            Join thousands of users who trust DoseSafe AI to keep their medications safe and effective.
            Start your journey to better health today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/signup" className="btn bg-white text-primary-600 hover:bg-gray-100 text-lg px-8 py-4">
              Get Started Free
            </Link>
            <Link to="/login" className="btn bg-transparent border-2 border-white text-white hover:bg-white hover:text-primary-600 text-lg px-8 py-4">
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
