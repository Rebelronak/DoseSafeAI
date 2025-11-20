import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMetrics } from '../contexts/MetricsContext';
import { 
  History,
  Calendar,
  FileImage,
  User,
  AlertTriangle,
  CheckCircle,
  Eye,
  Trash2,
  Pill,
  Clock,
  Search,
  Filter
} from 'lucide-react';

const PreviousScansPage = () => {
  const [scanHistory, setScanHistory] = useState([]);
  const [filteredScans, setFilteredScans] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all'); // 'all', 'image', 'manual'
  const [filterRisk, setFilterRisk] = useState('all'); // 'all', 'low', 'moderate', 'high'
  const { metrics, refreshMetrics } = useMetrics();
  const navigate = useNavigate();

  // Load scan history on component mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('scan_history');
    if (savedHistory) {
      try {
        const history = JSON.parse(savedHistory);
        setScanHistory(history);
        setFilteredScans(history);
      } catch (error) {
        console.error('Error parsing scan history:', error);
        setScanHistory([]);
        setFilteredScans([]);
      }
    }
  }, []);

  // Filter scans based on search and filters
  useEffect(() => {
    let filtered = [...scanHistory];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(scan => 
        scan.medications?.some(med => 
          med.name?.toLowerCase().includes(searchTerm.toLowerCase())
        ) ||
        scan.patientInfo?.disease?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        scan.fileName?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Type filter
    if (filterType !== 'all') {
      filtered = filtered.filter(scan => scan.type === filterType);
    }

    // Risk filter
    if (filterRisk !== 'all') {
      filtered = filtered.filter(scan => scan.riskLevel === filterRisk);
    }

    // Sort by timestamp (newest first)
    filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    setFilteredScans(filtered);
  }, [scanHistory, searchTerm, filterType, filterRisk]);

  const handleViewScan = (scan) => {
    // Save the selected scan as the latest result
    localStorage.setItem('latest_scan_result', JSON.stringify(scan));
    navigate('/results');
  };

  const handleDeleteScan = (scanId) => {
    if (window.confirm('Are you sure you want to delete this scan?')) {
      const updatedHistory = scanHistory.filter(scan => scan.id !== scanId);
      setScanHistory(updatedHistory);
      localStorage.setItem('scan_history', JSON.stringify(updatedHistory));
      // Refresh metrics to reflect the updated scan history
      refreshMetrics();
    }
  };

  const getRiskLevelColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'high':
      case 'critical':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'moderate':
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
      default:
        return 'bg-green-100 text-green-800 border-green-200';
    }
  };

  const getRiskIcon = (level) => {
    switch (level?.toLowerCase()) {
      case 'high':
      case 'critical':
        return <AlertTriangle className="w-4 h-4 text-red-600" />;
      case 'moderate':
      case 'medium':
        return <AlertTriangle className="w-4 h-4 text-yellow-600" />;
      case 'low':
      default:
        return <CheckCircle className="w-4 h-4 text-green-600" />;
    }
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return `Today at ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    } else if (diffDays === 1) {
      return `Yesterday at ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="text-center mb-12 animate-slide-down">
        <div className="flex items-center justify-center gap-4 mb-6">
          <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center shadow-lg">
            <History className="w-8 h-8 text-white" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Scan History</h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          View and manage all your previous prescription analyses and safety reports
        </p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 mb-8 animate-slide-up">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Search */}
          <div className="flex-1 relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="h-6 w-6 text-gray-400" />
            </div>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-4 border-2 border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 text-gray-900 placeholder-gray-500"
              placeholder="Search by medication name, condition, or filename..."
            />
          </div>

          {/* Type Filter */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gray-100 rounded-xl flex items-center justify-center">
              <Filter className="w-5 h-5 text-gray-600" />
            </div>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-4 py-4 border-2 border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 text-gray-900 min-w-0"
            >
              <option value="all">All Types</option>
              <option value="image">Image Scans</option>
              <option value="manual">Manual Entry</option>
            </select>
          </div>

          {/* Risk Filter */}
          <select
            value={filterRisk}
            onChange={(e) => setFilterRisk(e.target.value)}
            className="px-4 py-4 border-2 border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 text-gray-900 min-w-0"
          >
            <option value="all">All Risk Levels</option>
            <option value="low">Low Risk</option>
            <option value="moderate">Moderate Risk</option>
            <option value="high">High Risk</option>
          </select>
        </div>
      </div>

      {/* Scan History List */}
      {filteredScans.length === 0 ? (
        <div className="text-center py-20">
          {scanHistory.length === 0 ? (
            <div className="animate-fade-in">
              <div className="w-24 h-24 bg-gradient-primary rounded-3xl flex items-center justify-center mx-auto mb-8">
                <History className="w-12 h-12 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                No Scans Yet
              </h3>
              <p className="text-gray-600 mb-8 max-w-md mx-auto text-lg">
                Start by scanning your first prescription to see your medication analysis history here.
              </p>
              <button
                onClick={() => navigate('/scan')}
                className="btn bg-gradient-primary hover:shadow-xl text-white px-8 py-4 rounded-2xl transform hover:scale-105 transition-all duration-200"
              >
                <Pill className="w-5 h-5 mr-2" />
                Scan Your First Prescription
              </button>
            </div>
          ) : (
            <div className="animate-fade-in">
              <div className="w-24 h-24 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto mb-8">
                <Search className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                No Results Found
              </h3>
              <p className="text-gray-600 mb-8 text-lg">
                Try adjusting your search terms or filters to find what you're looking for.
              </p>
              <button
                onClick={() => {
                  setSearchTerm('');
                  setFilterType('all');
                  setFilterRisk('all');
                }}
                className="btn bg-white border-2 border-gray-300 text-gray-700 hover:bg-gray-50 px-6 py-3 rounded-2xl"
              >
                Clear Filters
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-6">
          {filteredScans.map((scan, index) => (
            <div
              key={scan.id}
              className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 hover:shadow-2xl transition-all duration-300 transform hover:scale-[1.02] animate-fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
                {/* Left Side - Scan Info */}
                <div className="flex items-center gap-6 flex-1 min-w-0">
                  {/* Icon */}
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-2xl flex items-center justify-center flex-shrink-0">
                    {scan.type === 'image' ? (
                      <FileImage className="w-8 h-8 text-blue-600" />
                    ) : (
                      <User className="w-8 h-8 text-blue-600" />
                    )}
                  </div>

                  {/* Details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-center gap-4 mb-3">
                      <h3 className="text-xl font-bold text-gray-900 truncate">
                        {scan.type === 'image' 
                          ? (scan.fileName || 'Image Scan')
                          : `Manual Entry - ${scan.medicationCount || scan.medications?.length || 0} medication(s)`
                        }
                      </h3>
                      <div className={`px-4 py-2 rounded-2xl border-2 font-bold text-sm flex items-center gap-2 ${getRiskLevelColor(scan.riskLevel)}`}>
                        {getRiskIcon(scan.riskLevel)}
                        {scan.riskLevel?.charAt(0).toUpperCase() + scan.riskLevel?.slice(1) || 'Low'} Risk
                      </div>
                    </div>
                    
                    <div className="flex flex-wrap items-center gap-6 text-sm text-gray-600 mb-4">
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4" />
                        <span className="font-medium">{formatDate(scan.timestamp)}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Pill className="w-4 h-4" />
                        <span className="font-medium">{scan.medications?.length || 0} medication(s)</span>
                      </div>
                      {scan.interactions && scan.interactions.length > 0 && (
                        <div className="flex items-center gap-2 text-red-600">
                          <AlertTriangle className="w-4 h-4" />
                          <span className="font-medium">{scan.interactions.length} interaction(s)</span>
                        </div>
                      )}
                    </div>

                    {/* Medications Preview */}
                    {scan.medications && scan.medications.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {scan.medications.slice(0, 3).map((med, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-xl"
                          >
                            {med.name}
                          </span>
                        ))}
                        {scan.medications.length > 3 && (
                          <span className="px-3 py-1 bg-gray-100 text-gray-600 text-sm font-medium rounded-xl">
                            +{scan.medications.length - 3} more
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Right Side - Actions */}
                <div className="flex items-center gap-4 flex-shrink-0">
                  <button
                    onClick={() => handleViewScan(scan)}
                    className="btn bg-gradient-primary hover:shadow-lg text-white px-6 py-3 rounded-2xl transition-all duration-200 transform hover:scale-105"
                    title="View Details"
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    View Details
                  </button>
                  <button
                    onClick={() => handleDeleteScan(scan.id)}
                    className="btn bg-white border-2 border-red-200 text-red-600 hover:bg-red-50 hover:border-red-300 px-4 py-3 rounded-2xl transition-all duration-200 transform hover:scale-105"
                    title="Delete Scan"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Summary Stats */}
      {scanHistory.length > 0 && (
        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 text-center animate-slide-up">
            <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <History className="w-8 h-8 text-blue-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900 mb-2">
              {metrics.prescriptions}
            </p>
            <p className="text-gray-600 font-medium">Total Scans</p>
          </div>

          <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 text-center animate-slide-up">
            <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Pill className="w-8 h-8 text-green-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900 mb-2">
              {metrics.medications}
            </p>
            <p className="text-gray-600 font-medium">Medications Analyzed</p>
          </div>

          <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 text-center animate-slide-up">
            <div className="w-16 h-16 bg-red-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <AlertTriangle className="w-8 h-8 text-red-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900 mb-2">
              {metrics.interactions}
            </p>
            <p className="text-gray-600 font-medium">Interactions Found</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default PreviousScansPage;
