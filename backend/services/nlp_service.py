import csv
import os
import re

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
WARNINGS_FILE = os.path.join(DATA_DIR, 'drug_warning.csv')
INTERACTIONS_FILE = os.path.join(DATA_DIR, 'drug_interactions.csv')

DOSE_PATTERN = re.compile(r'(\d+\s?(mg|ml|g|tablets?|capsules?|drops?))', re.IGNORECASE)

def load_all_drug_names():
    drug_names = set()
    # From warnings
    with open(WARNINGS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            drug_names.add(row['drug_name'].strip().lower())
    # From interactions
    with open(INTERACTIONS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            drug_names.add(row['drug1'].strip().lower())
            drug_names.add(row['drug2'].strip().lower())
    return list(drug_names)

ALL_DRUGS = load_all_drug_names()

def extract_medicines_and_dosages(text):
    medicines = []
    all_drugs = set([d.lower() for d in ALL_DRUGS])  # ALL_DRUGS from your CSVs
    for line in text.lower().split('\n'):
        line = line.strip()
        if line in all_drugs:
            # Try to extract dose
            dose_match = DOSE_PATTERN.search(line)
            dose = dose_match.group(0) if dose_match else ""
            medicines.append({"name": line.title(), "dose": dose})
    return medicines