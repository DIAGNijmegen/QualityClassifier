from pathlib import Path
from getting_data.utils.utils import load_json_to_dict, save_elements_to_json

if __name__ == "__main__":
    procanceri = load_json_to_dict(Path('hq_dwi_procanceri.json'))
    rumc = load_json_to_dict(Path('hq_dwi_rumc.json'))
    umcg = load_json_to_dict(Path('hq_dwi_umcg.json'))
    zgt = load_json_to_dict(Path('hq_dwi_zgt.json'))

    merged_dict = {**procanceri, **rumc, **umcg, **zgt}
    save_elements_to_json(merged_dict, 'hq_dwi_final.json')
