from flask import Blueprint, request, jsonify
import base64
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

ai_ocr_bp = Blueprint('ai_ocr', __name__)

def setup_ai_client():
    """Initialize AI client with proper error handling"""
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        try:
            return Groq(api_key=api_key)
        except Exception as e:
            print(f"Failed to initialize Groq client: {e}")
            return None
    else:
        print("Warning: GROQ_API_KEY not found")
        return None

client = setup_ai_client()

@ai_ocr_bp.route('/enhance-text', methods=['POST'])
def enhance_ocr_text():
    """Use AI to clean up messy OCR text and extract medicines"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        messy_text = data.get('text', '')
        
        if not messy_text.strip():
            return jsonify({"error": "No text provided for enhancement"}), 400
        
        print(f"AI OCR processing: {messy_text[:100]}...")
        
        if not client:
            return jsonify({
                "error": "AI OCR service unavailable",
                "cleaned_text": messy_text,
                "medicines": [],
                "ai_processed": False,
                "confidence": "Low"
            }), 503
            
        # Clean up OCR text with AI
        enhanced_result = ai_enhance_prescription_text(messy_text)
        
        # Validate medicine data
        if 'medicines' in enhanced_result:
            enhanced_result['medicines'] = validate_and_format_medicines(enhanced_result['medicines'])
        
        return jsonify(enhanced_result)
        
    except Exception as e:
        print(f"AI OCR error: {str(e)}")
        return jsonify({
            "error": str(e),
            "cleaned_text": messy_text if 'messy_text' in locals() else "",
            "medicines": [],
            "ai_processed": False
        }), 500

def validate_and_format_medicines(medicines):
    """Validate and format medicine data from AI response"""
    validated_medicines = []
    
    for medicine in medicines:
        if isinstance(medicine, dict) and medicine.get('name'):
            validated_medicine = {
                'name': medicine.get('name', 'Unknown'),
                'dose': medicine.get('dose', 'Not specified'),
                'frequency': medicine.get('frequency', 'As prescribed'),
                'instructions': medicine.get('instructions', 'Follow prescription')
            }
            validated_medicines.append(validated_medicine)
    
    return validated_medicines

@ai_ocr_bp.route('/extract-handwritten', methods=['POST'])
def extract_handwritten():
    """Special AI processing for handwritten prescriptions"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        print("🖊️ Processing handwritten prescription with AI...")
        
        result = ai_process_handwritten_prescription(text)
        return jsonify(result)
        
    except Exception as e:
        print(f"Handwritten processing error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def ai_enhance_prescription_text(messy_text):
    """Use AI to fix OCR errors and extract structured data"""
    
    prompt = f"""
You are a medical AI expert in prescription analysis. Fix this messy OCR text from a prescription and extract medicine information:

MESSY OCR TEXT:
{messy_text}

Tasks:
1. Fix spelling errors and OCR mistakes
2. Identify all medications mentioned
3. Extract dosages and frequencies
4. Correct medical terminology

Return response in this JSON format:
{{
    "cleaned_text": "Fixed and readable prescription text",
    "medicines": [
        {{"name": "Medicine Name", "dose": "Amount", "frequency": "Instructions"}},
    ],
    "patient_info": {{"age": "if found", "name": "if found"}},
    "doctor_info": {{"name": "if found", "clinic": "if found"}},
    "confidence": "High/Medium/Low",
    "corrections_made": ["List of corrections"]
}}

Focus on medical accuracy. If uncertain, indicate in confidence level.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a medical AI specialist in prescription text processing and OCR error correction. You have extensive knowledge of medical terminology and prescription formats."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.1
        )
        
        ai_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON response
        try:
            result = json.loads(ai_text)
            result["ai_processed"] = True
            print("✅ AI OCR enhancement successful!")
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, return structured fallback
            return {
                "cleaned_text": ai_text,
                "medicines": [],
                "ai_processed": True,
                "confidence": "Low",
                "error": "JSON parsing failed but got AI response"
            }
            
    except Exception as e:
        print(f"AI OCR enhancement failed: {e}")
        return {
            "cleaned_text": messy_text,
            "medicines": [],
            "ai_processed": False,
            "error": str(e)
        }

def ai_process_handwritten_prescription(text):
    """Special AI processing for handwritten prescriptions"""
    
    prompt = f"""
You are a medical AI specialized in interpreting handwritten prescriptions. This text comes from handwritten prescription OCR:

HANDWRITTEN TEXT:
{text}

Handwritten prescriptions often have:
- Abbreviated medicine names
- Unclear dosages
- Medical shorthand
- Poor handwriting artifacts

Tasks:
1. Interpret medical abbreviations and shorthand
2. Expand abbreviated medicine names to full names
3. Clarify unclear dosages
4. Identify potential OCR misreads of common medicines

Return JSON:
{{
    "interpreted_medicines": [
        {{
            "original_text": "what OCR found",
            "interpreted_name": "corrected medicine name", 
            "dose": "clarified dosage",
            "confidence": "High/Medium/Low",
            "alternative_names": ["possible alternatives"]
        }}
    ],
    "doctor_notes": "any special instructions found",
    "interpretation_notes": "explanation of corrections made",
    "overall_confidence": "High/Medium/Low"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a medical AI expert in handwritten prescription interpretation with knowledge of medical abbreviations, shorthand, and common prescription patterns."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.2
        )
        
        ai_result = response.choices[0].message.content.strip()
        
        try:
            result = json.loads(ai_result)
            result["processing_type"] = "handwritten"
            print("✅ Handwritten prescription AI processing complete!")
            return result
        except json.JSONDecodeError:
            return {
                "interpreted_medicines": [],
                "interpretation_notes": ai_result,
                "processing_type": "handwritten",
                "error": "JSON parsing failed"
            }
            
    except Exception as e:
        print(f"Handwritten AI processing failed: {e}")
        return {
            "interpreted_medicines": [],
            "error": str(e),
            "processing_type": "handwritten"
        }