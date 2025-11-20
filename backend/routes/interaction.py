from flask import Blueprint, request, jsonify

interaction_bp = Blueprint('interaction', __name__)

@interaction_bp.route('/check', methods=['POST'])
def interaction_check():
    try:
        data = request.get_json()
        medicines = data.get('medicines', [])
        age = data.get('age', 30)
        
        print(f"Checking interactions for: {medicines}, age: {age}")
        
        # Extract medicine names from objects or use strings directly
        medicine_names = extract_medicine_names(medicines)
        print(f"Extracted medicine names: {medicine_names}")
        
        interactions = check_comprehensive_interactions(medicine_names)
        warnings = check_comprehensive_warnings(medicine_names, age)
        
        return jsonify({
            "interactions": interactions,
            "warnings": warnings,
            "medicine_count": len(medicine_names),
            "analysis_type": "comprehensive_interaction_check"
        })
        
    except Exception as e:
        print(f"Interaction error: {str(e)}")
        return jsonify({
            "error": str(e),
            "interactions": [],
            "warnings": []
        }), 500

def extract_medicine_names(medicines):
    """Extract medicine names from various input formats"""
    medicine_names = []
    
    for med in medicines:
        if isinstance(med, dict):
            # Medicine is an object with name field
            name = med.get('name', '').strip()
            if name:
                medicine_names.append(name)
        elif isinstance(med, str):
            # Medicine is already a string
            if med.strip():
                medicine_names.append(med.strip())
    
    print(f"Extracted {len(medicine_names)} medicine names: {medicine_names}")
    return medicine_names

def check_comprehensive_interactions(medicine_names):
    """Comprehensive interaction checking with detailed clinical information"""
    interactions = []
    
    # Expanded dangerous drug combinations with clinical details
    dangerous_combinations = {
        ('aspirin', 'warfarin'): {
            'severity': 'High',
            'clinical_effect': 'Significantly increased bleeding risk',
            'mechanism': 'Additive anticoagulant and antiplatelet effects',
            'management': 'Monitor INR closely, consider dose adjustment or alternative therapy'
        },
        ('hydroxyzine', 'lorazepam'): {
            'severity': 'High', 
            'clinical_effect': 'Excessive sedation and respiratory depression',
            'mechanism': 'Additive CNS depressant effects',
            'management': 'Avoid combination, use alternative medications'
        },
        ('metformin', 'alcohol'): {
            'severity': 'Moderate',
            'clinical_effect': 'Increased risk of lactic acidosis',
            'mechanism': 'Alcohol interferes with lactate metabolism',
            'management': 'Limit alcohol consumption, monitor for symptoms'
        },
        ('aspirin', 'ibuprofen'): {
            'severity': 'Moderate',
            'clinical_effect': 'Increased bleeding and GI ulceration risk',
            'mechanism': 'Dual NSAID effects on platelet function and GI mucosa',
            'management': 'Consider alternative pain relief, monitor for GI bleeding'
        },
        ('lisinopril', 'potassium'): {
            'severity': 'Moderate',
            'clinical_effect': 'Risk of hyperkalemia',
            'mechanism': 'ACE inhibitors reduce potassium excretion',
            'management': 'Monitor serum potassium levels regularly'
        },
        ('metoprolol', 'verapamil'): {
            'severity': 'High',
            'clinical_effect': 'Severe bradycardia and heart block',
            'mechanism': 'Additive effects on cardiac conduction',
            'management': 'Avoid combination, monitor ECG if necessary'
        },
        ('simvastatin', 'gemfibrozil'): {
            'severity': 'High',
            'clinical_effect': 'Increased risk of rhabdomyolysis',
            'mechanism': 'Gemfibrozil inhibits statin metabolism',
            'management': 'Use alternative statin or fibrate, monitor CK levels'
        },
        ('omeprazole', 'clopidogrel'): {
            'severity': 'Moderate',
            'clinical_effect': 'Reduced antiplatelet effectiveness',
            'mechanism': 'PPI inhibits clopidogrel activation',
            'management': 'Consider alternative PPI or antiplatelet agent'
        }
    }
    
    # Normalize medicine names for comparison
    normalized_names = [name.lower().strip() for name in medicine_names]
    
    # Check all combinations
    for i, med1 in enumerate(normalized_names):
        for j, med2 in enumerate(normalized_names[i+1:], i+1):
            # Check both orders of the combination
            combo1 = tuple(sorted([med1, med2]))
            combo2 = (med1, med2)
            combo3 = (med2, med1)
            
            interaction_data = None
            if combo1 in dangerous_combinations:
                interaction_data = dangerous_combinations[combo1]
            elif combo2 in dangerous_combinations:
                interaction_data = dangerous_combinations[combo2]
            elif combo3 in dangerous_combinations:
                interaction_data = dangerous_combinations[combo3]
            
            if interaction_data:
                interaction = {
                    'drug1': medicine_names[i],  # Use original case
                    'drug2': medicine_names[j],  # Use original case
                    'severity': interaction_data['severity'],
                    'clinical_effect': interaction_data['clinical_effect'],
                    'mechanism': interaction_data['mechanism'],
                    'management': interaction_data['management'],
                    'note': f"{interaction_data['clinical_effect']} - {interaction_data['management']}"
                }
                interactions.append(interaction)
    
    print(f"Found {len(interactions)} drug interactions")
    return interactions

def check_comprehensive_warnings(medicine_names, age):
    """Comprehensive age-based and condition-specific warnings"""
    warnings = []
    
    # Age-specific medication concerns
    if age >= 65:
        elderly_concerns = {
            'hydroxyzine': {
                'risk_level': 'High',
                'age_concern': 'Elderly patient population',
                'specific_risk': 'Increased fall risk, cognitive impairment, and prolonged sedation',
                'monitoring': 'Use lowest effective dose, monitor for confusion and falls'
            },
            'lorazepam': {
                'risk_level': 'High',
                'age_concern': 'Elderly patient population', 
                'specific_risk': 'Increased fall risk, cognitive impairment, and prolonged sedation',
                'monitoring': 'Use lowest effective dose, monitor for confusion and falls'
            },
            'alprazolam': {
                'risk_level': 'High',
                'age_concern': 'Elderly patient population',
                'specific_risk': 'Increased fall risk, cognitive impairment, and prolonged sedation',
                'monitoring': 'Use lowest effective dose, monitor for confusion and falls'
            },
            'tramadol': {
                'risk_level': 'Moderate',
                'age_concern': 'Elderly patient population',
                'specific_risk': 'Increased risk of seizures and serotonin syndrome',
                'monitoring': 'Monitor for neurological symptoms, start with low dose'
            },
            'diphenhydramine': {
                'risk_level': 'High',
                'age_concern': 'Elderly patient population',
                'specific_risk': 'Anticholinergic effects, confusion, urinary retention',
                'monitoring': 'Avoid if possible, monitor cognitive function'
            }
        }
        
        # Check each medicine against elderly concerns
        for medicine_name in medicine_names:
            medicine_lower = medicine_name.lower().strip()
            
            for risky_med, concern_data in elderly_concerns.items():
                if risky_med in medicine_lower:
                    warning = {
                        'drug': medicine_name,
                        'risk_level': concern_data['risk_level'],
                        'age_concern': concern_data['age_concern'],
                        'specific_risk': concern_data['specific_risk'],
                        'monitoring': concern_data['monitoring'],
                        'severity': concern_data['risk_level'],  # For backward compatibility
                        'warning': f"Age-related concern for patients ≥65 years",
                        'note': concern_data['specific_risk']
                    }
                    warnings.append(warning)
    
    # Pediatric warnings (if age < 18)
    if age < 18:
        pediatric_concerns = {
            'aspirin': {
                'risk_level': 'High',
                'age_concern': 'Pediatric population',
                'specific_risk': 'Risk of Reye syndrome, especially with viral infections',
                'monitoring': 'Avoid in children with viral infections, monitor for neurological symptoms'
            },
            'tramadol': {
                'risk_level': 'High',
                'age_concern': 'Pediatric population under 12 years',
                'specific_risk': 'Respiratory depression and death reported',
                'monitoring': 'Contraindicated in children under 12, caution in adolescents'
            }
        }
        
        for medicine_name in medicine_names:
            medicine_lower = medicine_name.lower().strip()
            
            for risky_med, concern_data in pediatric_concerns.items():
                if risky_med in medicine_lower:
                    warning = {
                        'drug': medicine_name,
                        'risk_level': concern_data['risk_level'],
                        'age_concern': concern_data['age_concern'],
                        'specific_risk': concern_data['specific_risk'],
                        'monitoring': concern_data['monitoring'],
                        'severity': concern_data['risk_level'],
                        'warning': f"Pediatric safety concern",
                        'note': concern_data['specific_risk']
                    }
                    warnings.append(warning)
    
    print(f"Found {len(warnings)} age-related warnings")
    return warnings

# Additional utility functions for enhanced interaction checking
def check_food_interactions(medicine_names):
    """Check for significant food-drug interactions"""
    food_interactions = []
    
    food_interaction_database = {
        'warfarin': {
            'foods': ['leafy greens', 'vitamin K supplements'],
            'effect': 'Reduced anticoagulant effectiveness',
            'recommendation': 'Maintain consistent vitamin K intake'
        },
        'metformin': {
            'foods': ['alcohol'],
            'effect': 'Increased risk of lactic acidosis',
            'recommendation': 'Limit alcohol consumption'
        },
        'lisinopril': {
            'foods': ['salt substitutes', 'potassium supplements'],
            'effect': 'Risk of hyperkalemia',
            'recommendation': 'Monitor potassium levels, avoid salt substitutes'
        }
    }
    
    for medicine_name in medicine_names:
        medicine_lower = medicine_name.lower().strip()
        
        for med, interaction_data in food_interaction_database.items():
            if med in medicine_lower:
                food_interactions.append({
                    'drug': medicine_name,
                    'interacting_foods': interaction_data['foods'],
                    'effect': interaction_data['effect'],
                    'recommendation': interaction_data['recommendation']
                })
    
    return food_interactions

def get_interaction_summary(interactions, warnings):
    """Generate summary of interaction analysis"""
    if not interactions and not warnings:
        return {
            'overall_risk': 'Low',
            'summary': 'No significant drug interactions or age-related warnings identified',
            'recommendation': 'Continue current medication regimen as prescribed'
        }
    
    high_risk_interactions = len([i for i in interactions if i.get('severity') == 'High'])
    high_risk_warnings = len([w for w in warnings if w.get('risk_level') == 'High'])
    
    if high_risk_interactions > 0 or high_risk_warnings > 0:
        return {
            'overall_risk': 'High',
            'summary': f'{high_risk_interactions} high-risk interactions and {high_risk_warnings} high-risk warnings detected',
            'recommendation': 'Immediate prescriber consultation recommended'
        }
    else:
        return {
            'overall_risk': 'Moderate',
            'summary': f'{len(interactions)} interactions and {len(warnings)} warnings require monitoring',
            'recommendation': 'Regular monitoring and follow-up recommended'
        }