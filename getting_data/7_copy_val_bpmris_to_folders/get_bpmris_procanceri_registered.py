import logging
import json
from pathlib import Path
from getting_data.utils.utils import load_json_to_dict
import shutil
import sys

# Setup logging
log_file = 'copy_scans_log.txt'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)
logging.getLogger().addHandler(console_handler)

checkpoint_file = 'completed_patients.json'

# Load or initialize checkpoint data
if Path(checkpoint_file).exists():
    with open(checkpoint_file, 'r') as f:
        completed_patients = json.load(f)
else:
    completed_patients = {}

unipi_count = 0
unipi_cases_file = 'unipi_cases.json'
unipi_studies = []


def save_unipi_cases():
    with open(unipi_cases_file, 'w') as f:
        json.dump(unipi_studies, f, indent=2)


def save_checkpoint():
    with open(checkpoint_file, 'w') as f:
        json.dump(completed_patients, f, indent=2)

def copy_file_with_logging(src, dest, scan_type):
    try:
        shutil.copy(src, dest)
        logging.info(f"Copied {scan_type} scan from '{src}' to '{dest}'")
    except FileNotFoundError:
        logging.error(f"File not found: '{src}' for {scan_type} scan")
    except Exception as e:
        logging.error(f"Error copying {scan_type} scan from '{src}' to '{dest}': {e}")

def check_patient_folder(patient_path):
    required_scans = ["_t2w.mha", "_hbv.mha", "_adc.mha"]
    existing_scans = {scan for scan in required_scans if (patient_path / (patient_path.name + scan)).is_file()}

    if existing_scans == set(required_scans):
        for scan in required_scans:
            scan_path = patient_path / (patient_path.name + scan)
            if scan_path.stat().st_size == 0:
                logging.warning(f"File '{scan_path}' appears to be empty. Will re-copy this patient.")
                return False
        logging.info(f"Patient folder '{patient_path}' already has complete scans. Skipping...")
        return True
    return False

if __name__ == '__main__':
    try:
        proci_list = load_json_to_dict(Path('../../getting_data/1_get_procanceri_val_set/procanceri_val_set_100.json'))
        logging.info("Loaded study list successfully.")
    except FileNotFoundError:
        logging.error("Error: list JSON file not found.")
        sys.exit(1)

    mountpoint = Path('/Volumes')
    prostate_archive = mountpoint / 'pelvis/data/prostate-MRI'
    val_path = mountpoint / 'pelvis/projects/tiago/DWI_IQA/validation_procanceri_100'
    procanceri_dir = mountpoint / 'pelvis/data/prostate-MRI/procancer-i/routine-data'
    procanceri_t2w = procanceri_dir / 'center'
    procanceri_registered = procanceri_dir / 'images-registered/Bosma24a'
    procanceri_registered_adc_normalized = procanceri_dir / 'images-registered-adc-normalized'

    for study in proci_list:
        patient_id = study.split('_')[0]
        if patient_id in completed_patients:
            logging.info(f"Patient {patient_id} already processed. Skipping.")
            continue

        out_patient_path = val_path / patient_id
        if out_patient_path.exists() and check_patient_folder(out_patient_path):
            completed_patients[patient_id] = True
            save_checkpoint()
            continue

        out_patient_path.mkdir(parents=True, exist_ok=True)
        t2w_copied, hbv_copied, adc_copied = False, False, False
        adc_check = False

        for hospital in procanceri_t2w.iterdir():
            if (hospital / patient_id).is_dir():
                t2w_src = hospital / patient_id / f"{study}_t2w.mha"
                t2w_dest = out_patient_path / f"{study}_t2w.mha"
                copy_file_with_logging(t2w_src, t2w_dest, "T2W")
                t2w_copied = True

                adc_normalized_src = procanceri_registered_adc_normalized / f"{study}_adc_normalized.mha"
                adc_dest = out_patient_path / f"{study}_adc.mha"
                if adc_normalized_src.exists():
                    copy_file_with_logging(adc_normalized_src, adc_dest, "ADC")
                    adc_copied = True
                    adc_check = True

                if hospital.name == "UNIPI":
                    logging.info(f"Hospital is UNIPI, will skip HBV and ProCancerI registered ADC for patient {patient_id}")
                    unipi_studies.append(study)
                    unipi_count += 1
                else:
                    for seg in procanceri_registered.iterdir():
                        if Path(seg / hospital.name / patient_id).is_dir():
                            hbv_src = seg / hospital.name / patient_id / f"{study}_hbv_voxel_translation.mha"
                            hbv_dest = out_patient_path / f"{study}_hbv.mha"
                            copy_file_with_logging(hbv_src, hbv_dest, "HBV")
                            hbv_copied = True

                            if not adc_check:
                                adc_src = seg / hospital.name / patient_id / f"{study}_adc_voxel_translation.mha"
                                copy_file_with_logging(adc_src, adc_dest, "ADC")
                                adc_copied = True
                            break
                            # Proceed with your processing

            if t2w_copied and hbv_copied and adc_copied:
                completed_patients[patient_id] = True
                save_checkpoint()

    # Save the list of UNIPI studies for manual handling
    save_unipi_cases()
    logging.info(f"Total UNIPI cases: {unipi_count}")

    logging.info("Processing complete.")
    for handler in logging.root.handlers[:]:
        handler.flush()
        handler.close()
        logging.root.removeHandler(handler)