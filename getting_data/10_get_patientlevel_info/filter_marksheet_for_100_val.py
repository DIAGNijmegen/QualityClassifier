import pandas as pd
import json

# Load JSON list
with open('/Volumes/pelvis/projects/tiago/DWI_IQA/QualityClassifier/getting_data/1_get_procanceri_val_set/procanceri_val_set_100.json', 'r') as f:
    patient_study_list = json.load(f)

# Split JSON entries into patient_id and study_id
filtered_ids = [entry.split('_')[0] for entry in patient_study_list]
filtered_df = pd.DataFrame(filtered_ids, columns=['patient_id', 'study_id'])

# Load Excel file
df = pd.read_excel('/Users/tiago/Library/CloudStorage/OneDrive-Radboudumc/sbatch scripts/ProCAncer-I-PICAI-patient-level-marksheet.xlsx')

# Merge on 'patient_id' and 'study_id'
filtered_df = df.merge(filtered_df, on=['patient_id', 'study_id'])

# Save to a new Excel file
filtered_df.to_csv('proci_val_100.csv', index=False)
