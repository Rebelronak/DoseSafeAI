from flask import Blueprint, request, jsonify
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize Groq client with proper error handling
client = None
try:
    from groq import Groq
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        client = Groq(api_key=api_key)
        print("Groq AI client initialized successfully")
        print("Using Llama 3.3-70B model for medical analysis")
    else:
        print("Error: GROQ_API_KEY not found in environment variables")
except Exception as initialization_error:
    print(f"Groq client initialization failed: {initialization_error}")

@chatbot_bp.route('/ask', methods=['POST'])
def chatbot_ask():
    """
    Main endpoint for generating clinical prescription explanations
    Handles both AI-powered and fallback explanation generation
    """
    try:
        request_data = request.get_json()
        clinical_context = request_data.get('context', {})
        
        # Parse context if it's provided as string
        if isinstance(clinical_context, str):
            clinical_context = json.loads(clinical_context)
        
        # Generate explanation using AI or fallback system
        if client:
            explanation_response = generate_comprehensive_ai_explanation(clinical_context)
        else:
            explanation_response = generate_professional_fallback_explanation(clinical_context)
            
        return jsonify({"response": explanation_response})
        
    except Exception as processing_error:
        print(f"Chatbot processing error: {str(processing_error)}")
        # Use fallback explanation when error occurs
        fallback_response = generate_professional_fallback_explanation(clinical_context)
        return jsonify({"response": fallback_response})

def generate_comprehensive_ai_explanation(clinical_context):
    """
    Generate comprehensive clinical explanation using AI language model
    Processes medicine data, interactions, and warnings into professional analysis
    """
    medicine_list = clinical_context.get('medicines', [])
    drug_interactions = clinical_context.get('interactions', [])
    age_warnings = clinical_context.get('warnings', [])
    
    # Format medicine information for analysis
    formatted_medicines = []
    for medication in medicine_list:
        medicine_name = medication.get('name', 'Unknown medication')
        medicine_dose = medication.get('dose', 'Dose not specified')
        formatted_medicines.append(f"{medicine_name} ({medicine_dose})")
    
    # Format interaction data for comprehensive analysis
    formatted_interactions = []
    for interaction in drug_interactions:
        first_drug = interaction.get('drug1', 'Drug A')
        second_drug = interaction.get('drug2', 'Drug B')
        interaction_severity = interaction.get('severity', 'Unknown severity')
        clinical_note = interaction.get('note', 'Interaction detected')
        formatted_interactions.append(f"{first_drug} + {second_drug}: {interaction_severity} severity - {clinical_note}")
    
    # Format warning information for patient safety assessment
    formatted_warnings = []
    for warning in age_warnings:
        warning_drug = warning.get('drug', 'Unknown medication')
        warning_severity = warning.get('severity', 'Unknown severity')
        warning_note = warning.get('note', 'Age-related concern identified')
        formatted_warnings.append(f"{warning_drug}: {warning_severity} severity - {warning_note}")

    # Create comprehensive clinical analysis prompt
    clinical_analysis_prompt = f"""
You are a board-certified clinical pharmacist conducting a comprehensive prescription review. Generate a structured clinical report using professional medical terminology.

CLINICAL DATA FOR ANALYSIS:
Patient Medications: {formatted_medicines if formatted_medicines else ['No medications clearly identified']}
Drug-Drug Interactions: {formatted_interactions if formatted_interactions else ['No interactions detected']}
Age-Related Safety Concerns: {formatted_warnings if formatted_warnings else ['No age-specific warnings applicable']}

Generate a professional clinical analysis using this structured format:

**CLINICAL PRESCRIPTION ANALYSIS**

**1. MEDICATION OVERVIEW**
Provide therapeutic classification and primary indication for each identified medication

**2. DRUG INTERACTION ASSESSMENT**
Analyze clinical significance, mechanisms, and patient impact of any identified interactions

**3. AGE-RELATED CONSIDERATIONS**
Address age-specific contraindications, dosing considerations, and monitoring requirements

**4. CLINICAL RECOMMENDATIONS**
Provide evidence-based recommendations for safe medication use and optimization

**5. MONITORING REQUIREMENTS**
Specify clinical parameters, laboratory values, and patient symptoms requiring monitoring

**6. PRESCRIBER CONTACT INDICATIONS**
Define circumstances requiring immediate healthcare provider notification

Requirements:
- Use professional medical terminology while maintaining clarity
- Provide evidence-based recommendations
- Focus on patient safety and clinical outcomes
- Keep analysis concise and actionable
- Limit response to 300 words maximum
"""

    try:
        # Generate AI-powered clinical analysis
        ai_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert clinical pharmacist with extensive experience in medication therapy management, drug safety, and patient care. Generate professional, evidence-based clinical analyses that prioritize patient safety and provide actionable clinical recommendations."
                },
                {"role": "user", "content": clinical_analysis_prompt}
            ],
            max_tokens=500,
            temperature=0.08  # Very low temperature for clinical accuracy
        )
        
        ai_generated_analysis = ai_response.choices[0].message.content.strip()
        
        # Add professional disclaimer and attribution
        complete_clinical_response = f"{ai_generated_analysis}\n\n---\n**Clinical Analysis:** Llama 3.3-70B Medical AI | **Disclaimer:** For educational purposes only"
        
        print("AI-powered clinical analysis generated successfully")
        return complete_clinical_response
        
    except Exception as ai_error:
        print(f"AI analysis generation failed: {ai_error}")
        return generate_professional_fallback_explanation(clinical_context)

def generate_professional_fallback_explanation(clinical_context):
    """
    Generate professional fallback explanation when AI is unavailable
    Uses structured clinical analysis format with available data
    """
    medicine_list = clinical_context.get('medicines', [])
    drug_interactions = clinical_context.get('interactions', [])
    age_warnings = clinical_context.get('warnings', [])
    
    clinical_report_sections = []
    clinical_report_sections.append("**CLINICAL PRESCRIPTION ANALYSIS**\n")
    
    # Medication Overview Section
    clinical_report_sections.append("**1. MEDICATION OVERVIEW**")
    if medicine_list:
        for medication in medicine_list:
            medicine_name = medication.get('name', 'Unknown medication')
            medicine_dose = medication.get('dose', 'Dose not specified')
            clinical_report_sections.append(f"• {medicine_name} ({medicine_dose}) - Requires therapeutic class verification and indication review")
    else:
        clinical_report_sections.append("• No medications clearly identified in prescription documentation")
    clinical_report_sections.append("")
    
    # Drug Interaction Assessment Section
    clinical_report_sections.append("**2. DRUG INTERACTION ASSESSMENT**")
    if drug_interactions:
        for interaction in drug_interactions:
            first_drug = interaction.get('drug1', 'Drug A')
            second_drug = interaction.get('drug2', 'Drug B')
            interaction_severity = interaction.get('severity', 'Unknown severity')
            clinical_note = interaction.get('note', 'Clinical significance requires evaluation')
            clinical_report_sections.append(f"• {first_drug} + {second_drug}: {interaction_severity} severity interaction - {clinical_note}")
    else:
        clinical_report_sections.append("• No clinically significant drug-drug interactions identified in current analysis")
    clinical_report_sections.append("")
    
    # Age-Related Considerations Section
    clinical_report_sections.append("**3. AGE-RELATED CONSIDERATIONS**")
    if age_warnings:
        for warning in age_warnings:
            warning_drug = warning.get('drug', 'Unknown medication')
            warning_severity = warning.get('severity', 'Unknown severity')
            warning_description = warning.get('warning', 'Age-related concern identified')
            clinical_report_sections.append(f"• {warning_drug}: {warning_severity} severity - {warning_description}")
    else:
        clinical_report_sections.append("• No specific age-related contraindications or dosing adjustments identified")
    clinical_report_sections.append("")
    
    # Clinical Recommendations Section
    clinical_report_sections.append("**4. CLINICAL RECOMMENDATIONS**")
    clinical_report_sections.append("• Adhere to prescribed dosing regimen and administration schedule")
    clinical_report_sections.append("• Monitor therapeutic response and document any adverse effects")
    clinical_report_sections.append("• Maintain comprehensive medication reconciliation records")
    clinical_report_sections.append("• Consult prescriber before making any medication modifications")
    clinical_report_sections.append("")
    
    # Monitoring Requirements Section
    clinical_report_sections.append("**5. MONITORING REQUIREMENTS**")
    clinical_report_sections.append("• Assess medication effectiveness through appropriate clinical markers")
    clinical_report_sections.append("• Monitor for adverse drug reactions and drug-related problems")
    clinical_report_sections.append("• Evaluate patient adherence and medication understanding")
    clinical_report_sections.append("• Track relevant laboratory values and vital signs as indicated")
    clinical_report_sections.append("")
    
    # Prescriber Contact Indications Section
    clinical_report_sections.append("**6. PRESCRIBER CONTACT INDICATIONS**")
    clinical_report_sections.append("• Severe adverse reactions or suspected allergic responses")
    clinical_report_sections.append("• Significant deterioration in clinical condition")
    clinical_report_sections.append("• Questions regarding medication therapy or dosing adjustments")
    clinical_report_sections.append("• Need for medication therapy optimization or alternative treatments")
    clinical_report_sections.append("")
    
    # Professional footer
    clinical_report_sections.append("---")
    clinical_report_sections.append("**Clinical Analysis:** Professional Backup System | **Disclaimer:** For educational purposes only")
    
    return '\n'.join(clinical_report_sections)

# Helper function for context validation
def validate_clinical_context(context_data):
    """
    Validate clinical context data for completeness and structure
    Ensures required fields are present for proper analysis
    """
    
    required_fields = ['medicines', 'interactions', 'warnings']
    validation_successful = True
    
    for field in required_fields:
        if field not in context_data:
            print(f"Warning: Missing required field '{field}' in clinical context")
            validation_successful = False
    
    # Validate medicine entries structure
    medicines = context_data.get('medicines', [])
    for index, medicine in enumerate(medicines):
        if not isinstance(medicine, dict) or not medicine.get('name'):
            print(f"Warning: Medicine entry {index} has invalid structure or missing name")
            validation_successful = False
    
    return validation_successful

# Utility function for response formatting
def format_clinical_response(analysis_text, processing_metadata=None):
    """
    Format clinical response with proper structure and metadata
    Ensures consistent presentation of clinical analysis results
    """
    
    formatted_response = analysis_text.strip()
    
    # Add processing metadata if provided
    if processing_metadata:
        processing_method = processing_metadata.get('method', 'Unknown')
        processing_time = processing_metadata.get('time', 'Not recorded')
        
        metadata_section = f"\n\n**Processing Information:**\n"
        metadata_section += f"• Method: {processing_method}\n"
        metadata_section += f"• Processing Time: {processing_time}"
        
        formatted_response += metadata_section
    
    return formatted_response

# Error handling helper for clinical analysis
def handle_analysis_error(error_details, fallback_context):
    """
    Handle errors in clinical analysis generation
    Provides appropriate fallback responses and error logging
    """
    
    print(f"Clinical analysis error encountered: {error_details}")
    
    # Generate safe fallback response
    fallback_response = generate_professional_fallback_explanation(fallback_context)
    
    # Add error handling note
    error_note = "\n\n**Note:** This analysis was generated using backup systems due to processing limitations."
    
    return fallback_response + error_note

@chatbot_bp.route('/chat', methods=['POST'])
def chatbot_chat():
    """
    General chat endpoint for medical questions and conversations
    Uses Groq's Llama model for real-time responses
    """
    try:
        request_data = request.get_json()
        user_message = request_data.get('message', '')
        conversation_history = request_data.get('history', [])
        
        if not user_message.strip():
            return jsonify({
                "response": "Please provide a question about medications or health.",
                "type": "error"
            }), 400
        
        # Generate response using AI or fallback
        if client:
            response_text = generate_medical_chat_response(user_message, conversation_history)
            response_type = "info"
        else:
            response_text = generate_fallback_chat_response(user_message)
            response_type = "fallback"
            
        return jsonify({
            "response": response_text,
            "type": response_type
        })
        
    except Exception as error:
        print(f"Chat endpoint error: {str(error)}")
        fallback_response = generate_fallback_chat_response(user_message if 'user_message' in locals() else "")
        return jsonify({
            "response": fallback_response,
            "type": "error"
        })

def generate_medical_chat_response(user_message, conversation_history):
    """
    Generate medical chat response using Groq's Llama model
    """
    try:
        # Build conversation context
        messages = [
            {
                "role": "system",
                "content": """You are a knowledgeable medical AI assistant specializing in medication safety, drug interactions, and general health guidance. 

IMPORTANT GUIDELINES:
- Provide accurate, helpful information about medications and health
- Always remind users to consult healthcare professionals for medical decisions
- Be clear about what requires immediate medical attention
- Use professional but accessible language
- Include relevant safety warnings when appropriate
- Stay focused on medication-related and general health topics

Do not:
- Provide specific medical diagnoses
- Recommend specific dosages without professional consultation
- Give emergency medical advice (direct to emergency services)
- Replace professional medical consultation

Format your responses to be clear, informative, and include relevant safety reminders."""
            }
        ]
        
        # Add conversation history (last 10 messages for context)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({
            "role": "user", 
            "content": user_message
        })
        
        # Generate response using Groq
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",  # Fast and capable model
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            stream=False
        )
        
        response_content = chat_completion.choices[0].message.content
        
        # Add safety disclaimer if not already present
        if "consult" not in response_content.lower() and "healthcare" not in response_content.lower():
            response_content += "\n\n⚠️ **Important**: Always consult with your healthcare provider for personalized medical advice."
        
        return response_content
        
    except Exception as ai_error:
        print(f"Groq AI generation error: {ai_error}")
        return generate_fallback_chat_response(user_message)

def generate_fallback_chat_response(user_message):
    """
    Generate fallback response when AI is unavailable
    """
    message_lower = user_message.lower()
    
    # Medication interaction questions
    if any(keyword in message_lower for keyword in ['interaction', 'combine', 'together', 'mix']):
        return """Drug interactions can occur when medications affect each other's effectiveness or cause unexpected side effects. Common types include:

• **Additive effects**: When drugs have similar effects that add up
• **Opposing effects**: When drugs work against each other
• **Altered absorption**: When one drug affects how another is absorbed

**Safety Tips**:
- Always inform your doctor and pharmacist about ALL medications you take
- This includes prescriptions, over-the-counter drugs, and supplements
- Use one pharmacy when possible for better interaction checking
- Read medication labels carefully

⚠️ **Important**: Always consult your healthcare provider before combining medications."""

    # Side effects questions
    elif any(keyword in message_lower for keyword in ['side effect', 'adverse', 'reaction']):
        return """Medication side effects are unwanted effects that can occur alongside the intended therapeutic benefits:

**Common Types**:
• **Mild**: Nausea, headache, drowsiness, upset stomach
• **Moderate**: Dizziness, skin rash, changes in appetite
• **Severe**: Difficulty breathing, severe allergic reactions, chest pain

**When to Seek Help**:
- Severe allergic reactions (swelling, difficulty breathing)
- Unusual or persistent symptoms
- Symptoms that worsen over time

**Management Tips**:
- Take medications with food if stomach upset occurs
- Report all side effects to your healthcare provider
- Don't stop medications abruptly without medical guidance

⚠️ **Important**: Contact your doctor if you experience concerning side effects."""

    # Storage questions
    elif any(keyword in message_lower for keyword in ['store', 'storage', 'keep', 'temperature']):
        return """Proper medication storage is crucial for maintaining effectiveness and safety:

**General Storage Guidelines**:
• **Room temperature**: Most medications (68-77°F)
• **Cool, dry place**: Away from heat, light, and moisture
• **Original containers**: Keep labels and child-resistant caps
• **Avoid**: Bathroom medicine cabinets (too humid)

**Special Storage**:
- Refrigerated medications: Store in fridge, don't freeze
- Liquids: Check for separation or color changes
- Inhalers: Store at room temperature

**Safety Tips**:
- Check expiration dates regularly
- Dispose of expired medications safely
- Keep medications away from children and pets

⚠️ **Important**: Follow specific storage instructions on your medication labels."""

    # Alcohol questions
    elif any(keyword in message_lower for keyword in ['alcohol', 'drink', 'wine', 'beer']):
        return """Alcohol can interact with many medications, potentially causing dangerous effects:

**Common Risks**:
• **Increased drowsiness**: With sedatives, antihistamines, pain medications
• **Liver damage**: With acetaminophen and other liver-processed drugs
• **Blood pressure changes**: With heart medications
• **Reduced effectiveness**: Some antibiotics and other medications

**Medications to Avoid with Alcohol**:
- Pain medications (opioids, NSAIDs)
- Sedatives and sleep aids
- Antidepressants and anxiety medications
- Blood thinners
- Diabetes medications

**Safety Guidelines**:
- Read medication labels for alcohol warnings
- Ask your pharmacist about alcohol interactions
- Consider timing if occasional alcohol use is approved by your doctor

⚠️ **Important**: Always ask your healthcare provider about alcohol use with your specific medications."""

    # General medication questions
    else:
        return """I'm here to help with medication and health questions! I can provide information about:

**Medication Topics**:
• Drug interactions and safety
• Common side effects and management
• Proper storage and handling
• General medication guidelines

**Health & Safety**:
• When to seek medical attention
• Medication safety tips
• General health guidance

**Popular Questions**:
• "What are drug interactions?"
• "How should I store my medications?"
• "What are common side effects?"
• "Can I take medication with alcohol?"

Feel free to ask specific questions about medications, interactions, side effects, or general health topics!

⚠️ **Important**: I provide general information only. Always consult your healthcare provider for personalized medical advice."""