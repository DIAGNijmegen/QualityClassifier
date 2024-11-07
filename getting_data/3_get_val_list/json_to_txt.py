import json

# Load JSON data from file
with open('/Volumes/pelvis/projects/tiago/DWI_IQA/QualityClassifier/getting_data/1_get_procanceri_val_set/procanceri_val_set_100.json', 'r') as json_file:
    patient_list = json.load(json_file)

# Save the entries to a text file
with open('/Volumes/pelvis/projects/tiago/DWI_IQA/validation_procanceri_100/subject_list.txt', 'w') as txt_file:
    for entry in patient_list:
        txt_file.write(entry + '\n')