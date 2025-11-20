import csv
import os
import difflib
import re

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
INTERACTIONS_FILE = os.path.join(DATA_DIR, 'drug_interactions.csv')
WARNINGS_FILE = os.path.join(DATA_DIR, 'drug_warning.csv')

# Load drug interactions into a list of dicts
def load_interactions():
    interactions = []
    with open(INTERACTIONS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            interactions.append({
                'drug1': row['drug1'].strip().lower(),
                'drug2': row['drug2'].strip().lower(),
                'severity': row.get('severity', ''),
                'note': row.get('note', '')
            })
    return interactions

# Load drug warnings into a dict: drug_name -> warning/note/age_group/severity
def load_warnings():
    warnings = {}
    with open(WARNINGS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            drug = row['drug_name'].strip().lower()
            warning_obj = {
                'warning': row.get('warning', ''),
                'note': row.get('note', ''),
                'age_group': row.get('age_group', 'all'),
                'severity': row.get('severity', '')
            }
            if drug not in warnings:
                warnings[drug] = []
            warnings[drug].append(warning_obj)
    return warnings

INTERACTIONS = load_interactions()
WARNINGS = load_warnings()

print("Loaded interactions:", INTERACTIONS[:3])  # Show first 3 for brevity
print("Loaded warnings:", list(WARNINGS.items())[:3])  # Show first 3 for brevity

SEVERITY_RANK = {'critical': 3, 'high': 2, 'moderate': 1, 'low': 0}

def get_severity_rank(severity):
    ranks = {"critical": 4, "high": 3, "medium": 2, "moderate": 2, "low": 1}
    return ranks.get(severity.lower(), 0)

def normalize(name):
    return re.sub(r'[^a-zA-Z]', '', name).lower()

def interaction_matches(med1, med2, csv1, csv2):
    n1, n2 = normalize(med1), normalize(med2)
    c1, c2 = normalize(csv1), normalize(csv2)
    return (n1 == c1 and n2 == c2) or (n1 == c2 and n2 == c1)

def is_warning_relevant(warning_age_group, patient_age):
    if warning_age_group.lower() in ['all', '', 'any']:
        return True
    try:
        if '<' in warning_age_group:
            limit = int(''.join(filter(str.isdigit, warning_age_group)))
            return patient_age is not None and patient_age < limit
        if '>' in warning_age_group:
            limit = int(''.join(filter(str.isdigit, warning_age_group)))
            return patient_age is not None and patient_age > limit
        if 'neonate' in warning_age_group.lower() and patient_age is not None and patient_age < 1:
            return True
        if 'child' in warning_age_group.lower() and patient_age is not None and patient_age < 18:
            return True
        if 'elderly' in warning_age_group.lower() and patient_age is not None and patient_age >= 65:
            return True
    except Exception:
        return False
    return False

def check_interactions_and_warnings(medicines, age=None):
    print("Medicines received:", medicines, "Age:", age)
    print("All warning keys:", list(WARNINGS.keys())[:10])  # show first 10 for brevity

    meds = [m.strip().lower() for m in medicines]
    found_interactions = {}
    found_warnings = []

    # Check interactions (deduplicate and keep highest severity)
    for i in range(len(meds)):
        for j in range(i+1, len(meds)):
            for entry in INTERACTIONS:
                pair = tuple(sorted([entry['drug1'], entry['drug2']]))
                if interaction_matches(meds[i], meds[j], entry['drug1'], entry['drug2']):
                    current = found_interactions.get(pair)
                    new_severity = get_severity_rank(entry['severity'])
                    if not current or new_severity > get_severity_rank(current['severity']):
                        found_interactions[pair] = {
                            'drug1': entry['drug1'].title(),
                            'drug2': entry['drug2'].title(),
                            'severity': entry['severity'],
                            'note': entry['note']
                        }

    # Check single-drug warnings (with age logic)
    for med in meds:
        best_warning = None
        best_severity = 0
        for warning in WARNINGS.get(med, []):
            warning_age_group = warning.get('age_group', 'all')
            if is_warning_relevant(warning_age_group, age):
                severity_rank = get_severity_rank(warning.get('severity', ''))
                if severity_rank > best_severity:
                    best_severity = severity_rank
                    best_warning = {
                        'drug': med.title(),
                        'warning': warning['warning'],
                        'note': warning['note'],
                        'severity': warning.get('severity', '')
                    }
        if best_warning and best_severity >= 2:  # Only show medium or higher
            found_warnings.append(best_warning)

    # Remove duplicate warnings by drug name (optional)
    unique_warnings = {}
    for w in found_warnings:
        key = w['drug']
        if key not in unique_warnings or get_severity_rank(w['severity']) > get_severity_rank(unique_warnings[key]['severity']):
            unique_warnings[key] = w
    found_warnings = list(unique_warnings.values())

    # Filter by severity
    filtered_warnings = []
    for warning in found_warnings:
        if warning.get('severity', '').lower() in ['critical', 'high', 'medium']:
            filtered_warnings.append(warning)

    print("Returning warnings:", filtered_warnings)
    return list(found_interactions.values()), filtered_warnings