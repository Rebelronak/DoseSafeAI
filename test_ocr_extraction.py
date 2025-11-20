"""
Test script to verify improved OCR medicine extraction
"""

import sys
import os

# Add ml_models directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_models'))

from ml_integration import extract_medicines, get_ml_status

def test_ocr_extraction():
    """Test with the actual OCR text from user's prescription"""
    
    print("🧪 Testing Improved OCR Medicine Extraction")
    print("=" * 60)
    
    # Test 1: Check ML status
    print("\n📊 ML Status:")
    status = get_ml_status()
    print(f"   ML Available: {status['ml_available']}")
    print(f"   Drug Database Size: {status['drug_database_size']}")
    
    # Test 2: Your actual OCR text
    print("\n💊 Testing with your OCR text:")
    ocr_text = "eDexamethasone,0.5mgoncedaily Ciprofloxacin:Severeinteraction, avoidconcurrentuse. eLorazepam,0.5mgatbedtime eParacetamol,650mgevery6hoursasneeded"
    
    print(f"   Input OCR: {ocr_text}")
    print("\n🔍 Extracting medicines...")
    
    medicines = extract_medicines(ocr_text)
    print(f"\n✅ Extracted medicines: {medicines}")
    print(f"   Total found: {len(medicines)}")
    
    # Expected medicines
    expected = ['Dexamethasone', 'Ciprofloxacin', 'Lorazepam', 'Paracetamol']
    print(f"\n📋 Expected medicines: {expected}")
    
    # Check matches
    found_count = 0
    for exp in expected:
        if any(exp.lower() in med.lower() for med in medicines):
            print(f"   ✅ Found: {exp}")
            found_count += 1
        else:
            print(f"   ❌ Missing: {exp}")
    
    print(f"\n🎯 Success Rate: {found_count}/{len(expected)} ({found_count/len(expected)*100:.1f}%)")
    
    # Test 3: Clean version for comparison
    print("\n🧹 Testing with clean text:")
    clean_text = "Dexamethasone 0.5mg once daily, Ciprofloxacin, Lorazepam 0.5mg at bedtime, Paracetamol 650mg every 6 hours"
    clean_medicines = extract_medicines(clean_text)
    print(f"   Clean text medicines: {clean_medicines}")

if __name__ == "__main__":
    test_ocr_extraction()
