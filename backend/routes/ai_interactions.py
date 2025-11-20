from flask import Blueprint, request, jsonify
import json
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

# Initialize blueprint for AI interaction routes
ai_interactions_bp = Blueprint('ai_interactions', __name__)

# Setup Groq client with error handling
def initialize_groq_client():
    """Initialize Groq client with proper error handling"""
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("Warning: GROQ_API_KEY not found in environment")
        return None
    
    try:
        return Groq(api_key=api_key)
    except Exception as error:
        print(f"Failed to initialize Groq client: {error}")
        return None

client = initialize_groq_client()

@ai_interactions_bp.route('/comprehensive-check', methods=['POST'])
def comprehensive_interaction_check():
    """
    Performs comprehensive drug interaction analysis using AI
    Returns detailed interaction data with safety assessments
    """
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "No data provided"}), 400
            
        medication_list = request_data.get('medicines', [])
        patient_age = request_data.get('age', 30)
        
        print(f"Processing interaction check for {len(medication_list)} medications (patient age: {patient_age})")
        
        if not client:
            return jsonify({
                "error": "AI service temporarily unavailable",
                "fallback_message": "Please try again later"
            }), 503
            
        # Perform comprehensive analysis
        analysis_result = perform_comprehensive_analysis(medication_list, patient_age)
        return jsonify(analysis_result)
        
    except Exception as error:
        print(f"Error in comprehensive check: {str(error)}")
        return jsonify({
            "error": "Analysis failed", 
            "details": str(error)
        }), 500

@ai_interactions_bp.route('/advanced-warnings', methods=['POST'])
def advanced_warnings():
    """
    Generates advanced patient-specific warnings and recommendations
    Considers patient profile, medical history, and individual risk factors
    """
    try:
        request_data = request.get_json()
        medication_list = request_data.get('medicines', [])
        patient_profile = request_data.get('patient_info', {})
        
        print("Generating advanced warning analysis for patient profile")
        
        if not client:
            return jsonify({"error": "Warning system unavailable"}), 503
            
        warning_result = generate_advanced_warnings(medication_list, patient_profile)
        return jsonify(warning_result)
        
    except Exception as error:
        print(f"Advanced warnings generation failed: {str(error)}")
        return jsonify({"error": str(error)}), 500

def perform_comprehensive_analysis(medications, age):
    """
    Core function for comprehensive drug interaction analysis
    Handles both AI-powered analysis and fallback scenarios
    """
    
    # Build medication list with proper formatting
    formatted_meds = []
    for medication in medications:
        med_name = medication.get('name', 'Unspecified medication')
        med_dosage = medication.get('dose', 'dosage not specified')
        formatted_meds.append(f"{med_name} ({med_dosage})")
    
    print(f"Analyzing drug interactions for: {', '.join(formatted_meds)}")
    
    # Create detailed analysis prompt
    analysis_prompt = build_interaction_analysis_prompt(formatted_meds, age)
    
    try:
        if client:
            # Request AI analysis
            ai_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an experienced clinical pharmacist specializing in drug interaction analysis. Provide evidence-based assessments."
                    },
                    {
                        "role": "user", 
                        "content": analysis_prompt
                    }
                ],
                max_tokens=1200,
                temperature=0.15  # Slightly higher for more natural responses
            )
            
            ai_content = ai_response.choices[0].message.content.strip()
            
            try:
                # Parse AI response
                parsed_result = json.loads(ai_content)
                parsed_result["ai_powered"] = True
                
                # Log results
                interaction_count = len(parsed_result.get('drug_drug_interactions', []))
                warning_count = len(parsed_result.get('age_related_warnings', []))
                print(f"Analysis complete: {interaction_count} interactions, {warning_count} warnings identified")
                
                return parsed_result
                
            except json.JSONDecodeError as parse_error:
                print(f"JSON parsing failed: {parse_error}")
                # Use fallback analysis
                return create_fallback_analysis(medications, age)
                
    except Exception as ai_error:
        print(f"AI analysis failed: {ai_error}")
        return create_fallback_analysis(medications, age)

def build_interaction_analysis_prompt(med_list, patient_age):
    """Constructs a detailed prompt for AI interaction analysis"""
    
    prompt = f"""
As a clinical pharmacist, analyze these medications for a {patient_age}-year-old patient:

MEDICATIONS: {med_list}

Please evaluate:
1. Drug-drug interactions (especially CNS depressants)
2. Age-appropriate prescribing concerns
3. Monitoring requirements

Provide analysis in JSON format:
{{
    "drug_drug_interactions": [
        {{
            "drug1": "First medication",
            "drug2": "Second medication",
            "severity": "High/Moderate/Low",
            "mechanism": "Interaction mechanism",
            "clinical_effect": "Expected clinical outcome",
            "management": "Recommended management strategy"
        }}
    ],
    "age_related_warnings": [
        {{
            "drug": "Medication name",
            "age_concern": "Age-specific concern",
            "risk_level": "High/Moderate/Low", 
            "specific_risk": "Particular risk factors",
            "monitoring": "Monitoring recommendations"
        }}
    ],
    "overall_assessment": {{
        "total_interactions": 0,
        "highest_severity": "Risk level",
        "overall_risk": "Overall patient risk"
    }}
}}

Focus on clinically significant interactions, particularly:
- CNS depressant combinations (Hydroxyzine + Lorazepam)
- Cardiovascular drug interactions
- Elderly patient considerations (age ≥65)
"""
    return prompt

def create_fallback_analysis(medications, age):
    """
    Creates fallback analysis when AI is unavailable
    Uses rule-based logic for common interactions
    """
    
    detected_interactions = []
    identified_warnings = []
    
    # Extract medication names for analysis
    med_names = [med.get('name', '').lower() for med in medications]
    
    # Check for known high-risk combinations
    high_risk_combos = check_high_risk_combinations(med_names)
    detected_interactions.extend(high_risk_combos)
    
    # Check age-related concerns
    if int(age) >= 65:
        elderly_warnings = check_elderly_warnings(medications)
        identified_warnings.extend(elderly_warnings)
    
    # Assess overall risk
    risk_assessment = assess_overall_risk(detected_interactions, identified_warnings)
    
    return {
        "drug_drug_interactions": detected_interactions,
        "age_related_warnings": identified_warnings,
        "overall_assessment": risk_assessment,
        "ai_powered": False,
        "fallback_analysis": True
    }

def check_high_risk_combinations(medication_names):
    """Identifies high-risk drug combinations using rule-based logic"""
    
    interactions = []
    
    # CNS depressant combinations
    cns_depressants = ['hydroxyzine', 'lorazepam', 'diazepam', 'alprazolam']
    found_cns = [med for med in medication_names if any(cns in med for cns in cns_depressants)]
    
    if len(found_cns) >= 2:
        interactions.append({
            "drug1": found_cns[0].title(),
            "drug2": found_cns[1].title(),
            "severity": "High",
            "mechanism": "Additive central nervous system depression",
            "clinical_effect": "Enhanced sedation and respiratory depression risk",
            "management": "Consider dose reduction and increased monitoring"
        })
    
    # Beta-blocker interactions
    if 'metoprolol' in medication_names:
        for med in medication_names:
            if 'verapamil' in med or 'diltiazem' in med:
                interactions.append({
                    "drug1": "Metoprolol",
                    "drug2": med.title(),
                    "severity": "Moderate",
                    "mechanism": "Additive cardiac depression",
                    "clinical_effect": "Bradycardia and hypotension risk",
                    "management": "Monitor heart rate and blood pressure closely"
                })
    
    return interactions

def check_elderly_warnings(medications):
    """Generates age-related warnings for elderly patients"""
    
    warnings = []
    high_risk_elderly_meds = {
        'hydroxyzine': 'Anticholinergic effects and falls risk',
        'lorazepam': 'Cognitive impairment and falls risk',
        'diazepam': 'Prolonged half-life in elderly',
        'diphenhydramine': 'Anticholinergic burden'
    }
    
    for medication in medications:
        med_name = medication.get('name', '').lower()
        
        for risky_med, risk_description in high_risk_elderly_meds.items():
            if risky_med in med_name:
                warnings.append({
                    "drug": medication.get('name'),
                    "age_concern": "Elderly patient (≥65 years)",
                    "risk_level": "High",
                    "specific_risk": risk_description,
                    "monitoring": "Assess for sedation, confusion, and fall risk regularly"
                })
    
    return warnings

def assess_overall_risk(interactions, warnings):
    """Calculates overall risk assessment based on findings"""
    
    total_findings = len(interactions) + len(warnings)
    
    # Determine highest severity
    high_severity_count = sum(1 for item in interactions if item.get('severity') == 'High')
    high_severity_count += sum(1 for item in warnings if item.get('risk_level') == 'High')
    
    if high_severity_count > 0:
        overall_risk = "High"
        highest_severity = "Major"
    elif total_findings > 0:
        overall_risk = "Moderate"  
        highest_severity = "Moderate"
    else:
        overall_risk = "Low"
        highest_severity = "Minor"
    
    return {
        "total_interactions": len(interactions),
        "total_warnings": len(warnings),
        "highest_severity": highest_severity,
        "overall_risk": overall_risk,
        "clinical_significance": f"{total_findings} potential safety concerns identified"
    }

def generate_advanced_warnings(medications, patient_info):
    """
    Generates comprehensive patient-specific warnings
    Considers full patient profile including conditions and allergies
    """
    
    patient_age = patient_info.get('age', 'Not specified')
    medical_conditions = patient_info.get('conditions', [])
    known_allergies = patient_info.get('allergies', [])
    
    # Build comprehensive analysis prompt
    advanced_prompt = f"""
As a clinical decision support specialist, provide comprehensive safety analysis:

PATIENT MEDICATIONS: {[med.get('name') for med in medications]}
PATIENT PROFILE:
- Age: {patient_age}
- Medical Conditions: {medical_conditions if medical_conditions else 'None specified'}
- Known Allergies: {known_allergies if known_allergies else 'None specified'}

Please provide detailed safety assessment including:

1. CONTRAINDICATIONS: Absolute and relative contraindications
2. ALLERGY CONSIDERATIONS: Cross-reactivity risks and alternatives  
3. CONDITION-SPECIFIC WARNINGS: Disease interaction concerns
4. MONITORING PROTOCOLS: Required laboratory and clinical monitoring
5. PATIENT EDUCATION: Key safety points for patient understanding

Format as JSON:
{{
    "contraindications": [
        {{
            "drug": "Medication name",
            "contraindication_type": "Absolute/Relative",
            "reason": "Medical rationale",
            "severity": "Critical/High/Moderate",
            "alternative_suggested": "Safer alternative",
            "clinical_guidance": "Recommended action"
        }}
    ],
    "allergy_warnings": [
        {{
            "drug": "Medication name",
            "allergy_risk": "Cross-reactivity concern",
            "risk_level": "High/Moderate/Low",
            "symptoms_to_monitor": ["symptom1", "symptom2"],
            "emergency_protocol": "Action plan for allergic reaction"
        }}
    ],
    "monitoring_requirements": [
        {{
            "drug": "Medication name",
            "monitoring_type": "Laboratory/Clinical/Vital signs",
            "parameter": "What to monitor",
            "frequency": "Monitoring frequency",
            "target_values": "Normal ranges",
            "action_threshold": "When to intervene"
        }}
    ],
    "patient_education": [
        "Essential safety information for patient"
    ],
    "emergency_indicators": [
        "Signs requiring immediate medical attention"
    ]
}}
"""

    try:
        ai_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a clinical decision support specialist with expertise in medication safety, patient-specific risk assessment, and clinical monitoring protocols."
                },
                {
                    "role": "user", 
                    "content": advanced_prompt
                }
            ],
            max_tokens=1500,
            temperature=0.1
        )
        
        response_content = ai_response.choices[0].message.content.strip()
        
        try:
            parsed_warnings = json.loads(response_content)
            parsed_warnings["advanced_analysis"] = True
            
            total_warnings = len(parsed_warnings.get('contraindications', []))
            total_monitoring = len(parsed_warnings.get('monitoring_requirements', []))
            print(f"Advanced analysis complete: {total_warnings} contraindications, {total_monitoring} monitoring requirements")
            
            return parsed_warnings
            
        except json.JSONDecodeError as parse_error:
            print(f"Advanced warning JSON parsing failed: {parse_error}")
            return {
                "contraindications": [],
                "advanced_analysis": True,
                "parsing_error": "Unable to parse AI response",
                "raw_response": response_content[:500]  # Truncated for safety
            }
            
    except Exception as analysis_error:
        print(f"Advanced warning generation failed: {analysis_error}")
        return {
            "contraindications": [],
            "advanced_analysis": False,
            "error_details": str(analysis_error),
            "fallback_message": "Advanced analysis temporarily unavailable"
        }