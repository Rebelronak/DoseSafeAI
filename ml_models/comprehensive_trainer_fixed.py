"""
Advanced ML Training Pipeline for DoseSafe-AI
Uses existing CSV data to train comprehensive ML models with proper evaluation metrics
"""

import pandas as pd
import numpy as np
import os
import json
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
import xgboost as xgb
import lightgbm as lgb
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class DoseSafeMLTrainer:
    """
    Comprehensive ML trainer using your existing CSV data
    """
    
    def __init__(self, data_dir="../data"):
        # Fix the path to your actual data directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(current_dir, "..", "data")
        print(f"📁 Data directory: {self.data_dir}")
        
        self.models = {}
        self.vectorizers = {}
        self.encoders = {}
        self.training_stats = {}
        
    def load_existing_data(self):
        """Load your existing CSV files"""
        
        print("📊 Loading existing DoseSafe-AI data...")
        
        # Check if data directory exists
        if not os.path.exists(self.data_dir):
            print(f"❌ Data directory not found: {self.data_dir}")
            return False
        
        # Load drug interactions
        interactions_path = os.path.join(self.data_dir, "drug_interactions.csv")
        if not os.path.exists(interactions_path):
            print(f"❌ File not found: {interactions_path}")
            return False
            
        self.drug_interactions = pd.read_csv(interactions_path)
        print(f"✅ Loaded {len(self.drug_interactions)} drug interactions")
        print(f"   Sample: {self.drug_interactions.head(2).to_dict('records')}")
        
        # Load drug warnings  
        warnings_path = os.path.join(self.data_dir, "drug_warning.csv")
        if not os.path.exists(warnings_path):
            print(f"❌ File not found: {warnings_path}")
            return False
            
        self.drug_warnings = pd.read_csv(warnings_path)
        print(f"✅ Loaded {len(self.drug_warnings)} drug warnings")
        print(f"   Sample: {self.drug_warnings.head(2).to_dict('records')}")
        
        # Extract unique drugs
        drugs_from_interactions = set(self.drug_interactions['drug1'].tolist() + self.drug_interactions['drug2'].tolist())
        drugs_from_warnings = set(self.drug_warnings[' drug_name'].str.strip().tolist())
        
        self.all_drugs = drugs_from_interactions.union(drugs_from_warnings)
        print(f"✅ Total unique drugs: {len(self.all_drugs)}")
        print(f"   Sample drugs: {list(self.all_drugs)[:10]}")
        
        return True
    
    def create_expanded_interaction_dataset(self):
        """Create expanded dataset for interaction prediction"""
        
        print("🔄 Creating expanded interaction dataset...")
        
        # Base interactions from CSV
        interactions_data = []
        
        for _, row in self.drug_interactions.iterrows():
            interactions_data.append({
                'drug1': row['drug1'].strip(),
                'drug2': row['drug2'].strip(), 
                'severity': row['severity'].strip(),
                'has_interaction': 1,
                'note': row['note']
            })
        
        # Create negative samples (no interaction)
        drug_list = list(self.all_drugs)
        negative_samples = 0
        target_negatives = len(interactions_data) * 2  # 2:1 ratio negative:positive
        
        existing_pairs = set()
        for item in interactions_data:
            pair1 = (item['drug1'], item['drug2'])
            pair2 = (item['drug2'], item['drug1'])
            existing_pairs.add(pair1)
            existing_pairs.add(pair2)
        
        while negative_samples < target_negatives:
            drug1 = np.random.choice(drug_list)
            drug2 = np.random.choice(drug_list)
            
            if drug1 != drug2 and (drug1, drug2) not in existing_pairs:
                interactions_data.append({
                    'drug1': drug1,
                    'drug2': drug2,
                    'severity': 'none',
                    'has_interaction': 0,
                    'note': 'No known interaction'
                })
                existing_pairs.add((drug1, drug2))
                existing_pairs.add((drug2, drug1))
                negative_samples += 1
        
        self.interaction_dataset = pd.DataFrame(interactions_data)
        print(f"✅ Created interaction dataset: {len(self.interaction_dataset)} samples")
        print(f"   - Positive samples (interactions): {sum(self.interaction_dataset['has_interaction'])}")
        print(f"   - Negative samples (no interaction): {len(self.interaction_dataset) - sum(self.interaction_dataset['has_interaction'])}")
        
        return self.interaction_dataset
    
    def create_medicine_extraction_dataset(self):
        """Create dataset for medicine name extraction training"""
        
        print("🔄 Creating medicine extraction dataset...")
        
        extraction_data = []
        
        # Positive samples - actual medicine names
        for drug in self.all_drugs:
            clean_drug = drug.strip()
            if len(clean_drug) > 2:  # Skip very short names
                extraction_data.append({
                    'text': clean_drug,
                    'is_medicine': 1,
                    'drug_category': self._get_drug_category(clean_drug)
                })
                
                # Add variations
                variations = [
                    clean_drug.upper(),
                    clean_drug.lower(), 
                    clean_drug.title(),
                    clean_drug + "variant22",
                    clean_drug + "variant21",
                    clean_drug + " tablet",
                    clean_drug + " capsule"
                ]
                
                for variation in variations:
                    extraction_data.append({
                        'text': variation,
                        'is_medicine': 1,
                        'drug_category': self._get_drug_category(clean_drug)
                    })
        
        # Negative samples - non-medicine words
        non_medicine_words = [
            "patient", "age", "doctor", "hospital", "clinic", "prescription",
            "daily", "twice", "morning", "evening", "tablet", "capsule",
            "before", "after", "meals", "food", "water", "instructions",
            "dose", "dosage", "frequency", "continue", "stop", "start",
            "monday", "tuesday", "wednesday", "thursday", "friday",
            "january", "february", "march", "april", "may", "june",
            "blood", "pressure", "heart", "diabetes", "pain", "headache",
            "mg", "ml", "g", "mcg", "units", "times", "per", "day",
            "take", "use", "apply", "as", "needed", "directed", "prescribed"
        ]
        
        # Add negative samples (multiply to balance dataset)
        for _ in range(3):
            for word in non_medicine_words:
                extraction_data.append({
                    'text': word,
                    'is_medicine': 0,
                    'drug_category': 'none'
                })
        
        self.extraction_dataset = pd.DataFrame(extraction_data)
        print(f"✅ Created extraction dataset: {len(self.extraction_dataset)} samples")
        print(f"   - Medicine samples: {sum(self.extraction_dataset['is_medicine'])}")
        print(f"   - Non-medicine samples: {len(self.extraction_dataset) - sum(self.extraction_dataset['is_medicine'])}")
        
        return self.extraction_dataset
    
    def _get_drug_category(self, drug_name):
        """Simple drug categorization based on name patterns"""
        
        drug_lower = drug_name.lower()
        
        if any(word in drug_lower for word in ['pril', 'sartan']):
            return 'cardiovascular'
        elif any(word in drug_lower for word in ['statin', 'atorv', 'simv']):
            return 'lipid_lowering'
        elif any(word in drug_lower for word in ['pam', 'zolam', 'zepam']):
            return 'psychiatric'
        elif any(word in drug_lower for word in ['cillin', 'mycin', 'floxacin']):
            return 'antibiotic'
        elif any(word in drug_lower for word in ['ibuprofen', 'aspirin', 'naproxen']):
            return 'nsaid'
        elif any(word in drug_lower for word in ['metformin', 'insulin']):
            return 'antidiabetic'
        else:
            return 'other'
    
    def train_interaction_predictor(self):
        """Train drug interaction prediction model"""
        
        print("🚀 Training Drug Interaction Predictor...")
        
        # Create features
        X_features = []
        for _, row in self.interaction_dataset.iterrows():
            drug1 = row['drug1'].lower().strip()
            drug2 = row['drug2'].lower().strip()
            
            # Text features
            combined_text = f"{drug1} {drug2}"
            
            # Similarity features
            similarity = fuzz.ratio(drug1, drug2) / 100.0
            
            # Length features
            len_diff = abs(len(drug1) - len(drug2))
            avg_len = (len(drug1) + len(drug2)) / 2
            
            # Category features
            cat1 = self._get_drug_category(drug1)
            cat2 = self._get_drug_category(drug2)
            same_category = 1 if cat1 == cat2 else 0
            
            features = {
                'combined_text': combined_text,
                'similarity': similarity,
                'len_diff': len_diff,
                'avg_len': avg_len,
                'same_category': same_category
            }
            
            X_features.append(features)
        
        # Convert to DataFrame
        features_df = pd.DataFrame(X_features)
        
        # Vectorize text features
        self.vectorizers['interaction_text'] = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        text_features = self.vectorizers['interaction_text'].fit_transform(features_df['combined_text'])
        
        # Combine with numerical features
        numerical_features = features_df[['similarity', 'len_diff', 'avg_len', 'same_category']].values
        X = np.hstack([text_features.toarray(), numerical_features])
        
        # Target variables
        y_interaction = self.interaction_dataset['has_interaction'].values
        y_severity = self.interaction_dataset['severity'].values
        
        # Encode severity labels
        self.encoders['severity'] = LabelEncoder()
        y_severity_encoded = self.encoders['severity'].fit_transform(y_severity)
        
        # Split data
        X_train, X_test, y_int_train, y_int_test, y_sev_train, y_sev_test = train_test_split(
            X, y_interaction, y_severity_encoded, test_size=0.2, random_state=42, stratify=y_interaction
        )
        
        print(f"📊 Training set: {X_train.shape[0]} samples")
        print(f"📊 Test set: {X_test.shape[0]} samples")
        
        # Train interaction classifier
        print("🔧 Training interaction classifier...")
        self.models['interaction_classifier'] = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        
        self.models['interaction_classifier'].fit(X_train, y_int_train)
        
        # Evaluate interaction classifier
        y_int_pred = self.models['interaction_classifier'].predict(X_test)
        int_f1 = f1_score(y_int_test, y_int_pred)
        int_precision = precision_score(y_int_test, y_int_pred)
        int_recall = recall_score(y_int_test, y_int_pred)
        
        print(f"\\n📈 Interaction Classifier Results:")
        print(f"   F1 Score: {int_f1:.4f}")
        print(f"   Precision: {int_precision:.4f}")
        print(f"   Recall: {int_recall:.4f}")
        
        # Train severity classifier (only on positive interactions)
        interaction_mask = y_int_train == 1
        if np.sum(interaction_mask) > 10:  # Ensure enough samples
            print("🔧 Training severity classifier...")
            self.models['severity_classifier'] = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            self.models['severity_classifier'].fit(X_train[interaction_mask], y_sev_train[interaction_mask])
            
            # Evaluate severity classifier
            test_interaction_mask = y_int_test == 1
            if np.sum(test_interaction_mask) > 0:
                y_sev_pred = self.models['severity_classifier'].predict(X_test[test_interaction_mask])
                sev_f1 = f1_score(y_sev_test[test_interaction_mask], y_sev_pred, average='weighted')
                
                print(f"\\n📈 Severity Classifier Results:")
                print(f"   F1 Score (weighted): {sev_f1:.4f}")
        
        # Store training stats
        self.training_stats['interaction_model'] = {
            'f1_score': float(int_f1),
            'precision': float(int_precision),
            'recall': float(int_recall),
            'training_samples': X_train.shape[0],
            'test_samples': X_test.shape[0]
        }
        
        return True
    
    def train_medicine_extractor(self):
        """Train medicine name extraction model"""
        
        print("🚀 Training Medicine Extractor...")
        
        # Prepare features
        texts = self.extraction_dataset['text'].values
        labels = self.extraction_dataset['is_medicine'].values
        
        # Create text features
        self.vectorizers['medicine_text'] = TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 3),
            analyzer='char',  # Character-level for better medicine matching
            lowercase=True
        )
        
        X = self.vectorizers['medicine_text'].fit_transform(texts)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        print(f"📊 Training set: {X_train.shape[0]} samples")
        print(f"📊 Test set: {X_test.shape[0]} samples")
        
        # Train model
        self.models['medicine_extractor'] = xgb.XGBClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        
        self.models['medicine_extractor'].fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.models['medicine_extractor'].predict(X_test)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        
        print(f"\n📈 Medicine Extractor Results:")
        print(f"   F1 Score: {f1:.4f}")
        print(f"   Precision: {precision:.4f}")
        print(f"   Recall: {recall:.4f}")
        
        # Detailed classification report
        print("\n📋 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=['Non-Medicine', 'Medicine']))
        
        # Store training stats
        self.training_stats['medicine_extractor'] = {
            'f1_score': float(f1),
            'precision': float(precision),
            'recall': float(recall),
            'training_samples': X_train.shape[0],
            'test_samples': X_test.shape[0]
        }
        
        return True
    
    def train_age_warning_classifier(self):
        """Train age-related warning classifier"""
        
        print("🚀 Training Age Warning Classifier...")
        
        # Prepare age warning data
        warning_data = []
        for _, row in self.drug_warnings.iterrows():
            drug_name = row[' drug_name'].strip()
            age_group = row['age_group'].strip()
            severity = row['severity'].strip()
            
            warning_data.append({
                'drug_name': drug_name,
                'age_group': age_group,
                'severity': severity,
                'has_warning': 1
            })
        
        # Create negative samples (drugs without warnings for certain age groups)
        age_groups = ['<2 years', '<18', 'Elderly', 'Adult', 'All', 'Neonates']
        drugs_with_warnings = set(self.drug_warnings[' drug_name'].str.strip())
        
        for drug in self.all_drugs:
            if drug not in drugs_with_warnings:
                for age_group in age_groups[:3]:  # Add some negative samples
                    warning_data.append({
                        'drug_name': drug,
                        'age_group': age_group,
                        'severity': 'none',
                        'has_warning': 0
                    })
        
        warning_df = pd.DataFrame(warning_data)
        
        # Create features
        drug_texts = warning_df['drug_name'].values
        age_groups = warning_df['age_group'].values
        
        # Text features for drugs
        self.vectorizers['warning_drug'] = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        drug_features = self.vectorizers['warning_drug'].fit_transform(drug_texts)
        
        # Encode age groups
        self.encoders['age_group'] = LabelEncoder()
        age_features = self.encoders['age_group'].fit_transform(age_groups).reshape(-1, 1)
        
        # Combine features
        X = np.hstack([drug_features.toarray(), age_features])
        y = warning_df['has_warning'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.models['age_warning_classifier'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            random_state=42
        )
        
        self.models['age_warning_classifier'].fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.models['age_warning_classifier'].predict(X_test)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        
        print(f"\\n📈 Age Warning Classifier Results:")
        print(f"   F1 Score: {f1:.4f}")
        print(f"   Precision: {precision:.4f}")
        print(f"   Recall: {recall:.4f}")
        
        # Store training stats
        self.training_stats['age_warning_classifier'] = {
            'f1_score': float(f1),
            'precision': float(precision),
            'recall': float(recall),
            'training_samples': X_train.shape[0],
            'test_samples': X_test.shape[0]
        }
        
        return True
    
    def save_models(self, models_dir="models"):
        """Save all trained models"""
        
        os.makedirs(models_dir, exist_ok=True)
        
        # Save models
        for model_name, model in self.models.items():
            model_path = os.path.join(models_dir, f"{model_name}.joblib")
            joblib.dump(model, model_path)
            print(f"💾 Saved {model_name} to {model_path}")
        
        # Save vectorizers
        for vec_name, vectorizer in self.vectorizers.items():
            vec_path = os.path.join(models_dir, f"{vec_name}_vectorizer.joblib")
            joblib.dump(vectorizer, vec_path)
            print(f"💾 Saved {vec_name} vectorizer to {vec_path}")
        
        # Save encoders
        for enc_name, encoder in self.encoders.items():
            enc_path = os.path.join(models_dir, f"{enc_name}_encoder.joblib")
            joblib.dump(encoder, enc_path)
            print(f"💾 Saved {enc_name} encoder to {enc_path}")
        
        # Save training stats
        stats_path = os.path.join(models_dir, "training_stats.json")
        with open(stats_path, 'w') as f:
            json.dump(self.training_stats, f, indent=2)
        print(f"📊 Saved training statistics to {stats_path}")
        
        # Save drug list
        drugs_path = os.path.join(models_dir, "drug_database.json")
        with open(drugs_path, 'w') as f:
            json.dump(list(self.all_drugs), f, indent=2)
        print(f"💊 Saved drug database to {drugs_path}")
    
    def generate_training_report(self):
        """Generate comprehensive training report"""
        
        print("\\n" + "="*60)
        print("🎯 DOSESAFE-AI ML TRAINING REPORT")
        print("="*60)
        
        print(f"\\n📊 Dataset Summary:")
        print(f"   • Drug Interactions: {len(self.drug_interactions)} from CSV")
        print(f"   • Drug Warnings: {len(self.drug_warnings)} from CSV")
        print(f"   • Unique Drugs: {len(self.all_drugs)}")
        print(f"   • Generated Training Samples: {len(self.interaction_dataset)}")
        
        print(f"\\n🤖 Model Performance:")
        for model_name, stats in self.training_stats.items():
            print(f"\\n   {model_name.upper()}:")
            print(f"     F1 Score: {stats['f1_score']:.4f}")
            print(f"     Precision: {stats['precision']:.4f}")
            print(f"     Recall: {stats['recall']:.4f}")
            print(f"     Training Samples: {stats['training_samples']}")
            print(f"     Test Samples: {stats['test_samples']}")
        
        print(f"\\n🎉 Training completed successfully!")
        print(f"✅ All models saved and ready for production use")
        
        return self.training_stats

def main():
    """Main training pipeline"""
    
    print("🏥 DoseSafe-AI Advanced ML Training Pipeline")
    print("Using existing CSV data + synthetic augmentation")
    print("="*70)
    
    # Initialize trainer
    trainer = DoseSafeMLTrainer()
    
    # Load existing data
    if not trainer.load_existing_data():
        print("❌ Failed to load data. Please check your CSV files.")
        return None
    
    # Create expanded datasets
    trainer.create_expanded_interaction_dataset()
    trainer.create_medicine_extraction_dataset()
    
    # Train all models
    trainer.train_interaction_predictor()
    trainer.train_medicine_extractor()
    trainer.train_age_warning_classifier()
    
    # Save models
    trainer.save_models()
    
    # Generate report
    trainer.generate_training_report()
    
    return trainer

if __name__ == "__main__":
    trainer = main()
