"""
Training Pipeline Script for DoseSafe-AI ML Models
Run this script to train all ML models for the project
"""

import os
import sys
import argparse
from pathlib import Path

def train_all_models():
    """
    Train all ML models for DoseSafe-AI
    """
    
    print("🚀 Starting DoseSafe-AI ML Training Pipeline")
    print("=" * 60)
    
    # 1. Train Drug Interaction Predictor
    print("\n💊 Training Drug Interaction Prediction Model...")
    try:
        from drug_interaction_predictor import DrugInteractionPredictor, create_enhanced_training_data
        
        # Create training data
        df = create_enhanced_training_data()
        
        # Train model
        predictor = DrugInteractionPredictor()
        X, y_int, y_sev = predictor.prepare_features(df)
        results = predictor.train_interaction_model(X, y_int, y_sev)
        predictor.save_models()
        
        print(f"✅ Drug interaction model trained successfully!")
        print(f"   - Interaction accuracy: {results['interaction_accuracy']:.3f}")
        print(f"   - Severity accuracy: {results['severity_accuracy']:.3f}")
        
    except Exception as e:
        print(f"❌ Drug interaction training failed: {e}")
    
    # 2. Train Medical NER Model
    print("\n🏷️ Training Medical NER Model...")
    try:
        from medical_ner_trainer import MedicalNERTrainer
        
        trainer = MedicalNERTrainer("dosesafe_ner_v1")
        trainer.create_training_data()
        trainer.setup_model()
        trainer.train_model(iterations=200)
        trainer.save_model()
        
        print("✅ Medical NER model trained successfully!")
        
    except Exception as e:
        print(f"❌ Medical NER training failed: {e}")
    
    # 3. Setup OCR Training (requires manual data collection)
    print("\n📷 OCR Model Training Setup...")
    try:
        from ocr_trainer import create_sample_training_data
        create_sample_training_data()
        
        print("✅ OCR training structure created")
        print("   📝 Add prescription images to train custom OCR")
        
    except Exception as e:
        print(f"❌ OCR setup failed: {e}")
    
    print("\n🎉 ML Training Pipeline Complete!")
    print("\n📋 Next Steps:")
    print("1. Test models with real prescription data")
    print("2. Collect more training data to improve accuracy")
    print("3. Integrate models with main application")
    print("4. Monitor model performance in production")

def test_models():
    """
    Test all trained models
    """
    
    print("🧪 Testing Trained Models")
    print("=" * 40)
    
    # Test drug interaction model
    try:
        from drug_interaction_predictor import DrugInteractionPredictor
        
        predictor = DrugInteractionPredictor()
        predictor.load_models()
        
        test_result = predictor.predict_interaction("Aspirin", "Warfarin")
        print("💊 Drug Interaction Test:")
        print(f"   Prediction: {test_result}")
        
    except Exception as e:
        print(f"❌ Drug interaction test failed: {e}")
    
    # Test NER model
    try:
        from medical_ner_trainer import MedicalNERTrainer
        
        trainer = MedicalNERTrainer()
        trainer.load_model()
        
        test_text = "Patient should take Aspirin 81mg daily and Metoprolol 50mg twice daily."
        result = trainer.extract_medicines(test_text)
        
        print("\n🏷️ Medical NER Test:")
        print(f"   Input: {test_text}")
        print(f"   Extracted: {result}")
        
    except Exception as e:
        print(f"❌ NER test failed: {e}")

def create_demo_notebook():
    """
    Create Jupyter notebook for ML model demonstration
    """
    
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# DoseSafe-AI Machine Learning Models Demo\n",
                    "\n",
                    "This notebook demonstrates the trained ML models for DoseSafe-AI:\n",
                    "1. Drug Interaction Prediction\n",
                    "2. Medical Named Entity Recognition\n",
                    "3. Custom OCR for Medical Documents"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Import required libraries\n",
                    "import sys\n",
                    "sys.path.append('../')\n",
                    "\n",
                    "from drug_interaction_predictor import DrugInteractionPredictor\n",
                    "from medical_ner_trainer import MedicalNERTrainer\n",
                    "from ml_integration import MLModelManager\n",
                    "\n",
                    "import json\n",
                    "import pandas as pd"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Drug Interaction Prediction Demo"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Load drug interaction predictor\n",
                    "predictor = DrugInteractionPredictor()\n",
                    "predictor.load_models()\n",
                    "\n",
                    "# Test drug interaction prediction\n",
                    "test_drugs = [('Aspirin', 'Warfarin'), ('Metoprolol', 'Verapamil'), ('Simvastatin', 'Clarithromycin')]\n",
                    "\n",
                    "print('Drug Interaction Predictions:')\n",
                    "print('=' * 50)\n",
                    "\n",
                    "for drug1, drug2 in test_drugs:\n",
                    "    result = predictor.predict_interaction(drug1, drug2)\n",
                    "    print(f'\\n{drug1} + {drug2}:')\n",
                    "    print(f'  Interaction: {result.get(\"predicted_interaction\", \"Unknown\")}')\n",
                    "    print(f'  Severity: {result.get(\"predicted_severity\", \"Unknown\")}')\n",
                    "    print(f'  Confidence: {result.get(\"interaction_confidence\", 0):.3f}')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Medical NER Demo"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Load medical NER model\n",
                    "ner_trainer = MedicalNERTrainer()\n",
                    "ner_trainer.load_model()\n",
                    "\n",
                    "# Test medicine extraction\n",
                    "test_texts = [\n",
                    "    'Patient prescribed Aspirin 81mg daily and Metoprolol 25mg twice daily.',\n",
                    "    'Take Lisinopril 10mg once daily for blood pressure control.',\n",
                    "    'Ibuprofen 400mg every 8 hours as needed for pain relief.'\n",
                    "]\n",
                    "\n",
                    "print('Medicine Extraction Results:')\n",
                    "print('=' * 50)\n",
                    "\n",
                    "for text in test_texts:\n",
                    "    result = ner_trainer.extract_medicines(text)\n",
                    "    print(f'\\nInput: {text}')\n",
                    "    print('Extracted medicines:')\n",
                    "    for med in result['medicines']:\n",
                    "        print(f'  - {med[\"name\"]} {med[\"dose\"]} {med[\"frequency\"]}')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Complete ML Pipeline Demo"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Load complete ML pipeline\n",
                    "ml_manager = MLModelManager()\n",
                    "ml_manager.load_all_models()\n",
                    "\n",
                    "# Test complete analysis\n",
                    "sample_prescription = '''\n",
                    "Patient: John Doe, Age: 65\n",
                    "Medications:\n",
                    "1. Aspirin 81mg once daily\n",
                    "2. Warfarin 5mg daily\n",
                    "3. Metoprolol 50mg twice daily\n",
                    "4. Lisinopril 10mg once daily\n",
                    "'''\n",
                    "\n",
                    "# Run complete analysis\n",
                    "analysis = ml_manager.enhanced_ocr_analysis(sample_prescription, use_ml=True)\n",
                    "\n",
                    "print('Complete ML Analysis:')\n",
                    "print('=' * 50)\n",
                    "print(json.dumps(analysis, indent=2, default=str))"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    import json
    
    with open("ml_models/ML_Demo.ipynb", "w") as f:
        json.dump(notebook_content, f, indent=2)
    
    print("📓 Demo notebook created: ml_models/ML_Demo.ipynb")

def main():
    """
    Main training pipeline function
    """
    
    parser = argparse.ArgumentParser(description="DoseSafe-AI ML Training Pipeline")
    parser.add_argument("--mode", choices=["train", "test", "demo"], default="train",
                       help="Mode: train models, test models, or create demo")
    
    args = parser.parse_args()
    
    if args.mode == "train":
        train_all_models()
    elif args.mode == "test":
        test_models()
    elif args.mode == "demo":
        create_demo_notebook()

if __name__ == "__main__":
    main()
