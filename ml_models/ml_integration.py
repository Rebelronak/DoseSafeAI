"""
ML Integration Module for DoseSafe-AI
Loads trained models and provides easy-to-use functions for real-time prediction
"""

import os
import json
import joblib
import numpy as np
from fuzzywuzzy import fuzz
import warnings
warnings.filterwarnings('ignore')

class DoseSafeMLPredictor:
    """
    Production-ready ML predictor for DoseSafe-AI
    Loads trained models and provides prediction functions
    """
    
    def __init__(self, models_dir=None):
        if models_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            models_dir = os.path.join(current_dir, "models")
        
        self.models_dir = models_dir
        self.models = {}
        self.vectorizers = {}
        self.encoders = {}
        self.drug_database = []
        self.is_loaded = False
        
        # Try to load models
        self.load_models()
    
    def load_models(self):
        """Load all trained models, vectorizers, and encoders"""
        
        try:
            if not os.path.exists(self.models_dir):
                print(f"❌ Models directory not found: {self.models_dir}")
                return False
            
            print(f"🔄 Loading ML models from {self.models_dir}...")
            
            # Load models
            model_files = {
                'interaction_classifier': 'interaction_classifier.joblib',
                'severity_classifier': 'severity_classifier.joblib', 
                'medicine_extractor': 'medicine_extractor.joblib',
                'age_warning_classifier': 'age_warning_classifier.joblib'
            }
            
            for model_name, filename in model_files.items():
                model_path = os.path.join(self.models_dir, filename)
                if os.path.exists(model_path):
                    self.models[model_name] = joblib.load(model_path)
                    print(f"✅ Loaded {model_name}")
                else:
                    print(f"⚠️ Model not found: {filename}")
            
            # Load vectorizers
            vectorizer_files = {
                'interaction_text': 'interaction_text_vectorizer.joblib',
                'medicine_text': 'medicine_text_vectorizer.joblib',
                'warning_drug': 'warning_drug_vectorizer.joblib'
            }
            
            for vec_name, filename in vectorizer_files.items():
                vec_path = os.path.join(self.models_dir, filename)
                if os.path.exists(vec_path):
                    self.vectorizers[vec_name] = joblib.load(vec_path)
                    print(f"✅ Loaded {vec_name} vectorizer")
            
            # Load encoders
            encoder_files = {
                'severity': 'severity_encoder.joblib',
                'age_group': 'age_group_encoder.joblib'
            }
            
            for enc_name, filename in encoder_files.items():
                enc_path = os.path.join(self.models_dir, filename)
                if os.path.exists(enc_path):
                    self.encoders[enc_name] = joblib.load(enc_path)
                    print(f"✅ Loaded {enc_name} encoder")
            
            # Load drug database
            drugs_path = os.path.join(self.models_dir, "drug_database.json")
            if os.path.exists(drugs_path):
                with open(drugs_path, 'r') as f:
                    self.drug_database = json.load(f)
                print(f"✅ Loaded drug database with {len(self.drug_database)} drugs")
            
            self.is_loaded = True
            print(f"🎉 ML models loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading ML models: {e}")
            return False
    
    def _extract_medicine_section(self, text):
        """
        Extract only the medicine/prescription section from a full prescription document
        """
        lines = text.split('\n')
        medicine_lines = []
        
        # Look for lines that likely contain medicines (have dosage info or start with 'e')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip header info (hospital, doctor, patient info)
            if any(header in line.lower() for header in [
                'hospital', 'clinic', 'medical', 'doctor', 'physician', 'm.d.',
                'street', 'avenue', 'address', 'cityville', 'patient:', 'date:'
            ]):
                continue
            
            # Include lines that look like medicines
            if any(med_indicator in line.lower() for med_indicator in [
                'mg', 'ml', 'daily', 'bedtime', 'hours', 'tablet', 'capsule',
                'e' + line[1:2].lower() if len(line) > 1 else ''  # eMedicine pattern
            ]) or line.startswith('e') and len(line) > 3:
                medicine_lines.append(line)
        
        return ' '.join(medicine_lines) if medicine_lines else text

    def extract_medicines_from_text(self, text):
        """
        Extract medicine names from text using trained ML model with improved OCR handling
        """
        if not self.is_loaded or 'medicine_extractor' not in self.models:
            return self._fallback_medicine_extraction(text)
        
        try:
            print(f"🔍 Processing OCR text: {text[:100]}...")
            
            # First, extract only the medicine section from the full prescription
            medicine_section = self._extract_medicine_section(text)
            print(f"📋 Medicine section: {medicine_section[:100]}...")
            
            # Enhanced text preprocessing for messy OCR
            processed_text = self._preprocess_ocr_text(medicine_section)
            
            # Extract only the medicine section from the text
            medicine_section = self._extract_medicine_section(processed_text)
            print(f"  🏷️ Medicine section: {medicine_section}")
            
            # Split text into potential medicine words
            words = medicine_section.replace(',', ' ').replace(';', ' ').replace('\n', ' ').split()
            medicines = []
            confidences = []
            
            for word in words:
                cleaned_word = word.strip().strip('.,;:()[]{}')
                if len(cleaned_word) > 2:  # Skip very short words
                    
                    # Remove common prefixes that OCR adds
                    if cleaned_word.startswith('e') and len(cleaned_word) > 3:
                        cleaned_word = cleaned_word[1:]  # Remove 'e' prefix
                    
                    # Use ML model to predict if it's a medicine
                    X = self.vectorizers['medicine_text'].transform([cleaned_word])
                    prediction = self.models['medicine_extractor'].predict(X)[0]
                    confidence = self.models['medicine_extractor'].predict_proba(X)[0].max()
                    
                    if prediction == 1 and confidence > 0.6:  # Lowered threshold for OCR
                        medicines.append(cleaned_word)
                        confidences.append(float(confidence))
                        print(f"  ✅ Found medicine: {cleaned_word} (confidence: {confidence:.3f})")
            
            # Also try database matching for known medicines
            if self.drug_database:
                for drug in self.drug_database:
                    if drug.lower() in processed_text.lower():
                        if drug not in medicines:
                            medicines.append(drug)
                            print(f"  ✅ Database match: {drug}")
            
            # Remove duplicates while preserving order
            unique_medicines = []
            seen = set()
            for med in medicines:
                if med.lower() not in seen:
                    unique_medicines.append(med)
                    seen.add(med.lower())
            
            # Filter out false positives
            filtered_medicines = self._filter_false_positives(unique_medicines)
            
            print(f"🤖 ML extracted {len(filtered_medicines)} medicines: {filtered_medicines}")
            return filtered_medicines
            
        except Exception as e:
            print(f"❌ ML medicine extraction failed: {e}")
            return self._fallback_medicine_extraction(text)
    
    def _filter_false_positives(self, medicines):
        """
        Filter out false positives from extracted medicines
        """
        filtered_medicines = []
        
        # Exact matches to exclude (not substring matches)
        exclude_exact = [
            # Dosing instructions
            'oncedaily', 'onceadaily', 'twicedaily', 'threetimes', 'fourtimes',
            'bedtime', 'morning', 'evening', 'night', 'afternoon',
            'withfood', 'withoutfood', 'beforefood', 'afterfood',
            'asneeded', 'whennecessary', 'ifneeded',
            
            # Administration routes
            'oral', 'topical', 'injection', 'infusion', 'intravenous',
            'intramuscular', 'subcutaneous', 'sublingual',
            
            # General medical terms
            'avoidconcurrentuse', 'concurrent', 'interaction', 'warning',
            'severe', 'moderate', 'mild', 'contraindicated',
            'monitor', 'caution', 'avoid', 'reduce', 'increase',
            
            # Units and measurements
            'tablet', 'capsule', 'liquid', 'solution', 'suspension',
            'drop', 'drops', 'spray', 'patch', 'cream', 'ointment',
            
            # Common OCR artifacts
            'e', 'o', 'i', 'a', 'u',  # Single letters
            
            # Hospital/Medical facility terms
            'hospital', 'generalhospital', 'clinic', 'medical', 'center',
            'internalmedicine', 'medicine', 'patient', 'doctor', 'physician',
            'address', 'street', 'avenue', 'cityville', 'date'
        ]
        
        # Known legitimate medicine names that should never be filtered
        known_medicines = [
            'dexamethasone', 'ciprofloxacin', 'lorazepam', 'paracetamol',
            'aspirin', 'ibuprofen', 'warfarin', 'metformin', 'hydroxyzine',
            'amoxicillin', 'prednisolone', 'diazepam', 'morphine'
        ]
        
        # Minimum reasonable medicine name length
        min_length = 3
        
        for med in medicines:
            med_clean = med.lower().strip()
            
            # Skip if too short
            if len(med_clean) < min_length:
                continue
            
            # Always keep known medicines
            if med_clean in known_medicines:
                # Clean up the medicine name
                cleaned_med = self._clean_medicine_name(med)
                filtered_medicines.append(cleaned_med)
                print(f"  ✅ Kept known medicine: {cleaned_med}")
                continue
            
            # Check if it's an exact match to exclude patterns
            if med_clean in exclude_exact:
                print(f"  🚫 Filtered out false positive: {med}")
                continue
            
            # Clean up medicine names that have artifacts
            cleaned_med = self._clean_medicine_name(med)
            
            # Only keep if still reasonable length after cleaning
            if len(cleaned_med.strip()) >= min_length:
                # Avoid adding duplicates within the filtering process
                if cleaned_med.strip() not in filtered_medicines:
                    filtered_medicines.append(cleaned_med.strip())
        
        # Remove duplicates while preserving order (case-insensitive)
        unique_medicines = []
        seen = set()
        for med in filtered_medicines:
            med_lower = med.lower()
            if med_lower not in seen:
                unique_medicines.append(med)
                seen.add(med_lower)
        
        return unique_medicines
    
    def _clean_medicine_name(self, med):
        """Clean up a medicine name by removing artifacts"""
        import re
        
        # Clean up medicine names that have artifacts
        # e.g., "Ciprofloxacin:Severeinteraction" -> "Ciprofloxacin"
        if ':' in med:
            med = med.split(':')[0].strip()
            
        # Remove trailing dosing info
        # e.g., "Metformin500mg" -> "Metformin"
        med = re.sub(r'\d+\s*(mg|ml|mcg|g|units?).*$', '', med, flags=re.IGNORECASE).strip()
        
        return med

    def _preprocess_ocr_text(self, text):
        """Preprocess messy OCR text to improve medicine extraction"""
        import re
        
        # Fix common OCR issues
        text = text.replace('mg', ' mg ')  # Add spaces around mg
        text = text.replace('ml', ' ml ')  # Add spaces around ml
        text = text.replace('tablet', ' tablet ')
        text = text.replace('capsule', ' capsule ')
        
        # Split concatenated words that contain medicine names
        # Look for patterns like "eDexamethasone" or "eLorazepam"
        text = re.sub(r'e([A-Z][a-z]+)', r' \1', text)  # eDexamethasone -> Dexamethasone
        
        # Add spaces before dosages
        text = re.sub(r'([a-z])(\d+)', r'\1 \2', text)  # mg5 -> mg 5
        text = re.sub(r'(\d+)([a-z])', r'\1 \2', text)  # 5mg -> 5 mg
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def check_drug_interactions(self, drug1, drug2):
        """
        Check for drug interactions using trained ML model
        """
        if not self.is_loaded or 'interaction_classifier' not in self.models:
            return self._fallback_interaction_check(drug1, drug2)
        
        try:
            # Prepare features (same as training)
            drug1_clean = drug1.lower().strip()
            drug2_clean = drug2.lower().strip()
            
            combined_text = f"{drug1_clean} {drug2_clean}"
            similarity = fuzz.ratio(drug1_clean, drug2_clean) / 100.0
            len_diff = abs(len(drug1_clean) - len(drug2_clean))
            avg_len = (len(drug1_clean) + len(drug2_clean)) / 2
            
            # Simple category detection
            same_category = 1 if self._get_drug_category(drug1_clean) == self._get_drug_category(drug2_clean) else 0
            
            # Vectorize text
            text_features = self.vectorizers['interaction_text'].transform([combined_text])
            
            # Combine features
            numerical_features = np.array([[similarity, len_diff, avg_len, same_category]])
            X = np.hstack([text_features.toarray(), numerical_features])
            
            # Predict interaction
            has_interaction = self.models['interaction_classifier'].predict(X)[0]
            interaction_confidence = self.models['interaction_classifier'].predict_proba(X)[0].max()
            
            result = {
                'has_interaction': bool(has_interaction),
                'confidence': float(interaction_confidence),
                'severity': 'unknown'
            }
            
            # If interaction detected, predict severity
            if has_interaction and 'severity_classifier' in self.models:
                try:
                    severity_encoded = self.models['severity_classifier'].predict(X)[0]
                    severity = self.encoders['severity'].inverse_transform([severity_encoded])[0]
                    result['severity'] = severity
                except:
                    result['severity'] = 'medium'  # Default
            
            print(f"🤖 ML interaction check: {drug1} + {drug2} = {result}")
            return result
            
        except Exception as e:
            print(f"❌ ML interaction check failed: {e}")
            return self._fallback_interaction_check(drug1, drug2)
    
    def check_age_warnings(self, drug_name, age_group="Adult"):
        """
        Check for age-related warnings using trained ML model
        """
        if not self.is_loaded or 'age_warning_classifier' not in self.models:
            return self._fallback_age_check(drug_name, age_group)
        
        try:
            # Prepare features
            drug_features = self.vectorizers['warning_drug'].transform([drug_name])
            
            # Encode age group
            try:
                age_encoded = self.encoders['age_group'].transform([age_group])[0]
            except:
                # If age group not seen during training, use a default
                age_encoded = 0
            
            age_features = np.array([[age_encoded]])
            
            # Combine features
            X = np.hstack([drug_features.toarray(), age_features])
            
            # Predict warning
            has_warning = self.models['age_warning_classifier'].predict(X)[0]
            warning_confidence = self.models['age_warning_classifier'].predict_proba(X)[0].max()
            
            result = {
                'has_warning': bool(has_warning),
                'confidence': float(warning_confidence),
                'age_group': age_group,
                'drug_name': drug_name
            }
            
            print(f"🤖 ML age warning check: {drug_name} for {age_group} = {result}")
            return result
            
        except Exception as e:
            print(f"❌ ML age warning check failed: {e}")
            return self._fallback_age_check(drug_name, age_group)
    
    def _get_drug_category(self, drug_name):
        """Simple drug categorization"""
        drug_lower = drug_name.lower()
        
        if any(word in drug_lower for word in ['pril', 'sartan']):
            return 'cardiovascular'
        elif any(word in drug_lower for word in ['statin', 'atorv', 'simv']):
            return 'lipid_lowering'
        elif any(word in drug_lower for word in ['pam', 'zolam', 'zepam']):
            return 'psychiatric'
        elif any(word in drug_lower for word in ['cillin', 'mycin', 'floxacin']):
            return 'antibiotic'
        else:
            return 'other'
    
    def _fallback_medicine_extraction(self, text):
        """Fallback method when ML is not available - enhanced for OCR text"""
        print("⚠️ Using enhanced fallback medicine extraction")
        
        # Preprocess the text
        processed_text = self._preprocess_ocr_text(text)
        
        # Simple keyword-based extraction
        words = processed_text.replace(',', ' ').replace(';', ' ').split()
        medicines = []
        
        for word in words:
            cleaned = word.strip().strip('.,;:()[]{}')
            
            # Remove common OCR prefixes
            if cleaned.startswith('e') and len(cleaned) > 3:
                cleaned = cleaned[1:]
            
            if len(cleaned) > 3 and any(c.isalpha() for c in cleaned):
                # Check against drug database if available
                if self.drug_database:
                    for drug in self.drug_database:
                        # Exact match or partial match
                        if (cleaned.lower() == drug.lower() or 
                            drug.lower() in cleaned.lower() or 
                            cleaned.lower() in drug.lower()):
                            medicines.append(drug)
                            print(f"  ✅ Fallback found: {drug}")
                            break
                else:
                    # Very basic heuristic for common medicine patterns
                    if any(suffix in cleaned.lower() for suffix in ['cin', 'ine', 'ol', 'am', 'one', 'zole']):
                        medicines.append(cleaned)
        
        # Also check for exact medicine names in the original text
        common_medicines = [
            'Dexamethasone', 'Ciprofloxacin', 'Lorazepam', 'Paracetamol',
            'Aspirin', 'Ibuprofen', 'Warfarin', 'Metformin', 'Hydroxyzine'
        ]
        
        for med in common_medicines:
            if med.lower() in text.lower():
                if med not in medicines:
                    medicines.append(med)
                    print(f"  ✅ Common medicine found: {med}")
        
        # Filter out false positives and remove duplicates
        all_medicines = self._filter_false_positives(medicines)
        return list(set(all_medicines))  # Remove duplicates
    
    def _fallback_interaction_check(self, drug1, drug2):
        """Fallback method when ML is not available"""
        print("⚠️ Using fallback interaction check")
        
        # Simple similarity-based check
        similarity = fuzz.ratio(drug1.lower(), drug2.lower())
        
        return {
            'has_interaction': similarity > 90,  # Very conservative
            'confidence': 0.5,
            'severity': 'unknown'
        }
    
    def _fallback_age_check(self, drug_name, age_group):
        """Fallback method when ML is not available"""
        print("⚠️ Using fallback age warning check")
        
        # Basic age-related warnings
        risky_for_children = ['aspirin', 'codeine', 'tramadol']
        risky_for_elderly = ['benzodiazepine', 'anticholinergic']
        
        has_warning = False
        if age_group in ['<18', '<2 years', 'Neonates']:
            has_warning = any(risk in drug_name.lower() for risk in risky_for_children)
        elif age_group == 'Elderly':
            has_warning = any(risk in drug_name.lower() for risk in risky_for_elderly)
        
        return {
            'has_warning': has_warning,
            'confidence': 0.6,
            'age_group': age_group,
            'drug_name': drug_name
        }
    
    def get_model_status(self):
        """Get status of loaded models"""
        return {
            'ml_available': self.is_loaded,
            'models_loaded': list(self.models.keys()),
            'vectorizers_loaded': list(self.vectorizers.keys()),
            'encoders_loaded': list(self.encoders.keys()),
            'drug_database_size': len(self.drug_database)
        }

# Global instance for easy import
dosesafe_ml = DoseSafeMLPredictor()

# Convenience functions for easy use
def extract_medicines(text):
    """Extract medicines from text using ML"""
    return dosesafe_ml.extract_medicines_from_text(text)

def check_interactions(drug1, drug2):
    """Check drug interactions using ML"""
    return dosesafe_ml.check_drug_interactions(drug1, drug2)

def check_age_warnings(drug_name, age_group="Adult"):
    """Check age warnings using ML"""
    return dosesafe_ml.check_age_warnings(drug_name, age_group)

def get_ml_status():
    """Get ML system status"""
    return dosesafe_ml.get_model_status()
