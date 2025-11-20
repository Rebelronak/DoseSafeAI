import React, { useState, useEffect, useRef } from 'react';
import { chatbotService } from '../services/api';
import { 
  Send, 
  Bot, 
  User, 
  Loader, 
  AlertCircle, 
  CheckCircle, 
  Info,
  MessageCircle,
  Pill,
  Shield
} from 'lucide-react';

const ChatbotPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  // Predefined quick questions
  const quickQuestions = [
    "What are common drug interactions?",
    "How should I store my medications?",
    "What are the side effects of Ibuprofen?",
    "Can I take medication with alcohol?",
    "What should I do if I miss a dose?",
    "Are there any pregnancy warnings?",
    "How do I know if medications are expired?",
    "What are the signs of allergic reactions?"
  ];

  // Initialize chat
  useEffect(() => {
    // Check if there's context from a recent scan
    const scanContext = localStorage.getItem('chatbot_context');
    let initialMessage = "Hello! I'm your AI medication assistant. How can I help you today?";
    
    if (scanContext) {
      try {
        const context = JSON.parse(scanContext);
        if (context.medications && context.medications.length > 0) {
          initialMessage = `Hello! I see you recently scanned ${context.medications.length} medication(s). I can help answer questions about your medications, interactions, or general medication safety. What would you like to know?`;
        }
      } catch (error) {
        console.error('Error parsing scan context:', error);
      }
    }

    setMessages([{
      id: 1,
      type: 'bot',
      content: initialMessage,
      timestamp: new Date()
    }]);
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (messageText = inputMessage) => {
    if (!messageText.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: messageText.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError('');

    try {
      // Get conversation history for context
      const conversationHistory = messages.map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }));

      // Call the chatbot API
      const response = await chatbotService.sendMessage(messageText, conversationHistory);
      
      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.response || response.message || "I'm sorry, I couldn't process your request. Please try again.",
        messageType: response.message_type || 'info',
        timestamp: new Date()
      };

      // Simulate typing delay
      setTimeout(() => {
        setMessages(prev => [...prev, botMessage]);
        setIsLoading(false);
      }, 1000);

    } catch (err) {
      console.error('Chatbot error:', err);
      
      // Fallback to predefined responses
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: getPredefinedResponse(messageText),
        messageType: 'info',
        timestamp: new Date()
      };

      setTimeout(() => {
        setMessages(prev => [...prev, botMessage]);
        setIsLoading(false);
      }, 1000);
    }
  };

  // Predefined responses for common questions
  const getPredefinedResponse = (question) => {
    const lowerQuestion = question.toLowerCase();
    
    if (lowerQuestion.includes('drug interaction') || lowerQuestion.includes('interaction')) {
      return "Drug interactions can occur when two or more medications affect each other's effectiveness or increase side effects. Common types include:\n\n• **Drug-drug interactions**: Between different medications\n• **Drug-food interactions**: Medications with certain foods\n• **Drug-alcohol interactions**: Medications with alcohol\n\nAlways inform your healthcare provider about all medications, supplements, and herbal products you're taking.";
    }
    
    if (lowerQuestion.includes('store') || lowerQuestion.includes('storage')) {
      return "Proper medication storage is crucial for maintaining effectiveness:\n\n• **Keep in original containers** with labels\n• **Store in cool, dry places** away from bathrooms and kitchens\n• **Avoid extreme temperatures** (unless refrigeration is required)\n• **Keep away from children** and pets\n• **Check expiration dates** regularly\n• **Don't store in pill organizers** long-term unless recommended";
    }
    
    if (lowerQuestion.includes('ibuprofen')) {
      return "**Ibuprofen** is a nonsteroidal anti-inflammatory drug (NSAID). Common side effects include:\n\n• Stomach upset or heartburn\n• Nausea or vomiting\n• Dizziness or headache\n• Increased blood pressure\n\n**Serious side effects** (seek medical attention):\n• Severe stomach pain or bleeding\n• Difficulty breathing\n• Swelling of face, lips, or throat\n• Unusual bruising or bleeding\n\n**Take with food** to reduce stomach irritation.";
    }
    
    if (lowerQuestion.includes('alcohol')) {
      return "**Alcohol and medication interactions** can be dangerous:\n\n• **Increased drowsiness** with sedatives, antihistamines\n• **Liver damage** with acetaminophen\n• **Stomach bleeding** with NSAIDs (ibuprofen, aspirin)\n• **Blood sugar changes** with diabetes medications\n• **Increased bleeding** with blood thinners\n\n**Always check with your pharmacist** before consuming alcohol with any medication.";
    }
    
    if (lowerQuestion.includes('miss') && lowerQuestion.includes('dose')) {
      return "**If you miss a dose:**\n\n• **Take it as soon as you remember** if it's close to the scheduled time\n• **Skip the missed dose** if it's almost time for the next dose\n• **Never double up** on doses to catch up\n• **Set reminders** to help prevent missed doses\n• **Contact your healthcare provider** if you frequently miss doses\n\n**For critical medications** (heart, diabetes, seizure drugs), contact your doctor immediately.";
    }
    
    if (lowerQuestion.includes('pregnancy') || lowerQuestion.includes('pregnant')) {
      return "**Medication safety during pregnancy** is crucial:\n\n• **Consult your doctor** before taking any medication\n• **Avoid these common medications**:\n  - Aspirin (third trimester)\n  - Ibuprofen (third trimester)\n  - Some antibiotics\n  - ACE inhibitors\n\n• **Generally safe** (with doctor approval):\n  - Acetaminophen for pain/fever\n  - Certain antibiotics\n  - Prenatal vitamins\n\n**Always inform healthcare providers** about pregnancy status.";
    }
    
    if (lowerQuestion.includes('expire') || lowerQuestion.includes('expiration')) {
      return "**Medication expiration and safety:**\n\n• **Check dates regularly** - most medications lose potency over time\n• **Don't use expired medications** especially:\n  - Antibiotics\n  - Insulin\n  - Nitroglycerin\n  - Liquid medications\n\n• **Disposal of expired medications:**\n  - Use pharmacy take-back programs\n  - FDA-approved disposal kits\n  - Some can be flushed (check FDA flush list)\n\n**Never share medications** with others, even if symptoms seem similar.";
    }
    
    if (lowerQuestion.includes('allergic') || lowerQuestion.includes('allergy')) {
      return "**Signs of allergic reactions to medications:**\n\n**Mild reactions:**\n• Skin rash or hives\n• Itching\n• Mild swelling\n\n**Severe reactions (seek emergency care):**\n• Difficulty breathing or wheezing\n• Swelling of face, lips, tongue, or throat\n• Rapid pulse\n• Dizziness or fainting\n• Severe whole-body rash\n\n**If you suspect an allergic reaction:**\n• Stop taking the medication\n• Contact your healthcare provider immediately\n• For severe reactions, call emergency services";
    }
    
    return "I'm here to help with medication-related questions! I can provide information about drug interactions, side effects, storage, dosing, and general medication safety. What specific question do you have about your medications?";
  };

  const getMessageIcon = (messageType) => {
    switch (messageType) {
      case 'warning':
        return <AlertCircle className="w-4 h-4 text-yellow-600" />;
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-600" />;
      default:
        return <Info className="w-4 h-4 text-blue-600" />;
    }
  };

  const getMessageBgColor = (messageType) => {
    switch (messageType) {
      case 'warning':
        return 'bg-yellow-50 border-yellow-200';
      case 'success':
        return 'bg-green-50 border-green-200';
      case 'error':
        return 'bg-red-50 border-red-200';
      default:
        return 'bg-blue-50 border-blue-200';
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 h-full">
      {/* Header */}
      <div className="text-center mb-8 animate-slide-down">
        <div className="flex items-center justify-center gap-4 mb-6">
          <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center shadow-lg">
            <MessageCircle className="w-8 h-8 text-white" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">AI Medical Assistant</h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Get instant, expert answers about medications, interactions, and safety guidelines
        </p>
      </div>

      {/* Chat Container */}
      <div className="bg-white rounded-3xl shadow-xl border border-gray-200 h-[700px] flex flex-col animate-slide-up">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-8 space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-4 ${
                message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              {/* Avatar */}
              <div className={`w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-sm ${
                message.type === 'user' 
                  ? 'bg-gradient-primary' 
                  : 'bg-white border-2 border-gray-200'
              }`}>
                {message.type === 'user' ? (
                  <User className="w-6 h-6 text-white" />
                ) : (
                  <Bot className="w-6 h-6 text-primary-600" />
                )}
              </div>

              {/* Message Bubble */}
              <div className={`max-w-md lg:max-w-lg px-6 py-4 rounded-2xl relative ${
                message.type === 'user'
                  ? 'bg-gradient-primary text-white'
                  : `${getMessageBgColor(message.messageType)} border-2`
              }`}>
                {/* Message type indicator for bot messages */}
                {message.type === 'bot' && message.messageType && (
                  <div className="flex items-center gap-2 mb-3">
                    {getMessageIcon(message.messageType)}
                    <span className="text-xs font-bold uppercase tracking-wider">
                      {message.messageType}
                    </span>
                  </div>
                )}
                
                {/* Message content */}
                <div className="whitespace-pre-wrap text-sm leading-relaxed">
                  {message.content}
                </div>
                
                {/* Timestamp */}
                <div className={`text-xs mt-3 ${
                  message.type === 'user' ? 'text-orange-100' : 'text-gray-500'
                }`}>
                  {message.timestamp.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </div>

                {/* Message tail */}
                <div className={`absolute top-4 w-3 h-3 transform rotate-45 ${
                  message.type === 'user' 
                    ? 'bg-gradient-primary -right-1' 
                    : `${getMessageBgColor(message.messageType).split(' ')[0]} -left-1 border-l-2 border-b-2`
                }`}></div>
              </div>
            </div>
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-2xl bg-white border-2 border-gray-200 flex items-center justify-center">
                <Bot className="w-6 h-6 text-primary-600" />
              </div>
              <div className="bg-gray-100 px-6 py-4 rounded-2xl relative">
                <div className="flex items-center gap-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm text-gray-600 font-medium">AI is thinking...</span>
                </div>
                <div className="absolute top-4 -left-1 w-3 h-3 bg-gray-100 transform rotate-45 border-l-2 border-b-2 border-gray-200"></div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Questions */}
        {messages.length <= 1 && (
          <div className="px-8 py-6 border-t border-gray-100 bg-gray-50">
            <p className="text-sm font-semibold text-gray-700 mb-4">Popular questions to get you started:</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {quickQuestions.slice(0, 4).map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleSendMessage(question)}
                  className="px-4 py-3 text-sm bg-white hover:bg-primary-50 border border-gray-200 hover:border-primary-300 rounded-xl text-gray-700 hover:text-primary-700 transition-all duration-200 text-left"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="p-8 border-t border-gray-100 bg-gray-50">
          <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }} className="flex gap-4">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask about medications, interactions, side effects..."
              className="flex-1 px-6 py-4 border-2 border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 text-gray-900 placeholder-gray-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || isLoading}
              className="bg-gradient-primary hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-white px-8 py-4 rounded-2xl transition-all duration-200 transform hover:scale-105 flex items-center gap-2"
            >
              <Send className="w-5 h-5" />
              <span className="hidden sm:inline">Send</span>
            </button>
          </form>
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 border-2 border-red-200 rounded-xl text-red-700 text-sm flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="mt-8 bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-200 rounded-3xl p-6 animate-fade-in">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 bg-yellow-100 rounded-2xl flex items-center justify-center flex-shrink-0">
            <Shield className="w-6 h-6 text-yellow-600" />
          </div>
          <div>
            <h3 className="font-bold text-yellow-900 mb-2 text-lg">Medical Disclaimer</h3>
            <p className="text-sm text-yellow-800 leading-relaxed">
              This AI assistant provides general information only and should not replace professional medical advice. 
              Always consult with qualified healthcare professionals for medical decisions and medication changes.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;
