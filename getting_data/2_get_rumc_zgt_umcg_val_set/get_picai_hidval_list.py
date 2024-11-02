from pathlib import Path
from getting_data.utils.utils import save_elements_to_json

images_path = Path('/Volumes/pelvis/data/prostate-MRI/picai/hidden_validation/images')


def list_directory_names(path):
    return [d.name for d in Path(path).iterdir() if d.is_dir()]


if __name__ == '__main__':
    picai_hidval_list = list_directory_names(images_path)
    save_elements_to_json(picai_hidval_list, 'rumc_zgt_umcg_val_set.json')