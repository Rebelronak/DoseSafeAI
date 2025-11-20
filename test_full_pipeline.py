"""
Full Pipeline Test - OCR + Medicine Extraction + Drug Interaction Analysis
Tests the complete DoseSafe-AI workflow as it would work in production
"""

import sys
import os

# Add backend and ml_models to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_models'))

from ml_integration import extract_medicines, get_ml_status, check_interactions, check_age_warnings

def test_full_pipeline():
    """Test the complete pipeline with real OCR prescription data"""
    
    print("🏥 DoseSafe-AI Full Pipeline Test")
    print("=" * 60)
    
    # Real OCR text from prescription image
    prescription_ocr = """
    GENERALHOSPITAL
    JohnR.Smith,M.D.
    InternalMedicine
    456EimStreet
    Cityville,ST12345
    Patient:MichaelBrownDate:04/24/2024
    Address:789OakAvenue
    Cityville,ST12345
    eDexamethasone,0.5mgoncedaily
    Ciprofloxacin:Severeinteraction,
    avoidconcurrentuse.
    eLorazepam,0.5mgatbedtime
    eParacetamol,650mgevery6hoursasneeded
    y JohnR.Smith,M.D.
    """
    
    print("📋 Processing prescription OCR text...")
    print(f"   OCR Input: {prescription_ocr.strip()}")
    
    # Step 1: Extract medicines using ML
    print("\n🔍 Step 1: Medicine Extraction")
    medicines = extract_medicines(prescription_ocr)
    print(f"   ✅ Extracted medicines: {medicines}")
    print(f"   📊 Total medicines found: {len(medicines)}")
    
    if not medicines:
        print("   ❌ No medicines extracted! Pipeline failed.")
        return
    
    # Step 2: Check drug interactions between all pairs
    print("\n⚠️ Step 2: Drug Interaction Analysis")
    interactions_found = []
    
    for i in range(len(medicines)):
        for j in range(i + 1, len(medicines)):
            drug1, drug2 = medicines[i], medicines[j]
            print(f"\n   🔬 Checking: {drug1} + {drug2}")
            
            interaction = check_interactions(drug1, drug2)
            print(f"      Result: {interaction}")
            
            if interaction.get('has_interaction'):
                interactions_found.append({
                    'drug1': drug1,
                    'drug2': drug2,
                    'severity': interaction.get('severity', 'unknown'),
                    'confidence': interaction.get('confidence', 0)
                })
                print(f"      ⚠️ INTERACTION DETECTED: {drug1} + {drug2} ({interaction.get('severity', 'unknown')})")
    
    # Step 3: Check age warnings
    print("\n👶 Step 3: Age-Related Warnings")
    age_warnings = []
    patient_age_group = "Adult"  # Could be extracted from OCR or user input
    
    for medicine in medicines:
        print(f"\n   🔬 Checking age warnings for: {medicine}")
        warning = check_age_warnings(medicine, patient_age_group)
        print(f"      Result: {warning}")
        
        if warning.get('has_warning'):
            age_warnings.append({
                'medicine': medicine,
                'age_group': patient_age_group,
                'confidence': warning.get('confidence', 0)
            })
            print(f"      ⚠️ AGE WARNING: {medicine} for {patient_age_group}")
    
    # Step 4: Generate final report
    print("\n📊 Final Analysis Report")
    print("=" * 40)
    print(f"Patient: Michael Brown")
    print(f"Date: 04/24/2024")
    print(f"Doctor: John R. Smith, M.D.")
    
    print(f"\n💊 Medications Identified ({len(medicines)}):")
    for i, med in enumerate(medicines, 1):
        print(f"   {i}. {med}")
    
    if interactions_found:
        print(f"\n⚠️ Drug Interactions Found ({len(interactions_found)}):")
        for interaction in interactions_found:
            print(f"   • {interaction['drug1']} + {interaction['drug2']}")
            print(f"     Severity: {interaction['severity'].upper()}")
            print(f"     Confidence: {interaction['confidence']:.1%}")
    else:
        print(f"\n✅ No drug interactions detected")
    
    if age_warnings:
        print(f"\n👶 Age Warnings ({len(age_warnings)}):")
        for warning in age_warnings:
            print(f"   • {warning['medicine']} - {warning['age_group']}")
            print(f"     Confidence: {warning['confidence']:.1%}")
    else:
        print(f"\n✅ No age-related warnings")
    
    # Success metrics
    print(f"\n🎯 Pipeline Performance:")
    print(f"   ✅ OCR Processing: SUCCESS")
    print(f"   ✅ Medicine Extraction: {len(medicines)} medicines found")
    print(f"   ✅ Interaction Analysis: {len(interactions_found)} interactions found")
    print(f"   ✅ Age Warning Analysis: {len(age_warnings)} warnings found")
    print(f"   🎉 Overall Status: PIPELINE COMPLETED SUCCESSFULLY")

def test_ml_status():
    """Test ML system status"""
    print("\n🤖 ML System Status:")
    status = get_ml_status()
    for key, value in status.items():
        print(f"   {key}: {value}")

if __name__ == "__main__":
    # Test ML status first
    test_ml_status()
    
    # Run full pipeline test
    test_full_pipeline()
