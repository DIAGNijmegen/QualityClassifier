
# Remove from the initial lists scans that were rendomly selected for 20% procanceri val set

from pathlib import Path
from getting_data.utils.utils import load_json_to_dict, save_elements_to_json

procanceri_val_set_path = Path('../../getting_data/1_get_procanceri_val_set/procanceri_val_set.json')
lq_dwi_original_path = Path('lq_dwi_from_mactags.json')


def filter_data(data, exclusion_list):
    filtered_data = {}
    count = 0
    for hospital, ids in data.items():
        # Filter IDs that are not in the exclusion list
        remaining_ids = [id_ for id_ in ids if id_ not in exclusion_list]

        # Find and print IDs to be removed
        removed_ids = [id_ for id_ in ids if id_ in exclusion_list]
        for id_ in removed_ids:
            print(f"{id_} removed from {hospital}")
            count += 1

        # Update filtered data
        if remaining_ids:
            filtered_data[hospital] = remaining_ids
    print(f"Removed {count} scans")
    return filtered_data


if __name__ == '__main__':

    procanceri_val_set = load_json_to_dict(procanceri_val_set_path)
    procanceri_val_set_string = ''.join(procanceri_val_set)
    lq_dwi_original = load_json_to_dict(lq_dwi_original_path)
    filtered_data = filter_data(lq_dwi_original, procanceri_val_set_string)
    save_elements_to_json(filtered_data, 'lq_dwi_final.json')










