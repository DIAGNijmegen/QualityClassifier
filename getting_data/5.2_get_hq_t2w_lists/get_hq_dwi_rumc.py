from pathlib import Path
import random
from getting_data.utils.utils import load_json_to_dict, save_elements_to_json, load_seed
import datetime
from getting_data.exclusion_lists.rumc_exclusion_lists import exclusion_list_default



def get_study_sequence(filename):
    stem = filename.stem
    patient, study, sequence = stem.split('_')
    return patient + '_' + study, sequence


if __name__ == '__main__':
    hospital_dir = Path("/Volumes/pelvis/data/prostate-MRI/rumc/images-reconverted")
    path_lq = Path('../4.2_get_lq_t2w_lists/lq_t2w_final.json')

    lq_dwi = load_json_to_dict(path_lq)
    hq_dict = {}

    hospital_name = 'RUMC'
    len_lq = len(lq_dwi[hospital_name])
    print(f'LQ Len of {hospital_name}: {len_lq}')
    len_hq = len_lq #* 3
    print(f'HQ Max Len of {hospital_name}: {len_hq}')
    hq_dict[hospital_name] = []
    # Shufle the files to select hq
    seed = load_seed()
    random.seed(seed)
    file_paths = list(hospital_dir.iterdir())
    random.shuffle(file_paths)
    count=0
    for patient_path in file_paths:
        if patient_path.is_dir():
            # Get the modified date of the folder
            modified_timestamp = patient_path.stat().st_mtime
            modified_date = datetime.datetime.fromtimestamp(modified_timestamp)
            target_date = datetime.datetime(2024, 10, 1)
            if modified_date < target_date:  # Recent patients
                if len(hq_dict[hospital_name]) < len_hq:
                    for study_path in patient_path.iterdir():
                        study, sequence = get_study_sequence(study_path)
                        if study not in exclusion_list_default:
                            if sequence == 'hbv':
                                hq_dict[hospital_name].append(study)
                                count += 1
                                print(count)
                                break  # only one study per patient

                else:
                    break
    print(f'HQ Len of {hospital_name}: {len(hq_dict[hospital_name])}')

    save_elements_to_json(hq_dict, 'hq_t2w_rumc_50_50.json')