import logging
from pathlib import Path
from getting_data.utils.utils import load_json_to_dict
import shutil
import sys

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

if __name__ == '__main__':
    # Load the list of DWI studies
    try:
        lq_dwi_list = load_json_to_dict(Path('../../getting_data/4_get_lq_dwi_lists/lq_dwi_final.json'))
        hq_dwi_list = load_json_to_dict(Path('../../getting_data/5_get_hq_dwi_lists/hq_dwi_final.json'))
        logging.info("Loaded DWI study list successfully.")
    except FileNotFoundError:
        logging.error("Error: DWI list JSON file not found.")
        sys.exit(1)

    # Define mount points and paths
    mountpoint = Path('/Volumes')
    prostate_archive = mountpoint / 'pelvis/data/prostate-MRI'
    lq_out_path = mountpoint / 'pelvis/projects/tiago/DWI_IQA/data/raw/LQ'
    hq_out_path = mountpoint / 'pelvis/projects/tiago/DWI_IQA/data/raw/HQ'

    # Ensure output paths exist
    lq_out_path.mkdir(parents=True, exist_ok=True)
    hq_out_path.mkdir(parents=True, exist_ok=True)

    # Define the lists and output paths
    dwi_list = {'lq_dwi_list': (lq_dwi_list, lq_out_path),
                'hq_dwi_list': (hq_dwi_list, hq_out_path)}

    # Process each list with progress tracking
    for list_name, (dwi_studies, output_path) in dwi_list.items():
        logging.info(f"Processing {list_name} with output path: {output_path}")

        total_hospitals = len(dwi_studies)
        hospital_count = 1

        # Process each hospital and its studies
        for hospital, studies in dwi_studies.items():
            logging.info(f"Processing hospital {hospital_count}/{total_hospitals}: {hospital}...")
            hospital_count += 1

            # Determine the hospital path
            is_procanceri = False
            if hospital == 'RUMC':
                patients_folder = prostate_archive / 'rumc/images-reconverted'
            elif hospital == 'UMCG':
                patients_folder = prostate_archive / 'umcg/images'
            elif hospital == 'ZGT':
                patients_folder = prostate_archive / 'zgt/images-reconverted'
            else:
                patients_folder = prostate_archive / 'procancer-i/routine-data/center' / hospital
                is_procanceri = True

            # Verify hospital folder exists
            if not patients_folder.exists():
                logging.warning(f"Warning: Hospital folder '{patients_folder}' not found. Skipping...")
                continue

            # Process each study
            total_studies = len(studies)
            for study_index, study in enumerate(studies, start=1):
                logging.info(f"  Processing study {study_index}/{total_studies}: {study}")

                try:
                    if is_procanceri:
                        study_path = patients_folder / study
                        if not study_path.exists():
                            logging.warning(f"    Study folder '{study_path}' not found. Skipping study.")
                            continue

                        # Copy the first series with 'hbv' in the name
                        copied = False
                        for series_path in study_path.iterdir():
                            if 'hbv' in series_path.name:
                                logging.info(f"    Copying series '{series_path.name}' to output directory.")
                                shutil.copy(series_path, output_path / series_path.name)
                                copied = True
                                break
                        if not copied:
                            logging.warning(f"    No 'hbv' series found for study '{study}' in Procancer-i. Skipping.")

                    else:
                        patient, _ = study.split('_')
                        series_path = patients_folder / patient / (study + '_hbv.mha')
                        if series_path.exists():
                            logging.info(f"    Copying series '{series_path.name}' to output directory.")
                            shutil.copy(series_path, output_path / series_path.name)
                        else:
                            logging.warning(f"    Series file '{series_path}' not found. Skipping.")

                except Exception as e:
                    logging.error(f"Error while processing study '{study}' in hospital '{hospital}': {e}")

    logging.info("Processing complete.")
    # Flush and close all handlers at the end
    for handler in logging.root.handlers[:]:
        handler.flush()
        handler.close()
        logging.root.removeHandler(handler)
