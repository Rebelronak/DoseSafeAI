import React from 'react';
import { Loader, Brain, Shield, CheckCircle, Search } from 'lucide-react';

const AnalyzingAnimation = ({ stage = 'scanning' }) => {
  const stages = {
    scanning: {
      icon: Search,
      text: 'Scanning prescription...',
      subtext: 'Extracting text from image'
    },
    analyzing: {
      icon: Brain,
      text: 'AI Analysis in progress...',
      subtext: 'Identifying medications and interactions'
    },
    checking: {
      icon: Shield,
      text: 'Checking drug interactions...',
      subtext: 'Analyzing safety profiles'
    },
    completing: {
      icon: CheckCircle,
      text: 'Finalizing results...',
      subtext: 'Preparing comprehensive report'
    }
  };

  const currentStage = stages[stage] || stages.analyzing;
  const Icon = currentStage.icon;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4 text-center">
        {/* Main spinning icon */}
        <div className="mb-6">
          <div className="relative">
            {/* Outer rotating ring */}
            <div className="w-24 h-24 mx-auto">
              <div className="absolute inset-0 border-4 border-primary-200 rounded-full animate-spin border-t-primary-600"></div>
              <div className="absolute inset-2 border-4 border-primary-100 rounded-full animate-spin-slow border-t-primary-500"></div>
              <div className="absolute inset-4 bg-primary-50 rounded-full flex items-center justify-center">
                <Icon className="w-8 h-8 text-primary-600 animate-pulse" />
              </div>
            </div>
          </div>
        </div>

        {/* Progress text */}
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          {currentStage.text}
        </h3>
        <p className="text-gray-600 mb-6">
          {currentStage.subtext}
        </p>

        {/* Progress dots */}
        <div className="flex justify-center space-x-2">
          {[0, 1, 2].map((dot) => (
            <div
              key={dot}
              className={`w-3 h-3 rounded-full bg-primary-300 animate-pulse`}
              style={{
                animationDelay: `${dot * 0.2}s`,
                animationDuration: '1s'
              }}
            />
          ))}
        </div>

        {/* Analyzing steps visualization */}
        <div className="mt-8 space-y-3">
          <div className="flex items-center text-sm">
            <div className={`w-4 h-4 rounded-full mr-3 ${
              ['scanning', 'analyzing', 'checking', 'completing'].includes(stage) 
                ? 'bg-green-500' 
                : 'bg-gray-300'
            }`}>
              {['scanning', 'analyzing', 'checking', 'completing'].includes(stage) && (
                <CheckCircle className="w-4 h-4 text-white" />
              )}
            </div>
            <span className={['scanning', 'analyzing', 'checking', 'completing'].includes(stage) ? 'text-green-600' : 'text-gray-500'}>
              OCR Text Extraction
            </span>
          </div>
          
          <div className="flex items-center text-sm">
            <div className={`w-4 h-4 rounded-full mr-3 ${
              ['analyzing', 'checking', 'completing'].includes(stage) 
                ? 'bg-green-500' 
                : stage === 'scanning' 
                ? 'bg-primary-500 animate-pulse' 
                : 'bg-gray-300'
            }`}>
              {['analyzing', 'checking', 'completing'].includes(stage) && (
                <CheckCircle className="w-4 h-4 text-white" />
              )}
            </div>
            <span className={['analyzing', 'checking', 'completing'].includes(stage) ? 'text-green-600' : 'text-gray-500'}>
              AI Medication Analysis
            </span>
          </div>
          
          <div className="flex items-center text-sm">
            <div className={`w-4 h-4 rounded-full mr-3 ${
              ['checking', 'completing'].includes(stage) 
                ? 'bg-green-500' 
                : ['scanning', 'analyzing'].includes(stage) 
                ? 'bg-primary-500 animate-pulse' 
                : 'bg-gray-300'
            }`}>
              {['checking', 'completing'].includes(stage) && (
                <CheckCircle className="w-4 h-4 text-white" />
              )}
            </div>
            <span className={['checking', 'completing'].includes(stage) ? 'text-green-600' : 'text-gray-500'}>
              Drug Interaction Check
            </span>
          </div>
          
          <div className="flex items-center text-sm">
            <div className={`w-4 h-4 rounded-full mr-3 ${
              stage === 'completing' 
                ? 'bg-green-500' 
                : ['scanning', 'analyzing', 'checking'].includes(stage) 
                ? 'bg-primary-500 animate-pulse' 
                : 'bg-gray-300'
            }`}>
              {stage === 'completing' && (
                <CheckCircle className="w-4 h-4 text-white" />
              )}
            </div>
            <span className={stage === 'completing' ? 'text-green-600' : 'text-gray-500'}>
              Generate Safety Report
            </span>
          </div>
        </div>

        {/* Powered by AI badge */}
        <div className="mt-6 inline-flex items-center px-3 py-1 rounded-full bg-primary-100 text-primary-700 text-xs font-semibold">
          <Brain className="w-3 h-3 mr-1" />
          Powered by Groq Llama 3.3-70B
        </div>
      </div>
    </div>
  );
};

export default AnalyzingAnimation;
