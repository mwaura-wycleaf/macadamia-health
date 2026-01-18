
import pandas as pd
import re

def load_knowledge_base(csv_path):
    """Loads the macadamia knowledge base from a CSV file."""
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: The file '{csv_path}' was not found.")
        return None

def load_treatments(prolog_path):
    """Loads treatment data from a Prolog-like file."""
    treatments = {}
    try:
        with open(prolog_path, 'r') as f:
            content = f.read().replace('\n', '')
            matches = re.findall(r"(\w+)\('([^']*)',\s*\[(.*?)\]\)\.", content)
            for match in matches:
                category, name, diseases_str = match
                diseases = [d.strip().strip("'") for d in diseases_str.split(',')]
                for disease in diseases:
                    if disease not in treatments:
                        treatments[disease] = []
                    treatments[disease].append(name)
    except FileNotFoundError:
        print(f"Error: The file '{prolog_path}' was not found.")
        return None
    return treatments

def get_symptoms_from_kb(kb):
    """Extracts a unique, sorted list of all symptoms from the knowledge base."""
    all_symptoms = set()
    for _, row in kb.iterrows():
        # Symptoms are stored as a string representation of a list
        symptoms_list = eval(row['symptoms'])
        for symptom in symptoms_list:
            all_symptoms.add(symptom.strip())
    return sorted(list(all_symptoms))

def diagnose(selected_symptoms, kb):
    """Diagnoses the problem based on selected symptoms using a scoring system."""
    possible_causes = []
    for index, row in kb.iterrows():
        kb_symptoms = set(eval(row['symptoms']))
        match_score = len(selected_symptoms.intersection(kb_symptoms))
        
        if match_score > 0:
            possible_causes.append({
                'name': row['name'],
                'type': row['type'],
                'causal_agent': row['causal_agent'],
                'matched_symptoms': selected_symptoms.intersection(kb_symptoms),
                'all_symptoms': kb_symptoms,
                'match_score': match_score
            })
            
    # Sort by match score in descending order
    return sorted(possible_causes, key=lambda x: x['match_score'], reverse=True)

import sys

def main():
    """Main function to run the diagnostic tool."""
    print("--- Macadamia Disease and Pest Diagnostic Tool ---")

    kb = load_knowledge_base('macadamia_facts.csv')
    if kb is None:
        return

    treatments = load_treatments('pesticides_fungicides.pl')
    if treatments is None:
        return

    all_symptoms = get_symptoms_from_kb(kb)

    if len(sys.argv) == 1:
        print("\nUsage: python3 macadamia_doctor.py [symptom_number_1],[symptom_number_2],...")
        print("\nPlease select the symptoms you observe from the list below and pass their numbers as command-line arguments:")
        for i, symptom in enumerate(all_symptoms, 1):
            print(f"  {i}. {symptom}")
        return

    selected_indices = sys.argv[1]
    
    try:
        selected_symptoms = {all_symptoms[int(i)-1] for i in selected_indices.split(',')}
    except (ValueError, IndexError):
        print("\nError: Invalid input. Please enter numbers from the list.")
        return

    print("\n--- Diagnosis ---")
    if not selected_symptoms:
        print("No symptoms selected.")
        return

    results = diagnose(selected_symptoms, kb)

    disease_name_map = {
        'grey_mould': 'botrytis (gray mold)',
        'macadamia_husk_spot': 'cercospora leaf spot',
        'macadamia_husk_rot': 'anthracnose',
        'phytophthora_root_rot': 'root rot',
        'botryosphaeria_branch_dieback': 'dieback',
        'macadamia_anthracnose': 'anthracnose',
    }
    
    if not results:
        print("No matching disease or pest found for the selected symptoms.")
    else:
        for result in results:
            print(f"\nPossible Cause: {result['name']} ({result['type']})")
            print(f"  Causal Agent: {result['causal_agent']}")
            
            disease_name_for_treatment = result['name'].split('(')[0].strip().lower().replace(' ', '_')
            
            # Use the map to find the correct treatment name
            treatment_name = disease_name_map.get(disease_name_for_treatment, disease_name_for_treatment)
            
            found_treatment = False
            if treatment_name in treatments:
                print("  Suggested Treatments:")
                for treatment in treatments[treatment_name]:
                    print(f"    - {treatment}")
                found_treatment = True
            else:
                # Fallback for names that don't match perfectly
                for t_name, t_list in treatments.items():
                    if treatment_name in t_name or t_name in treatment_name:
                        print("  Suggested Treatments:")
                        for t in t_list:
                            print(f"    - {t}")
                        found_treatment = True
                        break
            if not found_treatment:
                print("  No specific treatment recommendations found in the knowledge base.")


if __name__ == "__main__":
    main()
