from pathlib import Path
import random
from getting_data.utils.utils import load_json_to_dict, save_elements_to_json, load_seed
import datetime
from getting_data.exclusion_lists.umcg_exclusion_lists import exclusion_list_default


def get_study_sequence(filename):
    stem = filename.stem
    patient, study, sequence = stem.split('_')
    return patient + '_' + study, sequence


if __name__ == '__main__':
    hospital_dir = Path("/Volumes/pelvis/data/prostate-MRI/umcg/images")
    path_lq = Path('../4_get_lq_dwi_lists/lq_dwi_final.json')

    lq_dwi = load_json_to_dict(path_lq)
    hq_dict = {}

    hospital_name = 'UMCG'
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
    count = 0
    for patient_path in file_paths:
        if patient_path.is_dir():
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

    save_elements_to_json(hq_dict, 'hq_dwi_umcg_50_50.json')