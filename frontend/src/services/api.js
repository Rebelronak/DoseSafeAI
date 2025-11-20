import axios from 'axios';
import { API_ENDPOINTS } from '../config/api';

// Use environment variable for API URL
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    console.log(`📡 Base URL: ${BASE_URL}`);
    return config;
  },
  (error) => {
    console.error('🚨 API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('🚨 API Error:', error);
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  login: async (email, password) => {
    const users = JSON.parse(localStorage.getItem('dosesafe_users') || '[]');
    const user = users.find(u => u.email === email && u.password === password);
    
    if (user) {
      const { password: _, ...userWithoutPassword } = user;
      localStorage.setItem('dosesafe_user', JSON.stringify(userWithoutPassword));
      return { data: { user: userWithoutPassword } };
    } else {
      throw new Error('Invalid credentials');
    }
  },
  
  register: async (userData) => {
    const users = JSON.parse(localStorage.getItem('dosesafe_users') || '[]');
    
    if (users.find(u => u.email === userData.email)) {
      throw new Error('User with this email already exists');
    }
    
    const newUser = {
      id: Date.now().toString(),
      ...userData,
      createdAt: new Date().toISOString()
    };
    
    users.push(newUser);
    localStorage.setItem('dosesafe_users', JSON.stringify(users));
    
    const { password: _, ...userWithoutPassword } = newUser;
    localStorage.setItem('dosesafe_user', JSON.stringify(userWithoutPassword));
    
    return { data: { user: userWithoutPassword } };
  },
  
  logout: () => {
    localStorage.removeItem('dosesafe_user');
  },
  
  getCurrentUser: () => {
    const user = localStorage.getItem('dosesafe_user');
    return user ? JSON.parse(user) : null;
  }
};

// OCR API - connects to your backend
export const ocrAPI = {
  uploadImage: async (file, patientAge = 30, patientCondition = '') => {
    try {
      console.log('🔍 Starting OCR processing...', { fileName: file.name, size: file.size });
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('patientAge', patientAge.toString());
      formData.append('patientCondition', patientCondition);
      
      const response = await api.post('/scan/image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 60000 // 60 second timeout for OCR processing
      });
      
      console.log('✅ OCR processing complete:', response.data);
      
      const result = {
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        type: 'image',
        patientAge,
        patientCondition,
        medications: response.data.medications || [],
        interactions: response.data.drug_interactions || response.data.interactions || [],
        ageWarnings: response.data.age_specific_warnings || [],
        contraindications: response.data.contraindications || [],
        harmfulCombinations: response.data.harmful_combinations || [],
        clinicalSummary: response.data.clinical_summary || '',
        ocrText: response.data.extracted_text || '',
        confidence: response.data.confidence || 'Medium',
        riskLevel: response.data.risk_level || 'low',
        totalMedications: response.data.total_medications || (response.data.medications ? response.data.medications.length : 0),
        totalInteractions: response.data.total_interactions || (response.data.drug_interactions ? response.data.drug_interactions.length : 0),
        processingTime: response.data.processing_time || 'N/A',
        source: response.data.source || 'OCR Processing'
      };
      
      return result;
    } catch (error) {
      console.error('🚨 OCR API Error:', error);
      
      if (error.response) {
        throw new Error(error.response.data.error || 'OCR processing failed');
      } else if (error.request) {
        throw new Error('Cannot connect to OCR service. Please check if the backend is running.');
      } else {
        throw new Error('OCR processing error: ' + error.message);
      }
    }
  },
  
  processManualEntry: async (medications, patientAge, patientCondition) => {
    try {
      console.log('📝 Processing manual entry...', { medicationCount: medications.length });
      
      const response = await api.post('/scan/manual', {
        medications: medications,
        patient_age: parseInt(patientAge) || 30,
        patient_condition: patientCondition || ''
      });
      
      console.log('✅ Manual processing complete:', response.data);
      
      const result = {
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        type: 'manual',
        patientAge,
        patientCondition,
        medications: response.data.medications || response.data.enhanced_medications || [],
        interactions: response.data.drug_interactions || response.data.interactions || [],
        ageWarnings: response.data.age_specific_warnings || response.data.age_warnings || [],
        contraindications: response.data.contraindications || [],
        harmfulCombinations: response.data.harmful_combinations || [],
        dosingConsiderations: response.data.dosing_considerations || [],
        clinicalSummary: response.data.clinical_summary || '',
        riskLevel: response.data.overall_risk_assessment || response.data.risk_level || 'low',
        totalMedications: response.data.total_medications || (response.data.medications ? response.data.medications.length : 0),
        totalInteractions: response.data.total_interactions || (response.data.drug_interactions ? response.data.drug_interactions.length : 0),
        source: response.data.source || 'Manual Entry'
      };
      
      return result;
    } catch (error) {
      console.error('🚨 Manual Entry API Error:', error);
      
      if (error.response) {
        throw new Error(error.response.data.error || 'Manual entry processing failed');
      } else if (error.request) {
        throw new Error('Cannot connect to processing service. Please check if the backend is running.');
      } else {
        throw new Error('Processing error: ' + error.message);
      }
    }
  }
};

// Drug Interaction API - connects to your backend
export const interactionAPI = {
  checkInteractions: async (medications, patientAge) => {
    try {
      const response = await api.post('/analyze-interactions-ai', {
        medications: medications.map(med => ({
          name: med.name,
          dosage: med.dosage || med.strength,
          frequency: med.frequency
        })),
        patient_age: parseInt(patientAge) || 30
      });
      
      return {
        interactions: response.data.interactions || [],
        riskLevel: response.data.overall_risk || 'low',
        warnings: response.data.warnings || [],
        recommendations: response.data.recommendations || []
      };
    } catch (error) {
      console.error('Interaction API Error:', error);
      return {
        interactions: [],
        riskLevel: 'low',
        warnings: [],
        recommendations: ['Always consult with your healthcare provider']
      };
    }
  }
};

// Chatbot API - connects to your backend
export const chatbotAPI = {
  sendMessage: async (message, conversationHistory = []) => {
    try {
      const response = await api.post('/chatbot/chat', {
        message,
        history: conversationHistory
      });
      
      return {
        response: response.data.response || 'I apologize, but I cannot process your request right now.',
        type: response.data.type || 'info'
      };
    } catch (error) {
      console.error('Chatbot API Error:', error);
      
      const fallbackResponses = {
        'drug interactions': {
          response: 'Drug interactions occur when two or more medications affect each other when taken together. This can increase or decrease the effectiveness of one or both drugs, or cause unexpected side effects. Always check with your pharmacist or doctor before combining medications.',
          type: 'info'
        },
        'side effects': {
          response: 'Common side effects vary by medication but may include nausea, dizziness, drowsiness, or upset stomach. If you experience severe side effects or allergic reactions, stop taking the medication and seek immediate medical attention.',
          type: 'warning'
        },
        'storage': {
          response: 'Most medications should be stored in a cool, dry place away from direct sunlight. Some medications require refrigeration. Always check the label for specific storage instructions and keep medications out of reach of children.',
          type: 'info'
        },
        'dosage': {
          response: 'Always take medications exactly as prescribed by your healthcare provider. Do not increase, decrease, or stop taking medications without consulting your doctor first. If you miss a dose, follow the instructions provided with your medication.',
          type: 'warning'
        }
      };
      
      const lowerMessage = message.toLowerCase();
      for (const [key, value] of Object.entries(fallbackResponses)) {
        if (lowerMessage.includes(key)) {
          return value;
        }
      }
      
      return {
        response: 'I apologize, but I cannot process your request right now. Please consult with your healthcare provider for personalized medical advice.',
        type: 'info'
      };
    }
  }
};

// Scan History API
export const scanHistoryAPI = {
  saveScan: (scanResult, analysisResult) => {
    const history = JSON.parse(localStorage.getItem('scan_history') || '[]');
    
    const scanRecord = {
      ...scanResult,
      ...analysisResult,
      id: scanResult.id,
      timestamp: scanResult.timestamp
    };
    
    history.unshift(scanRecord);
    
    if (history.length > 10) {
      history.splice(10);
    }
    
    localStorage.setItem('scan_history', JSON.stringify(history));
    localStorage.setItem('latest_scan_result', JSON.stringify(scanRecord));
    
    return scanRecord;
  },
  
  getHistory: () => {
    return JSON.parse(localStorage.getItem('scan_history') || '[]');
  },
  
  getLatestScan: () => {
    return JSON.parse(localStorage.getItem('latest_scan_result') || 'null');
  },
  
  deleteScan: (scanId) => {
    const history = JSON.parse(localStorage.getItem('scan_history') || '[]');
    const updatedHistory = history.filter(scan => scan.id !== scanId);
    localStorage.setItem('scan_history', JSON.stringify(updatedHistory));
    return updatedHistory;
  }
};

// Metrics API
export const metricsAPI = {
  getMetrics: () => {
    return {
      prescriptions: parseInt(localStorage.getItem('prescriptions') || '2500000'),
      interactions: parseInt(localStorage.getItem('interactions') || '150000'),
      users: parseInt(localStorage.getItem('users') || '500000')
    };
  },
  
  incrementMetric: (metric) => {
    const current = parseInt(localStorage.getItem(metric) || '0');
    localStorage.setItem(metric, (current + 1).toString());
  }
};

// Scan Service - combines OCR and interaction checking
export const scanService = {
  processImageScan: async (file, patientAge = 30, patientCondition = '') => {
    try {
      console.log('🖼️ Starting image scan process...', { patientAge, patientCondition });
      
      // Process OCR with comprehensive analysis
      const result = await ocrAPI.uploadImage(file, patientAge, patientCondition);
      
      // Save to history
      scanHistoryAPI.saveScan(result, {});
      
      console.log('✅ Image scan complete:', result);
      return result;
    } catch (error) {
      console.error('🚨 Image scan error:', error);
      throw error;
    }
  },
  
  processManualScan: async (medications, patientAge = 30, patientCondition = '') => {
    try {
      console.log('📝 Starting manual scan process...', { 
        medicationCount: medications.length, 
        patientAge, 
        patientCondition 
      });
      
      // Process manual entry with comprehensive analysis
      const result = await ocrAPI.processManualEntry(medications, patientAge, patientCondition);
      
      // Save to history
      scanHistoryAPI.saveScan(result, {});
      
      console.log('✅ Manual scan complete:', result);
      return result;
    } catch (error) {
      console.error('🚨 Manual scan error:', error);
      throw error;
    }
  }
};

// Chatbot Service - alias for chatbotAPI for backward compatibility
export const chatbotService = {
  sendMessage: chatbotAPI.sendMessage
};

export default api;
