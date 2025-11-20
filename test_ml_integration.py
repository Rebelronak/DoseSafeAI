"""
Test script to verify ML integration in DoseSafe-AI
Tests the ML models for medicine extraction, drug interactions, and age warnings
"""

import sys
import os

# Add ml_models directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_models'))

try:
    from ml_integration import extract_medicines, check_interactions, check_age_warnings, get_ml_status
    print("✅ Successfully imported ML integration")
except ImportError as e:
    print(f"❌ Failed to import ML integration: {e}")
    sys.exit(1)

def test_ml_integration():
    """Test all ML functionality"""
    
    print("🧪 Testing DoseSafe-AI ML Integration")
    print("=" * 50)
    
    # Test 1: Check ML status
    print("\n📊 ML Status:")
    status = get_ml_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Test 2: Medicine extraction
    print("\n💊 Testing Medicine Extraction:")
    test_text = "Patient should take Aspirin 100mg daily and Warfarin 5mg as prescribed by doctor"
    medicines = extract_medicines(test_text)
    print(f"   Input: {test_text}")
    print(f"   Extracted medicines: {medicines}")
    
    # Test 3: Drug interaction checking
    print("\n⚠️ Testing Drug Interaction Detection:")
    if len(medicines) >= 2:
        interaction = check_interactions(medicines[0], medicines[1])
        print(f"   Checking: {medicines[0]} + {medicines[1]}")
        print(f"   Interaction: {interaction}")
    else:
        interaction = check_interactions("Aspirin", "Warfarin")
        print(f"   Checking: Aspirin + Warfarin")
        print(f"   Interaction: {interaction}")
    
    # Test 4: Age warnings
    print("\n👶 Testing Age Warning Detection:")
    for age_group in ["<18", "Adult", "Elderly"]:
        warning = check_age_warnings("Aspirin", age_group)
        print(f"   Aspirin for {age_group}: {warning}")
    
    print("\n🎉 ML Integration Test Complete!")

if __name__ == "__main__":
    test_ml_integration()
