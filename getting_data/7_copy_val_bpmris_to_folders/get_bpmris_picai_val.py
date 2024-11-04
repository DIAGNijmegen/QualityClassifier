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

def copy_study(prostate_archive, val_path):
    patients_folder = prostate_archive / 'picai/hidden_validation/images'
    for patient in patients_folder.iterdir():
        if patient.is_dir():
            destination_path = val_path / patient.name
            try:
                shutil.copytree(patient, destination_path, dirs_exist_ok=True)
                logging.info(f"Copied '{patient}' to '{destination_path}'")
            except Exception as e:
                logging.error(f"Error copying '{patient}' to '{destination_path}': {e}")

if __name__ == '__main__':
    # Define mount points and paths
    mountpoint = Path('/Volumes')
    prostate_archive = mountpoint / 'pelvis/data/prostate-MRI'
    val_path = mountpoint / 'pelvis/projects/tiago/DWI_IQA/validation'

    # Ensure output paths exist
    val_path.mkdir(parents=True, exist_ok=True)
    copy_study(prostate_archive,val_path)

    logging.info("Processing complete.")
    # Flush and close all handlers at the end
    for handler in logging.root.handlers[:]:
        handler.flush()
        handler.close()
        logging.root.removeHandler(handler)

    # TODO: Test duplicates and lengths after the copies