from flask import Blueprint, request, jsonify
import re

nlp_bp = Blueprint('nlp', __name__)

@nlp_bp.route('/extract', methods=['POST'])
def nlp_extract():
    try:
        data = request.get_json()
        text = data.get('text', '')
        print(f"NLP processing text: {text[:100]}...")
        
        # Simple medicine extraction
        medicines = extract_medicines_simple(text)
        print(f"Extracted medicines: {medicines}")
        
        return jsonify({"medicines": medicines})
    except Exception as e:
        print(f"NLP error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def extract_medicines_simple(text):
    """Simple medicine extraction that actually works"""
    medicines = []
    
    # Look for medicine patterns in each line
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
            
        # Pattern 1: Medicine with dose
        pattern1 = r'([A-Za-z][A-Za-z\s]+?)\s+(\d+(?:\.\d+)?)\s*(mg|g|ml)'
        matches = re.findall(pattern1, line, re.IGNORECASE)
        for match in matches:
            name = match[0].strip()
            dose = f"{match[1]}{match[2]}"
            if len(name) > 2:
                medicines.append({"name": name.title(), "dose": dose})
        
        # Pattern 2: Just medicine names (common ones)
        common_medicines = ['aspirin', 'metformin', 'lisinopril', 'atorvastatin', 'metoprolol', 
                          'hydroxyzine', 'lorazepam', 'tramadol', 'omeprazole', 'simvastatin']
        
        for med in common_medicines:
            if med.lower() in line.lower():
                # Check if we already have this medicine
                if not any(m['name'].lower() == med for m in medicines):
                    medicines.append({"name": med.title(), "dose": "As prescribed"})
    
    return medicines[:10]  