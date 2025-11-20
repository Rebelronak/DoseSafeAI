"""
Drug Interaction Prediction Model
Train ML models to predict drug interactions and severity levels
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import json
import warnings
warnings.filterwarnings('ignore')

class DrugInteractionPredictor:
    """
    ML model to predict drug interactions and their severity levels
    """
    
    def __init__(self):
        self.model = None
        self.drug_encoder = LabelEncoder()
        self.interaction_encoder = LabelEncoder()
        self.severity_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def load_training_data(self, csv_path):
        """
        Load drug interaction data from CSV
        Expected columns: drug1, drug2, interaction_type, severity, description
        """
        
        print("📊 Loading drug interaction training data...")
        
        try:
            df = pd.read_csv(csv_path)
            print(f"✅ Loaded {len(df)} drug interaction records")
            print(f"📋 Columns: {list(df.columns)}")
            
            # Display sample data
            print("\n🔍 Sample data:")
            print(df.head())
            
            return df
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def prepare_features(self, df):
        """
        Create features for ML training from drug interaction data
        """
        
        print("🔧 Preparing features for ML training...")
        
        # Create drug combination features
        df['drug_pair'] = df['drug1'].str.lower() + '_' + df['drug2'].str.lower()
        
        # Encode categorical variables
        df['drug1_encoded'] = self.drug_encoder.fit_transform(df['drug1'].str.lower())
        df['drug2_encoded'] = self.drug_encoder.transform(df['drug2'].str.lower())
        
        # Create numerical features
        features = []
        feature_names = []
        
        # Drug encoding features
        features.append(df['drug1_encoded'].values.reshape(-1, 1))
        features.append(df['drug2_encoded'].values.reshape(-1, 1))
        feature_names.extend(['drug1_encoded', 'drug2_encoded'])
        
        # Drug name length features (simple heuristic)
        features.append(df['drug1'].str.len().values.reshape(-1, 1))
        features.append(df['drug2'].str.len().values.reshape(-1, 1))
        feature_names.extend(['drug1_length', 'drug2_length'])
        
        # Text features from description
        if 'description' in df.columns:
            tfidf = TfidfVectorizer(max_features=100, stop_words='english')
            desc_features = tfidf.fit_transform(df['description'].fillna(''))
            features.append(desc_features.toarray())
            feature_names.extend([f'desc_tfidf_{i}' for i in range(100)])
        
        # Combine all features
        X = np.hstack(features)
        
        # Prepare target variables
        y_interaction = self.interaction_encoder.fit_transform(df['interaction_type'])
        y_severity = self.severity_encoder.fit_transform(df['severity'])
        
        self.feature_names = feature_names
        
        print(f"✅ Created {X.shape[1]} features from {len(df)} samples")
        
        return X, y_interaction, y_severity
    
    def train_interaction_model(self, X, y_interaction, y_severity):
        """
        Train models to predict interaction type and severity
        """
        
        print("🚀 Training drug interaction prediction models...")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_int_train, y_int_test, y_sev_train, y_sev_test = train_test_split(
            X_scaled, y_interaction, y_severity, test_size=0.2, random_state=42
        )
        
        # Train interaction type model
        print("📈 Training interaction type classifier...")
        self.interaction_model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        self.interaction_model.fit(X_train, y_int_train)
        
        # Train severity model
        print("📈 Training severity classifier...")
        self.severity_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.severity_model.fit(X_train, y_sev_train)
        
        # Evaluate models
        print("\n📊 Model Performance:")
        print("=" * 50)
        
        # Interaction type evaluation
        int_pred = self.interaction_model.predict(X_test)
        print("🔍 Interaction Type Classification:")
        print(classification_report(y_int_test, int_pred))
        
        # Severity evaluation
        sev_pred = self.severity_model.predict(X_test)
        print("\n⚠️ Severity Classification:")
        print(classification_report(y_sev_test, sev_pred))
        
        return {
            'interaction_accuracy': self.interaction_model.score(X_test, y_int_test),
            'severity_accuracy': self.severity_model.score(X_test, y_sev_test)
        }
    
    def predict_interaction(self, drug1, drug2, description=""):
        """
        Predict interaction between two drugs
        """
        
        if not self.interaction_model or not self.severity_model:
            return {"error": "Models not trained yet"}
        
        try:
            # Prepare features for prediction
            drug1_enc = self.drug_encoder.transform([drug1.lower()])[0]
            drug2_enc = self.drug_encoder.transform([drug2.lower()])[0]
            
            # Create feature vector
            features = [
                drug1_enc,
                drug2_enc,
                len(drug1),
                len(drug2)
            ]
            
            # Add description features if available
            if hasattr(self, 'tfidf') and description:
                desc_features = self.tfidf.transform([description]).toarray()[0]
                features.extend(desc_features)
            else:
                features.extend([0] * 100)  # Pad with zeros
            
            X_pred = np.array(features).reshape(1, -1)
            X_pred_scaled = self.scaler.transform(X_pred)
            
            # Make predictions
            interaction_prob = self.interaction_model.predict_proba(X_pred_scaled)[0]
            severity_prob = self.severity_model.predict_proba(X_pred_scaled)[0]
            
            interaction_pred = self.interaction_model.predict(X_pred_scaled)[0]
            severity_pred = self.severity_model.predict(X_pred_scaled)[0]
            
            return {
                'drug1': drug1,
                'drug2': drug2,
                'predicted_interaction': self.interaction_encoder.inverse_transform([interaction_pred])[0],
                'interaction_confidence': float(max(interaction_prob)),
                'predicted_severity': self.severity_encoder.inverse_transform([severity_pred])[0],
                'severity_confidence': float(max(severity_prob)),
                'ml_model': 'GradientBoosting + RandomForest'
            }
            
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    
    def save_models(self, save_dir="ml_models/trained_models"):
        """
        Save trained models and encoders
        """
        
        import os
        os.makedirs(save_dir, exist_ok=True)
        
        # Save models
        joblib.dump(self.interaction_model, f"{save_dir}/interaction_model.pkl")
        joblib.dump(self.severity_model, f"{save_dir}/severity_model.pkl")
        
        # Save encoders and scaler
        joblib.dump(self.drug_encoder, f"{save_dir}/drug_encoder.pkl")
        joblib.dump(self.interaction_encoder, f"{save_dir}/interaction_encoder.pkl")
        joblib.dump(self.severity_encoder, f"{save_dir}/severity_encoder.pkl")
        joblib.dump(self.scaler, f"{save_dir}/scaler.pkl")
        
        # Save feature names
        with open(f"{save_dir}/feature_names.json", 'w') as f:
            json.dump(self.feature_names, f)
        
        print(f"💾 Models saved to {save_dir}")
    
    def load_models(self, save_dir="ml_models/trained_models"):
        """
        Load pre-trained models
        """
        
        try:
            self.interaction_model = joblib.load(f"{save_dir}/interaction_model.pkl")
            self.severity_model = joblib.load(f"{save_dir}/severity_model.pkl")
            self.drug_encoder = joblib.load(f"{save_dir}/drug_encoder.pkl")
            self.interaction_encoder = joblib.load(f"{save_dir}/interaction_encoder.pkl")
            self.severity_encoder = joblib.load(f"{save_dir}/severity_encoder.pkl")
            self.scaler = joblib.load(f"{save_dir}/scaler.pkl")
            
            with open(f"{save_dir}/feature_names.json", 'r') as f:
                self.feature_names = json.load(f)
            
            print("✅ Models loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")

def create_enhanced_training_data():
    """
    Create enhanced training dataset for drug interactions
    """
    
    # Enhanced drug interaction data
    interaction_data = [
        {
            'drug1': 'Aspirin',
            'drug2': 'Warfarin', 
            'interaction_type': 'pharmacodynamic',
            'severity': 'high',
            'description': 'Increased bleeding risk due to antiplatelet and anticoagulant effects'
        },
        {
            'drug1': 'Metoprolol',
            'drug2': 'Verapamil',
            'interaction_type': 'pharmacodynamic',
            'severity': 'moderate',
            'description': 'Additive negative inotropic and chronotropic effects'
        },
        {
            'drug1': 'Simvastatin',
            'drug2': 'Clarithromycin',
            'interaction_type': 'pharmacokinetic',
            'severity': 'high',
            'description': 'CYP3A4 inhibition increases statin levels and rhabdomyolysis risk'
        },
        {
            'drug1': 'Lisinopril',
            'drug2': 'Potassium',
            'interaction_type': 'pharmacodynamic',
            'severity': 'moderate',
            'description': 'Risk of hyperkalemia due to ACE inhibitor and potassium supplementation'
        },
        {
            'drug1': 'Digoxin',
            'drug2': 'Amiodarone',
            'interaction_type': 'pharmacokinetic',
            'severity': 'high',
            'description': 'P-glycoprotein inhibition increases digoxin levels'
        },
        {
            'drug1': 'Ibuprofen',
            'drug2': 'Lithium',
            'interaction_type': 'pharmacokinetic',
            'severity': 'moderate',
            'description': 'NSAIDs reduce lithium clearance increasing toxicity risk'
        }
    ]
    
    # Create DataFrame and save
    df = pd.DataFrame(interaction_data)
    df.to_csv('enhanced_drug_interactions.csv', index=False)
    
    print("📊 Enhanced training dataset created: 'enhanced_drug_interactions.csv'")
    print(f"Contains {len(interaction_data)} drug interaction examples")
    
    return df

if __name__ == "__main__":
    print("💊 Drug Interaction ML Trainer for DoseSafe-AI")
    print("=" * 60)
    
    # Create enhanced training data
    df = create_enhanced_training_data()
    
    # Initialize and train model
    predictor = DrugInteractionPredictor()
    
    # Prepare features and train
    X, y_int, y_sev = predictor.prepare_features(df)
    results = predictor.train_interaction_model(X, y_int, y_sev)
    
    print(f"\n🎯 Training Results:")
    print(f"Interaction Accuracy: {results['interaction_accuracy']:.3f}")
    print(f"Severity Accuracy: {results['severity_accuracy']:.3f}")
    
    # Test prediction
    test_result = predictor.predict_interaction("Aspirin", "Warfarin")
    print(f"\n🧪 Test Prediction:")
    print(json.dumps(test_result, indent=2))
    
    # Save models
    predictor.save_models()
