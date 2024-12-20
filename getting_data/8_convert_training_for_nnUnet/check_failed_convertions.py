import json
import re
from pathlib import Path


def find_missing_files_with_hospital_and_name(task_folder, lq_file, hq_file):
    task_folder = Path(task_folder)
    correspondence_path = task_folder / 'correspondence.json'

    # Load JSON files
    with open(correspondence_path, 'r') as f:
        correspondence = json.load(f)
    with open(lq_file, 'r') as f:
        lq_data = json.load(f)
    with open(hq_file, 'r') as f:
        hq_data = json.load(f)

    # Map original names to hospitals
    hospital_map = {}
    for hospital, ids in lq_data.items():
        for id_ in ids:
            hospital_map[id_] = hospital
    for hospital, ids in hq_data.items():
        for id_ in ids:
            hospital_map[id_] = hospital

    # Pattern to extract sequence number
    pattern = re.compile(r"ProstateQualityT2W_(\d+)_0000\.nii\.gz")

    # Extract sequence numbers from files in the directory
    sequence_numbers = []
    for file in task_folder.glob("imagesTr/ProstateQualityT2W_*.nii.gz"):
        match = pattern.match(file.name)
        if match:
            sequence_numbers.append(int(match.group(1)))

    # Find missing numbers in the sequence
    sequence_numbers.sort()
    all_numbers = set(range(sequence_numbers[0], sequence_numbers[-1] + 1))
    missing_numbers = sorted(all_numbers - set(sequence_numbers))

    # Map missing numbers back to original file names and hospitals
    print("Missing files in sequence:")
    for num in missing_numbers:
        file_name = f"ProstateQualityT2W_{num:04d}_0000.nii.gz"
        original_name = next((orig for orig, converted in correspondence.items() if converted == file_name), None)
        hospital = hospital_map.get(original_name.rstrip('_t2w.mha'), "Unknown") if original_name else "Unknown"

        print(f"Missing file: {file_name}")
        print(f"  Original name: {original_name if original_name else 'Not found in correspondence.json'}")
        print(f"  Hospital: {hospital}")


# Example usage
find_missing_files_with_hospital_and_name(
    task_folder='/Volumes/pelvis/projects/tiago/DWI_IQA/data_t2w/raw/nnUnet_raw_data/Task001_ProstateQualityT2W',
    hq_file='../5.2_get_hq_t2w_lists/hq_t2w_final_50_50.json',
    lq_file='../4.2_get_lq_t2w_lists/lq_t2w_final.json'
)
