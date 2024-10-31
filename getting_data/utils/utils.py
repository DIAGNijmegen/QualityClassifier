import json


def load_seed(file_path='/Users/tiago/Documents/GitHub/QualityClassifier/getting_data/utils/seed/seed.txt'):
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