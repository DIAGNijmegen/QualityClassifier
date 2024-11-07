import pandas as pd
import glob

# Load all CSV files
file_paths = glob.glob('/Volumes/pelvis/projects/tiago/DWI_IQA/QualityClassifier/getting_data/10_get_patientlevel_info/markseets/*.csv')
# replace with your directory path
dfs = []
for file in file_paths:
    df = pd.read_csv(file)
    # Rename 'scanner_model_name' to 'scanner_model' if it exists
    df.rename(columns={'scanner_model_name': 'scanner_model'}, inplace=True)
    dfs.append(df)

# Concatenate all CSVs into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Group by 'center' and 'scanner_manufacturer', aggregating unique 'scanner_model' per group
summary = (combined_df.groupby(['center', 'scanner_manufacturer'])['scanner_model']
           .unique()
           .reset_index())

# Save to a new CSV file
summary.to_csv('scanner_summary_per_center.csv', index=False)
