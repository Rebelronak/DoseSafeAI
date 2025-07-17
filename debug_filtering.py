#!/usr/bin/env python3

"""
Debug script to understand filtering behavior
"""

import sys
sys.path.append('ml_models')

from ml_integration import MLEngine

def test_filtering():
    """Test the filtering logic with known medicines"""
    
    # Initialize ML engine
    ml_engine = MLEngine()
    
    # Test medicines that should pass filtering
    test_medicines = [
        "Ciprofloxacin",
        "Dexamethasone", 
        "Lorazepam",
        "Metformin",
        "Aspirin",
        "Paracetamol",
        "Ibuprofen",
        "Warfarin",
        "Omeprazole",
        "Simvastatin"
    ]
    
    print("🧪 Testing filtering logic...")
    print("=" * 50)
    
    for med in test_medicines:
        print(f"\n🔍 Testing: {med}")
        filtered = ml_engine._filter_false_positives([med])
        if filtered:
            print(f"  ✅ PASSED: {filtered}")
        else:
            print(f"  ❌ FILTERED OUT")
    
    print("\n" + "=" * 50)
    
    # Test with messy OCR text
    messy_text = "eCiprofloxacin:Severeinteraction eDexamethasone:Moderateinteraction eLorazepam:Severeinteraction"
    print(f"\n🔍 Testing OCR extraction on: {messy_text}")
    
    extracted = ml_engine.extract_medicines_from_text(messy_text)
    print(f"Final result: {extracted}")

if __name__ == "__main__":
    test_filtering()
