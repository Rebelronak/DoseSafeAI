import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  Scan, 
  Shield, 
  CheckCircle,
  Users,
  FileText,
  History,
  ArrowRight,
  Sparkles
} from 'lucide-react';

const HomePage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-4">
      <div className="max-w-5xl mx-auto">
        
        {/* Main Container - Everything in One Box */}
        <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12 border border-gray-100">
          
          {/* Welcome Header */}
          <div className="text-center mb-10">
            <div className="flex items-center justify-center mb-6">
              <div className="p-4 bg-gradient-to-r from-primary-500 to-orange-500 rounded-2xl shadow-lg">
                <Shield className="h-10 w-10 text-white" />
              </div>
              <Sparkles className="h-6 w-6 text-yellow-400 ml-2 animate-pulse" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary-600 to-orange-600 bg-clip-text text-transparent mb-3">
              Welcome, {user?.name || 'Ronak'}!
            </h1>
            <p className="text-xl text-gray-600 font-medium">
              Your AI-powered prescription safety guardian
            </p>
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
            
            {/* Left - Scan Section */}
            <div className="bg-gradient-to-br from-primary-50 to-primary-100 rounded-2xl p-8 border-2 border-primary-200 hover:border-primary-300 transition-all duration-300 hover:shadow-lg">
              <div className="text-center">
                <div className="p-6 bg-gradient-to-r from-primary-500 to-orange-500 rounded-2xl w-24 h-24 mx-auto mb-6 flex items-center justify-center shadow-lg transform hover:scale-105 transition-transform duration-300">
                  <Scan className="h-12 w-12 text-white" />
                </div>
                <h2 className="text-3xl font-bold text-gray-800 mb-4">Scan Prescription</h2>
                <p className="text-gray-700 text-lg mb-8 leading-relaxed">
                  Upload your prescription or enter details manually for instant AI-powered safety analysis
                </p>
                <button
                  onClick={() => navigate('/scan')}
                  className="bg-gradient-to-r from-primary-500 to-orange-500 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 w-full flex items-center justify-center gap-2"
                >
                  Start Scanning <ArrowRight className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Right - Safety Status */}
            <div className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-2xl p-8 border-2 border-green-200">
              <div className="text-center mb-8">
                <div className="p-6 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl w-24 h-24 mx-auto mb-6 flex items-center justify-center shadow-lg">
                  <CheckCircle className="h-12 w-12 text-white" />
                </div>
                <h2 className="text-3xl font-bold text-gray-800">Safety Dashboard</h2>
              </div>
              
              {/* Stats Cards */}
              <div className="space-y-4">
                <div className="bg-white/80 backdrop-blur-sm p-5 rounded-xl shadow-md border border-green-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-green-100 rounded-lg">
                        <CheckCircle className="h-6 w-6 text-green-600" />
                      </div>
                      <span className="font-bold text-gray-800 text-lg">Prescriptions Checked</span>
                    </div>
                    <span className="text-3xl font-bold text-green-600">12</span>
                  </div>
                </div>
                
                <div className="bg-white/80 backdrop-blur-sm p-5 rounded-xl shadow-md border border-blue-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-blue-100 rounded-lg">
                        <Users className="h-6 w-6 text-blue-600" />
                      </div>
                      <span className="font-bold text-gray-800 text-lg">People Safe</span>
                    </div>
                    <span className="text-3xl font-bold text-blue-600">5</span>
                  </div>
                </div>
                
                <div className="bg-white/80 backdrop-blur-sm p-5 rounded-xl shadow-md border border-orange-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-orange-100 rounded-lg">
                        <FileText className="h-6 w-6 text-orange-600" />
                      </div>
                      <span className="font-bold text-gray-800 text-lg">Safety Reports</span>
                    </div>
                    <span className="text-3xl font-bold text-orange-600">8</span>
                  </div>
                </div>
              </div>
              
              <button
                onClick={() => navigate('/history')}
                className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-3 rounded-xl font-bold shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300 w-full mt-6 flex items-center justify-center gap-2"
              >
                <History className="h-5 w-5" />
                View Complete History
              </button>
            </div>
          </div>

          {/* Bottom Action - History Button */}
          <div className="text-center">
            <button
              onClick={() => navigate('/history')}
              className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-12 py-4 rounded-2xl font-bold text-xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300 inline-flex items-center gap-3"
            >
              <History className="h-6 w-6" />
              View All Previous Scans
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
