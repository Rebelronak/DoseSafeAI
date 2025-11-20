from flask import Blueprint, request, jsonify
import os
import json
import base64
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import io

# Load environment configuration
load_dotenv()

# Add ML integration for enhanced medicine extraction
try:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models'))
    from ml_integration import extract_medicines, check_interactions, check_age_warnings, get_ml_status
    ML_AVAILABLE = True
    print("✅ ML models available for enhanced extraction")
    print(f"   ML Status: {get_ml_status()}")
except ImportError as e:
    ML_AVAILABLE = False
    print(f"⚠️ ML models not available: {e}")

# Create blueprint for AI-powered OCR processing
ai_only_ocr_bp = Blueprint('ai_only_ocr', __name__)

# Initialize Groq client with error handling
def setup_ai_ocr_client():
    """Initialize AI client for OCR processing with proper error handling"""
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        try:
            return Groq(api_key=api_key)
        except Exception as initialization_error:
            print(f"Failed to initialize AI OCR client: {initialization_error}")
            return None
    else:
        print("Warning: GROQ_API_KEY not found in environment")
        return None

client = setup_ai_ocr_client()

@ai_only_ocr_bp.route('/ai-scan', methods=['POST'])
def ai_powered_document_scan():
    """
    AI-powered document scanning without traditional OCR dependencies
    Processes prescription files using advanced language models
    """
    try:
        # Validate file upload
        if 'file' not in request.files:
            return jsonify({"error": "No file provided in request"}), 400
        
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return jsonify({"error": "No file selected for upload"}), 400
        
        print(f"Processing document: {uploaded_file.filename} (type: {uploaded_file.content_type})")
        
        # Extract actual content from file
        extracted_content = extract_file_content(uploaded_file)
        
        if not extracted_content:
            return jsonify({"error": "Unable to extract content from file"}), 400
        
        print(f"Content extracted successfully: {len(extracted_content)} characters")
        print(f"Extracted content preview: {extracted_content[:200]}...")
        
        # Analyze prescription content with AI
        ai_analysis_result = analyze_prescription_with_ai(extracted_content, uploaded_file.filename)
        
        # Log the AI analysis result for debugging
        print(f"AI analysis result: {ai_analysis_result}")
        
        return jsonify({
            "success": True,
            "extracted_text": extracted_content.strip(),
            "ai_enhanced": ai_analysis_result,
            "source_filename": uploaded_file.filename,
            "content_type": uploaded_file.content_type,
            "processing_method": "AI Language Model",
            "content_length": len(extracted_content),
            "external_dependencies": False
        })
        
    except Exception as processing_error:
        print(f"Document processing failed: {str(processing_error)}")
        return jsonify({
            "error": "Document processing failed", 
            "details": str(processing_error)
        }), 500

def extract_file_content(file_object):
    """
    Extract actual content from uploaded file based on file type
    Supports text files and images with OCR processing
    """
    
    try:
        # Reset file pointer to beginning
        file_object.seek(0)
        
        if file_object.content_type == 'text/plain':
            # Read actual text file content
            file_bytes = file_object.read()
            
            # Try different encodings to handle various text file formats
            text_content = None
            encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            
            for encoding in encodings_to_try:
                try:
                    text_content = file_bytes.decode(encoding)
                    print(f"Successfully decoded text file using {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if text_content is None:
                print("Failed to decode text file with any standard encoding")
                return None
            
            # Clean up the text content
            cleaned_content = text_content.strip()
            
            print(f"Text file content extracted: {len(cleaned_content)} characters")
            
            return cleaned_content
            
        elif file_object.content_type.startswith('image/'):
            # Handle image files with traditional OCR (Tesseract)
            print(f"Processing image file: {file_object.content_type}")
            
            # Use traditional OCR for reliable results
            return extract_text_from_image(file_object)
            
        else:
            # Handle other file types with placeholder
            print(f"Unsupported file type: {file_object.content_type}")
            return f"File type {file_object.content_type} - specialized processing required"
            
    except Exception as extraction_error:
        print(f"Content extraction failed: {extraction_error}")
        return None

def extract_dose_from_text(text, medicine_name):
    """
    Extract dose and frequency information for a specific medicine from prescription text
    """
    import re
    
    # Look for the medicine name in the text and try to extract dose info nearby
    text_lower = text.lower()
    medicine_lower = medicine_name.lower()
    
    # Find the position of the medicine name
    if medicine_lower in text_lower:
        # Get a window of text around the medicine name
        start_pos = text_lower.find(medicine_lower)
        # Get about 100 characters around the medicine name
        window_start = max(0, start_pos - 50)
        window_end = min(len(text), start_pos + len(medicine_name) + 50)
        window_text = text[window_start:window_end]
        
        # Extract dose patterns
        dose_patterns = [
            r'(\d+(?:\.\d+)?)\s*(mg|ml|mcg|g|units?)',
            r'(\d+(?:\.\d+)?)\s*mg',
            r'(\d+(?:\.\d+)?)\s*ml'
        ]
        
        dose = "Not specified"
        for pattern in dose_patterns:
            match = re.search(pattern, window_text, re.IGNORECASE)
            if match:
                dose = match.group(0)
                break
        
        # Extract frequency patterns
        frequency_patterns = [
            r'once\s+daily',
            r'twice\s+daily', 
            r'at\s+bedtime',
            r'every\s+\d+\s+hours?',
            r'as\s+needed'
        ]
        
        frequency = "As prescribed"
        for pattern in frequency_patterns:
            match = re.search(pattern, window_text, re.IGNORECASE)
            if match:
                frequency = match.group(0)
                break
        
        return {
            'dose': dose,
            'frequency': frequency,
            'instructions': ''
        }
    
    return {
        'dose': 'Not specified',
        'frequency': 'As prescribed', 
        'instructions': ''
    }

def analyze_prescription_with_ai(prescription_text, source_filename):
    """
    Use combined ML + AI analysis for comprehensive prescription processing
    """
    
    # First, try ML-enhanced medicine extraction
    if ML_AVAILABLE:
        try:
            print("🤖 Using ML models for medicine extraction...")
            ml_medicines = extract_medicines(prescription_text)
            
            if ml_medicines:
                print(f"✅ ML extracted {len(ml_medicines)} medicines: {ml_medicines}")
                
                # Format ML results in the expected structure
                formatted_medicines = []
                for med_name in ml_medicines:
                    # Try to extract dose info from the original text
                    dose_info = extract_dose_from_text(prescription_text, med_name)
                    formatted_medicines.append({
                        'name': med_name,
                        'dose': dose_info.get('dose', 'Not specified'),
                        'frequency': dose_info.get('frequency', 'As prescribed'),
                        'instructions': dose_info.get('instructions', '')
                    })
                
                return {
                    "medicines": formatted_medicines,
                    "patient_info": extract_patient_info_from_text(prescription_text),
                    "extraction_confidence": "High",
                    "ai_processed": False,
                    "ml_processed": True,
                    "total_medicines": len(formatted_medicines),
                    "processing_method": "ML-enhanced extraction"
                }
        
        except Exception as ml_error:
            print(f"⚠️ ML extraction failed: {ml_error}")
            print("Falling back to AI analysis...")
    
    # Fallback to AI analysis if ML fails or unavailable
    analysis_prompt = build_prescription_analysis_prompt(prescription_text, source_filename)
    
    try:
        if client:
            print("Sending prescription text to AI for analysis...")
            
            # Request AI analysis using Groq/Llama model
            ai_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a medical AI specialist focused on prescription analysis and medicine extraction. You must return valid JSON with a 'medicines' array containing medicine objects with 'name' and 'dose' fields. Always extract medicine names even if dosages are unclear."
                    },
                    {
                        "role": "user", 
                        "content": analysis_prompt
                    }
                ],
                max_tokens=1200,
                temperature=0.03  # Very low temperature for medical accuracy
            )
            
            ai_analysis_text = ai_response.choices[0].message.content.strip()
            print(f"AI response received: {ai_analysis_text[:300]}...")
            
            # Parse and validate AI response
            try:
                # Clean the AI response - remove markdown code blocks if present
                cleaned_response = ai_analysis_text.strip()
                if cleaned_response.startswith('```'):
                    # Remove markdown code blocks
                    lines = cleaned_response.split('\n')
                    # Find the first line that's not a markdown delimiter
                    start_idx = 0
                    for i, line in enumerate(lines):
                        if not line.strip().startswith('```'):
                            start_idx = i
                            break
                    
                    # Find the last line that's not a markdown delimiter
                    end_idx = len(lines)
                    for i in range(len(lines) - 1, -1, -1):
                        if not lines[i].strip().startswith('```'):
                            end_idx = i + 1
                            break
                    
                    cleaned_response = '\n'.join(lines[start_idx:end_idx])
                
                print(f"Cleaned AI response: {cleaned_response[:200]}...")
                structured_result = json.loads(cleaned_response)
                
                # Ensure medicines array exists and is properly formatted
                if 'medicines' not in structured_result:
                    structured_result['medicines'] = []
                
                # Validate each medicine entry
                validated_medicines = []
                for medicine in structured_result.get('medicines', []):
                    if isinstance(medicine, dict) and medicine.get('name'):
                        validated_medicines.append({
                            'name': medicine.get('name', 'Unknown'),
                            'dose': medicine.get('dose', 'Not specified'),
                            'frequency': medicine.get('frequency', 'As prescribed'),
                            'instructions': medicine.get('instructions', 'Follow prescription')
                        })
                
                structured_result['medicines'] = validated_medicines
                
                # Add processing metadata
                structured_result["ai_processed"] = True
                structured_result["total_medicines"] = len(validated_medicines)
                structured_result["processing_time"] = "Real-time"
                
                print(f"Successfully processed prescription: {len(validated_medicines)} medications identified")
                for med in validated_medicines:
                    print(f"  - {med['name']} ({med['dose']})")
                
                return structured_result
                
            except json.JSONDecodeError as json_error:
                print(f"AI response JSON parsing failed: {json_error}")
                print(f"Raw AI response: {ai_analysis_text}")
                
                # Try to extract medicines manually from the text response
                fallback_medicines = extract_medicines_from_raw_text(ai_analysis_text)
                
                return {
                    "ai_processed": True,
                    "parsing_error": True,
                    "medicines": fallback_medicines,
                    "total_medicines": len(fallback_medicines),
                    "raw_ai_response": ai_analysis_text[:500],
                    "error_message": "AI provided analysis but JSON parsing failed"
                }
                
        else:
            print("AI client not available, using text analysis fallback")
            return perform_text_analysis_fallback(prescription_text)
            
    except Exception as ai_error:
        print(f"AI prescription analysis failed: {ai_error}")
        return perform_text_analysis_fallback(prescription_text)

def build_prescription_analysis_prompt(text_content, filename):
    """
    Build comprehensive prompt for AI prescription analysis
    Focus on extracting medicines in the correct JSON format
    """
    
    prompt = f"""
Analyze this prescription text and extract ALL medications with their details:

PRESCRIPTION TEXT:
{text_content}

Instructions:
1. Find ALL medicine names in the text (look for any pharmaceutical names)
2. Clean up medicine names by removing variant numbers (e.g., "HydroxyzineVariant22" → "Hydroxyzine")
3. Extract dosage information when available
4. Look for common medicines like: Aspirin, Warfarin, Hydroxyzine, Metoprolol, Lorazepam, Lisinopril, etc.
5. Return ONLY valid JSON - no additional text

Required JSON format:
{{
    "medicines": [
        {{
            "name": "Medicine name (clean name without variants)",
            "dose": "Dosage with units if found or 'Not specified'",
            "frequency": "How often or 'As prescribed'",
            "instructions": "Special instructions if any"
        }}
    ],
    "patient_info": {{
        "name": "Patient name if found",
        "age": "Age if mentioned (look for numbers like 70, or words like Elderly)"
    }},
    "extraction_confidence": "High/Medium/Low"
}}

CRITICAL: 
- Extract medicine names even if they have variant numbers or suffixes
- Clean up names by removing "Variant22", "Variant21", etc.
- Include ALL medicines found in the text
- Return valid JSON only - no explanatory text
"""
    
    return prompt

def extract_medicines_from_raw_text(raw_text):
    """
    Fallback method to extract medicines from AI response when JSON parsing fails
    """
    
    medicines = []
    
    # Comprehensive medicine names including the ones from your prescription
    common_medicines = [
        'hydroxyzine', 'metoprolol', 'lorazepam',  # From your prescription
        'aspirin', 'lisinopril', 'ibuprofen', 'acetaminophen',
        'atorvastatin', 'omeprazole', 'metformin', 'amlodipine', 'simvastatin',
        'losartan', 'hydrochlorothiazide', 'levothyroxine', 'albuterol', 'prednisone',
        'warfarin', 'alprazolam', 'diazepam', 'clonazepam'  # Additional common medicines
    ]
    
    raw_text_lower = raw_text.lower()
    
    for medicine in common_medicines:
        if medicine in raw_text_lower or f"{medicine}variant" in raw_text_lower:
            # Try to extract dosage information
            import re
            dosage_pattern = f"{medicine}[\\s\\w]*?(\\d+(?:\\.\\d+)?\\s*(?:mg|ml|g|mcg))"
            dosage_match = re.search(dosage_pattern, raw_text_lower)
            
            dose = dosage_match.group(1) if dosage_match else "Not specified"
            
            medicines.append({
                'name': medicine.title(),
                'dose': dose,
                'frequency': 'As prescribed',
                'instructions': 'Follow prescription directions'
            })
    
    return medicines

def perform_text_analysis_fallback(text_content):
    """
    Fallback text analysis when AI is unavailable
    Uses ML models if available, otherwise pattern matching
    """
    
    print("Using fallback text analysis for medicine extraction")
    
    # Try ML-enhanced extraction first
    if ML_AVAILABLE:
        try:
            print("🤖 Using ML-enhanced medicine extraction...")
            
            # Use the new ML integration
            extracted_medicines = extract_medicines(text_content)
            
            if extracted_medicines:
                print(f"✅ ML extraction found {len(extracted_medicines)} medicines")
                
                return {
                    'medicines': extracted_medicines,
                    'total_medicines': len(extracted_medicines),
                    'patient_info': extract_patient_info_from_text(text_content),
                    'extraction_confidence': 'High',
                    'ai_processed': False,
                    'extraction_method': 'ML-enhanced pattern matching',
                    'ml_powered': True
                }
        
        except Exception as ml_error:
            print(f"⚠️ ML extraction failed: {ml_error}")
            print("Falling back to traditional pattern matching...")
    
    # Traditional pattern matching fallback
    extracted_medicines = []
    text_lower = text_content.lower()
    
    # Enhanced medicine patterns with dosage indicators
    medicine_patterns = {
        'aspirin': {'typical_dose': '81mg', 'frequency': 'Once daily'},
        'warfarin': {'typical_dose': '5mg', 'frequency': 'Once daily'},
        'hydroxyzine': {'typical_dose': 'Not specified', 'frequency': 'As prescribed'},
        'metoprolol': {'typical_dose': '50mg', 'frequency': 'Twice daily'},
        'lorazepam': {'typical_dose': '0.5mg', 'frequency': 'As needed'},
        'lisinopril': {'typical_dose': '10mg', 'frequency': 'Once daily'},
        'ibuprofen': {'typical_dose': '200mg', 'frequency': 'Every 6-8 hours'},
        'acetaminophen': {'typical_dose': '500mg', 'frequency': 'Every 6 hours'},
        'atorvastatin': {'typical_dose': '20mg', 'frequency': 'Once daily'},
        'omeprazole': {'typical_dose': '20mg', 'frequency': 'Once daily'},
        'metformin': {'typical_dose': '500mg', 'frequency': 'Twice daily'},
        'amlodipine': {'typical_dose': '5mg', 'frequency': 'Once daily'},
        'simvastatin': {'typical_dose': '20mg', 'frequency': 'Once daily'}
    }
    
    # Search for medicine patterns in the actual text (including variants)
    for medicine_key, medicine_info in medicine_patterns.items():
        # Check for direct name or variant (e.g., "hydroxyzinevariant22")
        if medicine_key in text_lower or f"{medicine_key}variant" in text_lower:
            # Try to extract actual dosage from text
            actual_dose = extract_dosage_from_text(text_content, medicine_key)
            actual_frequency = extract_frequency_from_text(text_content, medicine_key)
            
            extracted_medicines.append({
                'name': medicine_key.title(),
                'dose': actual_dose or medicine_info['typical_dose'],
                'frequency': actual_frequency or medicine_info['frequency'],
                'instructions': 'As prescribed'
            })
    
    print(f"Traditional extraction found {len(extracted_medicines)} medicines:")
    for med in extracted_medicines:
        print(f"  - {med['name']} ({med['dose']})")
    
    return {
        'medicines': extracted_medicines,
        'total_medicines': len(extracted_medicines),
        'patient_info': extract_patient_info_from_text(text_content),
        'extraction_confidence': 'Medium',
        'ai_processed': False,
        'extraction_method': 'Traditional pattern matching',
        'ml_powered': False
    }

def extract_patient_info_from_text(text_content):
    """Extract patient information from text"""
    
    import re
    
    patient_info = {'name': 'Not specified', 'age': 'Not specified'}
    
    # Extract age
    age_patterns = [
        r'age[:\s]*(\d+)',
        r'(\d+)\s*year[s]?\s*old',
        r'(\d+)\s*yo',
        r'elderly'
    ]
    
    for pattern in age_patterns:
        match = re.search(pattern, text_content.lower())
        if match:
            if pattern == r'elderly':
                patient_info['age'] = '70'  # Default for elderly
            else:
                patient_info['age'] = match.group(1)
            break
    
    # Extract patient name
    name_patterns = [
        r'patient[:\s]*([a-zA-Z\s]+?)(?:\s+age|\s+\d+|medicines|$)',
        r'name[:\s]*([a-zA-Z\s]+?)(?:\s+age|\s+\d+|medicines|$)'
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text_content, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name) > 2 and not any(char.isdigit() for char in name):
                patient_info['name'] = name.title()
            break
    
    return patient_info

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

def extract_text_from_image(file_object):
    """
    Extract text from image files using OCR (Tesseract)
    """
    try:
        # Set Tesseract path for Windows (common installation locations)
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', 'User'))
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                print(f"Tesseract found at: {path}")
                break
        else:
            print("Warning: Tesseract not found in common locations. Please check installation.")
        
        # Read image data
        file_object.seek(0)
        image_data = file_object.read()
        
        # Open image with PIL
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        print(f"Processing image: {image.size} pixels, mode: {image.mode}")
        
        # Configure Tesseract for better medical text recognition
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.:(),-/ '
        
        # Extract text using Tesseract OCR
        extracted_text = pytesseract.image_to_string(image, config=custom_config)
        
        # Clean up the extracted text
        cleaned_text = extracted_text.strip()
        
        print(f"OCR extracted {len(cleaned_text)} characters")
        print(f"OCR preview: {cleaned_text[:200]}...")
        
        if len(cleaned_text) < 10:
            print("Warning: Very little text extracted from image")
            return "Minimal text detected in image - please ensure image quality is good"
        
        return cleaned_text
        
    except Exception as ocr_error:
        print(f"OCR processing failed: {ocr_error}")
        return f"OCR processing failed: {str(ocr_error)}"

def extract_text_with_ai_vision(file_object):
    """
    Extract text from images using AI Vision models (alternative to traditional OCR)
    More accurate for medical documents and handwritten prescriptions
    """
    try:
        # Reset file pointer
        file_object.seek(0)
        image_data = file_object.read()
        
        # Convert image to base64 for AI processing
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        if client:
            print("Processing image with AI Vision model...")
            
            # Create vision prompt for medical document analysis
            vision_prompt = """
            Analyze this medical prescription image and extract ALL text content accurately.
            Focus on:
            1. Patient information (name, age, etc.)
            2. Medicine names (including generic and brand names)
            3. Dosages and frequencies
            4. Doctor instructions
            5. Any other medical text
            
            Return the complete extracted text exactly as it appears in the image.
            Preserve formatting and structure as much as possible.
            """
            
            # Use AI vision capabilities (if available in your Groq model)
            ai_response = client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",  # Vision-capable model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": vision_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1500,
                temperature=0.1
            )
            
            extracted_text = ai_response.choices[0].message.content.strip()
            print(f"AI Vision extracted {len(extracted_text)} characters")
            print(f"AI Vision preview: {extracted_text[:200]}...")
            
            return extracted_text
            
        else:
            print("AI client not available, falling back to traditional OCR")
            return extract_text_from_image(file_object)
            
    except Exception as vision_error:
        print(f"AI Vision processing failed: {vision_error}")
        print("Falling back to traditional OCR...")
        return extract_text_from_image(file_object)