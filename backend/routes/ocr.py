from flask import Blueprint, request, jsonify
import pytesseract
from PIL import Image
import io
import os
import tempfile
import json
from werkzeug.utils import secure_filename

# Import our enhanced OCR service
from services.ocr_service import extract_text_from_image, extract_text_from_base64

ocr_bp = Blueprint('ocr', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ocr_bp.route('/scan', methods=['POST'])
def ocr_scan():
    """
    Enhanced OCR scan endpoint that handles file uploads and returns structured medication data
    """
    print("OCR scan endpoint called")
    print("Request files:", list(request.files.keys()) if request.files else "No files")
    print("Request form:", dict(request.form) if request.form else "No form data")
    
    try:
        # Handle file upload
        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed. Please upload PNG, JPG, JPEG, or PDF files."}), 400
        
        # Get patient info from form data
        patient_age = request.form.get('patientAge', '30')
        patient_condition = request.form.get('patientCondition', '')
        
        print(f"Processing file: {file.filename}")
        print(f"Patient age: {patient_age}, Condition: {patient_condition}")
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Extract text using enhanced OCR
            extracted_text = extract_text_from_image(temp_path)
            print(f"OCR extracted text: {extracted_text[:200]}...")
            
            if not extracted_text.strip():
                return jsonify({
                    "error": "No text could be extracted from the image",
                    "extracted_text": "",
                    "medicines": [],
                    "confidence": "Low"
                }), 400
            
            # Simple medicine extraction (you can enhance this with AI)
            medicines = extract_medicines_from_text(extracted_text)
            
            # Calculate confidence based on extracted medicines
            confidence = "High" if len(medicines) > 0 else "Medium" if extracted_text.strip() else "Low"
            
            result = {
                "success": True,
                "extracted_text": extracted_text,
                "medicines": medicines,
                "confidence": confidence,
                "patient_age": patient_age,
                "patient_condition": patient_condition,
                "processing_method": "Enhanced OCR"
            }
            
            print(f"OCR processing complete. Found {len(medicines)} medicines.")
            return jsonify(result)
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        print(f"OCR scan error: {str(e)}")
        return jsonify({
            "error": f"OCR processing failed: {str(e)}",
            "extracted_text": "",
            "medicines": [],
            "confidence": "Low"
        }), 500

def extract_medicines_from_text(text):
    """
    Extract medicine information from OCR text
    This is a basic implementation - you can enhance with AI/ML
    """
    medicines = []
    lines = text.split('\n')
    
    # Common medicine keywords and patterns
    medicine_keywords = [
        'tablet', 'capsule', 'syrup', 'mg', 'ml', 'injection', 
        'drops', 'cream', 'ointment', 'daily', 'twice', 'thrice'
    ]
    
    # Common medicine names (you can expand this list)
    common_medicines = [
        'paracetamol', 'ibuprofen', 'aspirin', 'amoxicillin', 'metformin',
        'lisinopril', 'simvastatin', 'omeprazole', 'amlodipine', 'warfarin',
        'prednisone', 'furosemide', 'atorvastatin', 'losartan', 'gabapentin'
    ]
    
    for line in lines:
        line_lower = line.lower().strip()
        if not line_lower:
            continue
            
        # Check if line contains medicine-related keywords
        has_medicine_keyword = any(keyword in line_lower for keyword in medicine_keywords)
        has_medicine_name = any(med in line_lower for med in common_medicines)
        
        if has_medicine_keyword or has_medicine_name:
            # Try to extract medicine information
            medicine_info = parse_medicine_line(line)
            if medicine_info:
                medicines.append(medicine_info)
    
    return medicines

def parse_medicine_line(line):
    """
    Parse a line of text to extract medicine information
    """
    try:
        # Basic parsing - you can make this more sophisticated
        words = line.split()
        
        # Look for medicine name (usually the first meaningful word)
        medicine_name = ""
        dosage = ""
        form = "tablet"  # default
        
        for i, word in enumerate(words):
            word_lower = word.lower()
            
            # Try to identify medicine name
            if not medicine_name and len(word) > 2 and word.isalpha():
                medicine_name = word
            
            # Try to identify dosage
            if 'mg' in word_lower or 'ml' in word_lower:
                dosage = word
            
            # Try to identify form
            forms = ['tablet', 'capsule', 'syrup', 'injection', 'cream', 'drops']
            for form_type in forms:
                if form_type in word_lower:
                    form = form_type
                    break
        
        if medicine_name:
            return {
                "name": medicine_name,
                "dosage": dosage or "Not specified",
                "form": form,
                "frequency": "As directed",
                "instructions": line.strip()
            }
    
    except Exception as e:
        print(f"Error parsing medicine line '{line}': {e}")
    
    return None

@ocr_bp.route('/test', methods=['GET'])
def test_ocr():
    """Test endpoint to verify OCR service is working"""
    return jsonify({
        "status": "OCR service is running",
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "endpoint": "/ocr/scan"
    })