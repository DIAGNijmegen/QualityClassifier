import logging
from pathlib import Path
from getting_data.utils.utils import load_json_to_dict
import shutil
import sys

# Setup logging with both file and console handlers
log_file = 'copy_t2w_scans_log.txt'
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
    # Load the list of t2w studies
    try:
        lq_t2w_list = load_json_to_dict(Path('../../getting_data/4.2_get_lq_t2w_lists/lq_t2w_final.json'))
        hq_t2w_list = load_json_to_dict(Path('../../getting_data/5.2_get_hq_t2w_lists/hq_t2w_final_50_50.json'))
        logging.info("Loaded t2w study list successfully.")
    except FileNotFoundError:
        logging.error("Error: t2w list JSON file not found.")
        sys.exit(1)

    # Define mount points and paths
    mountpoint = Path('/Volumes')
    prostate_archive = mountpoint / 'pelvis/data/prostate-MRI'
    lq_out_path = mountpoint / 'pelvis/projects/tiago/DWI_IQA/data_t2w/raw/LQ'
    hq_out_path = mountpoint / 'pelvis/projects/tiago/DWI_IQA/data_t2w/raw/HQ'

    # Ensure output paths exist
    lq_out_path.mkdir(parents=True, exist_ok=True)
    hq_out_path.mkdir(parents=True, exist_ok=True)

    # Define the lists and output paths
    t2w_list = {'lq_t2w_list': (lq_t2w_list, lq_out_path),
                'hq_t2w_list': (hq_t2w_list, hq_out_path)}

    # Process each list with progress tracking
    for list_name, (t2w_studies, output_path) in t2w_list.items():
        logging.info(f"Processing {list_name} with output path: {output_path}")

        total_hospitals = len(t2w_studies)
        hospital_count = 1

        # Process each hospital and its studies
        for hospital, studies in t2w_studies.items():
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

                        # Copy the first series with 't2w' in the name
                        copied = False
                        for series_path in study_path.iterdir():
                            if 't2w' in series_path.name:
                                logging.info(f"    Copying series '{series_path.name}' to output directory.")
                                shutil.copy(series_path, output_path / series_path.name)
                                copied = True
                                break
                        if not copied:
                            logging.warning(f"    No 't2w' series found for study '{study}' in Procancer-i. Skipping.")

                    else:
                        patient, _ = study.split('_')
                        series_path = patients_folder / patient / (study + '_t2w.mha')
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

    # TODO: Test duplicates and lengths after the copies
