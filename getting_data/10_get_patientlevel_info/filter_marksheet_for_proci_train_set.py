import pandas as pd
import json

# Load JSON file and extract patient IDs
with open('/Volumes/pelvis/projects/tiago/DWI_IQA/QualityClassifier/getting_data/4.2_get_lq_t2w_lists/lq_t2w_final.json', 'r') as f:
    data = json.load(f)

# Combine all patient IDs from each center
patient_ids = [pid for center in data.values() for pid in center]

# Load the CSV file
df = pd.read_excel('/Users/tiago/Library/CloudStorage/OneDrive-Radboudumc/sbatch scripts/ProCAncer-I-PICAI-patient-level-marksheet.xlsx')

# Filter the CSV based on patient IDs
filtered_df = df[df['patient_id'].isin(patient_ids)]

# Save to a new CSV file
filtered_df.to_csv('picai_lq_t2w_train.csv', index=False)
