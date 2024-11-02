import os
from pathlib import Path
import macos_tags as mt
import json


def create_exclusion_dict(root_paths, print_output=False, json_output_path=None):
    """
    Creates a dictionary of IDs and associated tags from given root paths.

    Args:
        root_paths (list of pathlib.Path or str): List of root paths containing hospital directories.
        print_output (bool): If True, prints the formatted output.
        json_output_path (str or pathlib.Path): If provided, saves the dictionary to the given path as JSON.

    Returns:
        dict: A dictionary with hospital names as keys, and dictionaries of IDs and comments as values.
    """
    if isinstance(root_paths, (str, Path)):
        root_paths = [root_paths]
    elif not isinstance(root_paths, list):
        raise TypeError("root_paths must be a list of paths or a single path.")

    lq_dict = {}

    for root_path in root_paths:
        root_path = Path(root_path)

        if not root_path.exists():
            print(f"Root path {root_path} does not exist.")
            continue
        if not root_path.is_dir():
            print(f"Root path {root_path} is not a directory.")
            continue

        # Get hospital directories
        hospital_dirs = [d for d in root_path.iterdir() if d.is_dir()]

        for hospital_dir in hospital_dirs:
            hospital_name = hospital_dir.name
            lq_dict[hospital_name] = []
            if print_output:
                print(f'# {hospital_name}')
            for file_path in hospital_dir.iterdir():
                if file_path.is_file():
                    try:
                        tags = mt.get_all(str(file_path))
                    except Exception as e:
                        print(f"Error getting tags for {file_path}: {e}")
                        continue
                    if tags:
                        for tag in tags:
                            if tag.name == 'LQ DWI':
                                lq_dict[hospital_name].append(file_path.stem)


    if json_output_path:
        json_output_path = Path(json_output_path)
        try:
            with json_output_path.open('w') as f:
                json.dump(lq_dict, f, indent=4)
            print(f"Dictionary saved to {json_output_path}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")

    return lq_dict


if __name__ == '__main__':
    #path_in = Path("/Users/tiago/Library/CloudStorage/OneDrive-Radboudumc/procancer-i copy")
    path_in = Path("/Users/tiago/Library/CloudStorage/OneDrive-Radboudumc/DWI_IQA_Preview")

    # Call the function with desired options
    exclude_dict = create_exclusion_dict(
        root_paths=path_in,
        print_output=False,  # Set to True if you want to print the output
        json_output_path='lq_dwi_from_mactags.json'  # Provide a path if you want to save to JSON
    )
