const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const API_ENDPOINTS = {
  SCAN_IMAGE: `${API_URL}/scan/image`,
  SCAN_MANUAL: `${API_URL}/scan/manual`,
  ANALYZE_INTERACTIONS: `${API_URL}/analyze-interactions-ai`,
  CHATBOT_MESSAGE: `${API_URL}/chatbot/message`,
  CHATBOT_CHAT: `${API_URL}/chatbot/chat`,
  HEALTH: `${API_URL}/health`,
};

export default API_URL;
