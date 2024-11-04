import logging
from pathlib import Path
from getting_data.utils.utils import load_json_to_dict
import sys
from collections import defaultdict

# Setup logging
log_file = 'patient_count_log.txt'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# File handler for logging to a file
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Console handler for logging to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

# Add handlers to the root logger
logging.getLogger().addHandler(file_handler)
logging.getLogger().addHandler(console_handler)


def count_patients(proci_list, prostate_archive):
    hospitals_folder = prostate_archive / 'procancer-i/routine-data/center'
    hospital_patient_counts = defaultdict(int)

    for study in proci_list:
        study_id = study.split('_')[0]

        # Check each hospital folder for the patient
        for hospital in hospitals_folder.iterdir():
            patient_path = hospital / study_id
            if patient_path.is_dir():
                hospital_name = hospital.name
                hospital_patient_counts[hospital_name] += 1
                logging.info(f"Found patient '{study_id}' in hospital '{hospital_name}'")
                break  # Stop searching once we find the patient in one hospital

    # Print and log final counts
    logging.info("Patient counts by hospital:")
    for hospital, count in hospital_patient_counts.items():
        logging.info(f"{hospital}: {count}")

    return hospital_patient_counts


if __name__ == '__main__':
    # Load the list of studies
    try:
        proci_list = load_json_to_dict(Path('../../getting_data/1_get_procanceri_val_set/procanceri_val_set.json'))
        logging.info("Loaded study list successfully.")
    except FileNotFoundError:
        logging.error("Error: list JSON file not found.")
        sys.exit(1)

    # Define mount points and paths
    mountpoint = Path('/Volumes')
    prostate_archive = mountpoint / 'pelvis/data/prostate-MRI'

    # Get patient counts by hospital
    hospital_counts = count_patients(proci_list, prostate_archive)

    # Display final summary
    print("Patient counts by hospital:")
    for hospital, count in hospital_counts.items():
        print(f"{hospital}: {count}")

    logging.info("Counting complete.")
    # Flush and close all handlers at the end
    for handler in logging.root.handlers[:]:
        handler.flush()
        handler.close()
        logging.root.removeHandler(handler)