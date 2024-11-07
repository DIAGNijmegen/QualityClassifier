import json
from pathlib import Path

path_1 = Path('/Volumes/pelvis/projects/tiago/DWI_IQA/QualityClassifier/getting_data/1_get_procanceri_val_set/procanceri_val_set.json')
path_2 = Path('picai_val_list2.json')

# Load the JSON files
with open(path_1, 'r') as f1, open(path_2, 'r') as f2:
    list1 = json.load(f1)
    list2 = json.load(f2)

# Write all entries to a text file, first from list1, then from list2
with open('patient_list.txt', 'w') as output_file:
    # Write all entries from the first list
    for entry in list1:
        output_file.write(f"{entry}\n")

    # Write all entries from the second list
    for entry in list2:
        output_file.write(f"{entry}\n")

print("Entries from both lists written to output.txt")