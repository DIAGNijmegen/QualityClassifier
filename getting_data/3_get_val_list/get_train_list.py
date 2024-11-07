from pathlib import Path
from getting_data.utils.utils import save_elements_to_json

images_path = Path('/Volumes/pelvis/projects/tiago/DWI_IQA/data_dwi/raw/nnUnet_raw_data/Task001_ProstateQualityDWI/imagesTr')


def list_directory_names(path):
    study_list = []
    for d in Path(path).iterdir():
        if d.is_dir():
            for study in d.iterdir():
                if study.suffix == '.mha' and '._' not in study.name:
                    patient = study.name.split('_')[0]
                    scan = study.name.split('_')[1]
                    study_list.append(patient + '_' + scan)
                    break
    return study_list


if __name__ == '__main__':
    picai_hidval_list = list_directory_names(images_path)
    save_elements_to_json(picai_hidval_list, 'picai_val_list.json')