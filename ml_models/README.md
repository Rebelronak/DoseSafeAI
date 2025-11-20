# 🤖 Machine Learning Training for DoseSafe-AI

This directory contains machine learning models and training scripts to enhance DoseSafe-AI with custom AI capabilities.

## 🎯 ML Training Opportunities

### 1. **Custom OCR Model for Medical Documents**
- **Purpose**: Train on prescription images, medical forms, handwritten prescriptions
- **Benefit**: Better accuracy than generic Tesseract for medical text
- **File**: `ocr_trainer.py`

### 2. **Drug Interaction Prediction Model**
- **Purpose**: Predict drug interactions and severity levels
- **Benefit**: Learn from real-world medical data patterns
- **File**: `drug_interaction_predictor.py`

### 3. **Medical NLP Model (Named Entity Recognition)**
- **Purpose**: Extract medicine names, dosages, frequencies from text
- **Benefit**: More accurate than pattern matching
- **File**: `medical_ner_trainer.py`

### 4. **Risk Assessment Model**
- **Purpose**: Predict patient risk based on age, medications, conditions
- **Benefit**: Personalized risk assessment
- **File**: `ml_integration.py`

## 🚀 Quick Start

### Step 1: Install ML Dependencies
```bash
cd ml_models
pip install -r ml_requirements.txt
```

### Step 2: Train All Models
```bash
python train_pipeline.py --mode train
```

### Step 3: Test Models
```bash
python train_pipeline.py --mode test
```

### Step 4: Create Demo Notebook
```bash
python train_pipeline.py --mode demo
```

## 📁 Project Structure

```
ml_models/
├── README.md                          # This file
├── __init__.py                        # Package initialization
├── ml_requirements.txt                # ML-specific dependencies
├── train_pipeline.py                  # Main training pipeline
├── 
├── # Core ML Models
├── ocr_trainer.py                     # Custom OCR model training
├── drug_interaction_predictor.py      # Drug interaction ML model
├── medical_ner_trainer.py             # NER model for medicine extraction
├── ml_integration.py                  # Model integration with main app
├── 
├── # Training Data (create these directories)
├── training_data/
│   ├── prescription_images/           # Images for OCR training
│   ├── drug_interactions.csv          # Drug interaction dataset
│   └── ner_labels.json               # NER training labels
├── 
├── # Trained Models (auto-created)
├── trained_models/
│   ├── medical_ocr_v1.h5             # Trained OCR model
│   ├── medical_ner/                  # NER model directory
│   ├── interaction_model.pkl         # Drug interaction classifier
│   └── severity_model.pkl            # Severity classifier
├── 
└── # Evaluation and Demo
    ├── ML_Demo.ipynb                  # Jupyter demo notebook
    └── evaluation/                    # Model evaluation scripts
```

## 🔧 Training Individual Models

### 1. Drug Interaction Predictor
```python
from drug_interaction_predictor import DrugInteractionPredictor

# Create and train model
predictor = DrugInteractionPredictor()
df = predictor.load_training_data('drug_interactions.csv')
X, y_int, y_sev = predictor.prepare_features(df)
predictor.train_interaction_model(X, y_int, y_sev)
predictor.save_models()

# Test prediction
result = predictor.predict_interaction("Aspirin", "Warfarin")
print(result)
```

### 2. Medical NER Training
```python
from medical_ner_trainer import MedicalNERTrainer

# Train NER model
trainer = MedicalNERTrainer("dosesafe_ner_v1")
trainer.create_training_data()
trainer.setup_model()
trainer.train_model(iterations=200)
trainer.save_model()

# Test extraction
result = trainer.extract_medicines("Take Aspirin 81mg daily")
print(result)
```

### 3. Custom OCR Training
```python
from ocr_trainer import MedicalOCRTrainer

# Prepare OCR training
trainer = MedicalOCRTrainer("medical_ocr_v1")
images, sequences = trainer.prepare_dataset('images/', 'labels.json')
trainer.build_model()
trainer.train_model(images, sequences, epochs=50)
trainer.save_model()
```

## 📊 Training Data Requirements

### OCR Training Data
```json
[
  {
    "filename": "prescription_001.jpg",
    "text": "Patient: John Doe\nMedicines:\nAspirin 81mg once daily\nMetoprolol 50mg twice daily"
  }
]
```

### NER Training Data
- Prescription texts with entity labels
- Medicine names, dosages, frequencies
- Patient information
- Medical instructions

### Drug Interaction Data
```csv
drug1,drug2,interaction_type,severity,description
Aspirin,Warfarin,pharmacodynamic,high,Increased bleeding risk
Metoprolol,Verapamil,pharmacodynamic,moderate,Additive cardiac effects
```

## 🔗 Integration with Main App

### Update OCR Pipeline
```python
# In routes/ai_only_ocr.py
from ml_models.ml_integration import MLModelManager

# Initialize ML manager
ml_manager = MLModelManager()
ml_manager.load_all_models()

# Use in OCR function
def analyze_prescription_with_ml(text, filename):
    return ml_manager.enhanced_ocr_analysis(text, use_ml=True)
```

## 📈 Model Performance Tracking

### Metrics to Track
1. **OCR Accuracy**: Character-level and word-level accuracy
2. **NER Performance**: Precision, Recall, F1-score for each entity type
3. **Drug Interaction Accuracy**: Classification accuracy and confidence scores
4. **End-to-End Performance**: Complete pipeline accuracy

### Evaluation Scripts
```python
# Create evaluation scripts in evaluation/ directory
- ocr_evaluation.py
- ner_evaluation.py  
- interaction_evaluation.py
- pipeline_evaluation.py
```

## 🎯 Next Steps for Production

### Phase 1: Basic ML Integration
1. ✅ Train initial models with sample data
2. ✅ Integrate with existing OCR pipeline
3. 📋 Test with real prescription data
4. 📋 Collect user feedback

### Phase 2: Data Collection & Improvement
1. 📋 Collect real prescription images
2. 📋 Expand drug interaction database
3. 📋 Create larger NER training dataset
4. 📋 Fine-tune models with domain data

### Phase 3: Advanced Features
1. 📋 Multi-language support
2. 📋 Handwritten prescription recognition
3. 📋 Real-time model updates
4. 📋 Federated learning for privacy

### Phase 4: Production Deployment
1. 📋 Model versioning and A/B testing
2. 📋 Performance monitoring
3. 📋 Automated retraining pipeline
4. 📋 Edge deployment for offline use

## 💡 Tips for Success

1. **Start Small**: Begin with the NER model as it's easiest to train
2. **Quality Data**: Focus on high-quality, diverse training data
3. **Iterative Improvement**: Train → Test → Collect Data → Retrain
4. **Domain Expertise**: Involve medical professionals in data labeling
5. **Evaluation**: Set up proper evaluation metrics early

## 🔍 Troubleshooting

### Common Issues
1. **Model Not Loading**: Check file paths and dependencies
2. **Low Accuracy**: Need more/better training data
3. **Memory Issues**: Reduce batch size or model complexity
4. **Integration Problems**: Check import paths and model formats

### Getting Help
- Check error logs in terminal output
- Verify training data format
- Test individual components separately
- Review model architecture for your data size

---

**🏥 Ready to enhance DoseSafe-AI with custom ML models!**

Run `python train_pipeline.py --mode train` to get started.
