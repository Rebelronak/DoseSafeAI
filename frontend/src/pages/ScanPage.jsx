import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMetrics } from '../contexts/MetricsContext';
import { scanService } from '../services/api';
import AnalyzingAnimation from '../components/AnalyzingAnimation';
import { 
  Upload, 
  Camera, 
  FileImage, 
  Plus, 
  Minus, 
  User, 
  Stethoscope,
  Loader,
  CheckCircle,
  AlertCircle,
  Pill
} from 'lucide-react';

const ScanPage = () => {
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' or 'manual'
  const [isLoading, setIsLoading] = useState(false);
  const [analyzingStage, setAnalyzingStage] = useState('scanning'); // 'scanning', 'analyzing', 'checking', 'completing'
  const [error, setError] = useState('');
  const { incrementPrescriptions } = useMetrics();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  // Image Upload State
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [dragActive, setDragActive] = useState(false);

  // Manual Entry State
  const [patientInfo, setPatientInfo] = useState({
    age: '',
    disease: ''
  });
  
  const [medications, setMedications] = useState([{
    id: 1,
    name: '',
    dosageForm: 'tablet',
    strength: '',
    strengthUnit: 'mg',
    quantity: '',
    frequency: '',
    route: 'oral',
    duration: '',
    instructions: ''
  }]);

  const dosageForms = [
    'tablet', 'capsule', 'syrup', 'injection', 'cream', 'ointment', 
    'drops', 'spray', 'patch', 'inhaler', 'suppository'
  ];

  const strengthUnits = ['mg', 'g', 'ml', 'mcg', 'IU', '%'];
  const routes = ['oral', 'topical', 'injection', 'inhalation', 'rectal', 'vaginal'];

  // Common medications for autocomplete
  const commonMedications = [
    'Amoxicillin', 'Ibuprofen', 'Paracetamol', 'Aspirin', 'Metformin', 
    'Lisinopril', 'Simvastatin', 'Omeprazole', 'Amlodipine', 'Warfarin',
    'Prednisone', 'Furosemide', 'Atorvastatin', 'Losartan', 'Gabapentin'
  ];

  // File Upload Handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (file) => {
    if (!file) return;

    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];
    if (!validTypes.includes(file.type)) {
      setError('Please select a valid image file (JPG, PNG) or PDF');
      return;
    }

    // Validate file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return;
    }

    setSelectedFile(file);
    setError('');

    // Create preview for images
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => setPreviewUrl(e.target.result);
      reader.readAsDataURL(file);
    } else {
      setPreviewUrl('');
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  // Manual Entry Handlers
  const addMedication = () => {
    const newId = Math.max(...medications.map(m => m.id)) + 1;
    setMedications([...medications, {
      id: newId,
      name: '',
      dosageForm: 'tablet',
      strength: '',
      strengthUnit: 'mg',
      quantity: '',
      frequency: '',
      route: 'oral',
      duration: '',
      instructions: ''
    }]);
  };

  const removeMedication = (id) => {
    if (medications.length > 1) {
      setMedications(medications.filter(m => m.id !== id));
    }
  };

  const updateMedication = (id, field, value) => {
    setMedications(medications.map(med => 
      med.id === id ? { ...med, [field]: value } : med
    ));
  };

  // Form Submission
  const handleImageSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('Please select a file to upload');
      return;
    }

    if (!patientInfo.age || patientInfo.age < 1 || patientInfo.age > 120) {
      setError('Please enter a valid patient age (1-120 years) before uploading');
      return;
    }

    setIsLoading(true);
    setError('');
    setAnalyzingStage('scanning');

    try {
      console.log('🚀 Submitting image scan...', {
        fileName: selectedFile.name,
        patientAge: patientInfo.age,
        patientCondition: patientInfo.disease
      });

      // Progressive animation stages
      setTimeout(() => setAnalyzingStage('analyzing'), 1000);
      setTimeout(() => setAnalyzingStage('checking'), 3000);
      setTimeout(() => setAnalyzingStage('completing'), 5000);

      const result = await scanService.processImageScan(
        selectedFile, 
        patientInfo.age ? parseInt(patientInfo.age) : 30,
        patientInfo.disease || ''
      );
      
      console.log('✅ Image scan result:', result);
      
      // Save result to localStorage
      localStorage.setItem('latest_scan_result', JSON.stringify({
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        type: 'image',
        fileName: selectedFile.name,
        patientInfo: {
          age: patientInfo.age,
          disease: patientInfo.disease
        },
        ...result
      }));

      incrementPrescriptions();
      navigate('/results');
    } catch (err) {
      console.error('🚨 Image scan error:', err);
      setError(err.message || 'Failed to process image. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleManualSubmit = async (e) => {
    e.preventDefault();
    
    // Validate required fields
    const incompleteMeds = medications.filter(med => !med.name || !med.strength);
    if (incompleteMeds.length > 0) {
      setError('Please fill in medication name and strength for all medications');
      return;
    }

    if (!patientInfo.age || patientInfo.age < 1 || patientInfo.age > 120) {
      setError('Please enter a valid patient age (1-120 years) before submitting');
      return;
    }

    setIsLoading(true);
    setError('');
    setAnalyzingStage('analyzing');

    try {
      console.log('🚀 Submitting manual scan...', {
        medicationCount: medications.length,
        patientAge: patientInfo.age,
        patientCondition: patientInfo.disease
      });

      // Progressive animation stages for manual entry
      setTimeout(() => setAnalyzingStage('checking'), 1000);
      setTimeout(() => setAnalyzingStage('completing'), 2500);

      const result = await scanService.processManualScan(
        medications, 
        patientInfo.age ? parseInt(patientInfo.age) : 30,
        patientInfo.disease || ''
      );
      
      console.log('✅ Manual scan result:', result);
      
      // Save result to localStorage
      localStorage.setItem('latest_scan_result', JSON.stringify({
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        type: 'manual',
        patientInfo: {
          age: patientInfo.age,
          disease: patientInfo.disease
        },
        medicationCount: medications.length,
        originalMedications: medications,
        ...result
      }));

      incrementPrescriptions();
      navigate('/results');
    } catch (err) {
      console.error('🚨 Manual scan error:', err);
      setError(err.message || 'Failed to process medications. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Page Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Scan Prescription</h1>
        <p className="text-gray-600">Upload a photo of your prescription or enter details manually for analysis</p>
      </div>

      {/* Patient Information Section */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Patient Information</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Age *</label>
            <input
              type="number"
              value={patientInfo.age}
              onChange={(e) => setPatientInfo({...patientInfo, age: e.target.value})}
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
              placeholder="Enter age in years"
              min="0"
              max="150"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Disease/Condition (Optional)</label>
            <input
              type="text"
              value={patientInfo.disease}
              onChange={(e) => setPatientInfo({...patientInfo, disease: e.target.value})}
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
              placeholder="e.g., Hypertension, Diabetes"
            />
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex justify-center mb-8">
        <div className="bg-gray-100 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('upload')}
            className={`px-6 py-2 rounded-md font-medium transition-all duration-200 flex items-center gap-2 ${
              activeTab === 'upload'
                ? 'bg-white text-gray-900 shadow'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Camera className="w-4 h-4" />
            Upload Image
          </button>
          <button
            onClick={() => setActiveTab('manual')}
            className={`px-6 py-2 rounded-md font-medium transition-all duration-200 flex items-center gap-2 ${
              activeTab === 'manual'
                ? 'bg-white text-gray-900 shadow'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Pill className="w-4 h-4" />
            Manual Entry
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-700 flex items-center gap-3 animate-shake">
          <AlertCircle className="w-6 h-6 flex-shrink-0" />
          <span className="font-medium">{error}</span>
        </div>
      )}

      {/* Upload Image Tab */}
      {activeTab === 'upload' && (
        <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 animate-slide-up">
          <form onSubmit={handleImageSubmit} className="space-y-8">
            {/* Modern Upload Area */}
            <div
              className={`relative border-2 border-dashed rounded-3xl p-16 text-center transition-all duration-300 ${
                dragActive 
                  ? 'border-primary-400 bg-gradient-to-br from-primary-50 to-blue-50 scale-105' 
                  : selectedFile
                  ? 'border-green-300 bg-gradient-to-br from-green-50 to-emerald-50'
                  : 'border-gray-300 bg-gradient-to-br from-gray-50 to-blue-50 hover:border-primary-300 hover:bg-gradient-to-br hover:from-primary-50 hover:to-blue-100'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              {selectedFile ? (
                <div className="space-y-6">
                  <div className="flex justify-center">
                    {previewUrl ? (
                      <div className="relative">
                        <img 
                          src={previewUrl} 
                          alt="Preview" 
                          className="max-w-sm max-h-64 rounded-2xl shadow-lg border-2 border-white"
                        />
                        <div className="absolute -top-2 -right-2 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                          <CheckCircle className="w-5 h-5 text-white" />
                        </div>
                      </div>
                    ) : (
                      <div className="w-24 h-24 bg-gradient-to-br from-blue-100 to-green-100 rounded-3xl flex items-center justify-center">
                        <FileImage className="w-12 h-12 text-blue-600" />
                      </div>
                    )}
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-xl font-bold text-gray-900">{selectedFile.name}</h3>
                    <p className="text-sm text-gray-500">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB • Ready for analysis
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedFile(null);
                      setPreviewUrl('');
                      if (fileInputRef.current) fileInputRef.current.value = '';
                    }}
                    className="text-primary-600 hover:text-primary-700 font-semibold transition-colors duration-200 hover:bg-primary-50 px-4 py-2 rounded-lg"
                  >
                    Remove file
                  </button>
                </div>
              ) : (
                <div className="space-y-8 relative z-10">
                  <div className="w-24 h-24 bg-gradient-primary rounded-3xl flex items-center justify-center mx-auto shadow-lg animate-float">
                    <Upload className="w-12 h-12 text-white" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-3">
                      Drop your prescription here
                    </h3>
                    <p className="text-gray-600 mb-6 max-w-md mx-auto">
                      Supports JPG, PNG, and PDF files up to 5MB. Our AI will extract medication information with 95% accuracy.
                    </p>
                  </div>
                  
                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className="btn bg-gradient-primary hover:shadow-xl text-white px-6 py-3 rounded-xl transform hover:scale-105 transition-all duration-200"
                    >
                      <FileImage className="w-5 h-5 mr-2" />
                      Browse Files
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        alert('Camera functionality would be implemented here with device camera access');
                      }}
                      className="btn bg-white border-2 border-primary-200 text-primary-600 hover:bg-primary-50 px-6 py-3 rounded-xl transform hover:scale-105 transition-all duration-200"
                    >
                      <Camera className="w-5 h-5 mr-2" />
                      Take Photo
                    </button>
                  </div>
                </div>
              )}
            </div>

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*,.pdf"
              onChange={handleFileInputChange}
              className="hidden"
            />

            {/* Submit Button */}
            <div className="flex justify-center pt-6">
              <button
                type="submit"
                disabled={!selectedFile || isLoading}
                className="btn bg-gradient-primary hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-white px-12 py-4 text-lg rounded-xl transform hover:scale-105 transition-all duration-200 flex items-center gap-3"
              >
                {isLoading ? (
                  <>
                    <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Analyzing Prescription...</span>
                  </>
                ) : (
                  <>
                    <CheckCircle className="w-6 h-6" />
                    <span>Analyze Prescription</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Manual Entry Tab */}
      {activeTab === 'manual' && (
        <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8 animate-slide-up">
          <form onSubmit={handleManualSubmit} className="space-y-10">
            {/* Patient Information */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-3">
                <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Stethoscope className="w-5 h-5 text-blue-600" />
                </div>
                Patient Information
                <span className="text-sm font-normal text-gray-500">(Optional)</span>
              </h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-900">Age</label>
                  <input
                    type="number"
                    value={patientInfo.age}
                    onChange={(e) => setPatientInfo({...patientInfo, age: e.target.value})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                    placeholder="Enter patient age"
                    min="0"
                    max="150"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-900">Medical Condition</label>
                  <input
                    type="text"
                    value={patientInfo.disease}
                    onChange={(e) => setPatientInfo({...patientInfo, disease: e.target.value})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                    placeholder="e.g., Diabetes, Hypertension"
                  />
                </div>
              </div>
            </div>

            {/* Medications */}
            <div>
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-xl font-bold text-gray-900 flex items-center gap-3">
                  <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                    <Pill className="w-5 h-5 text-green-600" />
                  </div>
                  Medications
                  <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm font-medium">
                    {medications.length} {medications.length === 1 ? 'medication' : 'medications'}
                  </span>
                </h3>
                <button
                  type="button"
                  onClick={addMedication}
                  className="btn bg-gradient-primary hover:shadow-lg text-white px-4 py-2 rounded-xl transition-all duration-200 transform hover:scale-105"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Medication
                </button>
              </div>

              <div className="space-y-8">
                {medications.map((medication, index) => (
                  <div key={medication.id} className="bg-gradient-to-r from-gray-50 to-blue-50 border border-gray-200 rounded-2xl p-8 relative">
                    <div className="absolute top-4 left-4 w-8 h-8 bg-primary-500 text-white rounded-lg flex items-center justify-center text-sm font-bold">
                      {index + 1}
                    </div>
                    
                    <div className="flex items-center justify-between mb-6 pl-12">
                      <h4 className="text-lg font-semibold text-gray-900">Medication {index + 1}</h4>
                      {medications.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeMedication(medication.id)}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50 p-2 rounded-lg transition-colors duration-200"
                        >
                          <Minus className="w-5 h-5" />
                        </button>
                      )}
                    </div>

                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {/* Drug Name */}
                      <div className="lg:col-span-2 space-y-2">
                        <label className="block text-sm font-semibold text-gray-900">
                          Drug Name <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="text"
                          value={medication.name}
                          onChange={(e) => updateMedication(medication.id, 'name', e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                          placeholder="Enter medication name"
                          list={`medications-${medication.id}`}
                          required
                        />
                        <datalist id={`medications-${medication.id}`}>
                          {commonMedications.map(med => (
                            <option key={med} value={med} />
                          ))}
                        </datalist>
                      </div>

                      {/* Dosage Form */}
                      <div className="space-y-2">
                        <label className="block text-sm font-semibold text-gray-900">Form</label>
                        <select
                          value={medication.dosageForm}
                          onChange={(e) => updateMedication(medication.id, 'dosageForm', e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                        >
                          {dosageForms.map(form => (
                            <option key={form} value={form}>
                              {form.charAt(0).toUpperCase() + form.slice(1)}
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* Strength */}
                      <div className="space-y-2">
                        <label className="block text-sm font-semibold text-gray-900">
                          Strength <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="text"
                          value={medication.strength}
                          onChange={(e) => updateMedication(medication.id, 'strength', e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                          placeholder="e.g., 500"
                          required
                        />
                      </div>

                      {/* Strength Unit */}
                      <div className="space-y-2">
                        <label className="block text-sm font-semibold text-gray-900">Unit</label>
                        <select
                          value={medication.strengthUnit}
                          onChange={(e) => updateMedication(medication.id, 'strengthUnit', e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                        >
                          {strengthUnits.map(unit => (
                            <option key={unit} value={unit}>{unit}</option>
                          ))}
                        </select>
                      </div>

                      {/* Frequency */}
                      <div className="space-y-2">
                        <label className="block text-sm font-semibold text-gray-900">Frequency</label>
                        <input
                          type="text"
                          value={medication.frequency}
                          onChange={(e) => updateMedication(medication.id, 'frequency', e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                          placeholder="e.g., Twice daily"
                        />
                      </div>

                      {/* Route */}
                      <div className="space-y-2">
                        <label className="block text-sm font-semibold text-gray-900">Route</label>
                        <select
                          value={medication.route}
                          onChange={(e) => updateMedication(medication.id, 'route', e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                        >
                          {routes.map(route => (
                            <option key={route} value={route}>
                              {route.charAt(0).toUpperCase() + route.slice(1)}
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* Duration */}
                      <div className="space-y-2">
                        <label className="block text-sm font-semibold text-gray-900">Duration</label>
                        <input
                          type="text"
                          value={medication.duration}
                          onChange={(e) => updateMedication(medication.id, 'duration', e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                          placeholder="e.g., 7 days"
                        />
                      </div>

                      {/* Instructions */}
                      <div className="lg:col-span-2 space-y-2">
                        <label className="block text-sm font-semibold text-gray-900">Special Instructions</label>
                        <input
                          type="text"
                          value={medication.instructions}
                          onChange={(e) => updateMedication(medication.id, 'instructions', e.target.value)}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                          placeholder="e.g., Take with food"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Submit Button */}
            <div className="flex justify-center pt-6">
              <button
                type="submit"
                disabled={isLoading}
                className="btn bg-gradient-primary hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-white px-12 py-4 text-lg rounded-xl transform hover:scale-105 transition-all duration-200 flex items-center gap-3"
              >
                {isLoading ? (
                  <>
                    <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Analyzing Medications...</span>
                  </>
                ) : (
                  <>
                    <CheckCircle className="w-6 h-6" />
                    <span>Check Interactions</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Help Section */}
      <div className="mt-12 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-3xl p-8 text-center">
        <div className="max-w-2xl mx-auto">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">Need Help?</h3>
          <p className="text-gray-600 mb-6">
            Our AI-powered system analyzes your medications for potential interactions, contraindications, and safety warnings.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate('/chatbot')}
              className="btn bg-white border-2 border-primary-200 text-primary-600 hover:bg-primary-50 px-6 py-3 rounded-xl"
            >
              Ask AI Assistant
            </button>
            <button
              onClick={() => navigate('/about')}
              className="btn bg-white border-2 border-gray-200 text-gray-600 hover:bg-gray-50 px-6 py-3 rounded-xl"
            >
              Learn More
            </button>
          </div>
        </div>
      </div>

      {/* Analyzing Animation */}
      {isLoading && (
        <AnalyzingAnimation stage={analyzingStage} />
      )}
    </div>
  );
};

export default ScanPage;
