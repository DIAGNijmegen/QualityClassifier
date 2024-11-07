import logging
from pathlib import Path
from getting_data.utils.utils import load_json_to_dict
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

# Setup logging with both file and console handlers
log_file = 'copy_scans_log.txt'
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

def copy_study(study, prostate_archive, val_path):
    hospitals_folder = prostate_archive / 'procancer-i/routine-data/center'
    for hospital in hospitals_folder.iterdir():
        patient_path = hospital / study.split('_')[0]
        if patient_path.is_dir():
            destination_path = val_path / study.split('_')[0]

            try:
                shutil.copytree(patient_path, destination_path, dirs_exist_ok=True)
                logging.info(f"Copied '{patient_path}' to '{destination_path}'")
            except Exception as e:
                logging.error(f"Error copying '{patient_path}' to '{destination_path}': {e}")

if __name__ == '__main__':
    # Load the list of DWI studies
    try:
        proci_list = load_json_to_dict(Path('../../getting_data/1_get_procanceri_val_set/procanceri_val_set.json'))
        logging.info("Loaded study list successfully.")
    except FileNotFoundError:
        logging.error("Error: list JSON file not found.")
        sys.exit(1)

    # Define mount points and paths
    mountpoint = Path('/Volumes')
    prostate_archive = mountpoint / 'pelvis/data/prostate-MRI'
    val_path = mountpoint / 'pelvis/projects/tiago/DWI_IQA/validation_procanceri_100'

    # Ensure output paths exist
    val_path.mkdir(parents=True, exist_ok=True)

    # Split work across available CPUs
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(copy_study, study, prostate_archive, val_path) for study in proci_list]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"An error occurred: {e}")

    logging.info("Processing complete.")
    # Flush and close all handlers at the end
    for handler in logging.root.handlers[:]:
        handler.flush()
        handler.close()
        logging.root.removeHandler(handler)

    # TODO: Test duplicates and lengths after the copies