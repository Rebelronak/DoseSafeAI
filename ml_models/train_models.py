#!/usr/bin/env python3
"""
Training Script for DoseSafe-AI ML Models
Trains medicine extraction and drug interaction models
"""

import os
import sys
import json
from ocr_trainer import MedicalTextClassifier

def train_medicine_extraction_model():
    """Train the medicine extraction model"""
    
    print("🚀 Training Medicine Extraction Model")
    print("=" * 50)
    
    # Initialize classifier
    classifier = MedicalTextClassifier("dosesafe_ml_v1")
    
    # Load medicine database
    classifier.load_medicine_database()
    
    # Train the model
    accuracy = classifier.train_medicine_classifier()
    
    # Test on sample texts
    test_texts = [
        "Patient: Age 70 (elderly)\nMedicines:\nAspirin\nWarfarin\nHydroxyzine",
        "HydroxyzineVariant22 25mg twice daily",
        "LorazepamVariant21 0.5mg as needed for anxiety",
        "Metoprolol 50mg BID, Aspirin 81mg daily",
        "Patient: John Doe\nAge: 45\nMedications:\nLisinopril 10mg daily\nAtorvastatin 20mg once daily"
    ]
    
    print("\n🔍 Testing medicine extraction:")
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: {text[:50]}...")
        medicines = classifier.extract_medicines_from_text(text)
        print(f"Extracted medicines:")
        for med in medicines:
            print(f"  - {med['name']} (confidence: {med.get('confidence', 'N/A')})")
    
    # Save the trained model
    models_dir = "models"
    classifier.save_model(models_dir)
    
    print(f"\n✅ Model training completed with {accuracy:.3f} accuracy")
    print(f"💾 Model saved to {models_dir}/")
    
    return classifier

def create_enhanced_medicine_database():
    """Create an enhanced medicine database with more medicines"""
    
    enhanced_database = [
        {
            "name": "Aspirin",
            "aliases": ["acetylsalicylic acid", "ASA", "aspirin", "baby aspirin"],
            "category": "NSAID",
            "common_doses": ["81mg", "325mg", "500mg"],
            "interactions": ["warfarin", "ibuprofen", "alcohol"],
            "age_warnings": {"elderly": "Increased bleeding risk"}
        },
        {
            "name": "Warfarin",
            "aliases": ["coumadin", "warfarin sodium", "warfarin"],
            "category": "Anticoagulant",
            "common_doses": ["1mg", "2mg", "5mg", "10mg"],
            "interactions": ["aspirin", "ibuprofen", "vitamin K"],
            "age_warnings": {"elderly": "Requires frequent monitoring"}
        },
        {
            "name": "Hydroxyzine",
            "aliases": ["atarax", "vistaril", "hydroxyzine hcl", "hydroxyzinevariant22"],
            "category": "Antihistamine",
            "common_doses": ["10mg", "25mg", "50mg"],
            "interactions": ["alcohol", "sedatives"],
            "age_warnings": {"elderly": "Anticholinergic effects"}
        },
        {
            "name": "Metoprolol",
            "aliases": ["lopressor", "toprol xl", "metoprolol tartrate", "metoprolol succinate"],
            "category": "Beta Blocker",
            "common_doses": ["25mg", "50mg", "100mg"],
            "interactions": ["insulin", "epinephrine"],
            "age_warnings": {"elderly": "Monitor blood pressure"}
        },
        {
            "name": "Lorazepam",
            "aliases": ["ativan", "lorazepam", "lorazepamvariant21"],
            "category": "Benzodiazepine",
            "common_doses": ["0.5mg", "1mg", "2mg"],
            "interactions": ["alcohol", "opioids", "sedatives"],
            "age_warnings": {"elderly": "High fall risk"}
        },
        {
            "name": "Lisinopril",
            "aliases": ["prinivil", "zestril", "lisinopril"],
            "category": "ACE Inhibitor",
            "common_doses": ["2.5mg", "5mg", "10mg", "20mg"],
            "interactions": ["potassium", "lithium"],
            "age_warnings": {"elderly": "Monitor kidney function"}
        },
        {
            "name": "Atorvastatin",
            "aliases": ["lipitor", "atorvastatin calcium"],
            "category": "Statin",
            "common_doses": ["10mg", "20mg", "40mg", "80mg"],
            "interactions": ["grapefruit", "digoxin"],
            "age_warnings": {"elderly": "Monitor liver function"}
        },
        {
            "name": "Omeprazole",
            "aliases": ["prilosec", "omeprazole"],
            "category": "PPI",
            "common_doses": ["20mg", "40mg"],
            "interactions": ["clopidogrel", "warfarin"],
            "age_warnings": {"elderly": "Long-term use concerns"}
        },
        {
            "name": "Metformin",
            "aliases": ["glucophage", "metformin hcl"],
            "category": "Antidiabetic",
            "common_doses": ["500mg", "750mg", "1000mg"],
            "interactions": ["alcohol", "contrast dye"],
            "age_warnings": {"elderly": "Monitor kidney function"}
        },
        {
            "name": "Amlodipine",
            "aliases": ["norvasc", "amlodipine besylate"],
            "category": "Calcium Channel Blocker",
            "common_doses": ["2.5mg", "5mg", "10mg"],
            "interactions": ["simvastatin", "grapefruit"],
            "age_warnings": {"elderly": "Monitor for edema"}
        }
    ]
    
    # Save enhanced database
    os.makedirs("data", exist_ok=True)
    with open("data/medicines.json", "w") as f:
        json.dump(enhanced_database, f, indent=2)
    
    print("✅ Enhanced medicine database created")
    return enhanced_database

def main():
    """Main training function"""
    
    print("🏥 DoseSafe-AI ML Model Training Suite")
    print("=" * 60)
    
    # Create enhanced database
    create_enhanced_medicine_database()
    
    # Train medicine extraction model
    classifier = train_medicine_extraction_model()
    
    print("\n🎉 Training Complete!")
    print("=" * 60)
    print("✅ Medicine extraction model trained and saved")
    print("✅ Enhanced medicine database created")
    print("✅ Models ready for integration with OCR pipeline")
    
    print("\n📋 Next Steps:")
    print("1. Models are now available in 'models/' directory")
    print("2. Enhanced OCR will automatically use trained models")
    print("3. Test with prescription uploads")
    print("4. Monitor accuracy and retrain if needed")
    
    return True

if __name__ == "__main__":
    main()
