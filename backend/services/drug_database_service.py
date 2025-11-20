import pandas as pd
import os
from fuzzywuzzy import fuzz, process
import json

class DrugDatabaseService:
    def __init__(self):
        self.interactions_df = None
        self.warnings_df = None
        self.drug_names = set()
        self.load_databases()
    
    def load_databases(self):
        """Load CSV databases"""
        try:
            # Load drug interactions
            interactions_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'drug_interactions.csv')
            if os.path.exists(interactions_path):
                self.interactions_df = pd.read_csv(interactions_path)
                print(f"✅ Loaded {len(self.interactions_df)} drug interactions")
                
                # Extract all drug names
                drugs1 = set(self.interactions_df['drug1'].str.lower().str.strip())
                drugs2 = set(self.interactions_df['drug2'].str.lower().str.strip())
                self.drug_names.update(drugs1, drugs2)
            
            # Load drug warnings
            warnings_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'drug_warning.csv')
            if os.path.exists(warnings_path):
                self.warnings_df = pd.read_csv(warnings_path)
                print(f"✅ Loaded {len(self.warnings_df)} drug warnings")
                
                # Extract drug names from warnings
                warning_drugs = set(self.warnings_df[' drug_name'].str.lower().str.strip())
                self.drug_names.update(warning_drugs)
                
            print(f"✅ Total unique drugs in database: {len(self.drug_names)}")
            
        except Exception as e:
            print(f"❌ Failed to load drug databases: {e}")
    
    def find_drug_matches(self, drug_name, threshold=80):
        """Find matching drugs using fuzzy matching"""
        if not self.drug_names:
            return []
            
        drug_name_clean = drug_name.lower().strip()
        
        # Exact match first
        if drug_name_clean in self.drug_names:
            return [drug_name_clean]
        
        # Fuzzy matching
        matches = process.extractBests(drug_name_clean, self.drug_names, 
                                     scorer=fuzz.ratio, score_cutoff=threshold, limit=3)
        
        return [match[0] for match in matches]
    
    def check_drug_interactions(self, medications):
        """Check for drug interactions using CSV data"""
        if self.interactions_df is None:
            return []
        
        interactions = []
        drug_list = []
        
        # Normalize medication names
        for med in medications:
            if isinstance(med, str):
                drug_name = med
            else:
                drug_name = med.get('name', '') or med.get('medication', '')
            
            matches = self.find_drug_matches(drug_name)
            if matches:
                drug_list.append(matches[0])  # Use best match
        
        # Check all pairs for interactions
        for i, drug1 in enumerate(drug_list):
            for j, drug2 in enumerate(drug_list[i+1:], i+1):
                # Check both directions
                interaction1 = self.interactions_df[
                    (self.interactions_df['drug1'].str.lower() == drug1) &
                    (self.interactions_df['drug2'].str.lower() == drug2)
                ]
                
                interaction2 = self.interactions_df[
                    (self.interactions_df['drug1'].str.lower() == drug2) &
                    (self.interactions_df['drug2'].str.lower() == drug1)
                ]
                
                for _, row in pd.concat([interaction1, interaction2]).iterrows():
                    interactions.append({
                        'drugs': [drug1.title(), drug2.title()],
                        'severity': row['severity'],
                        'mechanism': row['note'],
                        'clinical_effects': f"Interaction between {drug1.title()} and {drug2.title()}",
                        'recommendation': row['note'],
                        'monitoring': f"Monitor patient closely when using {drug1.title()} and {drug2.title()} together"
                    })
        
        return interactions
    
    def check_age_warnings(self, medications, patient_age):
        """Check for age-specific warnings using CSV data"""
        if self.warnings_df is None:
            return []
        
        warnings = []
        
        for med in medications:
            if isinstance(med, str):
                drug_name = med
            else:
                drug_name = med.get('name', '') or med.get('medication', '')
            
            matches = self.find_drug_matches(drug_name)
            
            for matched_drug in matches:
                # Find warnings for this drug
                drug_warnings = self.warnings_df[
                    self.warnings_df[' drug_name'].str.lower().str.strip() == matched_drug
                ]
                
                for _, row in drug_warnings.iterrows():
                    age_group = row['age_group']
                    is_applicable = self._check_age_applicability(age_group, patient_age)
                    
                    if is_applicable:
                        warnings.append({
                            'medication': matched_drug.title(),
                            'warning': row['warning'],
                            'severity': row['severity'],
                            'recommendation': f"Consider alternative: {row['alternative']}. {row['note']}",
                            'age_group': age_group
                        })
        
        return warnings
    
    def _check_age_applicability(self, age_group, patient_age):
        """Check if age group applies to patient"""
        try:
            if age_group == 'All':
                return True
            elif age_group == 'Elderly' and patient_age >= 65:
                return True
            elif age_group == 'Neonates' and patient_age < 1:
                return True
            elif '<' in age_group:
                threshold = int(age_group.replace('<', '').strip().split()[0])
                return patient_age < threshold
            elif '>' in age_group:
                threshold = int(age_group.replace('>', '').strip().split()[0])
                return patient_age > threshold
        except:
            pass
        
        return False
    
    def find_contraindications(self, medications):
        """Find contraindications based on high severity warnings"""
        contraindications = []
        
        if self.warnings_df is None:
            return contraindications
        
        for med in medications:
            if isinstance(med, str):
                drug_name = med
            else:
                drug_name = med.get('name', '') or med.get('medication', '')
            
            matches = self.find_drug_matches(drug_name)
            
            for matched_drug in matches:
                # Find high/critical severity warnings
                critical_warnings = self.warnings_df[
                    (self.warnings_df[' drug_name'].str.lower().str.strip() == matched_drug) &
                    (self.warnings_df['severity'].isin(['High', 'Critical']))
                ]
                
                for _, row in critical_warnings.iterrows():
                    contraindications.append({
                        'medication': matched_drug.title(),
                        'contraindication': row['warning'],
                        'reason': row['note'],
                        'severity': row['severity']
                    })
        
        return contraindications
    
    def find_harmful_combinations(self, medications):
        """Find harmful drug combinations from high severity interactions"""
        harmful = []
        
        if self.interactions_df is None:
            return harmful
        
        interactions = self.check_drug_interactions(medications)
        
        for interaction in interactions:
            if interaction['severity'].lower() in ['high', 'severe']:
                harmful.append({
                    'medications': interaction['drugs'],
                    'danger_level': 'high',
                    'potential_harm': interaction['mechanism']
                })
        
        return harmful

# Global instance
drug_db_service = DrugDatabaseService()
