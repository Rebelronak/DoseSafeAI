import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Heart, Brain } from 'lucide-react';

const SplashScreen = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/login');
    }, 2000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-600 via-orange-500 to-orange-700 flex items-center justify-center relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-20 w-32 h-32 bg-white rounded-full"></div>
        <div className="absolute top-40 right-32 w-20 h-20 bg-white rounded-full"></div>
        <div className="absolute bottom-32 left-32 w-16 h-16 bg-white rounded-full"></div>
        <div className="absolute bottom-20 right-20 w-24 h-24 bg-white rounded-full"></div>
      </div>

      <div className="text-center z-10 animate-fade-in">
        {/* Logo with Shield - Pulsing Effect */}
        <div className="flex items-center justify-center gap-4 mb-8">
          <div className="animate-pulse">
            <div className="w-20 h-20 bg-white rounded-xl flex items-center justify-center shadow-xl">
              <Shield className="w-10 h-10 text-orange-600" />
            </div>
          </div>
          {/* Accent Icons with Bounce */}
          <div className="animate-bounce" style={{ animationDelay: '0.2s' }}>
            <Heart className="w-8 h-8 text-white" />
          </div>
          <div className="animate-bounce" style={{ animationDelay: '0.4s' }}>
            <Brain className="w-8 h-8 text-white" />
          </div>
        </div>

        {/* Main Logo - 48px */}
        <div className="mb-6">
          <h1 className="text-5xl font-bold text-white mb-2">
            DoseSafe AI
          </h1>
          <p className="text-xl text-orange-100">
            Protecting Lives Through Technology
          </p>
        </div>

        {/* Loading Indicator - Three White Dots with Staggered Bounce */}
        <div className="flex items-center justify-center gap-2">
          <div className="w-3 h-3 bg-white rounded-full animate-bounce"></div>
          <div className="w-3 h-3 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          <div className="w-3 h-3 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;
