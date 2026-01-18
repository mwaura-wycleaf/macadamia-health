
import streamlit as st
from macadamia_doctor import (
    load_knowledge_base,
    load_treatments,
    get_symptoms_from_kb,
    diagnose,
)

def main():
    """Main function to run the Streamlit app."""
    st.title("Macadamia Disease and Pest Diagnostic Tool")

    # Load data
    kb = load_knowledge_base('macadamia_facts.csv')
    treatments = load_treatments('pesticides_fungicides.pl')
    all_symptoms = get_symptoms_from_kb(kb)
    
    disease_name_map = {
        'grey_mould': 'botrytis (gray mold)',
        'macadamia_husk_spot': 'cercospora leaf spot',
        'macadamia_husk_rot': 'anthracnose',
        'phytophthora_root_rot': 'root rot',
        'botryosphaeria_branch_dieback': 'dieback',
        'macadamia_anthracnose': 'anthracnose',
    }

    # Symptom selection
    st.header("Select Symptoms")
    selected_symptoms = st.multiselect("Choose the symptoms you observe:", all_symptoms)

    # Diagnose button
    if st.button("Diagnose"):
        if not selected_symptoms:
            st.warning("No symptoms selected.")
        else:
            results = diagnose(set(selected_symptoms), kb)

            st.header("Diagnosis Results")
            if not results:
                st.info("No matching disease or pest found for the selected symptoms.")
            else:
                for result in results:
                    st.subheader(f"Possible Cause: {result['name']} ({result['type']})")
                    st.write(f"**Match Score:** {result['match_score']} out of {len(selected_symptoms)} selected symptoms")
                    st.write(f"**Causal Agent:** {result['causal_agent']}")
                    
                    disease_name_for_treatment = result['name'].split('(')[0].strip().lower().replace(' ', '_')
                    treatment_name = disease_name_map.get(disease_name_for_treatment, disease_name_for_treatment)

                    found_treatment = False
                    if treatment_name in treatments:
                        st.write("**Suggested Treatments:**")
                        for treatment in treatments[treatment_name]:
                            st.write(f"- {treatment}")
                        found_treatment = True
                    else:
                        for t_name, t_list in treatments.items():
                            if treatment_name in t_name or t_name in treatment_name:
                                st.write("**Suggested Treatments:**")
                                for t in t_list:
                                    st.write(f"- {t}")
                                found_treatment = True
                                break
                    
                    if not found_treatment:
                        st.write("**No specific treatment recommendations found in the knowledge base.**")
                    
                    st.write("---")

if __name__ == "__main__":
    main()
