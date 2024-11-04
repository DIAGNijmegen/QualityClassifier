from pathlib import Path
from utils import delete_dot_underscore_files

folder_path = Path('/Volumes/pelvis/projects/tiago/DWI_IQA/data')

delete_dot_underscore_files(folder_path)