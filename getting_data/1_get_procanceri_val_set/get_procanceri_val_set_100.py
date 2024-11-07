import random
from getting_data.exclusion_lists.procanceri_inclusion_lists import inclusion_list_picai_v1
from getting_data.utils.utils import load_seed, save_elements_to_json
import os
import random
from collections import defaultdict
from pathlib import Path
import json


# Define the path to your preview folders
preview_folder_path = Path("/Users/tiago/Library/CloudStorage/OneDrive-Radboudumc/DWI_IQA_Preview")  # Change this to your actual preview folder path

# Step 1: Map each case ID to its hospital
hospital_to_cases = defaultdict(list)
for case in inclusion_list_picai_v1:
    case_id = case.split('_')[0]  # Extract the part before the '_'
    found = False
    # Check each hospital folder
    for hospital_folder in preview_folder_path.iterdir():
        if hospital_folder.is_dir():
            # Check if the case's PNG preview exists in this hospital's folder
            preview_path = hospital_folder / f"{case_id}.png"
            if preview_path.exists():
                hospital_to_cases[hospital_folder.name].append(case)
                found = True
                break
    if not found:
        print(f"Warning: No matching hospital folder found for case {case}")

# Step 2: Sample 5 cases from each hospital and ensure a total of 100 cases
sampled_cases = []
remaining_cases = []  # For cases that will fill up to 100 if needed

# Sample at least 5 cases from each hospital if possible
for hospital, cases in hospital_to_cases.items():
    if len(cases) >= 5:
        sampled_cases.extend(random.sample(cases, 5))
        remaining_cases.extend([case for case in cases if case not in sampled_cases])
    else:
        print(f"Warning: Not enough cases for {hospital}. Found {len(cases)} cases.")

# Step 3: Randomly fill up to 100 cases if needed
remaining_needed = 100 - len(sampled_cases)
if remaining_needed > 0:
    additional_cases = random.sample(remaining_cases, min(remaining_needed, len(remaining_cases)))
    sampled_cases.extend(additional_cases)

# Ensure we have exactly 100 cases
sampled_cases = sampled_cases[:100]

# Step 4: Count the number of cases per hospital in the sampled list
hospital_counts = defaultdict(int)
for case in sampled_cases:
    case_id = case.split('_')[0]
    for hospital, cases in hospital_to_cases.items():
        if case in cases:
            hospital_counts[hospital] += 1
            break
            
print(hospital_counts)

save_elements_to_json(sampled_cases, 'procanceri_val_set_100.json')
