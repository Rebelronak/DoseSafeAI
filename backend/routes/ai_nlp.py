from flask import Blueprint, request, jsonify
import json
import os
from groq import Groq
from dotenv import load_dotenv

# Initialize environment configuration
load_dotenv()

# Create blueprint for natural language processing routes
ai_nlp_bp = Blueprint('ai_nlp', __name__)

# Setup AI client with fallback handling
def setup_ai_client():
    """Initialize AI client with proper error handling"""
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        try:
            return Groq(api_key=api_key)
        except Exception as init_error:
            print(f"AI client initialization failed: {init_error}")
            return None
    else:
        print("Warning: GROQ_API_KEY not configured")
        return None

# Initialize client
client = setup_ai_client()

@ai_nlp_bp.route('/smart-extract', methods=['POST'])
def smart_medicine_extraction():
    """
    Advanced medicine extraction using AI-powered natural language processing
    Handles complex prescription text with medical terminology
    """
    try:
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({"error": "No data provided"}), 400
            
        prescription_text = request_data.get('text', '')
        
        if not prescription_text.strip():
            return jsonify({
                "error": "Empty text provided",
                "medicines": [],
                "extraction_summary": {"total_medicines": 0}
            }), 400
        
        print(f"Processing prescription text for medicine extraction: {prescription_text[:100]}...")
        
        if not client:
            # Use fallback extraction when AI is unavailable
            fallback_result = perform_fallback_medicine_extraction(prescription_text)
            return jsonify(fallback_result)
            
        # Perform intelligent medicine extraction
        extraction_result = perform_intelligent_extraction(prescription_text)
        
        # Ensure the result has the correct structure
        if not extraction_result.get('medicines'):
            print("No medicines found by AI, trying fallback extraction")
            fallback_result = perform_fallback_medicine_extraction(prescription_text)
            extraction_result['medicines'] = fallback_result['medicines']
            extraction_result['fallback_used'] = True
        
        print(f"Final extraction result: {len(extraction_result.get('medicines', []))} medicines found")
        return jsonify(extraction_result)
        
    except Exception as processing_error:
        print(f"Medicine extraction error: {str(processing_error)}")
        # Use fallback extraction on error
        fallback_result = perform_fallback_medicine_extraction(prescription_text if 'prescription_text' in locals() else "")
        fallback_result['error'] = str(processing_error)
        return jsonify(fallback_result)

def perform_intelligent_extraction(prescription_text):
    """
    Core function for intelligent medicine extraction
    Uses advanced AI to understand medical context and terminology
    """
    
    # Build comprehensive extraction prompt
    extraction_prompt = create_extraction_prompt(prescription_text)
    
    try:
        # Request AI analysis
        ai_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert pharmaceutical AI specializing in prescription analysis. Extract ALL medicine names from text, even if mentioned casually. Return valid JSON with a medicines array containing objects with name and dose fields."
                },
                {
                    "role": "user", 
                    "content": extraction_prompt
                }
            ],
            max_tokens=1200,
            temperature=0.05  # Very low for accuracy
        )
        
        ai_content = ai_response.choices[0].message.content.strip()
        print(f"AI extraction response received: {ai_content[:200]}...")
        
        # Parse and validate AI response
        try:
            parsed_result = json.loads(ai_content)
            
            # Validate medicines array
            medicines = parsed_result.get('medicines', [])
            validated_medicines = []
            
            for medicine in medicines:
                if isinstance(medicine, dict) and medicine.get('name'):
                    validated_medicine = {
                        'name': medicine.get('name', 'Unknown'),
                        'dose': medicine.get('dose', 'Not specified'),
                        'frequency': medicine.get('frequency', 'As prescribed'),
                        'instructions': medicine.get('instructions', 'Follow prescription'),
                        'drug_class': medicine.get('drug_class', 'Not specified'),
                        'primary_use': medicine.get('primary_use', 'Not specified'),
                        'confidence': medicine.get('confidence', 'Medium')
                    }
                    validated_medicines.append(validated_medicine)
            
            # Build final result
            final_result = {
                "medicines": validated_medicines,
                "ai_enhanced": True,
                "processing_method": "advanced_ai_extraction",
                "extraction_summary": {
                    "total_medicines": len(validated_medicines),
                    "high_confidence_count": len([m for m in validated_medicines if m.get('confidence') == 'High']),
                    "medium_confidence_count": len([m for m in validated_medicines if m.get('confidence') == 'Medium']),
                    "low_confidence_count": len([m for m in validated_medicines if m.get('confidence') == 'Low'])
                }
            }
            
            # Add other fields from AI response
            if 'clinical_notes' in parsed_result:
                final_result['clinical_notes'] = parsed_result['clinical_notes']
            
            print(f"Successfully extracted {len(validated_medicines)} medicines using AI:")
            for med in validated_medicines:
                print(f"  - {med['name']} ({med['dose']})")
            
            return final_result
            
        except json.JSONDecodeError as json_error:
            print(f"JSON parsing failed: {json_error}")
            print(f"Raw AI response: {ai_content}")
            
            # Try to extract medicines from raw text
            fallback_medicines = extract_medicines_from_ai_text(ai_content)
            
            return {
                "medicines": fallback_medicines,
                "ai_enhanced": True,
                "parsing_error": True,
                "raw_ai_response": ai_content[:500],
                "extraction_summary": {
                    "total_medicines": len(fallback_medicines),
                    "extraction_method": "AI with manual parsing"
                }
            }
            
    except Exception as ai_error:
        print(f"AI extraction failed: {ai_error}")
        
        # Return fallback extraction
        return perform_fallback_medicine_extraction(prescription_text)

def create_extraction_prompt(text_content):
    """Creates a detailed prompt for medicine extraction"""
    
    prompt = f"""
Extract ALL medications from this prescription text. Look for common drug names like Aspirin, Metoprolol, Lisinopril, etc.

PRESCRIPTION TEXT:
{text_content}

Instructions:
1. Find ALL medicine names (brand names, generic names, common drugs)
2. Extract dosages when available
3. Include administration frequency
4. Provide confidence level for each extraction

Return ONLY this JSON structure:
{{
    "medicines": [
        {{
            "name": "Medicine name (e.g., Aspirin, Metoprolol, Lisinopril)",
            "dose": "Dosage with units (e.g., 81mg, 50mg) or 'Not specified'",
            "frequency": "Administration frequency (e.g., once daily, twice daily)",
            "instructions": "Special instructions if any",
            "drug_class": "Therapeutic class if known",
            "primary_use": "Main therapeutic purpose",
            "confidence": "High/Medium/Low"
        }}
    ],
    "extraction_summary": {{
        "total_medicines": 0,
        "extraction_challenges": []
    }},
    "clinical_notes": "Any additional observations"
}}

IMPORTANT:
- Extract medicine names even if dosage is unclear
- Look for common drugs: Aspirin, Metoprolol, Lisinopril, Ibuprofen, Acetaminophen, etc.
- Return valid JSON only - no additional text
"""
    
    return prompt

def perform_fallback_medicine_extraction(prescription_text):
    """
    Fallback medicine extraction using pattern matching
    Used when AI is unavailable or fails
    """
    
    print("Using fallback medicine extraction")
    
    extracted_medicines = []
    text_lower = prescription_text.lower()
    
    # Comprehensive medicine database with common drugs
    medicine_database = {
        'aspirin': {
            'name': 'Aspirin',
            'typical_dose': '81mg',
            'frequency': 'Once daily',
            'drug_class': 'Antiplatelet',
            'primary_use': 'Cardiovascular protection'
        },
        'metoprolol': {
            'name': 'Metoprolol',
            'typical_dose': '50mg',
            'frequency': 'Twice daily',
            'drug_class': 'Beta-blocker',
            'primary_use': 'Blood pressure control'
        },
        'lisinopril': {
            'name': 'Lisinopril',
            'typical_dose': '10mg',
            'frequency': 'Once daily',
            'drug_class': 'ACE Inhibitor',
            'primary_use': 'Blood pressure control'
        },
        'ibuprofen': {
            'name': 'Ibuprofen',
            'typical_dose': '200mg',
            'frequency': 'Every 6-8 hours',
            'drug_class': 'NSAID',
            'primary_use': 'Pain relief'
        },
        'acetaminophen': {
            'name': 'Acetaminophen',
            'typical_dose': '500mg',
            'frequency': 'Every 6 hours',
            'drug_class': 'Analgesic',
            'primary_use': 'Pain relief'
        },
        'atorvastatin': {
            'name': 'Atorvastatin',
            'typical_dose': '20mg',
            'frequency': 'Once daily',
            'drug_class': 'Statin',
            'primary_use': 'Cholesterol control'
        },
        'omeprazole': {
            'name': 'Omeprazole',
            'typical_dose': '20mg',
            'frequency': 'Once daily',
            'drug_class': 'PPI',
            'primary_use': 'Acid reduction'
        },
        'metformin': {
            'name': 'Metformin',
            'typical_dose': '500mg',
            'frequency': 'Twice daily',
            'drug_class': 'Antidiabetic',
            'primary_use': 'Diabetes control'
        },
        'amlodipine': {
            'name': 'Amlodipine',
            'typical_dose': '5mg',
            'frequency': 'Once daily',
            'drug_class': 'Calcium Channel Blocker',
            'primary_use': 'Blood pressure control'
        },
        'simvastatin': {
            'name': 'Simvastatin',
            'typical_dose': '20mg',
            'frequency': 'Once daily',
            'drug_class': 'Statin',
            'primary_use': 'Cholesterol control'
        }
    }
    
    # Search for medicines in text
    for medicine_key, medicine_info in medicine_database.items():
        if medicine_key in text_lower:
            # Try to extract actual dosage and frequency
            actual_dose = extract_dosage_from_text(prescription_text, medicine_key)
            actual_frequency = extract_frequency_from_text(prescription_text, medicine_key)
            
            extracted_medicine = {
                'name': medicine_info['name'],
                'dose': actual_dose or medicine_info['typical_dose'],
                'frequency': actual_frequency or medicine_info['frequency'],
                'instructions': 'As prescribed',
                'drug_class': medicine_info['drug_class'],
                'primary_use': medicine_info['primary_use'],
                'confidence': 'High' if actual_dose else 'Medium'
            }
            
            extracted_medicines.append(extracted_medicine)
    
    print(f"Fallback extraction found {len(extracted_medicines)} medicines:")
    for med in extracted_medicines:
        print(f"  - {med['name']} ({med['dose']})")
    
    return {
        'medicines': extracted_medicines,
        'ai_enhanced': False,
        'processing_method': 'pattern_matching_fallback',
        'extraction_summary': {
            'total_medicines': len(extracted_medicines),
            'extraction_method': 'Fallback pattern matching'
        }
    }

def extract_medicines_from_ai_text(ai_text):
    """Extract medicines from AI response when JSON parsing fails"""
    
    medicines = []
    
    # Look for medicine names in AI response
    common_medicines = [
        'aspirin', 'metoprolol', 'lisinopril', 'ibuprofen', 'acetaminophen',
        'atorvastatin', 'omeprazole', 'metformin', 'amlodipine', 'simvastatin',
        'losartan', 'hydrochlorothiazide', 'levothyroxine', 'albuterol', 'prednisone'
    ]
    
    ai_text_lower = ai_text.lower()
    
    for medicine in common_medicines:
        if medicine in ai_text_lower:
            # Try to find dosage near medicine name
            import re
            dosage_pattern = f"{medicine}[\\s\\w]*?(\\d+(?:\\.\\d+)?\\s*(?:mg|ml|g|mcg))"
            dosage_match = re.search(dosage_pattern, ai_text_lower)
            
            dose = dosage_match.group(1) if dosage_match else "Not specified"
            
            medicines.append({
                'name': medicine.title(),
                'dose': dose,
                'frequency': 'As prescribed',
                'instructions': 'Follow prescription',
                'drug_class': 'Not specified',
                'primary_use': 'As prescribed',
                'confidence': 'Medium'
            })
    
    return medicines

def extract_dosage_from_text(text, medicine_name):
    """Extract actual dosage information for a medicine from text"""
    import re
    
    # Pattern to find dosages near medicine names
    dosage_pattern = r'(\d+(?:\.\d+)?\s*(?:mg|ml|g|mcg|units?))'
    
    # Look for dosage within 50 characters of medicine name
    medicine_index = text.lower().find(medicine_name.lower())
    if medicine_index != -1:
        surrounding_text = text[max(0, medicine_index-25):medicine_index+75]
        dosage_match = re.search(dosage_pattern, surrounding_text, re.IGNORECASE)
        if dosage_match:
            return dosage_match.group(1)
    
    return None

def extract_frequency_from_text(text, medicine_name):
    """Extract frequency information for a medicine from text"""
    import re
    
    frequency_patterns = [
        r'(once\s+daily|daily|od)',
        r'(twice\s+daily|bid|b\.i\.d\.)',
        r'(three\s+times\s+daily|tid|t\.i\.d\.)',
        r'(every\s+\d+\s+hours?)',
        r'(as\s+needed|prn|p\.r\.n\.)'
    ]
    
    medicine_index = text.lower().find(medicine_name.lower())
    if medicine_index != -1:
        surrounding_text = text[max(0, medicine_index-25):medicine_index+100]
        
        for pattern in frequency_patterns:
            frequency_match = re.search(pattern, surrounding_text, re.IGNORECASE)
            if frequency_match:
                return frequency_match.group(1)
    
    return None

@ai_nlp_bp.route('/identify-unknown', methods=['POST'])
def identify_unknown_medicine():
    """
    Comprehensive medicine identification system
    Handles misspellings, abbreviations, and unknown drug names
    """
    try:
        request_data = request.get_json()
        unknown_medicine = request_data.get('medicine', '').strip()
        
        if not unknown_medicine:
            return jsonify({"error": "No medicine name provided"}), 400
        
        print(f"Identifying unknown medicine: '{unknown_medicine}'")
        
        if not client:
            return jsonify({
                "error": "Identification service unavailable",
                "identification": {"corrected_name": unknown_medicine, "confidence": "Low"}
            }), 503
        
        # Perform comprehensive medicine identification
        identification_result = perform_medicine_identification(unknown_medicine)
        
        return jsonify(identification_result)
        
    except Exception as identification_error:
        print(f"Medicine identification failed: {str(identification_error)}")
        return jsonify({
            "error": "Identification failed",
            "details": str(identification_error)
        }), 500

def perform_medicine_identification(medicine_name):
    """
    Comprehensive medicine identification with clinical context
    Handles various scenarios including misspellings and abbreviations
    """
    
    # Build identification prompt
    identification_prompt = create_identification_prompt(medicine_name)
    
    try:
        # Request comprehensive AI analysis
        ai_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a pharmaceutical database expert with comprehensive knowledge of global medications, drug safety, and clinical pharmacology. You can identify medications from partial names, misspellings, and abbreviations."
                },
                {
                    "role": "user", 
                    "content": identification_prompt
                }
            ],
            max_tokens=1400,
            temperature=0.1  # Low temperature for accurate identification
        )
        
        ai_content = ai_response.choices[0].message.content.strip()
        
        # Parse identification results
        try:
            identification_data = json.loads(ai_content)
            
            # Add processing metadata
            identification_data["ai_identification"] = True
            identification_data["identification_method"] = "comprehensive_ai_analysis"
            
            # Log identification success
            confidence = identification_data.get('identification', {}).get('confidence', 'Unknown')
            corrected_name = identification_data.get('identification', {}).get('corrected_name', medicine_name)
            print(f"Medicine identification complete: '{corrected_name}' (confidence: {confidence})")
            
            return identification_data
            
        except json.JSONDecodeError as parse_error:
            print(f"Identification JSON parsing failed: {parse_error}")
            
            # Create fallback identification
            return {
                "identification": {
                    "corrected_name": medicine_name,
                    "confidence": "Low",
                    "generic_name": "Unknown",
                    "parsing_error": True
                },
                "ai_identification": True,
                "error_details": "Response parsing failed",
                "raw_analysis": ai_content[:300]
            }
            
    except Exception as identification_error:
        print(f"Medicine identification process failed: {identification_error}")
        
        # Return minimal identification data
        return {
            "identification": {
                "corrected_name": medicine_name,
                "confidence": "Low",
                "generic_name": "Unknown",
                "analysis_failed": True
            },
            "ai_identification": False,
            "error_details": str(identification_error)
        }

def create_identification_prompt(medicine_name):
    """Creates comprehensive prompt for medicine identification"""
    
    prompt = f"""
Analyze and identify this potentially unknown, misspelled, or abbreviated medicine name:

MEDICINE TO IDENTIFY: "{medicine_name}"

Provide comprehensive pharmaceutical analysis including:

1. MEDICINE IDENTIFICATION:
   - Most likely correct spelling/name
   - Generic name (INN/USAN)
   - Common brand names globally
   - Alternative spellings or abbreviations
   - Confidence in identification

2. PHARMACEUTICAL DETAILS:
   - Therapeutic class and subclass
   - Active ingredient(s)
   - Mechanism of action summary
   - Available dosage forms and strengths
   - Route(s) of administration

3. CLINICAL INFORMATION:
   - Primary therapeutic indications
   - Common off-label uses
   - Typical dosing ranges
   - Duration of treatment

4. SAFETY PROFILE:
   - Major contraindications
   - Important drug interactions
   - Common adverse effects
   - Serious side effects to monitor

5. SPECIAL CONSIDERATIONS:
   - Age-specific warnings (pediatric, geriatric)
   - Pregnancy/lactation considerations
   - Renal/hepatic dosing adjustments
   - Monitoring requirements

Respond with this JSON format:
{{
    "identification": {{
        "corrected_name": "Most likely correct name",
        "confidence": "High/Medium/Low/Very Low",
        "generic_name": "International generic name",
        "brand_names": ["Common brand names"],
        "alternative_spellings": ["Possible variations"],
        "identification_reasoning": "Why this identification was chosen"
    }},
    "pharmaceutical_info": {{
        "therapeutic_class": "Primary therapeutic class",
        "active_ingredients": ["Active components"],
        "mechanism_of_action": "How the drug works",
        "dosage_forms": ["Available formulations"],
        "administration_routes": ["How it's given"]
    }},
    "clinical_use": {{
        "primary_indications": ["Main uses"],
        "common_off_label": ["Off-label uses"],
        "typical_dosing": "Standard dosing information",
        "treatment_duration": "Typical treatment length"
    }},
    "safety_information": {{
        "contraindications": ["When not to use"],
        "major_interactions": ["Important drug interactions"],
        "common_side_effects": ["Frequent adverse effects"],
        "serious_reactions": ["Severe adverse effects to watch for"]
    }},
    "special_populations": {{
        "pediatric_considerations": "Use in children",
        "geriatric_considerations": "Use in elderly",
        "pregnancy_category": "Pregnancy safety category",
        "renal_considerations": "Kidney function adjustments",
        "hepatic_considerations": "Liver function adjustments"
    }},
    "monitoring": {{
        "required_monitoring": ["What to monitor"],
        "monitoring_frequency": "How often to check",
        "target_parameters": ["Normal ranges/goals"]
    }},
    "database_match_status": "Found/Partial_Match/Not_Found/Uncertain"
}}

Provide thorough analysis based on pharmaceutical knowledge and clinical experience.
"""
    
    return prompt

# Helper function for logging and debugging
def log_processing_stats(operation_type, input_data, result_data):
    """Log processing statistics for monitoring and debugging"""
    
    try:
        if operation_type == "extraction":
            medicine_count = len(result_data.get('medicines', []))
            text_length = len(input_data)
            print(f"Extraction Stats: {medicine_count} medicines from {text_length} characters")
            
        elif operation_type == "identification":
            confidence = result_data.get('identification', {}).get('confidence', 'Unknown')
            print(f"Identification Stats: '{input_data}' -> confidence: {confidence}")
            
    except Exception as logging_error:
        print(f"Logging error: {logging_error}")

# Validation helper for extracted medicines
def validate_extraction_result(extraction_data):
    """Validates extraction results for completeness and accuracy"""
    
    required_fields = ['medicines', 'extraction_summary']
    
    for field in required_fields:
        if field not in extraction_data:
            print(f"Warning: Missing required field '{field}' in extraction result")
            return False
    
    medicines = extraction_data.get('medicines', [])
    for idx, medicine in enumerate(medicines):
        if not medicine.get('name'):
            print(f"Warning: Medicine {idx} missing name field")
            
    return True