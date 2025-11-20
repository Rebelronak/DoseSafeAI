"""
Test ML Compatibility Script
Test that all ML components work without TensorFlow/incompatible packages
"""

import sys
import importlib

def test_package_imports():
    """Test all required packages can be imported"""
    
    print("🧪 Testing ML Package Compatibility")
    print("=" * 50)
    
    required_packages = [
        ('sklearn', 'scikit-learn'),
        ('xgboost', 'XGBoost'),
        ('lightgbm', 'LightGBM'), 
        ('spacy', 'spaCy'),
        ('nltk', 'NLTK'),
        ('fuzzywuzzy', 'FuzzyWuzzy'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('matplotlib', 'Matplotlib'),
        ('seaborn', 'Seaborn'),
        ('joblib', 'Joblib'),
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow')
    ]
    
    successful_imports = 0
    failed_imports = []
    
    for package, display_name in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {display_name}: OK")
            successful_imports += 1
        except ImportError as e:
            print(f"❌ {display_name}: FAILED - {e}")
            failed_imports.append(display_name)
    
    print(f"\n📊 Import Results:")
    print(f"   - Successful: {successful_imports}/{len(required_packages)}")
    print(f"   - Failed: {len(failed_imports)}")
    
    if failed_imports:
        print(f"   - Failed packages: {', '.join(failed_imports)}")
        return False
    
    return True

def test_ml_components():
    """Test ML component initialization"""
    
    print("\n🔧 Testing ML Components")
    print("=" * 50)
    
    try:
        # Test Drug Interaction Predictor
        print("Testing Drug Interaction Predictor...")
        from drug_interaction_predictor import DrugInteractionPredictor
        predictor = DrugInteractionPredictor()
        print("✅ Drug Interaction Predictor: OK")
        
        # Test Medical NER Trainer
        print("Testing Medical NER Trainer...")
        from medical_ner_trainer import MedicalNERTrainer
        ner_trainer = MedicalNERTrainer()
        print("✅ Medical NER Trainer: OK")
        
        # Test OCR Trainer
        print("Testing OCR Trainer...")
        from ocr_trainer import MedicalTextClassifier
        ocr_trainer = MedicalTextClassifier()
        print("✅ OCR Trainer: OK")
        
        # Test ML Integration
        print("Testing ML Integration...")
        from ml_integration import MLModelManager
        ml_manager = MLModelManager()
        print("✅ ML Integration: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic ML functionality without models"""
    
    print("\n⚙️ Testing Basic Functionality")
    print("=" * 50)
    
    try:
        # Test text processing
        from fuzzywuzzy import fuzz
        similarity = fuzz.ratio("aspirin", "asprin")
        print(f"✅ Text similarity: {similarity}%")
        
        # Test data processing
        import pandas as pd
        import numpy as np
        
        test_data = pd.DataFrame({
            'drug1': ['Aspirin', 'Metoprolol'],
            'drug2': ['Warfarin', 'Lisinopril'],
            'interaction': ['Major', 'Minor']
        })
        print(f"✅ Data processing: {len(test_data)} records")
        
        # Test ML algorithms
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        rf = RandomForestClassifier(n_estimators=10)
        vectorizer = TfidfVectorizer()
        print("✅ ML algorithms initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def run_compatibility_tests():
    """Run all compatibility tests"""
    
    print("🎯 DoseSafe-AI ML Compatibility Test Suite")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_package_imports),
        ("ML Components", test_ml_components), 
        ("Basic Functionality", test_basic_functionality)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test...")
        
        try:
            if test_func():
                print(f"✅ {test_name} Test: PASSED")
                passed_tests += 1
            else:
                print(f"❌ {test_name} Test: FAILED")
        except Exception as e:
            print(f"❌ {test_name} Test: ERROR - {e}")
    
    print(f"\n📈 Test Results Summary")
    print("=" * 60)
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! ML components are ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = run_compatibility_tests()
    sys.exit(0 if success else 1)
