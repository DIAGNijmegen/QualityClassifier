import os
from pathlib import Path
import macos_tags as mt
import json
import random
from getting_data.utils.utils import load_json_to_dict, save_elements_to_json, load_seed


if __name__ == '__main__':
    #path_in = Path("/Users/tiago/Library/CloudStorage/OneDrive-Radboudumc/procancer-i copy")
    root_paths = Path("/Users/tiago/Library/CloudStorage/OneDrive-Radboudumc/DWI_IQA_Preview")
    path_lq = Path('../4_get_lq_dwi_lists/lq_dwi_final.json')

    lq_dwi = load_json_to_dict(path_lq)


    if isinstance(root_paths, (str, Path)):
        root_paths = [root_paths]
    elif not isinstance(root_paths, list):
        raise TypeError("root_paths must be a list of paths or a single path.")

    hq_dict = {}

    for root_path in root_paths:
        root_path = Path(root_path)

        if not root_path.exists():
            print(f"Root path {root_path} does not exist.")
            continue
        if not root_path.is_dir():
            print(f"Root path {root_path} is not a directory.")
            continue

        # Get hospital directories
        hospital_dirs = [d for d in root_path.iterdir() if d.is_dir() and d.name not in ['RUMC', 'ZGT', 'UMCG']]

        for hospital_dir in hospital_dirs:
            hospital_name = hospital_dir.name
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
            for file_path in file_paths:
                if len(hq_dict[hospital_name]) < len_hq:
                    if file_path.is_file() and file_path.suffix == '.png':
                        try:
                            tags = mt.get_all(str(file_path))
                        except Exception as e:
                            print(f"Error getting tags for {file_path}: {e}")
                            continue
                        if tags:
                            for tag in tags:
                                if tag.name == ('HQ DWI'):
                                    hq_dict[hospital_name].append(file_path.stem)
                else:
                    break
            print(f'HQ Len of {hospital_name}: {len(hq_dict[hospital_name])}')

    save_elements_to_json(hq_dict, 'hq_dwi_procanceri_50_50.json')