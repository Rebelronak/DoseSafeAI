import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMetrics } from '../contexts/MetricsContext';
import { 
  Calendar,
  Clock,
  FileImage,
  User,
  Pill,
  AlertTriangle,
  CheckCircle,
  ChevronDown,
  ChevronUp,
  MessageCircle,
  Scan,
  Shield,
  Info,
  ExternalLink
} from 'lucide-react';

const ResultsPage = () => {
  const [scanResult, setScanResult] = useState(null);
  const [expandedMedications, setExpandedMedications] = useState(new Set());
  const [expandedInteractions, setExpandedInteractions] = useState(new Set());
  const { incrementInteractions, incrementPeopleSaved } = useMetrics();
  const navigate = useNavigate();

  useEffect(() => {
    // Load scan result from localStorage
    const savedResult = localStorage.getItem('latest_scan_result');
    if (savedResult) {
      try {
        const result = JSON.parse(savedResult);
        setScanResult(result);
        
        // Update interaction count if there are interactions or warnings
        const totalWarnings = (result.interactions?.length || 0) + 
                             (result.harmfulCombinations?.length || 0) + 
                             (result.contraindications?.length || 0) + 
                             (result.ageWarnings?.length || 0);
        if (totalWarnings > 0) {
          incrementInteractions(totalWarnings);
          // Only increment people saved if there are actually harmful findings
          incrementPeopleSaved();
        }
      } catch (error) {
        console.error('Error parsing scan result:', error);
        navigate('/scan');
      }
    } else {
      // Redirect to scan if no result found
      navigate('/scan');
    }
  }, [navigate, incrementInteractions]);

  const toggleMedicationExpansion = (index) => {
    const newExpanded = new Set(expandedMedications);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedMedications(newExpanded);
  };

  const toggleInteractionExpansion = (index) => {
    const newExpanded = new Set(expandedInteractions);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedInteractions(newExpanded);
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

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
      case 'severe':
        return 'text-red-600 bg-red-50';
      case 'moderate':
        return 'text-yellow-600 bg-yellow-50';
      case 'low':
      case 'mild':
        return 'text-green-600 bg-green-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const handleAskAI = () => {
    // Save current scan context for chatbot
    localStorage.setItem('chatbot_context', JSON.stringify({
      medications: scanResult?.medications || [],
      interactions: scanResult?.interactions || [],
      harmfulCombinations: scanResult?.harmfulCombinations || [],
      contraindications: scanResult?.contraindications || [],
      ageWarnings: scanResult?.ageWarnings || [],
      clinicalSummary: scanResult?.clinicalSummary || '',
      riskLevel: scanResult?.riskLevel
    }));
    navigate('/chatbot');
  };

  const handleNewScan = () => {
    // Clear current result
    localStorage.removeItem('latest_scan_result');
    navigate('/scan');
  };

  if (!scanResult) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading scan results...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="text-center mb-12 animate-slide-down">
        <div className="flex items-center justify-center gap-4 mb-6">
          <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center shadow-lg">
            <Shield className="w-8 h-8 text-white" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Analysis Complete
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Your comprehensive medication safety analysis is ready for review
        </p>
      </div>

      {/* Scan Summary */}
      <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 mb-8 animate-slide-up">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-6">
          <div className="flex flex-wrap items-center gap-6">
            <div className="flex items-center gap-3 text-gray-600">
              <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                <Calendar className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Scan Date</p>
                <p className="font-semibold">{new Date(scanResult.timestamp).toLocaleDateString()}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 text-gray-600">
              <div className="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center">
                <Clock className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Time</p>
                <p className="font-semibold">{new Date(scanResult.timestamp).toLocaleTimeString()}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 text-gray-600">
              <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
                {scanResult.type === 'image' ? (
                  <FileImage className="w-5 h-5 text-purple-600" />
                ) : (
                  <User className="w-5 h-5 text-purple-600" />
                )}
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Method</p>
                <p className="font-semibold">{scanResult.type === 'image' ? 'Image Scan' : 'Manual Entry'}</p>
              </div>
            </div>
          </div>
          
          <div className={`px-6 py-3 rounded-2xl border-2 font-bold text-lg ${getRiskLevelColor(scanResult.riskLevel)} shadow-lg`}>
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5" />
              <span>Risk Level: {scanResult.riskLevel?.charAt(0).toUpperCase() + scanResult.riskLevel?.slice(1) || 'Low'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Left Column - Medications and Comprehensive Analysis */}
        <div className="lg:col-span-2 space-y-8">
          {/* Medications Section */}
          <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 animate-slide-up">
            <div className="flex items-center gap-4 mb-8">
              <div className="w-12 h-12 bg-green-100 rounded-2xl flex items-center justify-center">
                <Pill className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Medications Found</h2>
                <p className="text-gray-600">{scanResult.medications?.length || 0} medication(s) identified</p>
              </div>
            </div>
            
            <div className="space-y-4">
              {scanResult.medications?.map((medication, index) => (
                <div key={index} className="border border-gray-200 rounded-2xl overflow-hidden bg-gradient-to-r from-gray-50 to-blue-50">
                  <button
                    onClick={() => toggleMedicationExpansion(index)}
                    className="w-full p-6 text-left hover:bg-gradient-to-r hover:from-gray-100 hover:to-blue-100 transition-all duration-300"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 bg-white rounded-xl shadow-sm flex items-center justify-center">
                          <Pill className="w-5 h-5 text-primary-600" />
                        </div>
                        <div>
                          <h3 className="text-lg font-bold text-gray-900">{medication.name}</h3>
                          <p className="text-sm text-gray-600">
                            {medication.dosage || medication.strength} 
                            {medication.frequency && ` • ${medication.frequency}`}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {medication.warnings && medication.warnings.length > 0 && (
                          <div className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-lg text-xs font-medium">
                            {medication.warnings.length} Warning{medication.warnings.length !== 1 ? 's' : ''}
                          </div>
                        )}
                        {expandedMedications.has(index) ? (
                          <ChevronUp className="w-6 h-6 text-gray-400" />
                        ) : (
                          <ChevronDown className="w-6 h-6 text-gray-400" />
                        )}
                      </div>
                    </div>
                  </button>
                  
                  {expandedMedications.has(index) && (
                    <div className="px-6 pb-6 bg-white border-t border-gray-100">
                      <div className="pt-6 space-y-4">
                        {medication.description && (
                          <div className="bg-blue-50 rounded-xl p-4">
                            <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                              <Info className="w-4 h-4 text-blue-600" />
                              Description
                            </h4>
                            <p className="text-sm text-gray-700">{medication.description}</p>
                          </div>
                        )}
                        
                        {medication.warnings && medication.warnings.length > 0 && (
                          <div className="bg-yellow-50 rounded-xl p-4">
                            <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                              <AlertTriangle className="w-4 h-4 text-yellow-600" />
                              Warnings
                            </h4>
                            <ul className="text-sm text-gray-700 space-y-2">
                              {medication.warnings.map((warning, idx) => (
                                <li key={idx} className="flex items-start gap-3">
                                  <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2 flex-shrink-0"></div>
                                  <span>{warning}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        
                        {medication.sideEffects && medication.sideEffects.length > 0 && (
                          <div className="bg-gray-50 rounded-xl p-4">
                            <h4 className="font-semibold text-gray-900 mb-3">Common Side Effects</h4>
                            <ul className="text-sm text-gray-700 space-y-2">
                              {medication.sideEffects.map((effect, idx) => (
                                <li key={idx} className="flex items-start gap-3">
                                  <div className="w-2 h-2 bg-gray-400 rounded-full mt-2 flex-shrink-0"></div>
                                  <span>{effect}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )) || (
                <div className="text-center py-12">
                  <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Pill className="w-8 h-8 text-gray-400" />
                  </div>
                  <p className="text-gray-500 text-lg">No medications found</p>
                </div>
              )}
            </div>
          </div>

          {/* Drug Interactions Section */}
          {scanResult.interactions && scanResult.interactions.length > 0 && (
            <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 animate-slide-up">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 bg-red-100 rounded-2xl flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Drug Interactions</h2>
                  <p className="text-red-600 font-medium">{scanResult.interactions.length} interaction{scanResult.interactions.length !== 1 ? 's' : ''} detected</p>
                </div>
              </div>
              
              <div className="space-y-4">
                {scanResult.interactions.map((interaction, index) => (
                  <div key={index} className="border-2 border-red-200 rounded-2xl overflow-hidden bg-gradient-to-r from-red-50 to-orange-50">
                    <button
                      onClick={() => toggleInteractionExpansion(index)}
                      className="w-full p-6 text-left hover:bg-gradient-to-r hover:from-red-100 hover:to-orange-100 transition-all duration-300"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <div className="w-10 h-10 bg-white rounded-xl shadow-sm flex items-center justify-center">
                            <AlertTriangle className="w-5 h-5 text-red-600" />
                          </div>
                          <div>
                            <div className="flex items-center gap-3 mb-2">
                              <span className={`px-3 py-1 text-xs font-bold rounded-full ${getSeverityColor(interaction.severity)}`}>
                                {interaction.severity?.toUpperCase() || 'MODERATE'} RISK
                              </span>
                            </div>
                            <h3 className="text-lg font-bold text-gray-900">
                              {interaction.drugs?.join(' + ') || interaction.medications?.join(' + ') || 'Drug Interaction'}
                            </h3>
                            <p className="text-sm text-gray-600 line-clamp-2">
                              {interaction.mechanism || interaction.description || interaction.summary}
                            </p>
                          </div>
                        </div>
                        {expandedInteractions.has(index) ? (
                          <ChevronUp className="w-6 h-6 text-gray-400" />
                        ) : (
                          <ChevronDown className="w-6 h-6 text-gray-400" />
                        )}
                      </div>
                    </button>
                    
                    {expandedInteractions.has(index) && (
                      <div className="px-6 pb-6 bg-white border-t-2 border-red-200">
                        <div className="pt-6 space-y-4">
                          {interaction.mechanism && (
                            <div className="bg-red-50 rounded-xl p-4">
                              <h4 className="font-semibold text-gray-900 mb-3">Interaction Mechanism</h4>
                              <p className="text-sm text-gray-700">{interaction.mechanism}</p>
                            </div>
                          )}
                          
                          {interaction.clinical_effects && (
                            <div className="bg-orange-50 rounded-xl p-4">
                              <h4 className="font-semibold text-gray-900 mb-3">Clinical Effects</h4>
                              <p className="text-sm text-gray-700">{interaction.clinical_effects}</p>
                            </div>
                          )}
                          
                          {interaction.recommendation && (
                            <div className="bg-green-50 rounded-xl p-4">
                              <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                                <CheckCircle className="w-4 h-4 text-green-600" />
                                Recommendation
                              </h4>
                              <p className="text-sm text-gray-700">{interaction.recommendation}</p>
                            </div>
                          )}
                          
                          {interaction.monitoring && (
                            <div className="bg-blue-50 rounded-xl p-4">
                              <h4 className="font-semibold text-gray-900 mb-3">Monitoring Required</h4>
                              <p className="text-sm text-gray-700">{interaction.monitoring}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Harmful Combinations Section */}
          {scanResult.harmfulCombinations && scanResult.harmfulCombinations.length > 0 && (
            <div className="bg-white rounded-3xl shadow-xl border border-red-300 p-8 animate-slide-up">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 bg-red-100 rounded-2xl flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">⚠️ Harmful Drug Combinations</h2>
                  <p className="text-red-600 font-medium">{scanResult.harmfulCombinations.length} dangerous combination{scanResult.harmfulCombinations.length !== 1 ? 's' : ''} identified</p>
                </div>
              </div>
              
              <div className="space-y-4">
                {scanResult.harmfulCombinations.map((combination, index) => (
                  <div key={index} className="border-2 border-red-300 rounded-2xl p-6 bg-gradient-to-r from-red-100 to-red-50">
                    <div className="flex items-start gap-4">
                      <div className="w-10 h-10 bg-red-200 rounded-xl shadow-sm flex items-center justify-center flex-shrink-0">
                        <AlertTriangle className="w-5 h-5 text-red-700" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                          <span className={`px-3 py-1 text-xs font-bold rounded-full ${
                            combination.danger_level === 'high' ? 'bg-red-200 text-red-800' :
                            combination.danger_level === 'moderate' ? 'bg-orange-200 text-orange-800' :
                            'bg-yellow-200 text-yellow-800'
                          }`}>
                            {combination.danger_level?.toUpperCase() || 'HIGH'} DANGER
                          </span>
                        </div>
                        <h3 className="text-lg font-bold text-gray-900 mb-2">
                          {combination.medications?.join(' + ') || 'Harmful Combination'}
                        </h3>
                        <p className="text-sm text-gray-700">
                          <strong>Potential Harm:</strong> {combination.potential_harm}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Contraindications Section */}
          {scanResult.contraindications && scanResult.contraindications.length > 0 && (
            <div className="bg-white rounded-3xl shadow-xl border border-orange-300 p-8 animate-slide-up">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 bg-orange-100 rounded-2xl flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-orange-600" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">🚫 Contraindications</h2>
                  <p className="text-orange-600 font-medium">{scanResult.contraindications.length} contraindication{scanResult.contraindications.length !== 1 ? 's' : ''} found</p>
                </div>
              </div>
              
              <div className="space-y-4">
                {scanResult.contraindications.map((contraindication, index) => (
                  <div key={index} className="border-2 border-orange-200 rounded-2xl p-6 bg-gradient-to-r from-orange-50 to-yellow-50">
                    <div className="flex items-start gap-4">
                      <div className="w-10 h-10 bg-orange-200 rounded-xl shadow-sm flex items-center justify-center flex-shrink-0">
                        <AlertTriangle className="w-5 h-5 text-orange-700" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-bold text-gray-900 mb-2">
                          {contraindication.medication}
                        </h3>
                        <p className="text-sm text-gray-700 mb-2">
                          <strong>Contraindication:</strong> {contraindication.contraindication}
                        </p>
                        <p className="text-sm text-gray-600">
                          <strong>Reason:</strong> {contraindication.reason}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Age-Specific Warnings Section */}
          {scanResult.ageWarnings && scanResult.ageWarnings.length > 0 && (
            <div className="bg-white rounded-3xl shadow-xl border border-yellow-300 p-8 animate-slide-up">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 bg-yellow-100 rounded-2xl flex items-center justify-center">
                  <User className="w-6 h-6 text-yellow-600" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">👴 Age-Specific Warnings</h2>
                  <p className="text-yellow-600 font-medium">{scanResult.ageWarnings.length} age-related concern{scanResult.ageWarnings.length !== 1 ? 's' : ''}</p>
                </div>
              </div>
              
              <div className="space-y-4">
                {scanResult.ageWarnings.map((warning, index) => (
                  <div key={index} className="border-2 border-yellow-200 rounded-2xl p-6 bg-gradient-to-r from-yellow-50 to-amber-50">
                    <div className="flex items-start gap-4">
                      <div className="w-10 h-10 bg-yellow-200 rounded-xl shadow-sm flex items-center justify-center flex-shrink-0">
                        <User className="w-5 h-5 text-yellow-700" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-bold text-gray-900 mb-2">
                          {warning.medication}
                        </h3>
                        <p className="text-sm text-gray-700 mb-2">
                          <strong>Warning:</strong> {warning.warning}
                        </p>
                        <p className="text-sm text-gray-600">
                          <strong>Recommendation:</strong> {warning.recommendation}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* AI Clinical Summary Section with Enhanced Display */}
          {scanResult.clinicalSummary && (
            <div className="bg-white rounded-3xl shadow-xl border border-blue-300 p-8 animate-slide-up">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center">
                  <MessageCircle className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">🤖 AI Clinical Summary</h2>
                  <p className="text-blue-600 font-medium">Comprehensive analysis by Llama 3.3-70B</p>
                </div>
              </div>
              
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border-2 border-blue-200">
                <div className="prose prose-blue max-w-none">
                  <div className="text-gray-700 leading-relaxed whitespace-pre-line text-base">
                    {scanResult.clinicalSummary}
                  </div>
                </div>
                
                {/* Additional Clinical Insights */}
                {scanResult.keyInsights && (
                  <div className="mt-6 p-4 bg-blue-100 rounded-xl">
                    <h4 className="font-semibold text-blue-800 mb-2">💡 Key Clinical Insights:</h4>
                    <ul className="list-disc list-inside text-blue-700 space-y-1">
                      {scanResult.keyInsights.map((insight, index) => (
                        <li key={index}>{insight}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {/* Risk Assessment Display */}
                {scanResult.riskLevel && (
                  <div className="mt-6 flex items-center gap-3">
                    <span className="text-sm font-medium text-gray-600">Risk Assessment:</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      scanResult.riskLevel.toLowerCase() === 'high' || scanResult.riskLevel.toLowerCase() === 'severe' 
                        ? 'bg-red-100 text-red-800' 
                        : scanResult.riskLevel.toLowerCase() === 'moderate' 
                        ? 'bg-yellow-100 text-yellow-800' 
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {scanResult.riskLevel}
                    </span>
                  </div>
                )}
              </div>
              
              {/* Action Buttons */}
              <div className="mt-6 flex gap-3">
                <button
                  onClick={handleAskAI}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-xl transition-colors flex items-center justify-center gap-2"
                >
                  <MessageCircle className="w-4 h-4" />
                  Ask AI for Details
                </button>
                <button
                  onClick={() => window.print()}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-3 px-4 rounded-xl transition-colors"
                >
                  Print Report
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Right Column - Actions & Summary */}
        <div className="space-y-8">
          {/* Quick Actions */}
          <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 animate-slide-up">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
                <MessageCircle className="w-5 h-5 text-purple-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">Quick Actions</h3>
            </div>
            <div className="space-y-4">
              <button
                onClick={handleAskAI}
                className="w-full bg-gradient-primary hover:shadow-xl text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-3"
              >
                <MessageCircle className="w-5 h-5" />
                Ask AI Assistant
              </button>
              <button
                onClick={handleNewScan}
                className="w-full bg-white border-2 border-primary-200 text-primary-600 hover:bg-primary-50 font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-3"
              >
                <Scan className="w-5 h-5" />
                Scan Another Prescription
              </button>
            </div>
          </div>

          {/* Summary Stats */}
          <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 animate-slide-up">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                <Shield className="w-5 h-5 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">Analysis Summary</h3>
            </div>
            <div className="space-y-6">
              <div className="flex items-center justify-between p-4 bg-green-50 rounded-xl">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                    <Pill className="w-4 h-4 text-green-600" />
                  </div>
                  <span className="text-gray-700 font-medium">Medications Analyzed</span>
                </div>
                <span className="text-2xl font-bold text-green-600">{scanResult.medications?.length || 0}</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-red-50 rounded-xl">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                    <AlertTriangle className="w-4 h-4 text-red-600" />
                  </div>
                  <span className="text-gray-700 font-medium">Drug Interactions</span>
                </div>
                <span className="text-2xl font-bold text-red-600">
                  {scanResult.interactions?.length || 0}
                </span>
              </div>
              
              {scanResult.harmfulCombinations && scanResult.harmfulCombinations.length > 0 && (
                <div className="flex items-center justify-between p-4 bg-red-100 rounded-xl border-2 border-red-200">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-red-200 rounded-lg flex items-center justify-center">
                      <AlertTriangle className="w-4 h-4 text-red-700" />
                    </div>
                    <span className="text-gray-700 font-medium">Harmful Combinations</span>
                  </div>
                  <span className="text-2xl font-bold text-red-700">
                    {scanResult.harmfulCombinations.length}
                  </span>
                </div>
              )}
              
              {scanResult.contraindications && scanResult.contraindications.length > 0 && (
                <div className="flex items-center justify-between p-4 bg-orange-50 rounded-xl">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                      <AlertTriangle className="w-4 h-4 text-orange-600" />
                    </div>
                    <span className="text-gray-700 font-medium">Contraindications</span>
                  </div>
                  <span className="text-2xl font-bold text-orange-600">
                    {scanResult.contraindications.length}
                  </span>
                </div>
              )}
              
              {scanResult.ageWarnings && scanResult.ageWarnings.length > 0 && (
                <div className="flex items-center justify-between p-4 bg-yellow-50 rounded-xl">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                      <User className="w-4 h-4 text-yellow-600" />
                    </div>
                    <span className="text-gray-700 font-medium">Age Warnings</span>
                  </div>
                  <span className="text-2xl font-bold text-yellow-600">
                    {scanResult.ageWarnings.length}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Medical Disclaimer */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-3xl p-8 animate-slide-up">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center flex-shrink-0">
                <Info className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-bold text-blue-900 mb-3 text-lg">Medical Disclaimer</h3>
                <p className="text-sm text-blue-800 leading-relaxed mb-4">
                  This analysis is for informational purposes only and should not replace professional medical advice. 
                  Always consult with qualified healthcare professionals before making changes to your medication regimen.
                </p>
                <button className="text-sm text-blue-700 hover:text-blue-800 font-semibold flex items-center gap-2 transition-colors duration-200">
                  <span>Learn More</span>
                  <ExternalLink className="w-3 h-3" />
                </button>
              </div>
            </div>
          </div>

          {/* Success Badge */}
          {(!scanResult.interactions || scanResult.interactions.length === 0) && (
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-3xl p-8 text-center animate-slide-up">
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="font-bold text-green-900 mb-2 text-lg">All Clear!</h3>
              <p className="text-sm text-green-800">
                No dangerous interactions detected in your current medications.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
