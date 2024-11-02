import json
from pathlib import Path
import os
import stat

def load_seed(file_path='/seed/seed.txt'):
    with open(file_path, 'r') as f:
        seed = int(f.read())
    return seed


def save_elements_to_json(elements, output_file):
    with open(output_file, 'w') as f:
        json.dump(elements, f)
    print(f"Selected elements saved to '{output_file}'")


def load_json_to_dict(file_path):
    with open(file_path, 'r') as file:
        data_dict = json.load(file)
    return data_dict


def delete_dot_underscore_files(folder_path):
    print('WARNING: THIS FUNCTION DELETES ALL ._ FILES. REMOVE "pass" TO USE IT')
    # pass
    folder = Path(folder_path)
    # Search for all ._ files in the folder and its subdirectories
    dot_underscore_files = folder.rglob('._*')

    for file in dot_underscore_files:
        try:
            # Change file permissions to writable
            os.chmod(file, stat.S_IWRITE)
            file.unlink()  # Attempt to delete the file
            print(f"Deleted: {file}")
        except PermissionError:
            print(f"Permission denied: {file}")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"Failed to delete {file}: {e}")
