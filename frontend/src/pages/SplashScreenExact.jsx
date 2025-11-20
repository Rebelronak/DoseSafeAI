import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Heart, Brain } from 'lucide-react';

const SplashScreen = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/login');
    }, 2000); // 2 seconds as specified

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-600 via-orange-500 to-orange-700 flex items-center justify-center text-white">
      <div className="text-center animate-fade-in">
        {/* Main Icon - 80x80px white animated pulse */}
        <div className="flex justify-center mb-8">
          <div className="relative">
            <Shield className="h-20 w-20 text-white animate-pulse" />
            {/* Small bouncing icons - 24x24px */}
            <Heart className="h-6 w-6 text-white absolute -top-2 -right-2 animate-bounce" />
            <Brain className="h-6 w-6 text-white absolute -bottom-2 -left-2 animate-bounce" style={{ animationDelay: '0.5s' }} />
          </div>
        </div>
        
        {/* Title - 48px white bold */}
        <h1 className="text-5xl font-bold mb-4 text-white">
          DoseSafe AI
        </h1>
        
        {/* Subtitle - 20px orange-100 */}
        <p className="text-xl text-orange-100 mb-8">
          Protecting Lives Through Technology
        </p>
        
        {/* Loading dots - white bounce animation */}
        <div className="flex justify-center space-x-2">
          <div className="w-3 h-3 bg-white rounded-full animate-bounce"></div>
          <div className="w-3 h-3 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-3 h-3 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;
