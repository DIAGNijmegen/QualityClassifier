from pathlib import Path
from getting_data.utils.utils import load_json_to_dict, save_elements_to_json

if __name__ == "__main__":
    procanceri = load_json_to_dict(Path('hq_t2w_procanceri_50_50.json'))
    rumc = load_json_to_dict(Path('hq_t2w_rumc_50_50.json'))
    zgt = load_json_to_dict(Path('hq_t2w_zgt_50_50.json'))

    merged_dict = {**procanceri, **rumc, **zgt}
    save_elements_to_json(merged_dict, 'hq_t2w_final_50_50.json')
