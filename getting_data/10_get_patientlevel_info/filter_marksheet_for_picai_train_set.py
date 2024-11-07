import pandas as pd
import json

# Load JSON file and extract patient IDs
with open('/Volumes/pelvis/projects/tiago/DWI_IQA/QualityClassifier/getting_data/4_get_lq_dwi_lists/lq_dwi_final.json', 'r') as f:
    data = json.load(f)

# Combine all patient IDs from each center
patient_ids = [pid for center in data.values() for pid in center]

filtered_ids = [entry.split('_')[0] for entry in patient_ids]
#print(filtered_ids)
filtered_df = pd.DataFrame(filtered_ids, columns=['patient_id'])

# Load the CSV file
df = pd.read_excel('/Users/tiago/Library/CloudStorage/OneDrive-Radboudumc/sbatch scripts/PICAI-HidValidTest-PubPrivTrain-patient-level-marksheet_v2.xlsx')

# Filter the CSV based on patient IDs
filtered_df = df[df['patient_id'].isin(filtered_ids)]

# Save to a new CSV file
filtered_df.to_csv('picai_lq_dwi_train.csv', index=False)
