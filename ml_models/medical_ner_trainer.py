"""
Medical NLP Model for Drug Name Extraction
Train custom NER models for extracting medicine names from prescription text
"""

import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
import json
import pickle
from pathlib import Path

class MedicalNERTrainer:
    """
    Train custom Named Entity Recognition model for medical entities
    Specialized for drug names, dosages, and medical instructions
    """
    
    def __init__(self, model_name="medical_ner_v1"):
        self.model_name = model_name
        self.nlp = None
        self.training_data = []
        
    def create_training_data(self):
        """
        Create training data for medical NER
        Format: (text, {"entities": [(start, end, label)]})
        """
        
        training_examples = [
            (
                "Patient should take Aspirin 81mg once daily and Metoprolol 50mg twice daily.",
                {"entities": [
                    (19, 26, "DRUG"),  # Aspirin
                    (27, 31, "DOSAGE"),  # 81mg
                    (32, 43, "FREQUENCY"),  # once daily
                    (48, 58, "DRUG"),  # Metoprolol
                    (59, 63, "DOSAGE"),  # 50mg
                    (64, 76, "FREQUENCY")  # twice daily
                ]}
            ),
            (
                "Prescribed Lisinopril 10mg daily for blood pressure control.",
                {"entities": [
                    (10, 20, "DRUG"),  # Lisinopril
                    (21, 25, "DOSAGE"),  # 10mg
                    (26, 31, "FREQUENCY")  # daily
                ]}
            ),
            (
                "Take Ibuprofen 400mg every 8 hours as needed for pain.",
                {"entities": [
                    (5, 14, "DRUG"),  # Ibuprofen
                    (15, 20, "DOSAGE"),  # 400mg
                    (21, 35, "FREQUENCY")  # every 8 hours
                ]}
            ),
            (
                "Warfarin 5mg once daily, monitor INR levels regularly.",
                {"entities": [
                    (0, 7, "DRUG"),  # Warfarin
                    (8, 11, "DOSAGE"),  # 5mg
                    (12, 22, "FREQUENCY")  # once daily
                ]}
            ),
            (
                "Patient prescribed Atorvastatin 20mg at bedtime for cholesterol.",
                {"entities": [
                    (18, 30, "DRUG"),  # Atorvastatin
                    (31, 35, "DOSAGE"),  # 20mg
                    (36, 46, "FREQUENCY")  # at bedtime
                ]}
            ),
            (
                "Give Acetaminophen 500mg every 6 hours, maximum 4 doses per day.",
                {"entities": [
                    (5, 18, "DRUG"),  # Acetaminophen
                    (19, 24, "DOSAGE"),  # 500mg
                    (25, 39, "FREQUENCY")  # every 6 hours
                ]}
            ),
            (
                "Omeprazole 20mg before meals for acid reflux treatment.",
                {"entities": [
                    (0, 10, "DRUG"),  # Omeprazole
                    (11, 15, "DOSAGE"),  # 20mg
                    (16, 28, "FREQUENCY")  # before meals
                ]}
            ),
            (
                "Albuterol inhaler 2 puffs twice daily for asthma control.",
                {"entities": [
                    (0, 9, "DRUG"),  # Albuterol
                    (18, 25, "DOSAGE"),  # 2 puffs
                    (26, 37, "FREQUENCY")  # twice daily
                ]}
            )
        ]
        
        self.training_data = training_examples
        print(f"📚 Created {len(training_examples)} training examples")
        return training_examples
    
    def setup_model(self):
        """
        Setup spaCy model with custom NER component
        """
        
        print("🏗️ Setting up medical NER model...")
        
        # Create blank English model
        self.nlp = spacy.blank("en")
        
        # Add NER pipeline component
        ner = self.nlp.add_pipe("ner")
        
        # Add entity labels
        labels = ["DRUG", "DOSAGE", "FREQUENCY", "INSTRUCTION"]
        for label in labels:
            ner.add_label(label)
        
        print(f"✅ Model setup complete with labels: {labels}")
        
    def train_model(self, iterations=100):
        """
        Train the medical NER model
        """
        
        print(f"🚀 Training medical NER model for {iterations} iterations...")
        
        # Prepare training data
        training_examples = []
        for text, annotations in self.training_data:
            doc = self.nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            training_examples.append(example)
        
        # Initialize model
        self.nlp.initialize()
        
        # Training loop
        for i in range(iterations):
            random.shuffle(training_examples)
            losses = {}
            
            # Create batches
            batches = minibatch(training_examples, size=compounding(4.0, 32.0, 1.001))
            
            for batch in batches:
                self.nlp.update(batch, losses=losses)
            
            if i % 20 == 0:
                print(f"Iteration {i}, Losses: {losses}")
        
        print("✅ Training completed!")
        
    def test_model(self, test_texts):
        """
        Test the trained model on sample texts
        """
        
        print("🧪 Testing trained model...")
        
        for text in test_texts:
            doc = self.nlp(text)
            print(f"\nText: {text}")
            print("Entities found:")
            
            for ent in doc.ents:
                print(f"  - {ent.text} ({ent.label_})")
    
    def extract_medicines(self, text):
        """
        Extract medicine information from text using trained model
        """
        
        if not self.nlp:
            return {"error": "Model not trained"}
        
        doc = self.nlp(text)
        
        medicines = []
        current_drug = None
        current_dosage = None
        current_frequency = None
        
        for ent in doc.ents:
            if ent.label_ == "DRUG":
                # Save previous drug if exists
                if current_drug:
                    medicines.append({
                        "name": current_drug,
                        "dose": current_dosage or "Not specified",
                        "frequency": current_frequency or "As prescribed"
                    })
                
                # Start new drug
                current_drug = ent.text
                current_dosage = None
                current_frequency = None
                
            elif ent.label_ == "DOSAGE" and current_drug:
                current_dosage = ent.text
                
            elif ent.label_ == "FREQUENCY" and current_drug:
                current_frequency = ent.text
        
        # Add last drug
        if current_drug:
            medicines.append({
                "name": current_drug,
                "dose": current_dosage or "Not specified", 
                "frequency": current_frequency or "As prescribed"
            })
        
        return {
            "medicines": medicines,
            "total_medicines": len(medicines),
            "extraction_method": "Custom NER Model",
            "model_name": self.model_name
        }
    
    def save_model(self, save_path="ml_models/trained_models/medical_ner"):
        """
        Save the trained NER model
        """
        
        Path(save_path).mkdir(parents=True, exist_ok=True)
        self.nlp.to_disk(save_path)
        
        print(f"💾 Model saved to {save_path}")
    
    def load_model(self, model_path="ml_models/trained_models/medical_ner"):
        """
        Load a pre-trained model
        """
        
        try:
            self.nlp = spacy.load(model_path)
            print(f"✅ Model loaded from {model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")

def demonstrate_medical_ner():
    """
    Demonstrate medical NER training and usage
    """
    
    print("🏥 Medical NER Training Demo")
    print("=" * 40)
    
    # Initialize trainer
    trainer = MedicalNERTrainer("dosesafe_ner_v1")
    
    # Create training data
    trainer.create_training_data()
    
    # Setup and train model
    trainer.setup_model()
    trainer.train_model(iterations=150)
    
    # Test on sample texts
    test_texts = [
        "Patient needs Aspirin 81mg daily and Metoprolol 25mg twice daily.",
        "Prescribed Lisinopril 5mg once daily for hypertension management.",
        "Take Acetaminophen 500mg every 6 hours as needed for pain relief."
    ]
    
    trainer.test_model(test_texts)
    
    # Test extraction function
    print("\n🔍 Medicine Extraction Test:")
    result = trainer.extract_medicines("Patient should take Warfarin 5mg daily and Atorvastatin 20mg at bedtime.")
    print(json.dumps(result, indent=2))
    
    # Save model
    trainer.save_model()
    
    return trainer

if __name__ == "__main__":
    # Run demonstration
    trained_model = demonstrate_medical_ner()
    
    print("\n📋 Next Steps:")
    print("1. Collect more prescription texts for training")
    print("2. Expand entity labels (CONDITION, INSTRUCTION, etc.)")
    print("3. Integrate with main OCR pipeline")
    print("4. Fine-tune model with domain-specific data")
